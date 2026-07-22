"""Independent numerical objects for arXiv:2005.12667, Secs. III-IV.

The implementation follows the equations recorded in ``EQUATION_CARDS.json``.
All frequencies are angular frequencies in one consistent unit and ``hbar=1``.
Paper equation numbers in docstrings refer to arXiv v1, the source requested by
the user.  The published RMP version renumbered several equations.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.integrate import solve_ivp
from scipy.optimize import linear_sum_assignment


ComplexMatrix = NDArray[np.complex128]


def annihilation(dimension: int) -> ComplexMatrix:
    """Return the truncated bosonic annihilation operator."""

    if dimension < 2:
        raise ValueError("dimension must be at least 2")
    operator = np.zeros((dimension, dimension), dtype=np.complex128)
    operator[np.arange(dimension - 1), np.arange(1, dimension)] = np.sqrt(
        np.arange(1, dimension)
    )
    return operator


def transmon_coupling(
    omega_r: float,
    capacitance_ratio: float,
    ej_over_ec: float,
    impedance: float,
    resistance_quantum: float = 25_812.80745,
) -> float:
    """Eq. (31): capacitive transmon-resonator coupling ``g``."""

    if min(omega_r, capacitance_ratio, ej_over_ec, impedance) <= 0:
        raise ValueError("coupling parameters must be positive")
    return (
        omega_r
        * capacitance_ratio
        * (ej_over_ec / 2.0) ** 0.25
        * np.sqrt(np.pi * impedance / resistance_quantum)
    )


def transmon_coupling_via_alpha(
    omega_r: float,
    capacitance_ratio: float,
    ej_over_ec: float,
    impedance: float,
    vacuum_impedance: float = 376.730313668,
    resistance_quantum: float = 25_812.80745,
) -> float:
    """Eq. (33), algebraically equivalent to :func:`transmon_coupling`."""

    alpha = vacuum_impedance / (2.0 * resistance_quantum)
    return (
        omega_r
        * capacitance_ratio
        * (ej_over_ec / 2.0) ** 0.25
        * np.sqrt(impedance / vacuum_impedance)
        * np.sqrt(2.0 * np.pi * alpha)
    )


def jc_block(n: int, omega_r: float, omega_q: float, coupling: float) -> ComplexMatrix:
    """Jaynes-Cummings block in ``{|g,n>, |e,n-1>}`` with the paper shift.

    The paper adds the harmless global energy ``omega_r/2``.  With that shift,
    diagonalizing this matrix gives Eq. (38) directly.
    """

    if n < 1:
        raise ValueError("the doublet index n must be at least 1")
    detuning = omega_q - omega_r
    return np.array(
        [
            [n * omega_r - detuning / 2.0, coupling * np.sqrt(n)],
            [coupling * np.sqrt(n), n * omega_r + detuning / 2.0],
        ],
        dtype=np.complex128,
    )


def jc_analytic_energies(
    n: int, omega_r: float, omega_q: float, coupling: float
) -> tuple[float, float]:
    """Eq. (38): lower and upper dressed energies of excitation manifold ``n``."""

    detuning = omega_q - omega_r
    half_splitting = 0.5 * np.sqrt(detuning**2 + 4.0 * coupling**2 * n)
    center = n * omega_r
    return center - half_splitting, center + half_splitting


def jc_mixing_angle(n: int, omega_r: float, omega_q: float, coupling: float) -> float:
    """Eq. (39) mixing angle, using ``atan2`` to preserve the branch."""

    if n < 1:
        raise ValueError("the doublet index n must be at least 1")
    return float(np.arctan2(2.0 * coupling * np.sqrt(n), omega_q - omega_r))


def duffing_jc_hamiltonian(
    cavity_dimension: int,
    transmon_dimension: int,
    omega_r: float,
    omega_q: float,
    coupling: float,
    charging_energy_frequency: float,
) -> ComplexMatrix:
    """Eq. (32): RWA Duffing-transmon/Jaynes-Cummings Hamiltonian."""

    a_local = annihilation(cavity_dimension)
    b_local = annihilation(transmon_dimension)
    identity_r = np.eye(cavity_dimension, dtype=np.complex128)
    identity_q = np.eye(transmon_dimension, dtype=np.complex128)
    a = np.kron(a_local, identity_q)
    b = np.kron(identity_r, b_local)
    return (
        omega_r * a.conj().T @ a
        + omega_q * b.conj().T @ b
        - 0.5
        * charging_energy_frequency
        * b.conj().T
        @ b.conj().T
        @ b
        @ b
        + coupling * (b.conj().T @ a + b @ a.conj().T)
    )


def label_bare_state_energies(hamiltonian: ComplexMatrix) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Assign exact eigenstates to bare basis states by maximum total overlap."""

    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
    probabilities = np.abs(eigenvectors) ** 2
    bare_indices, eigen_indices = linear_sum_assignment(-probabilities)
    labelled = np.empty_like(eigenvalues)
    overlaps = np.empty_like(eigenvalues)
    labelled[bare_indices] = eigenvalues[eigen_indices]
    overlaps[bare_indices] = probabilities[bare_indices, eigen_indices]
    return labelled, overlaps


