"""Exact Bose-Hubbard dynamics in a fixed-particle-number sector.

The domain object is an occupation basis with an invariant total particle
number.  Hamiltonian construction, evolution, and observables are kept here;
file formats and plotting live in the runner.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from numpy.typing import NDArray


RealArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]
Basis = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class BackendResult:
    """Evolved states together with the backend provenance."""

    states: ComplexArray
    backend: str
    accelerator: str


def mhz_to_rad_per_ns(values: Sequence[float] | RealArray) -> RealArray:
    """Convert f/(2*pi) in MHz to angular frequency in rad/ns."""

    return np.asarray(values, dtype=np.float64) * (2.0 * np.pi * 1.0e-3)


def occupation_basis(
    site_count: int,
    particle_count: int,
    max_occupation: int | None = None,
) -> Basis:
    """Enumerate occupation tuples satisfying the sector invariants."""

    if site_count <= 0 or particle_count < 0:
        raise ValueError("site_count must be positive and particle_count non-negative")
    cap = particle_count if max_occupation is None else max_occupation
    if cap < 0 or site_count * cap < particle_count:
        raise ValueError("occupation cap cannot hold the requested particles")

    states: list[tuple[int, ...]] = []

    def append_states(prefix: tuple[int, ...], sites_left: int, particles_left: int) -> None:
        if sites_left == 1:
            if particles_left <= cap:
                states.append(prefix + (particles_left,))
            return
        for occupation in range(min(cap, particles_left) + 1):
            append_states(prefix + (occupation,), sites_left - 1, particles_left - occupation)

    append_states((), site_count, particle_count)
    return tuple(states)


def basis_index(basis: Basis) -> dict[tuple[int, ...], int]:
    return {state: index for index, state in enumerate(basis)}


def fock_state(basis: Basis, occupied_sites: Iterable[int]) -> ComplexArray:
    """Return a normalized basis vector for zero-based occupied site indices."""

    occupations = [0] * len(basis[0])
    for site in occupied_sites:
        if site < 0 or site >= len(occupations):
            raise IndexError(f"site {site} outside the chain")
        occupations[site] += 1
    try:
        index = basis_index(basis)[tuple(occupations)]
    except KeyError as exc:
        raise ValueError("requested Fock state is outside the selected basis") from exc
    state = np.zeros(len(basis), dtype=np.complex128)
    state[index] = 1.0
    return state


def build_hamiltonian(
    basis: Basis,
    couplings: Sequence[float] | RealArray,
    interactions: Sequence[float] | RealArray | None = None,
    onsite: Sequence[float] | RealArray | None = None,
) -> RealArray:
    """Build the exact sector Hamiltonian from EQC001-EQC002."""

    site_count = len(basis[0])
    coupling_array = np.asarray(couplings, dtype=np.float64)
    if coupling_array.shape != (site_count - 1,):
        raise ValueError("couplings must contain one value per nearest-neighbor bond")
    interaction_array = (
        np.zeros(site_count, dtype=np.float64)
        if interactions is None
        else np.asarray(interactions, dtype=np.float64)
    )
    onsite_array = (
        np.zeros(site_count, dtype=np.float64)
        if onsite is None
        else np.asarray(onsite, dtype=np.float64)
    )
    if interaction_array.shape != (site_count,) or onsite_array.shape != (site_count,):
        raise ValueError("interactions and onsite must contain one value per site")

    state_to_index = basis_index(basis)
    hamiltonian = np.zeros((len(basis), len(basis)), dtype=np.float64)
    for column, state_tuple in enumerate(basis):
        state = np.asarray(state_tuple, dtype=np.int64)
        hamiltonian[column, column] = np.sum(
            0.5 * interaction_array * state * (state - 1) + onsite_array * state
        )
        for bond, coupling in enumerate(coupling_array):
            if state[bond] > 0:
                moved = state.copy()
                moved[bond] -= 1
                moved[bond + 1] += 1
                row = state_to_index.get(tuple(int(value) for value in moved))
                if row is not None:
                    amplitude = coupling * np.sqrt(state[bond] * (state[bond + 1] + 1))
                    hamiltonian[row, column] += amplitude
            if state[bond + 1] > 0:
                moved = state.copy()
                moved[bond + 1] -= 1
                moved[bond] += 1
                row = state_to_index.get(tuple(int(value) for value in moved))
                if row is not None:
                    amplitude = coupling * np.sqrt(state[bond + 1] * (state[bond] + 1))
                    hamiltonian[row, column] += amplitude
    return hamiltonian


def _cupy_module():
    try:
        import cupy as cp  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError("CuPy backend requested but cupy is not installed") from exc
    if cp.cuda.runtime.getDeviceCount() < 1:
        raise RuntimeError("CuPy backend requested but no CUDA device is visible")
    return cp


def evolve_state(
    hamiltonian: RealArray,
    initial_state: ComplexArray,
    times_ns: Sequence[float] | RealArray,
    backend: str = "numpy",
) -> BackendResult:
    """Evaluate exp(-iHt)|psi0> by one Hermitian eigendecomposition."""

    selected = backend
    if backend == "auto":
        try:
            _cupy_module()
        except RuntimeError:
            selected = "numpy"
        else:
            selected = "cupy"
    times = np.asarray(times_ns, dtype=np.float64)
    if selected == "numpy":
        eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
        coefficients = eigenvectors.conj().T @ initial_state
        phases = np.exp(-1.0j * np.outer(times, eigenvalues))
        states = (phases * coefficients[None, :]) @ eigenvectors.T
        return BackendResult(np.asarray(states), "numpy", "CPU")
    if selected != "cupy":
        raise ValueError("backend must be numpy, cupy, or auto")

    cp = _cupy_module()
    h_gpu = cp.asarray(hamiltonian)
    psi_gpu = cp.asarray(initial_state)
    times_gpu = cp.asarray(times)
    eigenvalues, eigenvectors = cp.linalg.eigh(h_gpu)
    coefficients = eigenvectors.conj().T @ psi_gpu
    phases = cp.exp(-1.0j * times_gpu[:, None] * eigenvalues[None, :])
    states_gpu = (phases * coefficients[None, :]) @ eigenvectors.T
    cp.cuda.Stream.null.synchronize()
    accelerator = cp.cuda.runtime.getDeviceProperties(0)["name"]
    if isinstance(accelerator, bytes):
        accelerator = accelerator.decode("utf-8")
    return BackendResult(cp.asnumpy(states_gpu), "cupy", str(accelerator))


def state_norms(states: ComplexArray) -> RealArray:
    return np.sum(np.abs(states) ** 2, axis=1)


def site_density(states: ComplexArray, basis: Basis) -> RealArray:
    occupations = np.asarray(basis, dtype=np.float64)
    return np.abs(states) ** 2 @ occupations


def one_particle_entropy(density: RealArray) -> RealArray:
    clipped = np.clip(density, 0.0, 1.0)
    result = np.zeros_like(clipped)
    interior = (clipped > 0.0) & (clipped < 1.0)
    probabilities = clipped[interior]
    result[interior] = -probabilities * np.log(probabilities) - (1.0 - probabilities) * np.log1p(
        -probabilities
    )
    return result


def connected_z_correlation(density: RealArray) -> RealArray:
    """Connected sigma-z matrices for one-particle density rows."""

    result = -4.0 * density[:, :, None] * density[:, None, :]
    diagonal = 4.0 * density * (1.0 - density)
    indices = np.arange(density.shape[1])
    result[:, indices, indices] = diagonal
    return result


def one_particle_concurrence(states: ComplexArray) -> RealArray:
    amplitudes = np.abs(states)
    result = 2.0 * amplitudes[:, :, None] * amplitudes[:, None, :]
    indices = np.arange(states.shape[1])
    result[:, indices, indices] = 0.0
    return result


def two_particle_correlator(states: ComplexArray, basis: Basis) -> RealArray:
    occupations = np.asarray(basis, dtype=np.float64)
    basis_correlators = occupations[:, :, None] * occupations[:, None, :]
    indices = np.arange(occupations.shape[1])
    basis_correlators[:, indices, indices] = occupations * (occupations - 1.0)
    return np.tensordot(np.abs(states) ** 2, basis_correlators, axes=(1, 0))


def double_occupancy_probability(correlators: RealArray) -> RealArray:
    return np.diagonal(correlators, axis1=-2, axis2=-1) / 2.0


def normalized_correlation_distance(left: RealArray, right: RealArray) -> float:
    """Frobenius distance between normalized off-diagonal correlator patterns."""

    if left.shape != right.shape or left.ndim != 2:
        raise ValueError("correlators must be two matrices with identical shape")
    mask = ~np.eye(left.shape[0], dtype=bool)
    left_vector = left[mask]
    right_vector = right[mask]
    left_norm = np.linalg.norm(left_vector)
    right_norm = np.linalg.norm(right_vector)
    if left_norm == 0.0 or right_norm == 0.0:
        return float("inf")
    return float(np.linalg.norm(left_vector / left_norm - right_vector / right_norm))


def uniform_group_velocity(couplings_rad_per_ns: Sequence[float] | RealArray) -> float:
    """Uniform-chain ballistic scale in sites per microsecond."""

    return float(2.0 * np.mean(couplings_rad_per_ns) * 1000.0)
