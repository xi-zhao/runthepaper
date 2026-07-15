from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from scipy.linalg import expm

from .fidelity_response import (
    BASIS,
    BASIS_INDEX,
    HILBERT_DIMENSION,
    ATOM_ONE,
    ATOM_RYDBERG,
    Metric,
    average_response_from_fourier,
    frequency_noise_operator,
    input_projector,
)


NoiseKind = Literal["frequency", "intensity"]


@dataclass(frozen=True)
class ProtocolSegment:
    """One constant-amplitude control segment in units where Omega=1."""

    duration: float
    phase: float
    detuning_over_omega: float = 0.0


@dataclass(frozen=True)
class GateProtocol:
    name: str
    segments: tuple[ProtocolSegment, ...]
    parameter_match: str
    source: str

    @property
    def duration(self) -> float:
        return float(sum(segment.duration for segment in self.segments))


def levine_pichler_protocol() -> GateProtocol:
    """Return the two-pulse protocol from Levine et al. (2019)."""

    pulse_duration = 4.29268
    detuning = 0.377371
    return GateProtocol(
        name="Levine-Pichler",
        segments=(
            ProtocolSegment(pulse_duration, 0.0, detuning),
            ProtocolSegment(pulse_duration, 3.90242, detuning),
        ),
        parameter_match="cited_source_exact",
        source="Levine et al., PRL 123, 170503 (2019), Eq. S12",
    )


def fromonteil_protocol_ii_variant_1() -> GateProtocol:
    """Return the fully intensity-robust Protocol II, variant 1.

    A C_(pi/2) block is repeated twice. The target paper identifies the
    intensity-robust family but not the discrete variant; this implementation
    uses the first sequence printed by Fromonteil et al.
    """

    alpha_1 = np.pi / (2.0 * np.sqrt(2.0))
    alpha_2 = np.pi
    c_pi_over_2 = (
        ProtocolSegment(alpha_1, np.pi / 2.0),
        ProtocolSegment(alpha_2, np.pi),
        ProtocolSegment(alpha_1, np.pi / 2.0),
        ProtocolSegment(alpha_1, 0.0),
        ProtocolSegment(alpha_2, np.pi / 2.0),
        ProtocolSegment(alpha_1, 0.0),
    )
    return GateProtocol(
        name="Fromonteil Protocol II",
        segments=c_pi_over_2 + c_pi_over_2,
        parameter_match="cited_source_reconstructed_identity",
        source="Fromonteil et al., PRX Quantum 4, 020335 (2023), Protocol II variant 1",
    )


def control_hamiltonian(
    phase: float,
    *,
    detuning_over_omega: float = 0.0,
    amplitude_scale: float = 1.0,
) -> np.ndarray:
    """Return the infinite-blockade Hamiltonian for one constant segment."""

    matrix = np.zeros((HILBERT_DIMENSION, HILBERT_DIMENSION), dtype=np.complex128)
    coupling = 0.5 * amplitude_scale * np.exp(1.0j * phase)
    for state in BASIS:
        source_index = BASIS_INDEX[state]
        rydberg_count = state.count(ATOM_RYDBERG)
        matrix[source_index, source_index] = -detuning_over_omega * rydberg_count
        for atom_index in range(2):
            if state[atom_index] != ATOM_ONE:
                continue
            excited = list(state)
            excited[atom_index] = ATOM_RYDBERG
            excited_state = tuple(excited)
            if excited_state not in BASIS_INDEX:
                continue
            excited_index = BASIS_INDEX[excited_state]
            matrix[source_index, excited_index] = coupling
            matrix[excited_index, source_index] = np.conjugate(coupling)
    return matrix


def intensity_noise_operator(phase: float) -> np.ndarray:
    """Return dH/d(delta I/I), excluding the detuning term."""

    return 0.5 * control_hamiltonian(phase, detuning_over_omega=0.0)