def transmon_dispersive_shifts(
    max_level: int, coupling: float, detuning: float, charging_energy_frequency: float
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Eqs. (40)-(41): Lamb shifts ``Lambda_j`` and cavity pulls ``chi_j``."""

    if max_level < 0:
        raise ValueError("max_level must be nonnegative")

    def adjacent_shift(j_lower: int) -> float:
        transition_index = j_lower + 1
        denominator = detuning - j_lower * charging_energy_frequency
        if np.isclose(denominator, 0.0):
            raise ValueError("a transmon transition is resonant with the cavity")
        return transition_index * coupling**2 / denominator

    lamb = np.zeros(max_level + 1, dtype=float)
    chi = np.zeros(max_level + 1, dtype=float)
    for j in range(max_level + 1):
        lower = adjacent_shift(j - 1) if j > 0 else 0.0
        upper = adjacent_shift(j)
        lamb[j] = lower
        chi[j] = lower - upper
    return lamb, chi


def transmon_dispersive_energy(
    transmon_level: int,
    photon_number: int,
    omega_r: float,
    omega_q: float,
    charging_energy_frequency: float,
    lamb_shift: ArrayLike,
    cavity_pull: ArrayLike,
) -> float:
    """Diagonal energy read from Eq. (40), in ``hbar=1`` units."""

    lamb = np.asarray(lamb_shift, dtype=float)
    chi = np.asarray(cavity_pull, dtype=float)
    j = transmon_level
    n = photon_number
    return float(
        omega_r * n
        + omega_q * j
        - 0.5 * charging_energy_frequency * j * (j - 1)
        + lamb[j]
        + chi[j] * n
    )


def two_level_dispersive_parameters(
    omega_r: float, omega_q: float, coupling: float, charging_energy_frequency: float
) -> dict[str, float]:
    """Eq. (43): dressed frequencies and state-dependent dispersive shift."""

    detuning = omega_q - omega_r
    denominator = detuning - charging_energy_frequency
    if np.isclose(detuning * denominator, 0.0):
        raise ValueError("Eq. (43) is singular on resonance or in the straddling pole")
    return {
        "omega_r_dressed": omega_r - coupling**2 / denominator,
        "omega_q_dressed": omega_q + coupling**2 / detuning,
        "chi": -(coupling**2 * charging_energy_frequency)
        / (detuning * denominator),
    }


def critical_photon_number(
    transmon_level: int, coupling: float, detuning: float, charging_energy_frequency: float
) -> float:
    """Eq. (44): level-dependent critical photon-number estimate."""

    j = transmon_level
    return (
        (abs(detuning - j * charging_energy_frequency) ** 2 / (4.0 * coupling**2) - j)
        / (2 * j + 1)
    )


def linear_dressed_frequencies(
    omega_r: float, omega_q: float, coupling: float
) -> tuple[float, float]:
    """Eqs. (49a)-(49b), ordered for ``omega_q > omega_r``."""

    detuning = omega_q - omega_r
    split = np.sqrt(detuning**2 + 4.0 * coupling**2)
    return (omega_r + omega_q - split) / 2.0, (omega_r + omega_q + split) / 2.0


def bogoliubov_kerrs(
    coupling: float, detuning: float, charging_energy_frequency: float
) -> dict[str, float]:
    """Leading Kerr coefficients, using the correction in formal RMP Eq. (53).

    ArXiv v1 Eq. (51) prints an extra factor 1/2 in ``K_a``.  Expanding
    ``-(E_C/2) sin(Lambda)^4 a_dagger^2 a^2`` and comparing with the
    convention ``(hbar K_a/2) a_dagger^2 a^2`` gives the expression below.
    """

    if np.isclose(detuning * (detuning - charging_energy_frequency), 0.0):
        raise ValueError("Kerr expansion is singular at the chosen detuning")
    return {
        "K_a": -charging_energy_frequency * (coupling / detuning) ** 4,
        "K_b": -charging_energy_frequency,
        "chi_ab": -(2.0 * coupling**2 * charging_energy_frequency)
        / (detuning * (detuning - charging_energy_frequency)),
    }


@dataclass(frozen=True)
class BlackBoxKerr:
    chi: NDArray[np.float64]
    self_kerr: NDArray[np.float64]
    frequency_shift: NDArray[np.float64]
    participation: NDArray[np.float64]


def black_box_kerr(
    frequencies: ArrayLike, phase_zpf: ArrayLike, josephson_energy_frequency: float
) -> BlackBoxKerr:
    """Eqs. (55)-(58): black-box Kerr matrix from junction phase fluctuations."""

    omega = np.asarray(frequencies, dtype=float)
    phi = np.asarray(phase_zpf, dtype=float)
    if omega.ndim != 1 or phi.shape != omega.shape:
        raise ValueError("frequencies and phase_zpf must be one-dimensional and equal-length")
    chi = -josephson_energy_frequency * np.outer(phi**2, phi**2)
    participation = 2.0 * josephson_energy_frequency * phi**2 / omega
    return BlackBoxKerr(
        chi=chi,
        self_kerr=np.diag(chi) / 2.0,
        frequency_shift=0.5 * np.sum(chi, axis=1),
        participation=participation,
    )


def generic_multilevel_shifts(
    level_frequencies: ArrayLike, coupling_matrix: ArrayLike, omega_r: float
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Eqs. (61)-(62): second-order shifts for an arbitrary artificial atom."""

    levels = np.asarray(level_frequencies, dtype=float)
    couplings = np.asarray(coupling_matrix, dtype=np.complex128)
    if couplings.shape != (levels.size, levels.size):
        raise ValueError("coupling_matrix must be square with one row per level")
    lamb = np.zeros_like(levels)
    chi = np.zeros_like(levels)
    for j in range(levels.size):
        for i in range(levels.size):
            magnitude = abs(couplings[i, j]) ** 2
            if magnitude == 0.0:
                continue
            denominator_down = levels[j] - levels[i] - omega_r
            denominator_up = levels[i] - levels[j] - omega_r
            if np.isclose(denominator_down * denominator_up, 0.0):
                raise ValueError("multilevel dispersive denominator is zero")
            lamb[j] += magnitude / denominator_down
            chi[j] += magnitude / denominator_down - magnitude / denominator_up
    return lamb, chi


def longitudinal_block(
    oscillator_dimension: int,
    omega_r: float,
    omega_q: float,
    longitudinal_coupling: float,
    sigma_z: int,
) -> ComplexMatrix:
    """Eq. (63) restricted to one ``sigma_z=+/-1`` sector."""

    if sigma_z not in {-1, 1}:
        raise ValueError("sigma_z must be -1 or +1")
    a = annihilation(oscillator_dimension)
    return (
        omega_r * a.conj().T @ a
        + sigma_z * omega_q / 2.0 * np.eye(oscillator_dimension)
        + sigma_z * longitudinal_coupling * (a.conj().T + a)
    )


def longitudinal_analytic_energy(
    photon_number: int,
    omega_r: float,
    omega_q: float,
    longitudinal_coupling: float,
    sigma_z: int,
) -> float:
    """Completed-square spectrum of Eq. (63)."""

    return (
        photon_number * omega_r
        + sigma_z * omega_q / 2.0
        - longitudinal_coupling**2 / omega_r
    )


def dissipator(operator: ComplexMatrix, rho: ComplexMatrix) -> ComplexMatrix:
    """Eq. (69): Lindblad dissipator ``D[operator] rho``."""

    product = operator.conj().T @ operator
    return operator @ rho @ operator.conj().T - 0.5 * (product @ rho + rho @ product)


def lindblad_rhs(
    rho: ComplexMatrix, hamiltonian: ComplexMatrix, collapse_operators: list[ComplexMatrix]
) -> ComplexMatrix:
    """Eq. (68) with rates absorbed into the collapse operators and ``hbar=1``."""

    derivative = -1j * (hamiltonian @ rho - rho @ hamiltonian)
    for operator in collapse_operators:
        derivative += dissipator(operator, rho)
    return derivative


def thermal_oscillator_evolution(
    dimension: int,
    omega_r: float,
    kappa: float,
    thermal_occupation: float,
    initial_fock_state: int,
    times: ArrayLike,
) -> NDArray[np.complex128]:
    """Integrate Eq. (68) for a thermal harmonic oscillator."""

    if not 0 <= initial_fock_state < dimension:
        raise ValueError("initial_fock_state is outside the truncated oscillator")
    sample_times = np.asarray(times, dtype=float)
    a = annihilation(dimension)
    number = a.conj().T @ a
    hamiltonian = omega_r * number
    collapse = [np.sqrt(kappa * (thermal_occupation + 1.0)) * a]
    if thermal_occupation > 0.0:
        collapse.append(np.sqrt(kappa * thermal_occupation) * a.conj().T)
    rho0 = np.zeros((dimension, dimension), dtype=np.complex128)
    rho0[initial_fock_state, initial_fock_state] = 1.0

    def rhs(_: float, flat_rho: NDArray[np.complex128]) -> NDArray[np.complex128]:
        rho = flat_rho.reshape((dimension, dimension))
        return lindblad_rhs(rho, hamiltonian, collapse).reshape(-1)

    solution = solve_ivp(
        rhs,
        (float(sample_times[0]), float(sample_times[-1])),
        rho0.reshape(-1),
        t_eval=sample_times,
        rtol=2e-10,
        atol=2e-12,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution.y.T.reshape((-1, dimension, dimension))


def passive_one_port_response(
    detuning: ArrayLike, kappa: float, input_amplitude: complex = 1.0 + 0.0j
) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
    """Passive form equivalent to Eqs. (72) and (75), up to port phases.

    We use ``dot(a)=-(i*Delta+kappa/2)a+sqrt(kappa)b_in`` and
    ``b_out=b_in-sqrt(kappa)a``.  The relative minus sign is required by
    one-port passivity.  The paper's displayed signs are discussed explicitly
    in ``DERIVATION_TRACE.md``.
    """

    delta = np.asarray(detuning, dtype=float)
    cavity = np.sqrt(kappa) * input_amplitude / (1j * delta + kappa / 2.0)
    output = input_amplitude - np.sqrt(kappa) * cavity
    return cavity, output


def discretized_bath_hamiltonians(
    system_dimension: int = 3,
    bath_dimension: int = 3,
    coupling: float = 0.07,
) -> dict[str, ComplexMatrix]:
    """Finite-mode Hermiticity audit of arXiv Eqs. (66)-(67).

    The literal arXiv-v1 Eq. (67) has a minus sign and is anti-Hermitian.  The
    published RMP equation uses the Hermitian ``a b^dagger + a^dagger b``.
    """

    a = np.kron(annihilation(system_dimension), np.eye(bath_dimension))
    b = np.kron(np.eye(system_dimension), annihilation(bath_dimension))
    full_interaction = -coupling * (b.conj().T - b) @ (a.conj().T - a)
    arxiv_literal_rwa = coupling * (a @ b.conj().T - a.conj().T @ b)
    published_rwa = coupling * (a @ b.conj().T + a.conj().T @ b)
    return {
        "eq66_full": full_interaction,
        "eq67_arxiv_literal": arxiv_literal_rwa,
        "eq67_published_correction": published_rwa,
    }
