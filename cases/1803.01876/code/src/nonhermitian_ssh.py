"""Numerical kernels for the non-Hermitian SSH pilot."""

from __future__ import annotations

import numpy as np

try:
    from scipy.optimize import linear_sum_assignment
except ImportError:  # pragma: no cover - SciPy is part of the harness runtime.
    linear_sum_assignment = None


def open_chain_hamiltonian(
    L: int,
    t1: float,
    t2: float = 1.0,
    gamma: float = 4.0 / 3.0,
    t3: float = 0.0,
    left_bond_delta: float = 0.0,
) -> np.ndarray:
    """Return the open-boundary real-space Hamiltonian for the t3=0 model.

    Basis order is (A_1, B_1, A_2, B_2, ..., A_L, B_L). The optional
    left_bond_delta implements the Fig. 2(d) perturbation in a later target.
    """

    if L <= 0:
        raise ValueError("L must be positive")

    h = np.zeros((2 * L, 2 * L), dtype=np.complex128)

    for n in range(L):
        a = 2 * n
        b = a + 1
        local_t1 = t1 + left_bond_delta if n == 0 else t1

        h[a, b] = local_t1 + gamma / 2.0
        h[b, a] = local_t1 - gamma / 2.0

        if n > 0:
            h[a, 2 * (n - 1) + 1] = t2
            h[b, 2 * (n - 1)] = t3
        if n < L - 1:
            h[b, 2 * (n + 1)] = t2
            h[a, 2 * (n + 1) + 1] = t3

    return h


def open_chain_eigenvalues(
    L: int,
    t1: float,
    t2: float = 1.0,
    gamma: float = 4.0 / 3.0,
    t3: float = 0.0,
    left_bond_delta: float = 0.0,
    method: str = "chiral_block",
) -> np.ndarray:
    """Compute open-chain eigenvalues for the t3=0 model."""

    h = open_chain_hamiltonian(
        L=L,
        t1=t1,
        t2=t2,
        gamma=gamma,
        t3=t3,
        left_bond_delta=left_bond_delta,
    )
    if method == "direct":
        return np.linalg.eigvals(h)
    if method == "chiral_block":
        return chiral_block_eigenvalues(h)
    raise ValueError(f"unknown eigenvalue method: {method}")


def open_chain_squared_eigenvalues(
    L: int,
    t1: float,
    t2: float = 1.0,
    gamma: float = 4.0 / 3.0,
    t3: float = 0.0,
    left_bond_delta: float = 0.0,
) -> np.ndarray:
    """Compute the chiral-block eigenvalues E^2 for branch tracking."""

    h = open_chain_hamiltonian(
        L=L,
        t1=t1,
        t2=t2,
        gamma=gamma,
        t3=t3,
        left_bond_delta=left_bond_delta,
    )
    c_block = h[0::2, 1::2]
    d_block = h[1::2, 0::2]
    return stable_squared_chiral_spectrum(c_block @ d_block)


def track_eigenvalue_branches(eigenvalue_slices: list[np.ndarray]) -> list[np.ndarray]:
    """Order eigenvalues by continuity across neighboring parameter samples.

    Each visible spectrum line represents one eigenvalue branch as the swept
    parameter changes. A per-slice sort such as ``band_index`` is therefore not
    a valid line identity; it can swap labels at crossings or near-degeneracies.
    """

    slices = [np.asarray(values, dtype=np.complex128).reshape(-1) for values in eigenvalue_slices]
    if not slices:
        return []

    branch_count = len(slices[0])
    for values in slices:
        if len(values) != branch_count:
            raise ValueError("all eigenvalue slices must have the same length")

    start_order = np.lexsort((slices[0].imag, slices[0].real, np.abs(slices[0])))
    previous = slices[0][start_order].copy()
    tracked = [previous]
    for current in slices[1:]:
        cost = np.abs(previous[:, None] - current[None, :])
        previous_indices, current_indices = minimum_cost_assignment(cost)
        ordered = np.empty_like(previous)
        ordered[previous_indices] = current[current_indices]
        tracked.append(ordered)
        previous = ordered
    return tracked


