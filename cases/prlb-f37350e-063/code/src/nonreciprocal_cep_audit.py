"""Independent source and benchmark checks for PRL-Bench record idx63.

The source paper studies a nonreciprocal driven--dissipative condensate with
open boundaries.  This module deliberately keeps three objects separate:

* the exact linear Hatano--Nelson eigenpairs;
* bulk plane-wave and PH-symmetry statements; and
* the finite-time CEP protocol introduced by the benchmark record.

That separation matters because the frozen benchmark answer drops the
site-dependent phase of the skin eigenvectors and incorrectly excludes one
of the two PH-compatible static bulk waves.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np


Array = np.ndarray
Integrator = Literal["rk4", "heun"]
SeedStyle = Literal["generator", "legacy"]


@dataclass(frozen=True)
class BulkStaticSolution:
    """One time-independent bulk plane wave."""

    q: float
    density: float
    minimum_kappa: float
    ph_compatible: bool


@dataclass(frozen=True)
class JacobianDiagnostics:
    """Diagnostics prescribed by Task 4 for one accepted static state."""

    eigenvalues: Array
    lambda_1: complex
    lambda_2: complex
    nullity_1: int
    nullity_2: int
    singular_values: Array
    squared_singular_values: Array


def obc_linear_matrix(n: int, kappa: float, gamma: float) -> Array:
    """Return the exact complex OBC matrix in ``i d(alpha)/dt = H alpha``."""

    if n < 1:
        raise ValueError("n must be positive")
    if gamma <= 0.0 or np.isclose(gamma, 1.0):
        raise ValueError("gamma must be positive and different from 1")

    matrix = np.eye(n, dtype=np.complex128) * (1j * (kappa - 2.0 * gamma))
    upper = gamma - 1.0
    lower = -(1.0 + gamma)
    matrix[np.arange(n - 1), np.arange(1, n)] = upper
    matrix[np.arange(1, n), np.arange(n - 1)] = lower
    return matrix


def exact_obc_eigenpairs(n: int, kappa: float, gamma: float) -> tuple[Array, Array]:
    """Return branch-consistent exact right eigenpairs for all ``gamma != 1``.

    Let ``a=gamma-1`` and ``b=-(1+gamma)`` be the upper and lower
    off-diagonal entries.  The source supplement gives

    ``s = r exp(i delta/2)``, ``r^2=|b/a|``, ``delta=arg(b/a)``.

    Hence the right eigenvectors are ``s**j sin(q_m j)``.  In particular,
    ``delta=pi`` for ``gamma>1`` and the factor ``i**j`` cannot be absorbed
    into one constant normalization phase.
    """

    matrix = obc_linear_matrix(n, kappa, gamma)
    del matrix  # validation is shared with the direct matrix constructor
    upper = gamma - 1.0
    lower = -(1.0 + gamma)
    ratio = complex(lower / upper)
    radius = float(np.sqrt(abs(ratio)))
    delta = float(np.angle(ratio))
    skin_step = radius * np.exp(0.5j * delta)

    modes = np.arange(1, n + 1, dtype=float)
    q = np.pi * modes / (n + 1)
    effective_hopping = upper * skin_step
    eigenvalues = 1j * (kappa - 2.0 * gamma) + 2.0 * effective_hopping * np.cos(q)

    sites = np.arange(1, n + 1, dtype=float)[:, None]
    eigenvectors = skin_step ** sites * np.sin(sites * q[None, :])
    eigenvectors /= np.linalg.norm(eigenvectors, axis=0, keepdims=True)
    return eigenvalues, eigenvectors


def frozen_right_eigenvectors(n: int, gamma: float) -> Array:
    """Return the positive-real-only vectors printed by the frozen answer."""

    if gamma <= 0.0 or np.isclose(gamma, 1.0):
        raise ValueError("gamma must be positive and different from 1")
    radius = np.sqrt(abs((1.0 + gamma) / (1.0 - gamma)))
    sites = np.arange(1, n + 1, dtype=float)[:, None]
    q = np.pi * np.arange(1, n + 1, dtype=float) / (n + 1)
    vectors = radius**sites * np.sin(sites * q[None, :])
    vectors /= np.linalg.norm(vectors, axis=0, keepdims=True)
    return vectors.astype(np.complex128)


def frozen_obc_eigenpairs(
    n: int, kappa: float, gamma: float
) -> tuple[Array, Array]:
    """Return the eigenvalue/vector pairing printed by the frozen answer.

    For ``gamma < 1`` the printed eigenvalue *set* is correct only after the
    relabeling ``m -> N + 1 - m``; it is not paired with the printed positive
    real skin vector.  For ``gamma > 1`` the eigenvalues are correctly labeled
    but the vectors omit the indispensable site phase ``i**j``.
    """

    if n < 1:
        raise ValueError("n must be positive")
    if gamma <= 0.0 or np.isclose(gamma, 1.0):
        raise ValueError("gamma must be positive and different from 1")
    q = np.pi * np.arange(1, n + 1, dtype=float) / (n + 1)
    if gamma < 1.0:
        eigenvalues = (
            1j * (kappa - 2.0 * gamma)
            + 2.0 * np.sqrt(1.0 - gamma * gamma) * np.cos(q)
        )
    else:
        eigenvalues = 1j * (
            kappa
            - 2.0 * gamma
            + 2.0 * np.sqrt(gamma * gamma - 1.0) * np.cos(q)
        )
    return eigenvalues, frozen_right_eigenvectors(n, gamma)


def eigenpair_residuals(matrix: Array, eigenvalues: Array, eigenvectors: Array) -> Array:
    """Return relative 2-norm residuals for paired eigenvalues and vectors."""

    residual = matrix @ eigenvectors - eigenvectors * eigenvalues[None, :]
    scale = max(1.0, float(np.linalg.norm(matrix, ord=2)))
    return np.linalg.norm(residual, axis=0) / scale


def vacuum_threshold(n: int, gamma: float) -> tuple[float, tuple[int, ...]]:
    """Return the exact finite-N loss-of-stability pump and trigger modes."""

    if n < 1:
        raise ValueError("n must be positive")
    if gamma <= 0.0 or np.isclose(gamma, 1.0):
        raise ValueError("gamma must be positive and different from 1")
    if gamma < 1.0:
        return 2.0 * gamma, tuple(range(1, n + 1))
    threshold = 2.0 * gamma - 2.0 * np.sqrt(gamma * gamma - 1.0) * np.cos(
        np.pi / (n + 1)
    )
    return float(threshold), (1,)


def thermodynamic_vacuum_threshold(gamma: float) -> float:
    """Return the N->infinity vacuum threshold."""

    if gamma <= 0.0 or np.isclose(gamma, 1.0):
        raise ValueError("gamma must be positive and different from 1")
    if gamma < 1.0:
        return 2.0 * gamma
    return float(2.0 * gamma - 2.0 * np.sqrt(gamma * gamma - 1.0))


def ph_ratio(q: float, sites: Array) -> Array:
    """Return PH[alpha]_j/alpha_j for alpha_j proportional to exp(i q j)."""

    return np.exp(1j * (np.pi - 2.0 * q) * np.asarray(sites, dtype=float))


def is_ph_compatible(q: float, *, atol: float = 1.0e-12) -> bool:
    """Test PH compatibility up to one global U(1) phase for every site."""

    ratio = ph_ratio(q, np.arange(-4, 5))
    return bool(np.max(np.abs(ratio - ratio[0])) <= atol)


def bulk_static_solutions(kappa: float, gamma: float) -> tuple[BulkStaticSolution, ...]:
    """Return all strictly nonzero static bulk plane waves at theta=pi."""

    if kappa < 0.0 or gamma <= 0.0:
        raise ValueError("kappa must be nonnegative and gamma positive")
    candidates = ((0.5 * np.pi, kappa, 0.0), (-0.5 * np.pi, kappa - 4.0 * gamma, 4.0 * gamma))
    return tuple(
        BulkStaticSolution(
            q=float(q),
            density=float(density),
            minimum_kappa=float(minimum),
            ph_compatible=is_ph_compatible(float(q)),
        )
        for q, density, minimum in candidates
        if density > 0.0
    )


def complex_rhs(alpha: Array, kappa: float | Array, gamma: float = 0.3) -> Array:
    """Return d(alpha)/dt for one state or a batch of OBC states.

    The final axis is the lattice-site axis.  A batched ``kappa`` is expected
    to have one value per leading batch item and is broadcast over sites.
    """

    alpha = np.asarray(alpha, dtype=np.complex128)
    if alpha.ndim < 1:
        raise ValueError("alpha must have a site axis")
    pump = np.asarray(kappa, dtype=float)
    if pump.ndim:
        pump = pump[..., None]
    onsite = (pump - 2.0 * gamma - np.abs(alpha) ** 2) * alpha
    result = onsite.copy()
    result[..., :-1] += 1j * (1.0 - gamma) * alpha[..., 1:]
    result[..., 1:] += 1j * (1.0 + gamma) * alpha[..., :-1]
    return result


def real_rhs(x: Array, kappa: float, gamma: float = 0.3) -> Array:
    """Return the 2N-dimensional real vector field used by Task 4."""

    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or x.size % 2:
        raise ValueError("x must be a one-dimensional vector of even length")
    n = x.size // 2
    alpha = x[:n] + 1j * x[n:]
    derivative = complex_rhs(alpha, kappa, gamma)
    return np.concatenate((derivative.real, derivative.imag))


def seeded_initial_state(
    n: int = 40, *, seed: int = 1, style: SeedStyle = "generator"
) -> Array:
    """Return the benchmark initial state under either NumPy MT19937 API.

    ``Generator(MT19937(seed)).standard_normal`` and the legacy
    ``RandomState(seed).standard_normal`` both satisfy the prose phrase
    "NumPy MT19937 seed 1" but return different normal samples.  The
    benchmark does not select between them, so both are exposed explicitly.
    """

    if n < 1:
        raise ValueError("n must be positive")
    if style == "generator":
        rng = np.random.Generator(np.random.MT19937(seed))
    elif style == "legacy":
        rng = np.random.RandomState(seed)
    else:
        raise ValueError(f"unknown MT19937 API style: {style}")
    eta = rng.standard_normal(n)
    xi = rng.standard_normal(n)
    return 1.0e-3 * (eta + 1j * xi)


def integrate_fixed_step(
    alpha_0: Array,
    kappa: float | Array,
    *,
    gamma: float = 0.3,
    dt: float = 0.02,
    steps: int = 200_000,
    method: Integrator = "rk4",
) -> Array:
    """Apply the exact fixed-step RK4 or Heun update requested by Task 4."""

    if dt <= 0.0 or steps < 0:
        raise ValueError("dt must be positive and steps nonnegative")
    state = np.asarray(alpha_0, dtype=np.complex128).copy()
    for _ in range(steps):
        k1 = complex_rhs(state, kappa, gamma)
        if method == "rk4":
            k2 = complex_rhs(state + 0.5 * dt * k1, kappa, gamma)
            k3 = complex_rhs(state + 0.5 * dt * k2, kappa, gamma)
            k4 = complex_rhs(state + dt * k3, kappa, gamma)
            state += (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        elif method == "heun":
            predictor = state + dt * k1
            k2 = complex_rhs(predictor, kappa, gamma)
            state += 0.5 * dt * (k1 + k2)
        else:
            raise ValueError(f"unknown integration method: {method}")
    return state


def forward_difference_jacobian(
    x: Array, kappa: float, *, gamma: float = 0.3, epsilon: float = 1.0e-7
) -> Array:
    """Compute the benchmark's forward finite-difference real Jacobian."""

    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or x.size % 2:
        raise ValueError("x must be a one-dimensional vector of even length")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    base = real_rhs(x, kappa, gamma)
    shifted = np.repeat(x[None, :], x.size, axis=0)
    shifted[np.arange(x.size), np.arange(x.size)] += epsilon
    values = np.stack([real_rhs(row, kappa, gamma) for row in shifted], axis=1)
    return (values - base[:, None]) / epsilon


