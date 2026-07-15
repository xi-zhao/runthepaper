from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Literal

import numpy as np
from scipy.linalg import expm


Metric = Literal["haar", "symmetric_haar"]
NoiseKind = Literal["frequency", "intensity"]

ATOM_ZERO = 0
ATOM_ONE = 1
ATOM_RYDBERG = 2
BASIS = tuple(
    state
    for state in product((ATOM_ZERO, ATOM_ONE, ATOM_RYDBERG), repeat=2)
    if state != (ATOM_RYDBERG, ATOM_RYDBERG)
)
BASIS_INDEX = {state: index for index, state in enumerate(BASIS)}
HILBERT_DIMENSION = len(BASIS)


@dataclass(frozen=True)
class GateParameters:
    """Cited generic CZ pulse used by the reconstructed direct diagnostic."""

    omega_angular: float = 1.0
    phase_amplitude: float = 2.0 * np.pi * 0.1122
    phase_frequency_over_omega: float = 1.0431
    phase_offset: float = -0.7318
    detuning_over_omega: float = 0.0
    omega_duration_over_2pi: float = 1.215

    @property
    def duration(self) -> float:
        return 2.0 * np.pi * self.omega_duration_over_2pi / self.omega_angular


def phase(time: float | np.ndarray, params: GateParameters) -> float | np.ndarray:
    drive_frequency = params.phase_frequency_over_omega * params.omega_angular
    detuning = params.detuning_over_omega * params.omega_angular
    return (
        params.phase_amplitude * np.cos(drive_frequency * time - params.phase_offset)
        + detuning * time
    )


def ideal_hamiltonian(time: float, params: GateParameters) -> np.ndarray:
    """Return Eq. (12) after projecting out |rr> (infinite blockade)."""

    matrix = np.zeros((HILBERT_DIMENSION, HILBERT_DIMENSION), dtype=np.complex128)
    phase_value = float(phase(time, params))
    lowering = 0.5 * params.omega_angular * np.exp(-1.0j * phase_value)

    for state in BASIS:
        source_index = BASIS_INDEX[state]
        for atom_index in range(2):
            if state[atom_index] != ATOM_ONE:
                continue
            excited = list(state)
            excited[atom_index] = ATOM_RYDBERG
            excited_state = tuple(excited)
            if excited_state not in BASIS_INDEX:
                continue
            excited_index = BASIS_INDEX[excited_state]
            matrix[source_index, excited_index] = lowering
            matrix[excited_index, source_index] = np.conjugate(lowering)
    return matrix


def frequency_noise_operator() -> np.ndarray:
    """Return Eq. (13), with frequency fluctuations expressed in Hz."""

    populations = np.asarray(
        [state.count(ATOM_RYDBERG) for state in BASIS],
        dtype=np.float64,
    )
    return np.diag(-2.0 * np.pi * populations).astype(np.complex128)


def intensity_noise_operator(time: float, params: GateParameters) -> np.ndarray:
    """Return Eq. (14) for relative laser-intensity noise."""

    return 0.5 * ideal_hamiltonian(time, params)


def input_projector(metric: Metric) -> tuple[np.ndarray, int]:
    """Return the full or symmetric two-qubit computational projector."""

    vectors: list[np.ndarray] = []

    def ket(state: tuple[int, int]) -> np.ndarray:
        vector = np.zeros(HILBERT_DIMENSION, dtype=np.complex128)
        vector[BASIS_INDEX[state]] = 1.0
        return vector

    if metric == "haar":
        vectors = [
            ket((ATOM_ZERO, ATOM_ZERO)),
            ket((ATOM_ZERO, ATOM_ONE)),
            ket((ATOM_ONE, ATOM_ZERO)),
            ket((ATOM_ONE, ATOM_ONE)),
        ]
    elif metric == "symmetric_haar":
        vectors = [
            ket((ATOM_ZERO, ATOM_ZERO)),
            (ket((ATOM_ZERO, ATOM_ONE)) + ket((ATOM_ONE, ATOM_ZERO))) / np.sqrt(2.0),
            ket((ATOM_ONE, ATOM_ONE)),
        ]
    else:
        raise ValueError(f"unsupported fidelity metric: {metric}")

    projector = sum(np.outer(vector, np.conjugate(vector)) for vector in vectors)
    return projector, len(vectors)