def branch_tracked_spectrum_rows(
    t1_values: np.ndarray,
    eigenvalue_slices: list[np.ndarray],
) -> list[dict[str, float | int]]:
    """Return plot/data rows with branch identity and local band rank separated."""

    tracked = track_eigenvalue_branches(eigenvalue_slices)
    if len(t1_values) != len(tracked):
        raise ValueError("t1_values and eigenvalue_slices must have the same length")

    rows: list[dict[str, float | int]] = []
    for t1, values in zip(t1_values, tracked):
        abs_order = np.argsort(np.abs(values))
        abs_rank = np.empty(len(values), dtype=int)
        abs_rank[abs_order] = np.arange(len(values))
        for branch_id, value in enumerate(values):
            rows.append(
                {
                    "t1": float(t1),
                    "branch_id": int(branch_id),
                    "band_index": int(abs_rank[branch_id]),
                    "real_E": float(np.real(value)),
                    "imag_E": float(np.imag(value)),
                    "abs_E": float(abs(value)),
                }
            )
    return rows


def abs_rank_spectrum_rows(
    t1_values: np.ndarray,
    eigenvalue_slices: list[np.ndarray],
) -> list[dict[str, float | int]]:
    """Return rows whose branch id is the per-parameter ordered |E| level."""

    if len(t1_values) != len(eigenvalue_slices):
        raise ValueError("t1_values and eigenvalue_slices must have the same length")

    rows: list[dict[str, float | int]] = []
    for t1, values in zip(t1_values, eigenvalue_slices):
        values = np.asarray(values, dtype=np.complex128).reshape(-1)
        order = np.argsort(np.abs(values), kind="mergesort")
        for rank, value in enumerate(values[order]):
            rows.append(
                {
                    "t1": float(t1),
                    "branch_id": int(rank),
                    "band_index": int(rank),
                    "real_E": float(np.real(value)),
                    "imag_E": float(np.imag(value)),
                    "abs_E": float(abs(value)),
                }
            )
    return rows


def abs_ordered_squared_spectrum_rows(
    t1_values: np.ndarray,
    squared_eigenvalue_slices: list[np.ndarray],
) -> list[dict[str, float | int]]:
    """Return |E| rows whose branch id is the ordered absolute-energy level.

    For a panel that only shows ``|E|``, the visible line is the ordered open-chain
    spectrum level. Tracking the complex square-root branch can introduce
    artificial sign/phase swaps that are invisible in the plotted quantity.
    """

    if len(t1_values) != len(squared_eigenvalue_slices):
        raise ValueError("t1_values and squared_eigenvalue_slices must have the same length")

    rows: list[dict[str, float | int]] = []
    for t1, values in zip(t1_values, squared_eigenvalue_slices):
        values = np.asarray(values, dtype=np.complex128).reshape(-1)
        abs_energy = np.sqrt(np.abs(values))
        order = np.argsort(abs_energy)
        for branch_id, squared_energy in enumerate(values[order]):
            energy = signed_complex_sqrt(np.asarray([squared_energy]))[0]
            rows.append(
                {
                    "t1": float(t1),
                    "branch_id": int(branch_id),
                    "band_index": int(branch_id),
                    "real_E": float(np.real(energy)),
                    "imag_E": float(np.imag(energy)),
                    "abs_E": float(np.sqrt(abs(squared_energy))),
                }
            )
    return rows


