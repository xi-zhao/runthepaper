from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json

import numpy as np
import scipy.linalg
import scipy.ndimage
import scipy.sparse
import scipy.sparse.linalg


@dataclass(frozen=True)
class LongRangeModel:
    """Paper's M=2 onsite-disordered long-range chain.

    Matrix elements follow the paper convention H[i, j] = t_(j-i).
    """

    t_minus_2: float = 1.0
    t_minus_1: float = 1.0
    t_1: float = 1.5
    t_2: float = 0.5

    @property
    def hopping_range(self) -> int:
        return 2

    def hopping(self, displacement: int) -> float:
        values = {
            -2: self.t_minus_2,
            -1: self.t_minus_1,
            1: self.t_1,
            2: self.t_2,
        }
        try:
            return values[displacement]
        except KeyError as exc:
            raise ValueError(f"unsupported displacement: {displacement}") from exc

    def similarity_gauge(self, radius: float) -> "LongRangeModel":
        """Return the OBC-similar model with hoppings ``t_s * radius**s``.

        The diagonal transform improves conditioning of non-normal OBC
        eigensystems without changing their exact eigenvalues. It must not be
        substituted directly for a PBC Hamiltonian because wrapped hoppings
        carry the boundary gauge mismatch.
        """

        if radius <= 0.0:
            raise ValueError("similarity-gauge radius must be positive")
        return LongRangeModel(
            t_minus_2=self.t_minus_2 * radius**-2,
            t_minus_1=self.t_minus_1 * radius**-1,
            t_1=self.t_1 * radius,
            t_2=self.t_2 * radius**2,
        )

    def hamiltonian(
        self,
        onsite: np.ndarray,
        *,
        boundary: str = "obc",
        twist: complex = 1.0 + 0.0j,
    ) -> np.ndarray:
        onsite = np.asarray(onsite, dtype=float)
        if onsite.ndim != 1:
            raise ValueError("onsite disorder must be a one-dimensional array")
        if onsite.size < 2 * self.hopping_range + 1:
            raise ValueError("chain is shorter than the hopping stencil")
        if boundary not in {"obc", "pbc", "twisted"}:
            raise ValueError(f"unknown boundary: {boundary}")
        if boundary != "twisted":
            twist = 1.0 + 0.0j
        if boundary == "twisted" and abs(twist) == 0.0:
            raise ValueError("twist must be nonzero")

        length = onsite.size
        matrix = np.diag(onsite.astype(complex))
        for row in range(length):
            for displacement in (-2, -1, 1, 2):
                raw_col = row + displacement
                if boundary == "obc":
                    if 0 <= raw_col < length:
                        matrix[row, raw_col] += self.hopping(displacement)
                    continue

                factor = 1.0 + 0.0j
                if raw_col >= length:
                    factor = twist
                elif raw_col < 0:
                    factor = 1.0 / twist
                matrix[row, raw_col % length] += factor * self.hopping(displacement)
        return matrix


def sample_onsite(length: int, disorder_strength: float, rng: np.random.Generator) -> np.ndarray:
    if length <= 0:
        raise ValueError("length must be positive")
    if disorder_strength < 0:
        raise ValueError("disorder strength must be nonnegative")
    return rng.uniform(-disorder_strength, disorder_strength, size=length)


def site_transfer_matrices(
    energies: np.ndarray | complex,
    onsite: float,
    model: LongRangeModel,
) -> np.ndarray:
    """Return the paper's one-site 4x4 companion matrix for each energy."""

    energies_array = np.asarray(energies, dtype=complex)
    matrices = np.zeros(energies_array.shape + (4, 4), dtype=complex)
    matrices[..., 0, 0] = -model.t_1 / model.t_2
    matrices[..., 0, 1] = (energies_array - onsite) / model.t_2
    matrices[..., 0, 2] = -model.t_minus_1 / model.t_2
    matrices[..., 0, 3] = -model.t_minus_2 / model.t_2
    matrices[..., 1, 0] = 1.0
    matrices[..., 2, 1] = 1.0
    matrices[..., 3, 2] = 1.0
    return matrices