def ideal_trajectory(
    params: GateParameters,
    time_points: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Propagate the ideal gate with a midpoint piecewise-constant solver."""

    if time_points < 3:
        raise ValueError("time_points must be at least 3")
    times = np.linspace(0.0, params.duration, time_points, dtype=np.float64)
    propagators = np.empty(
        (time_points, HILBERT_DIMENSION, HILBERT_DIMENSION),
        dtype=np.complex128,
    )
    propagators[0] = np.eye(HILBERT_DIMENSION, dtype=np.complex128)
    for index in range(time_points - 1):
        step = times[index + 1] - times[index]
        midpoint = 0.5 * (times[index + 1] + times[index])
        step_unitary = expm(-1.0j * ideal_hamiltonian(midpoint, params) * step)
        propagators[index + 1] = step_unitary @ propagators[index]
    return times, propagators


def heisenberg_operators(
    times: np.ndarray,
    propagators: np.ndarray,
    params: GateParameters,
    noise_kind: NoiseKind,
) -> np.ndarray:
    """Return O_H(t)=U(t)^dagger O(t) U(t) along the ideal trajectory."""

    if len(times) != len(propagators):
        raise ValueError("times and propagators must have equal lengths")
    transformed = np.empty_like(propagators)
    static_frequency = frequency_noise_operator()
    for index, time in enumerate(times):
        if noise_kind == "frequency":
            operator = static_frequency
        elif noise_kind == "intensity":
            operator = intensity_noise_operator(float(time), params)
        else:
            raise ValueError(f"unsupported noise kind: {noise_kind}")
        unitary = propagators[index]
        transformed[index] = unitary.conj().T @ operator @ unitary
    return transformed


def fourier_operators(
    times: np.ndarray,
    operators: np.ndarray,
    normalized_frequencies: np.ndarray,
    *,
    omega_angular: float = 1.0,
    chunk_size: int = 128,
) -> np.ndarray:
    """Compute A(x)=integral exp(i*x*Omega*t) O_H(t) dt by trapezoids."""

    if len(times) != len(operators):
        raise ValueError("times and operators must have equal lengths")
    if len(times) < 2 or not np.allclose(np.diff(times), np.diff(times)[0]):
        raise ValueError("times must be a uniform grid")
    step = float(times[1] - times[0])
    weights = np.full(len(times), step, dtype=np.float64)
    weights[[0, -1]] *= 0.5
    weighted = (operators * weights[:, None, None]).reshape(len(times), -1)
    result = np.empty(
        (len(normalized_frequencies), HILBERT_DIMENSION, HILBERT_DIMENSION),
        dtype=np.complex128,
    )
    for start in range(0, len(normalized_frequencies), chunk_size):
        stop = min(start + chunk_size, len(normalized_frequencies))
        frequency_chunk = normalized_frequencies[start:stop]
        kernel = np.exp(1.0j * np.outer(frequency_chunk * omega_angular, times))
        result[start:stop] = (kernel @ weighted).reshape(
            stop - start,
            HILBERT_DIMENSION,
            HILBERT_DIMENSION,
        )
    return result


def average_response_from_fourier(
    fourier_values: np.ndarray,
    metric: Metric,
) -> np.ndarray:
    """Evaluate the Fourier-factorized form of Appendix Eq. (G7)."""

    projector, dimension = input_projector(metric)
    response = np.empty(len(fourier_values), dtype=np.float64)
    for index, value in enumerate(fourier_values):
        adjoint = value.conj().T
        first = np.trace(value @ adjoint @ projector) / dimension
        second = (
            np.trace(value @ projector @ adjoint @ projector)
            + abs(np.trace(value @ projector)) ** 2
        ) / (dimension * (dimension + 1))
        response[index] = float(np.real(first - second))
    if float(np.min(response)) >= -1.0e-10:
        response = np.maximum(response, 0.0)
    return response


def universal_responses(
    normalized_frequencies: np.ndarray,
    *,
    params: GateParameters | None = None,
    time_points: int = 4001,
) -> tuple[dict[str, np.ndarray], dict[str, float | np.ndarray]]:
    """Compute all four universal curves from one ideal trajectory."""

    params = params or GateParameters()
    frequencies = np.asarray(normalized_frequencies, dtype=np.float64)
    times, propagators = ideal_trajectory(params, time_points)
    curves: dict[str, np.ndarray] = {}
    for noise_kind in ("frequency", "intensity"):
        operators = heisenberg_operators(times, propagators, params, noise_kind)
        fourier_values = fourier_operators(
            times,
            operators,
            frequencies,
            omega_angular=params.omega_angular,
        )
        for metric in ("haar", "symmetric_haar"):
            curves[f"{metric}_{noise_kind}"] = average_response_from_fourier(
                fourier_values,
                metric,
            )
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
    return curves, diagnostics


_FIT_PARAMETERS: dict[tuple[Metric, NoiseKind], tuple[float, ...]] = {
    ("haar", "frequency"): (2.910, -0.02715, 0.5874, 3.022, 1.179, 0.5337),
    ("haar", "intensity"): (1.187, 6.423, 0.7670, 0.07678, 5.528, 0.2381),
    ("symmetric_haar", "frequency"): (3.062, -0.01507, 0.5588, 2.843, 1.232, 0.5339),
    ("symmetric_haar", "intensity"): (1.218, 5.790, 0.7580, 0.03630, 5.647, 0.2054),
}


def appendix_fit(
    normalized_frequencies: np.ndarray,
    metric: Metric,
    noise_kind: NoiseKind,
) -> np.ndarray:
    """Evaluate one of the four paper-exact Appendix-L response functions."""

    values = np.asarray(normalized_frequencies, dtype=np.float64)
    a, b, c, d, e, f = _FIT_PARAMETERS[(metric, noise_kind)]
    if noise_kind == "frequency":
        normalized = a * np.exp(-((values - b) / c) ** 2)
        normalized += d * np.exp(-((values - e) / f) ** 2)
        return (2.0 * np.pi) ** 2 * normalized
    if noise_kind == "intensity":
        return a * (1.0 + d * np.tanh(e * (values - f))) / (
            1.0 + np.exp(b * (values - c))
        )
    raise ValueError(f"unsupported noise kind: {noise_kind}")


def scale_universal_response(
    normalized_grid: np.ndarray,
    universal_frequency: np.ndarray,
    universal_intensity: np.ndarray,
    physical_frequency_mhz: np.ndarray,
    rabi_frequency_mhz: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply Eqs. (15)-(16) using MHz as the inverse-microsecond unit."""

    if rabi_frequency_mhz <= 0.0:
        raise ValueError("rabi_frequency_mhz must be positive")
    x_values = np.asarray(physical_frequency_mhz, dtype=np.float64) / rabi_frequency_mhz
    if float(np.min(x_values)) < float(normalized_grid[0]) or float(np.max(x_values)) > float(
        normalized_grid[-1]
    ):
        raise ValueError("normalized response grid does not cover requested physical frequencies")
    g_frequency = np.interp(x_values, normalized_grid, universal_frequency)
    g_intensity = np.interp(x_values, normalized_grid, universal_intensity)
    omega_mhz = 2.0 * np.pi * rabi_frequency_mhz
    return g_frequency / omega_mhz**2, g_intensity


def gate_diagnostics(final_propagator: np.ndarray) -> dict[str, float]:
    """Check computational return and the nonlocal controlled phase."""

    computational_states = (
        (ATOM_ZERO, ATOM_ZERO),
        (ATOM_ZERO, ATOM_ONE),
        (ATOM_ONE, ATOM_ZERO),
        (ATOM_ONE, ATOM_ONE),
    )
    embedding = np.zeros((HILBERT_DIMENSION, 4), dtype=np.complex128)
    for column, state in enumerate(computational_states):
        embedding[BASIS_INDEX[state], column] = 1.0
    block = embedding.conj().T @ final_propagator @ embedding
    outside = (
        np.eye(HILBERT_DIMENSION) - embedding @ embedding.conj().T
    ) @ final_propagator @ embedding
    leakage = np.sum(np.abs(outside) ** 2, axis=0)
    diagonal = np.diag(block)
    nonlocal_phase = np.angle(diagonal[3] * diagonal[0] / (diagonal[1] * diagonal[2]))
    phase_error = abs(np.angle(np.exp(1.0j * (nonlocal_phase - np.pi))))
    off_diagonal = block - np.diag(diagonal)
    return {
        "max_return_leakage": float(np.max(leakage)),
        "max_computational_off_diagonal": float(np.max(np.abs(off_diagonal))),
        "controlled_phase_radians": float(nonlocal_phase),
        "controlled_phase_error_radians": float(phase_error),
        "minimum_return_probability": float(np.min(np.abs(diagonal) ** 2)),
    }


def normalized_rmse(actual: np.ndarray, reference: np.ndarray) -> float:
    actual_values = np.asarray(actual, dtype=np.float64)
    reference_values = np.asarray(reference, dtype=np.float64)
    scale = float(np.max(np.abs(reference_values)))
    if scale == 0.0:
        return float(np.sqrt(np.mean((actual_values - reference_values) ** 2)))
    return float(np.sqrt(np.mean((actual_values - reference_values) ** 2)) / scale)
