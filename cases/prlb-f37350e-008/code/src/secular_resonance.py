"""Closed-form secular-resonance calculations for PRL-Bench idx8."""

from __future__ import annotations

import math

import numpy as np
from scipy.constants import G, astronomical_unit, c


SOLAR_MASS_KG = 1.98847e30


def coefficient_b(e_in: float) -> float:
    return -2.0 - 3.0 * e_in**2


def coefficient_c(m1: float, m2: float, a_in: float, a_out: float, e_in: float) -> float:
    return 15.0 / 8.0 * (m1 - m2) / (m1 + m2) * a_in / a_out * e_in * (4.0 + 3.0 * e_in**2)


def gamma_parameter(
    m1_solar: float,
    m2_solar: float,
    a_in_au: float,
    a_out_au: float,
    e_in: float,
) -> float:
    m1 = m1_solar * SOLAR_MASS_KG
    m2 = m2_solar * SOLAR_MASS_KG
    m12 = m1 + m2
    a_in = a_in_au * astronomical_unit
    a_out = a_out_au * astronomical_unit
    return 4.0 * G * m12**3 / (c**2 * m1 * m2 * a_in) * (a_out / a_in) ** 3.5 / (1.0 - e_in**2)


def resonance_semimajor_axis(a_in_initial_au: float, gamma_initial: float) -> float:
    """Solve gamma(a)=1 using gamma proportional to a^(-9/2)."""

    return a_in_initial_au * gamma_initial ** (2.0 / 9.0)


def coefficient_d(b: float, gamma: float) -> float:
    return -1.5 * b - 3.0 * gamma


def separatrix_peak(c_coefficient: float, d_coefficient: float) -> float:
    return c_coefficient / d_coefficient


def phase_curve(phi: np.ndarray, beta: float, radicand_parameter: float, branch: int = 1) -> np.ndarray:
    """Return the published curve solution, where the parameter equals -H/D."""

    phi = np.asarray(phi, dtype=float)
    discriminant = beta**2 * np.cos(phi) ** 2 + 4.0 * radicand_parameter
    root = np.where(discriminant >= 0.0, np.sqrt(np.maximum(discriminant, 0.0)), np.nan)
    eccentricity = 0.5 * (beta * np.cos(phi) + branch * root)
    return np.where(eccentricity >= 0.0, eccentricity, np.nan)


def dimensionless_linear_hamiltonian(e_out: np.ndarray, phi: np.ndarray, beta: float) -> np.ndarray:
    """H/D = -e^2 + beta e cos(phi)."""

    return -np.asarray(e_out) ** 2 + beta * np.asarray(e_out) * np.cos(phi)


def source_figc_beta() -> float:
    gamma = gamma_parameter(46.15, 13.85, 0.4, 5.0, 0.8)
    b = coefficient_b(0.8)
    c_value = coefficient_c(46.15, 13.85, 0.4, 5.0, 0.8)
    return separatrix_peak(c_value, coefficient_d(b, gamma))


def action_integrand(e_out: float) -> float:
    return 1.0 - math.sqrt(1.0 - e_out**2)
