"""Independent algebra for the idx40 MI-wedge source and frozen contract."""

from __future__ import annotations

import math

import numpy as np


def background_terms(
    x: float | np.ndarray,
    g11: float = 1.0,
    g22: float = 0.9375,
    g12: float = 0.98,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return A, Delta, and S=sqrt(Delta)-A for x=Q2^2."""

    x_array = np.asarray(x, dtype=float)
    q1_sq = 1.0 - x_array
    q2_sq = x_array
    a = g11 * q1_sq + g22 * q2_sq
    delta = (g11 * q1_sq - g22 * q2_sq) ** 2 + 4.0 * g12**2 * q1_sq * q2_sq
    return a, delta, np.sqrt(delta) - a


def stationarity(x: float, g11: float = 1.0, g22: float = 0.9375, g12: float = 0.98) -> float:
    """Derivative of S(x), used to locate the unique interior maximum."""

    a, delta, _ = background_terms(x, g11, g22, g12)
    del a
    contrast = g11 * (1.0 - x) - g22 * x
    delta_prime = -2.0 * (g11 + g22) * contrast + 4.0 * g12**2 * (1.0 - 2.0 * x)
    return float(delta_prime / (2.0 * np.sqrt(delta)) - (g22 - g11))


def omega_minus_squared(k: float | np.ndarray, s: float) -> np.ndarray:
    k_array = np.asarray(k, dtype=float)
    return k_array**2 * (k_array**2 - 2.0 * s)


def unstable_growth(k: float | np.ndarray, s: float) -> np.ndarray:
    k_array = np.asarray(k, dtype=float)
    return k_array * np.sqrt(2.0 * s - k_array**2)


def frozen_growth_derivative(k: float | np.ndarray, s: float) -> np.ndarray:
    """d Im(omega_-)/dk on the unstable branch."""

    k_array = np.asarray(k, dtype=float)
    return 2.0 * (s - k_array**2) / np.sqrt(2.0 * s - k_array**2)


def source_group_velocity(k: float | np.ndarray, s: float) -> np.ndarray:
    """d Re(omega_-)/dk on the stable branch, as used by the PRL."""

    k_array = np.asarray(k, dtype=float)
    return 2.0 * (k_array**2 - s) / np.sqrt(k_array**2 - 2.0 * s)


def unstable_endpoint(s: float) -> float:
    return math.sqrt(2.0 * s)


def source_edge_wavenumber(s: float) -> float:
    return math.sqrt(3.0 * s)


def source_edge_speed(s: float) -> float:
    return 4.0 * math.sqrt(s)


def frozen_claimed_speed(s: float) -> float:
    return 4.0 / math.sqrt(3.0) * math.sqrt(s)


def minority_coefficients(
    g11: float = 1.0,
    g22: float = 0.9375,
    g12: float = 0.98,
    *,
    source_definition: bool = True,
) -> tuple[float, float]:
    """Return Q2 and Q2^3 coefficients after expanding S through Q2^4."""

    g_eff = g22 - g12**2 / g11
    s1 = -2.0 * g_eff
    c_term = (g11 + g22) ** 2 - 4.0 * g12**2
    d_term = c_term / (2.0 * g11) - 2.0 * (g12**2 - g11**2) ** 2 / g11**3
    prefactor = 4.0 if source_definition else 4.0 / math.sqrt(3.0)
    return prefactor * math.sqrt(s1), prefactor * d_term / (2.0 * math.sqrt(s1))