def protocol_trajectory(
    protocol: GateProtocol,
    *,
    points_per_radian: int = 100,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Propagate a piecewise-constant protocol on a boundary-aligned grid."""

    if points_per_radian < 4:
        raise ValueError("points_per_radian must be at least four")
    times: list[float] = [0.0]
    propagators: list[np.ndarray] = [
        np.eye(HILBERT_DIMENSION, dtype=np.complex128)
    ]
    intensity_operators: list[np.ndarray] = [
        intensity_noise_operator(protocol.segments[0].phase)
    ]
    current_time = 0.0
    current_propagator = propagators[0]
    for segment in protocol.segments:
        if segment.duration <= 0.0:
            raise ValueError("protocol segment durations must be positive")
        steps = max(4, int(np.ceil(points_per_radian * segment.duration)))
        step = segment.duration / steps
        hamiltonian = control_hamiltonian(
            segment.phase,
            detuning_over_omega=segment.detuning_over_omega,
        )
        step_unitary = expm(-1.0j * hamiltonian * step)
        operator = intensity_noise_operator(segment.phase)
        for _ in range(steps):
            current_propagator = step_unitary @ current_propagator
            current_time += step
            times.append(current_time)
            propagators.append(current_propagator)
            intensity_operators.append(operator)
    return (
        np.asarray(times, dtype=np.float64),
        np.asarray(propagators, dtype=np.complex128),
        np.asarray(intensity_operators, dtype=np.complex128),
    )


def _trapezoid_weights(times: np.ndarray) -> np.ndarray:
    if len(times) < 2 or np.any(np.diff(times) <= 0.0):
        raise ValueError("times must be strictly increasing")
    weights = np.empty_like(times)
    weights[0] = 0.5 * (times[1] - times[0])
    weights[-1] = 0.5 * (times[-1] - times[-2])
    weights[1:-1] = 0.5 * (times[2:] - times[:-2])
    return weights


def _fourier_operators(
    times: np.ndarray,
    operators: np.ndarray,
    normalized_frequencies: np.ndarray,
    *,
    chunk_size: int = 128,
) -> np.ndarray:
    weights = _trapezoid_weights(times)
    weighted = (operators * weights[:, None, None]).reshape(len(times), -1)
    frequencies = np.asarray(normalized_frequencies, dtype=np.float64)
    result = np.empty(
        (len(frequencies), HILBERT_DIMENSION, HILBERT_DIMENSION),
        dtype=np.complex128,
    )
    for start in range(0, len(frequencies), chunk_size):
        stop = min(start + chunk_size, len(frequencies))
        kernel = np.exp(1.0j * np.outer(frequencies[start:stop], times))
        result[start:stop] = (kernel @ weighted).reshape(
            stop - start,
            HILBERT_DIMENSION,
            HILBERT_DIMENSION,
        )
    return result


def protocol_response(
    protocol: GateProtocol,
    normalized_frequencies: np.ndarray,
    *,
    metric: Metric = "symmetric_haar",
    noise_kind: NoiseKind,
    points_per_radian: int = 100,
) -> tuple[np.ndarray, dict[str, float | np.ndarray]]:
    """Calculate a protocol response directly from its ideal trajectory."""

    times, propagators, intensity_operators = protocol_trajectory(
        protocol,
        points_per_radian=points_per_radian,
    )
    if noise_kind == "frequency":
        lab_operators = np.repeat(
            frequency_noise_operator()[None, :, :],
            len(times),
            axis=0,
        )
    elif noise_kind == "intensity":
        lab_operators = intensity_operators
    else:
        raise ValueError(f"unsupported noise kind: {noise_kind}")
    heisenberg = np.einsum(
        "tji,tjk,tkl->til",
        np.conjugate(propagators),
        lab_operators,
        propagators,
        optimize=True,
    )
    fourier = _fourier_operators(times, heisenberg, normalized_frequencies)
    response = average_response_from_fourier(fourier, metric)
    diagnostics: dict[str, float | np.ndarray] = {
        "times": times,
        "final_propagator": propagators[-1],
        "unitarity_error": float(
            np.max(
                np.abs(
                    propagators[-1].conj().T @ propagators[-1]
                    - np.eye(HILBERT_DIMENSION)
                )
            )
        ),
    }
    return response, diagnostics


def integrated_rydberg_population(
    protocol: GateProtocol,
    *,
    metric: Metric = "symmetric_haar",
    points_per_radian: int = 100,
) -> float:
    """Return the ideal average Rydberg exposure in units of 1/Omega."""

    times, propagators, _ = protocol_trajectory(
        protocol,
        points_per_radian=points_per_radian,
    )
    projector, dimension = input_projector(metric)
    population = np.diag(
        [state.count(ATOM_RYDBERG) for state in BASIS]
    ).astype(np.complex128)
    values = np.empty(len(times), dtype=np.float64)
    for index, unitary in enumerate(propagators):
        values[index] = float(
            np.real(np.trace(population @ unitary @ projector @ unitary.conj().T))
            / dimension
        )
    return float(np.trapezoid(values, times))
