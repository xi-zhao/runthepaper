"""Independent operator and numerical audit for PRL-Bench idx58."""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq


@dataclass(frozen=True)
class NystromSystem:
    window: float
    half_intervals: int
    grid: np.ndarray
    step: float
    theta_minus: np.ndarray
    operator: np.ndarray
    second_variation: np.ndarray


@dataclass(frozen=True)
class ConstrainedResult:
    mu: float
    dual_eigenvalue: float
    marginal: float
    objective: float
    residual: float


def _validate_grid(window: float, half_intervals: int) -> None:
    if not np.isfinite(window) or window <= 0.0:
        raise ValueError("window must be positive and finite")
    if not isinstance(half_intervals, int) or half_intervals < 2:
        raise ValueError("half_intervals must be an integer >= 2")


def nystrom_system(window: float, half_intervals: int) -> NystromSystem:
    """Return the paper's symmetric Nyström system with Theta(0)=1/2."""

    _validate_grid(window, half_intervals)
    indices = np.arange(-half_intervals, half_intervals + 1)
    grid = window * indices / half_intervals
    step = window / half_intervals
    left = grid[:, None]
    right = grid[None, :]
    difference = left - right
    phase = left * left - right * right

    integral = -step * (left + right) / np.pi * np.sinc(phase / np.pi)
    theta_minus = (grid < 0.0).astype(float)
    theta_minus[half_intervals] = 0.5
    operator = integral.copy()
    operator[np.diag_indices_from(operator)] -= theta_minus
    second_variation = -step * difference * np.sin(phase) / np.pi
    return NystromSystem(
        window=float(window),
        half_intervals=half_intervals,
        grid=grid,
        step=step,
        theta_minus=theta_minus,
        operator=operator,
        second_variation=second_variation,
    )


def gaussian_operator(system: NystromSystem, alpha: float) -> np.ndarray:
    """Return K_alpha for the Gaussian-smoothed spatial readout."""

    if not np.isfinite(alpha):
        raise ValueError("alpha must be finite")
    grid = system.grid
    left = grid[:, None]
    right = grid[None, :]
    difference = left - right
    phase = left * left - right * right
    integral = (
        -system.step
        * np.exp(-(alpha * difference) ** 2)
        * (left + right)
        / np.pi
        * np.sinc(phase / np.pi)
    )
    result = integral
    result[np.diag_indices_from(result)] -= system.theta_minus
    return result


def top_eigenpair(matrix: np.ndarray) -> tuple[float, np.ndarray]:
    """Return only the largest eigenpair of a real symmetric matrix."""

    dimension = matrix.shape[0]
    if matrix.shape != (dimension, dimension):
        raise ValueError("matrix must be square")
    values, vectors = eigh(
        matrix,
        subset_by_index=[dimension - 1, dimension - 1],
        driver="evr",
        check_finite=True,
    )
    return float(values[0]), vectors[:, 0]


def spectral_edges(matrix: np.ndarray) -> tuple[float, float]:
    """Return the smallest and largest eigenvalues."""

    dimension = matrix.shape[0]
    if matrix.shape != (dimension, dimension):
        raise ValueError("matrix must be square")
    low = eigh(
        matrix,
        subset_by_index=[0, 0],
        eigvals_only=True,
        driver="evr",
        check_finite=True,
    )[0]
    high = eigh(
        matrix,
        subset_by_index=[dimension - 1, dimension - 1],
        eigvals_only=True,
        driver="evr",
        check_finite=True,
    )[0]
    return float(low), float(high)


def marginal(vector: np.ndarray, theta_minus: np.ndarray) -> float:
    return float(np.vdot(vector, theta_minus * vector).real)


def constrained_top(
    system: NystromSystem,
    target_marginal: float,
    *,
    bracket: tuple[float, float] = (-1.0, 1.0),
    xtol: float = 2.0e-11,
) -> ConstrainedResult:
    """Solve the dual top-eigenvalue flow at a fixed negative marginal."""

    if not 0.0 < target_marginal < 1.0:
        raise ValueError("target_marginal must lie in (0,1)")
    projection = np.diag(system.theta_minus)

    def solve(mu: float) -> tuple[float, float, np.ndarray]:
        value, vector = top_eigenpair(system.operator - mu * projection)
        return value, marginal(vector, system.theta_minus), vector

    def residual(mu: float) -> float:
        return solve(mu)[1] - target_marginal

    left, right = bracket
    if residual(left) * residual(right) >= 0.0:
        raise ValueError("bracket does not straddle the requested marginal")
    mu = float(brentq(residual, left, right, xtol=xtol))
    dual_value, observed, _ = solve(mu)
    objective = dual_value + mu * observed
    return ConstrainedResult(
        mu=mu,
        dual_eigenvalue=dual_value,
        marginal=observed,
        objective=objective,
        residual=observed - target_marginal,
    )


