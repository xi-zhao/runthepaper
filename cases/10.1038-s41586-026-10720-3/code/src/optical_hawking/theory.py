"""Analytic sideband and thermal-spectrum equations from Methods C--D.

This module is the domain layer for the paper's directly plottable theory.  It
does not know about the source PDF or plotting.  Experimental points may be
passed to :func:`fit_sideband_spectrum`, but the returned curve is generated
only from Eqs. (C.3), (C.4), and (D.1).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from itertools import product
from typing import Any

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import least_squares

from .model import C_NM_PER_FS


@dataclass(frozen=True)
class SidebandParameters:
    """Parameters of the incoherently averaged spectrum in Eq. (D.1)."""

    hawking_wavelength_nm: float
    backreaction_shift_nm: float
    spectral_width_rad_fs: float
    modulation_x: float
    hawking_intensity: float
    backreaction_intensity: float

    def validate(self) -> None:
        if self.hawking_wavelength_nm <= 0:
            raise ValueError("hawking_wavelength_nm must be positive")
        if not 0 < self.backreaction_shift_nm < self.hawking_wavelength_nm:
            raise ValueError("backreaction_shift_nm must place the peak in the UV")
        if self.spectral_width_rad_fs <= 0:
            raise ValueError("spectral_width_rad_fs must be positive")
        if not 0 < self.modulation_x < 1:
            raise ValueError("modulation_x must lie between zero and one")
        if self.hawking_intensity < 0 or self.backreaction_intensity < 0:
            raise ValueError("fitted intensities must be non-negative")

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


@dataclass(frozen=True)
class SidebandFit:
    """Auditable result of a red-data-only Eq. (D.1) fit."""

    parameters: SidebandParameters
    fit_cutoff_nm: float
    points_total: int
    points_fitted: int
    fit_nrmse: float
    all_points_nrmse: float
    optimizer_cost: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "parameters": self.parameters.as_dict(),
            "fit_cutoff_nm": self.fit_cutoff_nm,
            "points_total": self.points_total,
            "points_fitted": self.points_fitted,
            "fit_nrmse": self.fit_nrmse,
            "all_points_nrmse": self.all_points_nrmse,
            "optimizer_cost": self.optimizer_cost,
        }


@lru_cache(maxsize=16)
def _profile_table(mu: float) -> tuple[np.ndarray, np.ndarray, float]:
    """Tabulate the normalized integral defining the paper's ``I_H``.

    The integration limit 12 is already in the exponentially flat tail for
    every disclosed ``mu``.  The table turns a nested quadrature inside the
    nonlinear fit into a deterministic interpolation.
    """

    if mu <= 0:
        raise ValueError("mu must be positive")
    coordinate = np.linspace(0.0, 12.0, 50_001)
    powered = np.minimum(coordinate**mu, 350.0)
    integrand = 1.0 / np.cosh(powered) ** 2
    integral = cumulative_trapezoid(integrand, coordinate, initial=0.0)
    return coordinate, integral, float(integral[-1])


def hawking_peak_profile(nu: np.ndarray, mu: float) -> np.ndarray:
    """Return the normalized empirical peak ``I_H`` from Methods D.

    ``mu=1`` gives ``sech(nu)^2``.  As ``mu`` grows, the profile tends to the
    parabolic compact-support form ``max(1-nu^2, 0)``.
    """

    coordinate, integral, denominator = _profile_table(float(mu))
    theta = np.interp(
        np.abs(np.asarray(nu, dtype=float)),
        coordinate,
        integral,
        left=0.0,
        right=denominator,
    ) / denominator
    return np.maximum(1.0 - theta**2, 0.0)


def sideband_spectrum(
    wavelength_nm: np.ndarray,
    parameters: SidebandParameters,
    mu: float,
    maximum_order: int = 10,
) -> np.ndarray:
    """Evaluate the asymmetric sideband spectrum of Eq. (D.1).

    Eq. (C.4) makes the common band amplitudes asymmetric around the Hawking
    peak.  Propagation-time averaging removes coherent cross-band terms, so
    Eq. (D.1) is an incoherent sum of shifted peak profiles.
    """

    parameters.validate()
    if maximum_order < 0:
        raise ValueError("maximum_order must be non-negative")
    wavelength = np.asarray(wavelength_nm, dtype=float)
    if np.any(wavelength <= 0):
        raise ValueError("wavelength_nm must be positive")

    omega = 2.0 * np.pi * C_NM_PER_FS / wavelength
    omega_minus = 2.0 * np.pi * C_NM_PER_FS / parameters.hawking_wavelength_nm
    omega_backreaction = 2.0 * np.pi * C_NM_PER_FS / (
        parameters.hawking_wavelength_nm - parameters.backreaction_shift_nm
    )
    spacing = omega_backreaction - omega_minus
    x_value = parameters.modulation_x
    spectrum = np.zeros_like(wavelength)

    for order in range(-maximum_order, maximum_order + 1):
        centre = omega_minus - order * spacing
        if order < 0:
            prefactor = (
                parameters.hawking_intensity
                + parameters.backreaction_intensity / x_value**2
            )
        else:
            prefactor = (
                parameters.hawking_intensity
                + parameters.backreaction_intensity * x_value**2
            )
        weight = prefactor * x_value ** (2 * abs(order))
        spectrum += weight * hawking_peak_profile(
            (omega - centre) / parameters.spectral_width_rad_fs, mu
        )
    return spectrum


def _parameter_vector(parameters: SidebandParameters) -> np.ndarray:
    return np.asarray(
        [
            parameters.hawking_wavelength_nm,
            parameters.backreaction_shift_nm,
            parameters.spectral_width_rad_fs,
            parameters.modulation_x,
            parameters.hawking_intensity,
            parameters.backreaction_intensity,
        ],
        dtype=float,
    )


def _parameters_from_vector(values: np.ndarray) -> SidebandParameters:
    return SidebandParameters(*map(float, values))


def fit_sideband_spectrum(
    wavelength_nm: np.ndarray,
    counts_hz: np.ndarray,
    mu: float,
) -> SidebandFit:
    """Fit Eq. (D.1) using only the paper's corrected experimental points.

    The paper fits wavelengths to the left of and including the Hawking peak
    to avoid coherent NRR interference.  We locate that peak in the disclosed
    UV window and include one additional wavelength bin.  The public vector
    markers discretize a peak that lies between bins, so this is the closest
    source-available implementation of the Methods phrase "to the left and at
    the Hawking peaks".  A small deterministic multistart grid avoids selecting
    a sideband as the central peak.
    """

    wavelength = np.asarray(wavelength_nm, dtype=float)
    counts = np.asarray(counts_hz, dtype=float)
    if wavelength.ndim != 1 or counts.shape != wavelength.shape:
        raise ValueError("wavelength_nm and counts_hz must be matching 1-D arrays")
    if wavelength.size < 8:
        raise ValueError("at least eight experimental points are required")

    order = np.argsort(wavelength)
    wavelength = wavelength[order]
    counts = counts[order]
    peak_window = (wavelength > 232.4) & (wavelength < 233.8)
    if not np.any(peak_window):
        raise ValueError("the Hawking peak window is absent")
    peak_wavelength = wavelength[peak_window][np.argmax(counts[peak_window])]
    bin_width = float(np.median(np.diff(wavelength)))
    fit_cutoff = peak_wavelength + 1.05 * bin_width
    fit_mask = wavelength <= fit_cutoff
    scale = max(float(np.max(counts)), 1.0)

    lower = np.asarray([232.4, 0.04, 0.0003, 0.02, 0.0, 0.0])
    upper = np.asarray([233.8, 1.20, 0.0800, 0.98, scale * 30.0, scale * 30.0])
    best_cost = np.inf
    best_parameters: SidebandParameters | None = None

    starts = product(
        (peak_wavelength - 0.10, peak_wavelength + 0.10),
        (0.25, 0.50, 0.75),
        (0.006, 0.018),
        (0.25, 0.65),
    )
    for centre, shift, width, modulation in starts:
        initial = SidebandParameters(
            hawking_wavelength_nm=float(np.clip(centre, lower[0], upper[0])),
            backreaction_shift_nm=shift,
            spectral_width_rad_fs=width,
            modulation_x=modulation,
            hawking_intensity=0.70 * scale,
            backreaction_intensity=0.20 * scale,
        )

        def residual(values: np.ndarray) -> np.ndarray:
            prediction = sideband_spectrum(
                wavelength[fit_mask], _parameters_from_vector(values), mu
            )
            return (prediction - counts[fit_mask]) / np.sqrt(scale)

        result = least_squares(
            residual,
            _parameter_vector(initial),
            bounds=(lower, upper),
            x_scale="jac",
            max_nfev=1_500,
        )
        fitted = _parameters_from_vector(result.x)
        raw_residual = (
            sideband_spectrum(wavelength[fit_mask], fitted, mu) - counts[fit_mask]
        )
        cost = float(np.sum(raw_residual**2))
        if cost < best_cost:
            best_cost = cost
            best_parameters = fitted

    if best_parameters is None:  # pragma: no cover - defensive guard
        raise RuntimeError("no sideband fit completed")
    prediction = sideband_spectrum(wavelength, best_parameters, mu)
    fit_nrmse = float(np.sqrt(best_cost / np.count_nonzero(fit_mask)) / scale)
    all_nrmse = float(np.sqrt(np.mean((prediction - counts) ** 2)) / scale)
    return SidebandFit(
        parameters=best_parameters,
        fit_cutoff_nm=fit_cutoff,
        points_total=int(wavelength.size),
        points_fitted=int(np.count_nonzero(fit_mask)),
        fit_nrmse=fit_nrmse,
        all_points_nrmse=all_nrmse,
        optimizer_cost=best_cost,
    )


def thermal_line_fit(
    frequency_ratio: np.ndarray,
    log_probability: np.ndarray,
    exclude_first: bool,
) -> tuple[float, float, np.ndarray]:
    """Fit the straight-line thermal law used in Fig. 5."""

    ratio = np.asarray(frequency_ratio, dtype=float)
    values = np.asarray(log_probability, dtype=float)
    if ratio.ndim != 1 or values.shape != ratio.shape or ratio.size < 3:
        raise ValueError("thermal fit requires matching 1-D arrays")
    fit_slice = slice(1, None) if exclude_first else slice(None)
    slope, intercept = np.polyfit(ratio[fit_slice], values[fit_slice], 1)
    return float(slope), float(intercept), slope * ratio + intercept
