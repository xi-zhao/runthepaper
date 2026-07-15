from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np


NoiseKind = Literal["frequency", "intensity"]


@dataclass(frozen=True)
class ManyBodyModel:
    sites: int = 7
    rabi_frequency_mhz: float = 7.7
    duration_us: float = 6.0
    nearest_neighbor_interaction_over_omega: float = 20.0

    @property
    def omega_per_us(self) -> float:
        return 2.0 * np.pi * self.rabi_frequency_mhz

    @property
    def dimension(self) -> int:
        return 1 << self.sites


@dataclass(frozen=True)
class AdiabaticSchedule:
    tangent_shape: float = 1.35
    detuning_endpoint_over_omega: float = 10.0


def basis_operators(model: ManyBodyModel) -> dict[str, np.ndarray]:
    if model.sites < 1:
        raise ValueError("sites must be positive")
    basis = np.arange(model.dimension, dtype=np.uint64)
    occupations = np.asarray(
        [[(int(state) >> site) & 1 for site in range(model.sites)] for state in basis],
        dtype=np.float64,
    )
    occupation_count = np.sum(occupations, axis=1)
    flips = np.asarray(
        [basis ^ np.uint64(1 << site) for site in range(model.sites)],
        dtype=np.int64,
    )
    interaction = np.zeros(model.dimension, dtype=np.float64)
    nearest_neighbor = (
        model.nearest_neighbor_interaction_over_omega * model.omega_per_us
    )
    for left in range(model.sites):
        for right in range(left + 1, model.sites):
            separation = right - left
            interaction += (
                nearest_neighbor
                * occupations[:, left]
                * occupations[:, right]
                / separation**6
            )
    return {
        "occupation_count": occupation_count,
        "flips": flips,
        "interaction": interaction,
    }


def dense_hamiltonian(
    model: ManyBodyModel,
    *,
    omega_per_us: float,
    detuning_per_us: float,
) -> np.ndarray:
    operators = basis_operators(model)
    diagonal = operators["interaction"] - detuning_per_us * operators["occupation_count"]
    matrix = np.diag(diagonal.astype(np.complex128))
    basis = np.arange(model.dimension)
    for flipped in operators["flips"]:
        matrix[basis, flipped] += 0.5 * omega_per_us
    return matrix


def noise_operator(
    model: ManyBodyModel,
    *,
    omega_per_us: float,
    noise_kind: NoiseKind,
) -> np.ndarray:
    operators = basis_operators(model)
    if noise_kind == "frequency":
        return np.diag(-2.0 * np.pi * operators["occupation_count"]).astype(
            np.complex128
        )
    if noise_kind == "intensity":
        matrix = np.zeros((model.dimension, model.dimension), dtype=np.complex128)
        basis = np.arange(model.dimension)
        for flipped in operators["flips"]:
            matrix[basis, flipped] += 0.25 * omega_per_us
        return matrix
    raise ValueError(f"unsupported noise kind: {noise_kind}")


def quench_response(
    model: ManyBodyModel,
    normalized_frequencies: np.ndarray,
    *,
    noise_kind: NoiseKind,
) -> np.ndarray:
    """Evaluate the constant-quench response by exact spectral decomposition."""

    hamiltonian = dense_hamiltonian(
        model,
        omega_per_us=model.omega_per_us,
        detuning_per_us=0.0,
    )
    operator = noise_operator(
        model,
        omega_per_us=model.omega_per_us,
        noise_kind=noise_kind,
    )
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
    initial = np.zeros(model.dimension, dtype=np.complex128)
    initial[0] = 1.0
    coefficients = eigenvectors.conj().T @ initial
    transformed_operator = eigenvectors.conj().T @ operator @ eigenvectors
    energy_difference = eigenvalues[:, None] - eigenvalues[None, :]
    responses = np.empty(len(normalized_frequencies), dtype=np.float64)
    for index, normalized_frequency in enumerate(normalized_frequencies):
        physical_frequency_mhz = normalized_frequency * model.rabi_frequency_mhz
        angular_frequency = 2.0 * np.pi * physical_frequency_mhz
        sideband_responses: list[float] = []
        for sign in (-1.0, 1.0):
            phase_rate = sign * angular_frequency + energy_difference
            integral = (
                model.duration_us
                * np.exp(0.5j * phase_rate * model.duration_us)
                * np.sinc(phase_rate * model.duration_us / (2.0 * np.pi))
            )
            perturbed = np.sum(
                transformed_operator * coefficients[None, :] * integral,
                axis=1,
            )
            expectation = np.vdot(coefficients, perturbed)
            sideband_responses.append(
                float(np.real(np.vdot(perturbed, perturbed) - abs(expectation) ** 2))
            )
        responses[index] = 0.5 * sum(sideband_responses)
    return np.maximum(responses, 0.0)


