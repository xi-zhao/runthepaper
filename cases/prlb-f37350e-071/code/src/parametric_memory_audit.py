"""Independent audit helpers for PRL-Bench idx71."""

from __future__ import annotations

from decimal import Decimal, localcontext

import numpy as np


def _validate(lam: float, coupling: float) -> None:
    if lam <= 0.0:
        raise ValueError("lam must be positive")
    if coupling < 0.0:
        raise ValueError("coupling must be nonnegative")


def rotating_matrix(lam: float, coupling: float, delta: float) -> np.ndarray:
    """Constant matrix after removing the pump phase and coupling phase."""

    _validate(lam, coupling)
    return np.asarray(
        [[-lam - 1j * delta, coupling], [coupling, -lam + 1j * delta]],
        dtype=np.complex128,
    )


def floquet_exponents(lam: float, coupling: float, delta: float) -> np.ndarray:
    """Return the two principal-branch Floquet exponents."""

    _validate(lam, coupling)
    chi = np.sqrt(complex(coupling * coupling - delta * delta))
    return np.asarray([-lam + chi, -lam - chi], dtype=np.complex128)


def is_exponentially_unstable(lam: float, coupling: float, delta: float) -> bool:
    """Exact instability wedge."""

    _validate(lam, coupling)
    return coupling * coupling > lam * lam + delta * delta


def hyperbolic_pair(coupling: float, delta: float, time: np.ndarray | float) -> tuple[np.ndarray, np.ndarray]:
    """Return c(T), s(T) with exp(BT)=c I+s B, using real branches."""

    if coupling < 0.0:
        raise ValueError("coupling must be nonnegative")
    t = np.asarray(time, dtype=float)
    chi_sq = coupling * coupling - delta * delta
    if np.isclose(chi_sq, 0.0, atol=1.0e-15):
        return np.ones_like(t), t
    if chi_sq > 0.0:
        chi = np.sqrt(chi_sq)
        return np.cosh(chi * t), np.sinh(chi * t) / chi
    omega = np.sqrt(-chi_sq)
    return np.cos(omega * t), np.sin(omega * t) / omega


def exact_optimal_gain(
    lam: float, coupling: float, delta: float, time: np.ndarray | float
) -> np.ndarray:
    """Exact phase-optimized energy gain for physical inputs (sigma,sigma*).

    The absolute value is unavoidable when ``|delta| > coupling`` because the
    optimized phase switches whenever the oscillatory Bogoliubov coefficient
    crosses zero.
    """

    _validate(lam, coupling)
    t = np.asarray(time, dtype=float)
    if np.any(t < 0.0):
        raise ValueError("time must be nonnegative")
    _, s = hyperbolic_pair(coupling, delta, t)
    x = coupling * s
    return np.exp(-2.0 * lam * t) * (np.sqrt(1.0 + x * x) + np.abs(x)) ** 2


def frozen_optimal_gain(
    lam: float, coupling: float, delta: float, time: np.ndarray | float
) -> np.ndarray:
    """Gain expression printed by the frozen answer, for negative control."""

    _validate(lam, coupling)
    t = np.asarray(time, dtype=float)
    c, s = hyperbolic_pair(coupling, delta, t)
    return np.exp(-2.0 * lam * t) * (c + lam * s) ** 2


def brute_phase_gain(
    lam: float,
    coupling: float,
    delta: float,
    time: float,
    *,
    phase_count: int = 200_000,
) -> float:
    """Independently maximize the physical amplitude over initial phase."""

    _validate(lam, coupling)
    c, s = hyperbolic_pair(coupling, delta, float(time))
    a = complex(float(c), -delta * float(s))
    b = coupling * float(s)
    phase = np.linspace(0.0, np.pi, phase_count, endpoint=False)
    z = np.exp(1j * phase)
    amplitude = np.exp(-lam * time) * (a * z + b * np.conjugate(z))
    return float(np.max(np.abs(amplitude) ** 2))


def exact_transient_peak(
    lam: float, coupling: float, delta: float
) -> tuple[float, float] | None:
    """Return the unique positive transient maximum, if it exists.

    In the real-splitting stable wedge, an interior maximum exists iff
    ``coupling > lam`` in addition to ``chi < lam``.
    """

    _validate(lam, coupling)
    chi_sq = coupling * coupling - delta * delta
    if chi_sq <= 0.0:
        raise ValueError("the requested peak formula requires real positive chi")
    chi = np.sqrt(chi_sq)
    if chi >= lam:
        raise ValueError("the system must be strictly stable")
    if coupling <= lam:
        return None
    sinh_argument = (
        chi
        / coupling
        * np.sqrt((coupling * coupling - lam * lam) / (lam * lam - chi * chi))
    )
    time = float(np.arcsinh(sinh_argument) / chi)
    gain = float(exact_optimal_gain(lam, coupling, delta, time))
    return time, gain


def frozen_transient_peak(lam: float, coupling: float, delta: float) -> tuple[float, float]:
    """Peak printed by the frozen answer, for negative control."""

    _validate(lam, coupling)
    chi_sq = coupling * coupling - delta * delta
    if chi_sq <= 0.0:
        raise ValueError("chi must be real and positive")
    chi = np.sqrt(chi_sq)
    if chi >= lam:
        raise ValueError("the system must be strictly stable")
    time = float(np.arctanh(chi / lam) / chi)
    gain = float(
        np.exp(-2.0 * lam * time) / (1.0 - (chi / lam) ** 2)
    )
    return time, gain


def quantum_steady_occupation(ratio: np.ndarray | float) -> np.ndarray:
    """Exact vacuum-driven intracavity occupation below threshold."""

    r = np.asarray(ratio, dtype=float)
    if np.any((r < 0.0) | (r >= 1.0)):
        raise ValueError("ratio must satisfy 0 <= r < 1")
    return r * r / (2.0 * (1.0 - r * r))


def frozen_quantum_steady_occupation(ratio: np.ndarray | float) -> np.ndarray:
    """Twice-too-large occupation printed by the frozen answer."""

    r = np.asarray(ratio, dtype=float)
    if np.any((r < 0.0) | (r >= 1.0)):
        raise ValueError("ratio must satisfy 0 <= r < 1")
    return r * r / (1.0 - r * r)


def threshold_inversion(*, precision: int = 80) -> Decimal:
    """Reproduce frozen Task 6 with Decimal high-precision arithmetic."""

    with localcontext() as context:
        context.prec = precision
        n = Decimal(155)
        gamma = Decimal(10)
        kappa = Decimal(1)
        g29 = Decimal(3)
        omega39 = Decimal(4)
        delta8 = Decimal(200)
        alpha = gamma * kappa + g29 * g29 * n
        lam = kappa * omega39 * omega39 / alpha
        delta = Decimal("0.7") * lam
        critical_coupling = (lam * lam + delta * delta).sqrt()
        return (
            critical_coupling
            * alpha
            * (gamma * gamma + delta8 * delta8).sqrt()
            / (n * omega39 * g29)
        )
