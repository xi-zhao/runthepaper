"""Independent formulas for Lai--Ho vacuum-resonance mode conversion."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


B_Q_G = 4.414e13
RHO_COEFF_B12 = 9.640e-5
E_AD_COEFF_KEV = 2.520


def weak_field_f(_: float) -> float:
    """Leading weak-field asymptote of the QED correction."""

    return 1.0


def strong_field_f(b_gauss: float) -> float:
    """Leading strong-field asymptote from PRL 91, 071101 (2003)."""

    if b_gauss <= 0:
        raise ValueError("b_gauss must be positive")
    return math.sqrt(b_gauss / (5.0 * B_Q_G))


def resonance_density(
    b_gauss: float,
    energy_kev: float,
    electron_fraction: float,
    f_value: float,
) -> float:
    """Vacuum-resonance density in g cm^-3."""

    if min(b_gauss, energy_kev, electron_fraction, f_value) <= 0:
        raise ValueError("all physical inputs must be positive")
    b12 = b_gauss / 1.0e12
    return (
        RHO_COEFF_B12
        * b12**2
        * energy_kev**2
        / electron_fraction
        / f_value**2
    )


def adiabatic_energy(
    theta_kb_deg: float,
    h_rho_cm: float,
    *,
    f_value: float = 1.0,
    u_i: float = 0.0,
) -> float:
    """Correct Lai--Ho threshold, including the H_rho^(-1/3) factor."""

    if h_rho_cm <= 0 or f_value <= 0:
        raise ValueError("h_rho_cm and f_value must be positive")
    theta = math.radians(theta_kb_deg)
    angular = f_value * math.tan(theta) * abs(1.0 - u_i)
    return E_AD_COEFF_KEV * angular ** (2.0 / 3.0) * h_rho_cm ** (-1.0 / 3.0)


def frozen_literal_adiabatic_energy(
    theta_kb_deg: float,
    h_rho_cm: float,
    *,
    f_value: float = 1.0,
    u_i: float = 0.0,
) -> float:
    """Literal value of the benchmark's misprinted H_rho^(-1) formula."""

    theta = math.radians(theta_kb_deg)
    angular = f_value * math.tan(theta) * abs(1.0 - u_i)
    return E_AD_COEFF_KEV * angular ** (2.0 / 3.0) / h_rho_cm


def jump_probability(energy_kev: float | np.ndarray, e_ad_kev: float) -> np.ndarray:
    """Landau--Zener nonadiabatic jump probability."""

    if e_ad_kev <= 0:
        raise ValueError("e_ad_kev must be positive")
    energy = np.asarray(energy_kev, dtype=float)
    if np.any(energy < 0):
        raise ValueError("energy must be nonnegative")
    return np.exp(-0.5 * math.pi * (energy / e_ad_kev) ** 3)


def ion_cyclotron_energy_kev(b_gauss: float) -> float:
    """Proton cyclotron energy used by the source, 6.3 B12 eV."""

    return 0.0063 * (b_gauss / 1.0e12)


def electron_cyclotron_energy_kev(b_gauss: float) -> float:
    """Electron cyclotron energy used by the source, 11.6 B12 keV."""

    return 11.6 * (b_gauss / 1.0e12)


def ellipticity_branches(
    density: float | np.ndarray,
    *,
    b_gauss: float = 1.0e13,
    energy_kev: float = 5.0,
    electron_fraction: float = 1.0,
    theta_kb_deg: float = 45.0,
    f_value: float = 1.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Lossless source approximation for the PRL Fig. 1 K_+ and K_- curves."""

    rho = np.asarray(density, dtype=float)
    if np.any(rho <= 0):
        raise ValueError("density must be positive")
    rho_v = resonance_density(b_gauss, energy_kev, electron_fraction, f_value)
    u_e_sqrt = electron_cyclotron_energy_kev(b_gauss) / energy_kev
    u_i = (ion_cyclotron_energy_kev(b_gauss) / energy_kev) ** 2
    theta = math.radians(theta_kb_deg)
    prefactor = (
        u_e_sqrt
        * (1.0 - u_i)
        * math.sin(theta) ** 2
        / (2.0 * math.cos(theta))
    )
    beta = prefactor * (1.0 - rho_v / rho)
    radical = np.sqrt(beta**2 + 1.0)
    return beta + radical, beta - radical, beta


@dataclass(frozen=True)
class PolarizationOutcome:
    q_over_i: int
    u_over_i: int = 0
    v_over_i: int = 0
    rotation_deg: int = 0


def polarization_outcome(initial_mode: str, *, adiabatic: bool) -> PolarizationOutcome:
    """High-to-low density outcome; requires the omitted initial mode."""

    mode = initial_mode.upper()
    if mode not in {"X", "O"}:
        raise ValueError("initial_mode must be 'X' or 'O'")
    final_mode = ({"X": "O", "O": "X"}[mode] if adiabatic else mode)
    return PolarizationOutcome(
        q_over_i=1 if final_mode == "O" else -1,
        rotation_deg=90 if adiabatic else 0,
    )