def adiabatic_controls(
    model: ManyBodyModel,
    schedule: AdiabaticSchedule,
    time_us: float | np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return a disclosed ground-to-Z2 tangent reconstruction.

    With H=-Delta sum(n), the all-zero initial ground state requires negative
    Delta. The target paper plots the opposite signed detuning convention, so
    this schedule maps its +10 to -10 plotted sweep onto -10 to +10 here.
    """

    time = np.asarray(time_us, dtype=np.float64)
    fraction = np.clip(time / model.duration_us, 0.0, 1.0)
    omega = model.omega_per_us * np.sin(np.pi * fraction) ** 2
    scaled = 2.0 * fraction - 1.0
    detuning = (
        schedule.detuning_endpoint_over_omega
        * model.omega_per_us
        * np.tan(schedule.tangent_shape * scaled)
        / np.tan(schedule.tangent_shape)
    )
    return omega, detuning


def _hamiltonian_action(
    vectors: np.ndarray,
    *,
    omega_per_us: float,
    detuning_per_us: float,
    operators: dict[str, np.ndarray],
) -> np.ndarray:
    diagonal = operators["interaction"] - detuning_per_us * operators["occupation_count"]
    if vectors.ndim == 1:
        return diagonal * vectors + 0.5 * omega_per_us * np.sum(
            vectors[operators["flips"]],
            axis=0,
        )
    return diagonal[:, None] * vectors + 0.5 * omega_per_us * np.sum(
        vectors[operators["flips"]],
        axis=0,
    )


def _noise_action(
    state: np.ndarray,
    *,
    omega_per_us: float,
    noise_kind: NoiseKind,
    operators: dict[str, np.ndarray],
) -> np.ndarray:
    if noise_kind == "frequency":
        return -2.0 * np.pi * operators["occupation_count"] * state
    if noise_kind == "intensity":
        return 0.25 * omega_per_us * np.sum(state[operators["flips"]], axis=0)
    raise ValueError(f"unsupported noise kind: {noise_kind}")


def _split_propagate(
    vectors: np.ndarray,
    *,
    duration_us: float,
    omega_per_us: float,
    detuning_per_us: float,
    operators: dict[str, np.ndarray],
) -> np.ndarray:
    """Apply one unitary second-order diagonal/X split step."""

    diagonal = operators["interaction"] - detuning_per_us * operators["occupation_count"]
    diagonal_phase = np.exp(-0.5j * diagonal * duration_us)
    if vectors.ndim == 1:
        propagated = diagonal_phase * vectors
    else:
        propagated = diagonal_phase[:, None] * vectors
    cosine = np.cos(0.5 * omega_per_us * duration_us)
    sine = np.sin(0.5 * omega_per_us * duration_us)
    for flipped in operators["flips"]:
        previous = propagated
        propagated = cosine * previous - 1.0j * sine * previous[flipped]
    if vectors.ndim == 1:
        return diagonal_phase * propagated
    return diagonal_phase[:, None] * propagated


def adiabatic_response(
    model: ManyBodyModel,
    normalized_frequencies: np.ndarray,
    *,
    noise_kind: NoiseKind,
    schedule: AdiabaticSchedule | None = None,
    time_steps: int = 1600,
) -> tuple[np.ndarray, dict[str, float | np.ndarray]]:
    """Propagate the state and tangent equations with a unitary midpoint step."""

    if time_steps < 100:
        raise ValueError("time_steps must be at least 100")
    schedule = schedule or AdiabaticSchedule()
    frequencies = np.asarray(normalized_frequencies, dtype=np.float64)
    positive_angular = 2.0 * np.pi * frequencies * model.rabi_frequency_mhz
    angular_frequencies = np.concatenate((positive_angular, -positive_angular))
    operators = basis_operators(model)
    state = np.zeros(model.dimension, dtype=np.complex128)
    state[0] = 1.0
    tangents = np.zeros(
        (model.dimension, len(angular_frequencies)),
        dtype=np.complex128,
    )
    step = model.duration_us / time_steps
    for index in range(time_steps):
        midpoint = (index + 0.5) * step
        omega, detuning = adiabatic_controls(model, schedule, midpoint)
        omega_value = float(omega)
        detuning_value = float(detuning)
        state_midpoint = _split_propagate(
            state,
            duration_us=0.5 * step,
            omega_per_us=omega_value,
            detuning_per_us=detuning_value,
            operators=operators,
        )
        tangent_midpoint = _split_propagate(
            tangents,
            duration_us=0.5 * step,
            omega_per_us=omega_value,
            detuning_per_us=detuning_value,
            operators=operators,
        )
        drive = _noise_action(
            state_midpoint,
            omega_per_us=omega_value,
            noise_kind=noise_kind,
            operators=operators,
        )
        tangent_midpoint += (
            -1.0j
            * step
            * drive[:, None]
            * np.exp(1.0j * angular_frequencies[None, :] * midpoint)
        )
        state = _split_propagate(
            state_midpoint,
            duration_us=0.5 * step,
            omega_per_us=omega_value,
            detuning_per_us=detuning_value,
            operators=operators,
        )
        tangents = _split_propagate(
            tangent_midpoint,
            duration_us=0.5 * step,
            omega_per_us=omega_value,
            detuning_per_us=detuning_value,
            operators=operators,
        )

    overlap = np.einsum("i,ij->j", np.conjugate(state), tangents)
    sideband_response = np.sum(np.abs(tangents) ** 2, axis=0) - np.abs(overlap) ** 2
    midpoint = len(frequencies)
    response = 0.5 * (
        sideband_response[:midpoint] + sideband_response[midpoint:]
    )
    response = np.maximum(np.real(response), 0.0)
    diagnostics: dict[str, float | np.ndarray] = {
        "final_state": state,
        "norm_error": float(abs(np.vdot(state, state) - 1.0)),
        "time_steps": time_steps,
    }
    return response, diagnostics


def z2_probabilities(model: ManyBodyModel, state: np.ndarray) -> dict[str, float]:
    if len(state) != model.dimension:
        raise ValueError("state dimension does not match model")
    pattern_a = sum(1 << site for site in range(0, model.sites, 2))
    pattern_b = sum(1 << site for site in range(1, model.sites, 2))
    return {
        "pattern_a": float(abs(state[pattern_a]) ** 2),
        "pattern_b": float(abs(state[pattern_b]) ** 2),
        "total": float(abs(state[pattern_a]) ** 2 + abs(state[pattern_b]) ** 2),
    }