def second_variation_coefficient(system: NystromSystem) -> float:
    """Return the finite-window top-state quadratic form of V."""

    _, vector = top_eigenpair(system.operator)
    return float(np.vdot(vector, system.second_variation @ vector).real)


def linear_extrapolation(
    sizes: np.ndarray | list[float], values: np.ndarray | list[float]
) -> dict[str, float]:
    """Fit value = intercept + slope/size and reproduce the paper's error."""

    size = np.asarray(sizes, dtype=float)
    y = np.asarray(values, dtype=float)
    if size.ndim != 1 or y.shape != size.shape or len(size) < 3:
        raise ValueError("sizes and values must be matching 1D arrays of length >= 3")
    x = 1.0 / size
    design = np.column_stack([np.ones_like(x), x])
    intercept, slope = np.linalg.lstsq(design, y, rcond=None)[0]
    residuals = y - (intercept + slope * x)
    residual_sum = float(np.sum(residuals**2))
    denominator = len(x) * float(np.sum(x * x)) - float(np.sum(x)) ** 2
    variance = residual_sum / (len(x) - 2) * float(np.sum(x * x)) / denominator
    return {
        "intercept": float(intercept),
        "slope": float(slope),
        "residual_sum": residual_sum,
        "intercept_std": float(np.sqrt(variance)),
    }


def weighted_window_extrapolation(
    windows: np.ndarray | list[float],
    values: np.ndarray | list[float],
    uncertainties: np.ndarray | list[float],
) -> dict[str, float]:
    """Fit value = intercept + slope/window with paper uncertainties."""

    window = np.asarray(windows, dtype=float)
    y = np.asarray(values, dtype=float)
    sigma = np.asarray(uncertainties, dtype=float)
    if window.shape != y.shape or y.shape != sigma.shape or len(window) < 3:
        raise ValueError("weighted fit inputs must have matching length >= 3")
    if np.any(sigma <= 0.0):
        raise ValueError("uncertainties must be positive")
    x = 1.0 / window
    weights = 1.0 / sigma**2
    design = np.column_stack([np.ones_like(x), x])
    root_weight = np.sqrt(weights)
    intercept, slope = np.linalg.lstsq(
        design * root_weight[:, None], y * root_weight, rcond=None
    )[0]
    residuals = y - (intercept + slope * x)
    weighted_residual_sum = float(np.sum(weights * residuals**2))
    s0 = float(np.sum(weights))
    sx = float(np.sum(weights * x))
    sxx = float(np.sum(weights * x * x))
    determinant = s0 * sxx - sx * sx
    variance = weighted_residual_sum / (len(x) - 2) * sxx / determinant
    return {
        "intercept": float(intercept),
        "slope": float(slope),
        "weighted_residual_sum": weighted_residual_sum,
        "intercept_std": float(np.sqrt(variance)),
    }


def parse_published_fixed_window_tables(tex_path: Path) -> dict[int, dict[str, list[float]]]:
    """Extract the seven finite-N tables from the immutable source TeX."""

    text = tex_path.read_text(encoding="utf-8")
    tables: dict[int, dict[str, list[float]]] = {}
    for block in re.findall(r"\\begin\{table\}.*?\\end\{table\}", text, re.DOTALL):
        label = re.search(r"\\label\{alpha_for_L=(\d+)\}", block)
        if label is None:
            continue
        window = int(label.group(1))
        rows = re.findall(
            r"^\s*\d+\s*&\s*(\d+)\s*&\s*(0\.\d+)\s*(?:\\\\)?\s*$",
            block,
            re.MULTILINE,
        )
        if not rows:
            raise ValueError(f"no numeric rows parsed for L={window}")
        tables[window] = {
            "half_intervals": [int(row[0]) for row in rows],
            "top_eigenvalues": [float(row[1]) for row in rows],
        }
    expected = {10, 15, 20, 25, 30, 35, 40}
    if set(tables) != expected:
        raise ValueError(f"unexpected fixed-window tables: {sorted(tables)}")
    return tables


