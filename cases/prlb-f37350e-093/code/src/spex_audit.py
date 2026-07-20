"""Independent deterministic checks for the SPEx benchmark record."""

from __future__ import annotations

import math

import numpy as np


def double_well_potential(x0: np.ndarray, x1: np.ndarray, alpha: float) -> np.ndarray:
    """Source SI potential: alpha multiplies both terms inside the quarter."""

    return 0.25 * alpha * ((x0**2 + x1**2 - 4.0) ** 2 + x1**2)


def frozen_double_well_potential(x0: np.ndarray, x1: np.ndarray, alpha: float) -> np.ndarray:
    """Literal frozen transcription, with the x1^2 term moved outside alpha."""

    return 0.25 * alpha * (x0**2 + x1**2 - 4.0) ** 2 + x1**2


def free_energy_x0(
    x0: np.ndarray,
    alpha: float,
    *,
    y_max: float = 5.0,
    n_y: int = 20001,
    use_frozen_transcription: bool = False,
) -> np.ndarray:
    """Integrate exp(-U) over x1 and shift the free-energy minimum to zero."""

    y = np.linspace(-y_max, y_max, n_y)
    values = []
    for x in np.asarray(x0, dtype=float):
        potential = frozen_double_well_potential if use_frozen_transcription else double_well_potential
        u = potential(x, y, alpha)
        u0 = float(np.min(u))
        integral = np.trapezoid(np.exp(-(u - u0)), y)
        values.append(u0 - math.log(integral))
    free_energy = np.asarray(values)
    return free_energy - np.min(free_energy)


def path_bias_weight(bias_values: np.ndarray, beta: float = 1.0) -> float:
    return float(np.sum(np.exp(-beta * np.asarray(bias_values, dtype=float))))


def exchange_acceptance(
    old_bias: np.ndarray,
    new_bias: np.ndarray,
    *,
    new_path_is_reactive: bool,
    new_path_has_no_internal_basin_hits: bool,
    beta: float = 1.0,
) -> float:
    """Source Eq. (6), including both path-ensemble indicator factors."""

    if not new_path_is_reactive or not new_path_has_no_internal_basin_hits:
        return 0.0
    ratio = path_bias_weight(old_bias, beta) / path_bias_weight(new_bias, beta)
    return min(1.0, ratio)


def dominant_channel_ratio() -> float:
    return 0.862 / 0.084


def frozen_speedup() -> float:
    """Arithmetic of the frozen unsupported rate pair, not a source result."""

    return 27.3 / 1.2