def minimum_cost_assignment(cost: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return a global minimum-cost one-to-one assignment."""

    if linear_sum_assignment is not None:
        return linear_sum_assignment(cost)
    return greedy_minimum_cost_assignment(cost)


def greedy_minimum_cost_assignment(cost: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Small fallback for environments without SciPy's Hungarian solver."""

    cost = np.asarray(cost)
    pairs = [
        (float(cost[row, column]), row, column)
        for row in range(cost.shape[0])
        for column in range(cost.shape[1])
    ]
    pairs.sort()
    assigned_rows: set[int] = set()
    assigned_columns: set[int] = set()
    row_indices = []
    column_indices = []
    for _, row, column in pairs:
        if row in assigned_rows or column in assigned_columns:
            continue
        assigned_rows.add(row)
        assigned_columns.add(column)
        row_indices.append(row)
        column_indices.append(column)
        if len(row_indices) == min(cost.shape):
            break
    return np.asarray(row_indices, dtype=int), np.asarray(column_indices, dtype=int)


def chiral_block_eigenvalues(h: np.ndarray) -> np.ndarray:
    """Compute eigenvalues using the off-diagonal chiral block structure.

    In the alternating basis, the Hamiltonian has sublattice blocks
    H = [[0, C], [D, 0]] after grouping A sites before B sites. The squared
    energies are eigenvalues of C D. Returning +/- sqrt(lambda) enforces the
    exact E -> -E symmetry and is more stable for this non-normal matrix.
    """

    c_block = h[0::2, 1::2]
    d_block = h[1::2, 0::2]
    squared_matrix = c_block @ d_block
    squared = stable_squared_chiral_spectrum(squared_matrix)
    branch = signed_complex_sqrt(squared)
    return np.concatenate([branch, -branch])


def stable_squared_chiral_spectrum(squared_matrix: np.ndarray) -> np.ndarray:
    """Return eigenvalues of C D with a stable tridiagonal path when possible."""

    tridiagonal = tridiagonal_similarity_form(squared_matrix)
    if tridiagonal is not None:
        if np.allclose(tridiagonal.imag, 0.0, atol=1e-12):
            return np.linalg.eigvalsh(tridiagonal.real)
        return np.linalg.eigvals(tridiagonal)
    return np.linalg.eigvals(squared_matrix)


def tridiagonal_similarity_form(matrix: np.ndarray) -> np.ndarray | None:
    """Build the symmetric tridiagonal matrix similar to a tridiagonal matrix."""

    matrix = np.asarray(matrix, dtype=np.complex128)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        return None
    size = matrix.shape[0]
    if size == 0:
        return matrix.copy()

    far_mask = np.fromfunction(lambda i, j: np.abs(i - j) > 1, matrix.shape)
    if np.max(np.abs(matrix[far_mask])) > 1e-12:
        return None

    transformed = np.diag(np.diag(matrix)).astype(np.complex128)
    for i in range(size - 1):
        upper = matrix[i, i + 1]
        lower = matrix[i + 1, i]
        product = upper * lower
        if abs(product) < 1e-28:
            offdiag = 0.0j
        else:
            offdiag = np.sqrt(product)
        transformed[i, i + 1] = offdiag
        transformed[i + 1, i] = offdiag
    return transformed


def signed_complex_sqrt(values: np.ndarray) -> np.ndarray:
    """Take sqrt while suppressing roundoff-scale imaginary artifacts."""

    values = np.asarray(values, dtype=np.complex128)
    cleaned = values.copy()
    tiny_real_negative = (np.abs(cleaned.imag) < 1e-12) & (cleaned.real < 0.0) & (cleaned.real > -1e-12)
    cleaned[tiny_real_negative] = 0.0
    cleaned[np.abs(cleaned) < 1e-24] = 0.0
    return np.sqrt(cleaned)


def analytic_transition(t2: float = 1.0, gamma: float = 4.0 / 3.0) -> float:
    """Open-boundary transition |t1| from the paper's shortcut solution."""

    return float(np.sqrt(t2 * t2 + (gamma / 2.0) ** 2))


def generalized_brillouin_radius(t1: float, gamma: float = 4.0 / 3.0) -> float:
    """Return the t3=0 generalized Brillouin-zone radius."""

    denominator = t1 + gamma / 2.0
    if abs(denominator) < 1e-12:
        raise ValueError("C_beta radius is singular at t1 = -gamma/2")
    return float(np.sqrt(abs((t1 - gamma / 2.0) / denominator)))


def non_bloch_ab(
    beta: np.ndarray,
    t1: float,
    t2: float = 1.0,
    gamma: float = 4.0 / 3.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Return a(beta), b(beta) for H(beta) = [[0,b],[a,0]]."""

    beta = np.asarray(beta, dtype=np.complex128)
    a_beta = t1 - gamma / 2.0 + t2 * beta
    b_beta = t1 + gamma / 2.0 + t2 / beta
    return a_beta, b_beta


def non_bloch_ab_t3(
    beta: np.ndarray,
    t1: float,
    t2: float = 1.0,
    gamma: float = 4.0 / 3.0,
    t3: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Return a(beta), b(beta) for the nonzero-t3 Hamiltonian."""

    beta = np.asarray(beta, dtype=np.complex128)
    a_beta = t3 / beta + (t1 - gamma / 2.0) + t2 * beta
    b_beta = t2 / beta + (t1 + gamma / 2.0) + t3 * beta
    return a_beta, b_beta


def beta_roots_from_energy(
    energy: np.ndarray,
    t1: float,
    t2: float = 1.0,
    gamma: float = 4.0 / 3.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the two beta roots from Eq. (bulkeigen) for t3=0."""

    energy = np.asarray(energy, dtype=np.complex128)
    denominator = 2.0 * t2 * (t1 + gamma / 2.0)
    if abs(denominator) < 1e-12:
        raise ValueError("beta-root formula is singular at t1 = -gamma/2")
    numerator = energy**2 + gamma**2 / 4.0 - t1**2 - t2**2
    discriminant = numerator**2 - 4.0 * t2**2 * (t1**2 - gamma**2 / 4.0)
    root = np.sqrt(discriminant.astype(np.complex128))
    beta_1 = (numerator + root) / denominator
    beta_2 = (numerator - root) / denominator
    return beta_1, beta_2


def beta_roots_t3_from_energy(
    energy: complex,
    t1: float,
    t2: float = 1.0,
    gamma: float = 4.0 / 3.0,
    t3: float = 0.0,
) -> np.ndarray:
    """Return the four beta roots from Eq. (t3E)."""

    a0 = t1 - gamma / 2.0
    b0 = t1 + gamma / 2.0
    coefficients = [
        t2 * t3,
        a0 * t3 + b0 * t2,
        t2 * t2 + a0 * b0 + t3 * t3 - energy**2,
        b0 * t3 + a0 * t2,
        t2 * t3,
    ]
    if abs(t2 * t3) < 1e-14:
        raise ValueError("quartic beta-root formula requires nonzero t2 and t3")
    return np.roots(np.asarray(coefficients, dtype=np.complex128))


def open_chain_eigensystem(
    L: int,
    t1: float,
    t2: float = 1.0,
    gamma: float = 4.0 / 3.0,
    t3: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Return right eigenvalues and eigenvectors for the open chain."""

    h = open_chain_hamiltonian(L=L, t1=t1, t2=t2, gamma=gamma, t3=t3)
    return np.linalg.eig(h)


def cell_profile(vector: np.ndarray) -> np.ndarray:
    """Return per-cell right-eigenvector amplitude profile."""

    amplitudes = np.sqrt(np.abs(vector[0::2]) ** 2 + np.abs(vector[1::2]) ** 2)
    scale = np.max(amplitudes)
    if scale == 0:
        return amplitudes
    return amplitudes / scale


def analytic_left_zero_mode_profile(
    L: int,
    t1: float,
    t2: float = 1.0,
    gamma: float = 4.0 / 3.0,
) -> np.ndarray:
    """Return the normalized left zero-mode profile for the t3=0 model."""

    beta_zero = -(t1 - gamma / 2.0) / t2
    cells = np.arange(L)
    profile = np.abs(beta_zero) ** cells
    scale = np.max(profile)
    return profile / scale if scale else profile


def non_bloch_winding_t3_zero(
    t1: float,
    t2: float = 1.0,
    gamma: float = 4.0 / 3.0,
    n_beta: int = 150,
) -> tuple[int, float, float]:
    """Compute W for the t3=0 non-Bloch invariant.

    Returns (W, wind_a, wind_b), using W = (wind_a - wind_b) / 2.
    """

    if n_beta < 8:
        raise ValueError("n_beta must be at least 8")
    radius = generalized_brillouin_radius(t1=t1, gamma=gamma)
    angles = np.linspace(0.0, 2.0 * np.pi, n_beta, endpoint=False)
    beta = radius * np.exp(1j * angles)
    a_beta, b_beta = non_bloch_ab(beta=beta, t1=t1, t2=t2, gamma=gamma)
    wind_a = phase_winding(a_beta)
    wind_b = phase_winding(b_beta)
    winding = int(round((wind_a - wind_b) / 2.0))
    return winding, wind_a, wind_b


def phase_winding(values: np.ndarray) -> float:
    """Return the integer winding of a closed complex curve around zero."""

    values = np.asarray(values, dtype=np.complex128)
    closed = np.concatenate([values, values[:1]])
    phase = np.unwrap(np.angle(closed))
    return float((phase[-1] - phase[0]) / (2.0 * np.pi))


def chiral_pair_residual(eigenvalues: np.ndarray) -> float:
    """Return max nearest-neighbor residual for the symmetry E -> -E.

    This avoids greedy global pairing, which is unstable near dense spectra.
    """

    eig = np.asarray(eigenvalues)
    distances = np.abs(eig[:, None] + eig[None, :])
    np.fill_diagonal(distances, np.inf)
    return float(np.max(np.min(distances, axis=1)))