def lyapunov_exponents(
    energies: np.ndarray | complex,
    onsite_sequence: np.ndarray,
    model: LongRangeModel,
    *,
    qr_interval: int = 1,
) -> np.ndarray:
    """Estimate all four per-site Lyapunov exponents with periodic QR.

    Energies are evaluated in one batch. ``qr_interval=1`` reproduces the
    original implementation. A short larger interval amortizes the batched QR
    cost while retaining numerical stability for paper-scale grids.
    """

    energies_array = np.asarray(energies, dtype=complex)
    original_shape = energies_array.shape
    flat_energies = energies_array.reshape(-1)
    onsite_sequence = np.asarray(onsite_sequence, dtype=float)
    if onsite_sequence.ndim != 1 or onsite_sequence.size == 0:
        raise ValueError("onsite_sequence must be a nonempty one-dimensional array")
    if qr_interval <= 0:
        raise ValueError("qr_interval must be positive")

    count = flat_energies.size
    q = np.broadcast_to(np.eye(4, dtype=complex), (count, 4, 4)).copy()
    log_growth = np.zeros((count, 4), dtype=float)
    tiny = np.finfo(float).tiny

    for step, onsite in enumerate(onsite_sequence, start=1):
        transfer = site_transfer_matrices(flat_energies, float(onsite), model)
        q = transfer @ q
        if step % qr_interval == 0 or step == onsite_sequence.size:
            q, r = np.linalg.qr(q)
            log_growth += np.log(np.maximum(np.abs(np.diagonal(r, axis1=-2, axis2=-1)), tiny))

    exponents = np.sort(log_growth / onsite_sequence.size, axis=-1)
    return exponents.reshape(original_shape + (4,))


def clean_beta_exponents(
    energy: complex,
    model: LongRangeModel,
    onsite: float = 0.0,
) -> np.ndarray:
    """Analytic clean-limit exponents log|beta_s| from Appendix S3."""

    coefficients = [
        model.t_2,
        model.t_1,
        onsite - energy,
        model.t_minus_1,
        model.t_minus_2,
    ]
    roots = np.roots(coefficients)
    return np.sort(np.log(np.abs(roots)))


def lyapunov_potentials(exponents: np.ndarray, model: LongRangeModel) -> tuple[np.ndarray, np.ndarray]:
    exponents = np.asarray(exponents, dtype=float)
    if exponents.shape[-1] != 4:
        raise ValueError("expected four ordered Lyapunov exponents")
    constant = np.log(abs(model.t_2))
    obc = np.sum(exponents[..., 2:4], axis=-1) + constant
    pbc = np.sum(np.where(exponents > 0.0, exponents, 0.0), axis=-1) + constant
    return obc, pbc


def essential_lyapunov(exponents: np.ndarray) -> np.ndarray:
    exponents = np.asarray(exponents, dtype=float)
    lower = exponents[..., 1]
    upper = exponents[..., 2]
    return np.where(np.abs(lower) <= np.abs(upper), lower, upper)


def classify_state(exponents: np.ndarray, tolerance: float = 1e-8) -> np.ndarray:
    """Return 1 for ALM, 0 for UCS/edge, and -1 for a skin mode."""

    exponents = np.asarray(exponents, dtype=float)
    lower = exponents[..., 1]
    upper = exponents[..., 2]
    critical = (np.abs(lower) <= tolerance) | (np.abs(upper) <= tolerance)
    alm = (lower < -tolerance) & (upper > tolerance)
    return np.where(critical, 0, np.where(alm, 1, -1))


def winding_from_lyapunov(exponents: np.ndarray, tolerance: float = 1e-8) -> np.ndarray:
    exponents = np.asarray(exponents, dtype=float)
    positive_count = np.sum(exponents > tolerance, axis=-1)
    return 2 - positive_count


def finite_spectrum(
    onsite: np.ndarray,
    model: LongRangeModel,
    *,
    boundary: str,
) -> np.ndarray:
    matrix = model.hamiltonian(onsite, boundary=boundary)
    return scipy.linalg.eigvals(matrix, check_finite=False, overwrite_a=True)


