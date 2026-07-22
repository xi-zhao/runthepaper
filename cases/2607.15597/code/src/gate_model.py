"""Domain model for arXiv:2607.15597 atom-ion gate reproduction.

The functions in this module implement physical invariants and disclosed
scaling laws.  They do not read files or render figures.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

import numpy as np


HBAR: Final = 1.054_571_817e-34
ATOMIC_MASS: Final = 1.660_539_066_60e-27
BRANCHES: Final = ("g_down", "g_up", "r_down", "r_up")


@dataclass(frozen=True)
class GateParameters:
    """One paper operating point.

    ``coupling_ratio`` is omega_g / omega.  The default is the unique value
    that gives a pi conditional phase after one trap period.
    """

    coupling_ratio: float = 1.0 / (2.0 * np.sqrt(2.0))
    trap_frequency_hz: float = 200_000.0
    gate_time_us: float = 5.0
    ion_mass_amu: float = 171.0


def branch_forces(coupling_ratio: float) -> np.ndarray:
    """Return (ion, atom) force amplitudes for the four logical branches."""

    q = float(coupling_ratio)
    return np.asarray(((q, 0.0), (-q, 0.0), (2.0 * q, -q), (0.0, -q)))


def displacement(force: np.ndarray | float, t_over_period: np.ndarray | float) -> np.ndarray:
    """Rotating-frame coherent displacement for a constant force."""

    theta = 2.0 * np.pi * np.asarray(t_over_period, dtype=float)
    return np.asarray(force)[..., np.newaxis] * (1.0 - np.exp(1j * theta))


def geometric_phase(force_pair: np.ndarray, t_over_period: float) -> float:
    """Scalar phase accumulated by two independent forced oscillators."""

    theta = 2.0 * np.pi * float(t_over_period)
    return float(np.sum(np.square(force_pair)) * (theta - np.sin(theta)))


def branch_displacements(t_over_period: float, params: GateParameters = GateParameters()) -> np.ndarray:
    """Complex displacements with shape (logical branch, ion/atom mode)."""

    theta = 2.0 * np.pi * float(t_over_period)
    return branch_forces(params.coupling_ratio) * (1.0 - np.exp(1j * theta))


def branch_phases(t_over_period: float, params: GateParameters = GateParameters()) -> np.ndarray:
    """Geometric phase for each branch."""

    theta = 2.0 * np.pi * float(t_over_period)
    weights = np.sum(np.square(branch_forces(params.coupling_ratio)), axis=1)
    return weights * (theta - np.sin(theta))


def conditional_phase(t_over_period: float, params: GateParameters = GateParameters()) -> float:
    """Two-qubit phase invariant, insensitive to local Z phases."""

    phase = branch_phases(t_over_period, params)
    return float(phase[0] + phase[3] - phase[1] - phase[2])


def reduced_spin_state(
    t_over_period: float,
    params: GateParameters = GateParameters(),
    mean_phonon: float = 0.0,
) -> np.ndarray:
    """Trace both oscillator modes out of an equal four-branch input state."""

    if mean_phonon < 0:
        raise ValueError("mean_phonon must be non-negative")
    alpha = branch_displacements(t_over_period, params)
    phase = branch_phases(t_over_period, params)
    rho = np.empty((4, 4), dtype=complex)
    thermal_factor = 2.0 * float(mean_phonon) + 1.0
    for row in range(4):
        for col in range(4):
            delta = alpha[row] - alpha[col]
            overlap = np.exp(-0.5 * thermal_factor * np.vdot(delta, delta).real)
            rho[row, col] = 0.25 * overlap * np.exp(1j * (phase[row] - phase[col]))
    return 0.5 * (rho + rho.conj().T)


def rotated_basis_populations(rho: np.ndarray) -> dict[str, float]:
    """Populations in |g/r> tensor |+/-〉 for branch order BRANCHES."""

    if rho.shape != (4, 4):
        raise ValueError("rho must have shape (4, 4)")
    result: dict[str, float] = {}
    for atom, offset in (("g", 0), ("r", 2)):
        coherence = float(np.real(rho[offset, offset + 1]))
        diagonal = 0.5 * float(np.real(rho[offset, offset] + rho[offset + 1, offset + 1]))
        result[f"{atom}_plus"] = diagonal + coherence
        result[f"{atom}_minus"] = diagonal - coherence
    return result


def concurrence(rho: np.ndarray) -> float:
    """Wootters concurrence for a two-qubit density matrix."""

    sigma_y = np.asarray(((0.0, -1j), (1j, 0.0)))
    spin_flip = np.kron(sigma_y, sigma_y)
    product = rho @ spin_flip @ rho.conj() @ spin_flip
    eigenvalues = np.linalg.eigvals(product)
    roots = np.sort(np.sqrt(np.clip(np.real(eigenvalues), 0.0, None)))[::-1]
    return float(np.clip(roots[0] - np.sum(roots[1:]), 0.0, 1.0))


def ion_zero_point_m(params: GateParameters = GateParameters()) -> float:
    omega = 2.0 * np.pi * params.trap_frequency_hz
    mass = params.ion_mass_amu * ATOMIC_MASS
    return float(np.sqrt(HBAR / (2.0 * mass * omega)))


def cz_distance_m(c4_j_m4: float, params: GateParameters = GateParameters()) -> float:
    """Operating distance implied by the pi-phase condition."""

    if c4_j_m4 <= 0:
        raise ValueError("c4_j_m4 must be positive")
    omega = 2.0 * np.pi * params.trap_frequency_hz
    numerator = 8.0 * np.sqrt(2.0) * c4_j_m4 * ion_zero_point_m(params)
    return float((numerator / (HBAR * omega)) ** 0.2)


def decay_infidelity(gate_time_us: np.ndarray | float, lifetime_us: float) -> np.ndarray:
    """Half-basis process-averaged exponential decay probability."""

    if lifetime_us <= 0:
        raise ValueError("lifetime_us must be positive")
    time = np.asarray(gate_time_us, dtype=float)
    if np.any(time < 0):
        raise ValueError("gate_time_us must be non-negative")
    return -0.5 * np.expm1(-time / lifetime_us)


def anharmonic_infidelity(
    mean_phonon: np.ndarray | float,
    eta: float,
    coupling_ratio: float = GateParameters().coupling_ratio,
    reference_eta: float = 1.88e-3,
) -> np.ndarray:
    """Feature model reconstructed from SM S7 and its stated checkpoints."""

    occupation = np.asarray(mean_phonon, dtype=float)
    if np.any(occupation < 0) or eta <= 0:
        raise ValueError("mean_phonon must be non-negative and eta positive")
    x = 10.0 * np.pi * eta * coupling_ratio * (occupation + 0.5)
    zero_point = 3.0e-4 * (eta / reference_eta) ** 2
    return zero_point + 0.5 * np.square(x) / (1.0 + np.square(x))


def total_gate_infidelity(
    mean_phonon: np.ndarray | float,
    eta: float,
    lifetime_us: float,
    gate_time_us: float = 5.0,
    technical_error: float = 0.0,
) -> np.ndarray:
    return (
        anharmonic_infidelity(mean_phonon, eta)
        + decay_infidelity(gate_time_us, lifetime_us)
        + float(technical_error)
    )


def chain_gate_duration_us(number_of_ions: np.ndarray | float) -> np.ndarray:
    """Minimal disclosed-contract surrogate for Fig. 3 duration."""

    n_ions = np.asarray(number_of_ions, dtype=float)
    if np.any(n_ions < 1):
        raise ValueError("number_of_ions must be at least one")
    return np.where(n_ions <= 25.0, 5.0, 5.0 + 10.0 * (n_ions - 25.0) / 75.0)


def interconnect_times_us(distance_um: np.ndarray | float) -> dict[str, np.ndarray]:
    """Timing curves described around Fig. 4(a)."""

    distance = np.asarray(distance_um, dtype=float)
    if np.any(distance <= 0):
        raise ValueError("distance_um must be positive")
    return {
        "hybrid": 10.0 + 2.0 * distance,
        "ion_qccd": 600.0 + 5.0 * distance,
        "photon": np.full_like(distance, 4_000.0),
    }


def hybrid_storage_error_per_operation(
    number_of_operations: np.ndarray | float,
    transfer_error: float,
) -> np.ndarray:
    operations = np.asarray(number_of_operations, dtype=float)
    if np.any(operations <= 0) or transfer_error < 0:
        raise ValueError("operations must be positive and transfer_error non-negative")
    return 2.0 * transfer_error / operations


def fowler_logical_error(
    distance: np.ndarray | float,
    physical_error: float,
    threshold: float,
    prefactor: float = 0.1,
) -> np.ndarray:
    if physical_error <= 0 or threshold <= 0 or prefactor <= 0:
        raise ValueError("Fowler parameters must be positive")
    code_distance = np.asarray(distance, dtype=float)
    return prefactor * (physical_error / threshold) ** ((code_distance + 1.0) / 2.0)