def jacobian_diagnostics(jacobian: Array, *, tolerance: float = 5.0e-7) -> JacobianDiagnostics:
    """Apply the frozen SVD-nullity and eigenvalue-ordering conventions."""

    jacobian = np.asarray(jacobian, dtype=float)
    if jacobian.ndim != 2 or jacobian.shape[0] != jacobian.shape[1]:
        raise ValueError("jacobian must be square")
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    singular_values = np.linalg.svd(jacobian, compute_uv=False)
    squared = jacobian @ jacobian
    squared_singular_values = np.linalg.svd(squared, compute_uv=False)
    eigenvalues = np.linalg.eigvals(jacobian)
    order = np.lexsort((-eigenvalues.imag, -eigenvalues.real))
    ordered = eigenvalues[order]
    if len(ordered) < 2:
        raise ValueError("at least a 2x2 Jacobian is required")
    return JacobianDiagnostics(
        eigenvalues=ordered,
        lambda_1=complex(ordered[0]),
        lambda_2=complex(ordered[1]),
        nullity_1=int(np.count_nonzero(singular_values < tolerance)),
        nullity_2=int(np.count_nonzero(squared_singular_values < tolerance)),
        singular_values=singular_values,
        squared_singular_values=squared_singular_values,
    )


def cep_criterion(
    residual_norm: float, diagnostics: JacobianDiagnostics
) -> bool:
    """Return whether one grid point meets every frozen CEP condition."""

    return bool(
        residual_norm < 1.0e-8
        and abs(diagnostics.lambda_2.real) < 1.0e-5
        and diagnostics.nullity_1 == 1
        and diagnostics.nullity_2 == 2
    )