def finite_eigensystem(
    onsite: np.ndarray,
    model: LongRangeModel,
    *,
    boundary: str,
) -> tuple[np.ndarray, np.ndarray]:
    """Return eigenvalues and normalized right eigenvectors for one chain."""

    matrix = model.hamiltonian(onsite, boundary=boundary)
    values, vectors = scipy.linalg.eig(matrix, check_finite=False, overwrite_a=True)
    norms = np.linalg.norm(vectors, axis=0)
    vectors = vectors / np.maximum(norms, np.finfo(float).tiny)
    return values, vectors


def finite_eigensystem_with_obc_gauge(
    onsite: np.ndarray,
    model: LongRangeModel,
    *,
    radius: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return stable OBC eigenpairs and transform right states back to site space."""

    gauged_model = model.similarity_gauge(radius)
    values, gauged_vectors = finite_eigensystem(onsite, gauged_model, boundary="obc")
    diagonal = radius ** np.arange(len(onsite), dtype=float)
    vectors = diagonal[:, None] * gauged_vectors
    norms = np.linalg.norm(vectors, axis=0)
    vectors = vectors / np.maximum(norms, np.finfo(float).tiny)
    return values, vectors


def finite_potential(spectra: np.ndarray, energies: np.ndarray | complex) -> np.ndarray:
    """Ensemble-averaged finite-chain electrostatic potential."""

    spectra_array = np.asarray(spectra, dtype=complex)
    energies_array = np.asarray(energies, dtype=complex)
    if spectra_array.ndim == 1:
        spectra_array = spectra_array[None, :]
    if spectra_array.ndim != 2:
        raise ValueError("spectra must have shape (realizations, levels)")
    distances = np.abs(spectra_array[..., None] - energies_array.reshape(1, 1, -1))
    distances = np.maximum(distances, np.finfo(float).tiny)
    values = np.mean(np.log(distances), axis=(0, 1))
    return values.reshape(energies_array.shape)


def finite_logdet_potential(
    onsite: np.ndarray,
    model: LongRangeModel,
    energies: np.ndarray | complex,
) -> np.ndarray:
    """Evaluate the finite OBC potential from a stable banded sparse LU.

    This computes ``log|det(E-H)| / L`` directly and avoids constructing the
    numerically fragile eigenvalue cloud of a large non-normal OBC matrix.
    """

    onsite = np.asarray(onsite, dtype=float)
    energies_array = np.asarray(energies, dtype=complex)
    if onsite.ndim != 1 or onsite.size < 2 * model.hopping_range + 1:
        raise ValueError("onsite sequence is too short for the hopping stencil")
    values = np.empty(energies_array.size, dtype=float)
    off_diagonals = {
        -2: np.full(onsite.size - 2, -model.t_minus_2, dtype=complex),
        -1: np.full(onsite.size - 1, -model.t_minus_1, dtype=complex),
        1: np.full(onsite.size - 1, -model.t_1, dtype=complex),
        2: np.full(onsite.size - 2, -model.t_2, dtype=complex),
    }
    tiny = np.finfo(float).tiny
    for index, energy in enumerate(energies_array.reshape(-1)):
        matrix = scipy.sparse.diags(
            [
                off_diagonals[-2],
                off_diagonals[-1],
                energy - onsite,
                off_diagonals[1],
                off_diagonals[2],
            ],
            offsets=[-2, -1, 0, 1, 2],
            shape=(onsite.size, onsite.size),
            format="csc",
        )
        factor = scipy.sparse.linalg.splu(matrix, permc_spec="NATURAL")
        values[index] = float(np.sum(np.log(np.maximum(np.abs(factor.U.diagonal()), tiny))) / onsite.size)
    return values.reshape(energies_array.shape)


def direct_twist_winding(
    energy: complex,
    onsite: np.ndarray,
    model: LongRangeModel,
    *,
    theta_points: int = 129,
) -> int:
    """Compute the finite-chain winding of det[E-H(exp(i theta))]."""

    if theta_points < 9:
        raise ValueError("theta_points must be at least 9")
    identity = np.eye(len(onsite), dtype=complex)
    phases: list[float] = []
    for theta in np.linspace(0.0, 2.0 * np.pi, theta_points):
        twist = np.exp(1j * theta)
        matrix = energy * identity - model.hamiltonian(onsite, boundary="twisted", twist=twist)
        phases.append(_lu_logdet_phase(matrix))
    unwrapped = np.unwrap(np.asarray(phases))
    return int(np.rint((unwrapped[-1] - unwrapped[0]) / (2.0 * np.pi)))


def density_from_potential(
    potential: np.ndarray,
    real_axis: np.ndarray,
    imag_axis: np.ndarray,
    *,
    smoothing_sigma: float = 1.0,
) -> np.ndarray:
    """Apply the paper's two-dimensional Poisson relation on a regular grid."""

    potential = np.asarray(potential, dtype=float)
    real_axis = np.asarray(real_axis, dtype=float)
    imag_axis = np.asarray(imag_axis, dtype=float)
    expected_shape = (imag_axis.size, real_axis.size)
    if potential.shape != expected_shape:
        raise ValueError(f"potential shape {potential.shape} does not match grid {expected_shape}")
    smoothed = scipy.ndimage.gaussian_filter(potential, sigma=smoothing_sigma, mode="nearest")
    d_real = np.gradient(smoothed, real_axis, axis=1, edge_order=2)
    d2_real = np.gradient(d_real, real_axis, axis=1, edge_order=2)
    d_imag = np.gradient(smoothed, imag_axis, axis=0, edge_order=2)
    d2_imag = np.gradient(d_imag, imag_axis, axis=0, edge_order=2)
    return (d2_real + d2_imag) / (2.0 * np.pi)


def smoothed_spectral_histogram(
    spectra: np.ndarray,
    real_axis: np.ndarray,
    imag_axis: np.ndarray,
    *,
    smoothing_sigma: float = 1.0,
) -> np.ndarray:
    real_edges = _centers_to_edges(np.asarray(real_axis, dtype=float))
    imag_edges = _centers_to_edges(np.asarray(imag_axis, dtype=float))
    flat = np.asarray(spectra, dtype=complex).reshape(-1)
    counts, _, _ = np.histogram2d(flat.imag, flat.real, bins=[imag_edges, real_edges])
    density = scipy.ndimage.gaussian_filter(counts.astype(float), sigma=smoothing_sigma, mode="constant")
    mass = float(density.sum())
    return density / mass if mass else density


def normalized_positive_density(density: np.ndarray) -> np.ndarray:
    positive = np.clip(np.asarray(density, dtype=float), 0.0, None)
    mass = float(positive.sum())
    return positive / mass if mass else positive


def density_overlap(left: np.ndarray, right: np.ndarray) -> float:
    left = normalized_positive_density(left)
    right = normalized_positive_density(right)
    return float(np.sum(np.minimum(left, right)))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _centers_to_edges(centers: np.ndarray) -> np.ndarray:
    if centers.ndim != 1 or centers.size < 2:
        raise ValueError("grid centers must be a one-dimensional array with at least two values")
    midpoints = 0.5 * (centers[:-1] + centers[1:])
    first = centers[0] - 0.5 * (centers[1] - centers[0])
    last = centers[-1] + 0.5 * (centers[-1] - centers[-2])
    return np.concatenate([[first], midpoints, [last]])


def _lu_logdet_phase(matrix: np.ndarray) -> float:
    """Return determinant phase without forming its overflowing magnitude."""

    lu, pivots = scipy.linalg.lu_factor(matrix, overwrite_a=True, check_finite=False)
    diagonal = np.diag(lu)
    if np.any(np.abs(diagonal) < np.finfo(float).tiny):
        raise ValueError("twisted determinant crosses zero at a sampled theta")
    swaps = int(np.count_nonzero(pivots != np.arange(pivots.size)))
    return float(np.sum(np.angle(diagonal)) + (swaps % 2) * np.pi)