PUBLISHED_FIXED_WINDOW_TABLES = {
    10: {
        "half_intervals": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        "top_eigenvalues": [
            0.1089941477648881,
            0.1139918526091255,
            0.1156769692627627,
            0.1165224285063283,
            0.1170305983268448,
            0.1173697450068959,
            0.1176121707518563,
            0.1177940869441254,
            0.1179356345180387,
            0.1180489085192777,
        ],
    },
    15: {
        "half_intervals": [150, 300, 450, 600, 750, 900, 1050, 1200, 1350, 1500],
        "top_eigenvalues": [
            0.1119434239699512,
            0.1169883703222082,
            0.1186785116904098,
            0.1195264258732301,
            0.1200361158663618,
            0.1203763059276854,
            0.120619494212111,
            0.1208019926220471,
            0.1209439994908275,
            0.1210576451546305,
        ],
    },
    20: {
        "half_intervals": [400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200],
        "top_eigenvalues": [
            0.1184799591245791,
            0.1201715170800806,
            0.1210211077144216,
            0.12153204630868,
            0.121873155366299,
            0.1221170385559465,
            0.122300077843297,
            0.1224425165250773,
            0.1225565144042943,
            0.1226498163346949,
        ],
    },
    25: {
        "half_intervals": [500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750],
        "top_eigenvalues": [
            0.1193720192594545,
            0.121070092011453,
            0.1219223352025476,
            0.1224346215338796,
            0.1227765382427701,
            0.1230209570947946,
            0.1232043766828351,
            0.123347098871649,
            0.1234613160028462,
            0.1235547924141025,
        ],
    },
    30: {
        "half_intervals": [600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300],
        "top_eigenvalues": [
            0.1199705773485895,
            0.1216727154735607,
            0.1225237102038637,
            0.1230354498337929,
            0.1233770750757993,
            0.1236213172702387,
            0.1238046200925763,
            0.1239472601723789,
            0.124061416829827,
            0.1241548470766964,
        ],
    },
    35: {
        "half_intervals": [800, 1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000, 4400],
        "top_eigenvalues": [
            0.1210457163111231,
            0.1225236257266571,
            0.1232707319394567,
            0.123719661701017,
            0.1240192405176445,
            0.1242333716554072,
            0.1243940508807573,
            0.1245190718418926,
            0.1246191191181317,
            0.1247009962047494,
        ],
    },
    40: {
        "half_intervals": [1200, 1800, 2400, 3000, 3600, 4200, 4800, 5400],
        "top_eigenvalues": [
            0.1224211080034019,
            0.1235567482529446,
            0.12412652657885,
            0.1244689068130608,
            0.1246973635442337,
            0.1248606442986848,
            0.1249831574822948,
            0.1250784764658047,
        ],
    },
}


def published_fixed_window_tables() -> dict[int, dict[str, list[float]]]:
    """Return the source-derived numeric tables needed by the public rerun."""

    return {
        window: {
            "half_intervals": list(table["half_intervals"]),
            "top_eigenvalues": list(table["top_eigenvalues"]),
        }
        for window, table in PUBLISHED_FIXED_WINDOW_TABLES.items()
    }


PUBLISHED_WINDOW_LIMITS = {
    10: (0.1190457811547612, 5.561804879449029e-6),
    15: (0.1220638424358060, 3.375966537451888e-6),
    20: (0.1235739992757623, 1.794581838275372e-6),
    25: (0.1244822862467697, 1.477042007656790e-6),
    30: (0.1250829195703286, 9.338351587060546e-7),
    35: (0.1255108771862945, 2.433955824900637e-6),
    40: (0.1258365731314665, 1.017018984296298e-6),
}


def published_final_fit() -> dict[str, float]:
    windows = np.array(sorted(PUBLISHED_WINDOW_LIMITS), dtype=float)
    values = np.array([PUBLISHED_WINDOW_LIMITS[int(item)][0] for item in windows])
    uncertainties = np.array([PUBLISHED_WINDOW_LIMITS[int(item)][1] for item in windows])
    return weighted_window_extrapolation(windows, values, uncertainties)
