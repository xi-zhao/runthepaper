"""Independent analytic helpers for PRL-Bench idx28."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math

import numpy as np


@dataclass(frozen=True)
class StationaryPoint:
    vector: tuple[float, float, float]
    kind: str
    tangent_eigenvalues: tuple[float, float]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _require_positive(name: str, value: float) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")


def potential(vector: np.ndarray | tuple[float, float, float], lam: float, omega_k: float = 1.0) -> float:
    """Return U=-2 omega_K lambda n_y-omega_K n_z^2."""

    _require_positive("lam", lam)
    _require_positive("omega_k", omega_k)
    n = np.asarray(vector, dtype=float)
    if n.shape != (3,) or not np.isclose(np.linalg.norm(n), 1.0, atol=1.0e-10):
        raise ValueError("vector must be a unit 3-vector")
    return float(-2.0 * omega_k * lam * n[1] - omega_k * n[2] ** 2)


def stationary_points(lam: float, omega_k: float = 1.0) -> list[StationaryPoint]:
    """Complete constrained stationary set and tangent-Hessian classification."""

    _require_positive("lam", lam)
    _require_positive("omega_k", omega_k)
    points: list[StationaryPoint] = []
    plus_eigs = tuple(sorted((2.0 * omega_k * lam, 2.0 * omega_k * (lam - 1.0))))
    if np.isclose(lam, 1.0, atol=1.0e-12):
        plus_kind = "degenerate_global_minimum"
    elif lam < 1.0:
        plus_kind = "saddle"
    else:
        plus_kind = "global_minimum"
    points.append(StationaryPoint((0.0, 1.0, 0.0), plus_kind, plus_eigs))
    points.append(
        StationaryPoint(
            (0.0, -1.0, 0.0),
            "global_maximum",
            tuple(sorted((-2.0 * omega_k * lam, -2.0 * omega_k * (lam + 1.0)))),
        )
    )
    if lam < 1.0:
        z = math.sqrt(1.0 - lam * lam)
        eigs = tuple(sorted((2.0 * omega_k, 2.0 * omega_k * (1.0 - lam * lam))))
        points.extend(
            [
                StationaryPoint((0.0, lam, z), "global_minimum", eigs),
                StationaryPoint((0.0, lam, -z), "global_minimum", eigs),
            ]
        )
    return points


def positive_arc_energy(theta: np.ndarray | float, lam: float, omega_k: float = 1.0) -> np.ndarray:
    """Energy on n=(0,sin(theta),cos(theta)), theta in [0,pi]."""

    _require_positive("lam", lam)
    _require_positive("omega_k", omega_k)
    angle = np.asarray(theta, dtype=float)
    return -2.0 * omega_k * lam * np.sin(angle) - omega_k * np.cos(angle) ** 2


def negative_arc_energy(theta: np.ndarray | float, lam: float, omega_k: float = 1.0) -> np.ndarray:
    """Energy on the competing y<=0 arc."""

    _require_positive("lam", lam)
    _require_positive("omega_k", omega_k)
    angle = np.asarray(theta, dtype=float)
    return 2.0 * omega_k * lam * np.sin(angle) - omega_k * np.cos(angle) ** 2


def mep_barrier(lam: float, omega_k: float = 1.0) -> float:
    """Exact max(U)-min(U) on the minimax yz-circle arc."""

    _require_positive("lam", lam)
    _require_positive("omega_k", omega_k)
    if lam <= 0.5:
        return omega_k * (1.0 - lam) ** 2
    if lam <= 1.0:
        return omega_k * lam * lam
    return omega_k * (2.0 * lam - 1.0)


def frozen_mep_barrier(lam: float, omega_k: float = 1.0) -> float:
    """Piecewise value printed by the frozen benchmark answer."""

    _require_positive("lam", lam)
    _require_positive("omega_k", omega_k)
    if lam <= 1.0:
        return 2.0 * omega_k * lam
    return 2.0 * omega_k * ((lam - 1.0) ** 2 + 1.0)


def tracked_interior_response(lam: float) -> float:
    """dn_z/d(delta) for the interior stationary point at theta=pi/2.

    For lambda>1 this stationary point is a local minimum, not the MEP saddle
    postulated by frozen Task 3.
    """

    if lam <= 1.0:
        raise ValueError("response branch requires lam > 1")
    return -lam / (lam - 1.0)


def frozen_task3_response(lam: float) -> float:
    if lam <= 1.0:
        raise ValueError("response branch requires lam > 1")
    return 1.0 / (lam * lam - 1.0)


def tilted_stationarity(theta: float, delta: float, lam: float) -> float:
    """Dimensionless U_theta/(2 omega_K) on the yz circle."""

    _require_positive("lam", lam)
    return -lam * math.cos(theta - delta) + math.sin(theta) * math.cos(theta)


def tracked_stationary_theta(delta: float, lam: float, *, iterations: int = 12) -> float:
    """Newton continuation of the interior stationary point from pi/2."""

    if lam <= 1.0:
        raise ValueError("response branch requires lam > 1")
    theta = math.pi / 2.0 + delta * lam / (lam - 1.0)
    for _ in range(iterations):
        value = tilted_stationarity(theta, delta, lam)
        derivative = lam * math.sin(theta - delta) + math.cos(2.0 * theta)
        theta -= value / derivative
    return theta


def rigid_precession_solution(
    omega_e: float,
    omega_k: float,
    omega_f: float,
    eta: float,
    alpha: float,
    omega: float,
) -> tuple[float, float]:
    """Construct cos(theta) and omega_D for a rigid precession solution."""

    for name, value in (("omega_e", omega_e), ("omega_k", omega_k), ("omega_f", omega_f), ("alpha", alpha)):
        _require_positive(name, value)
    if not -1.0 < eta < 1.0:
        raise ValueError("eta must lie in (-1,1)")
    if omega == 0.0:
        raise ValueError("omega must be nonzero")
    theta_denominator = omega * omega + (1.0 + eta) * omega_f * omega - 2.0 * omega_e * omega_k
    if theta_denominator == 0.0:
        raise ValueError("theta equation is singular")
    cosine = -omega_e * (1.0 - eta) * omega_f / theta_denominator
    if abs(cosine) >= 1.0:
        raise ValueError("chosen omega does not give an interior precession")
    phi_denominator = (1.0 + eta) + (1.0 - eta) * cosine * omega / omega_e
    if phi_denominator == 0.0:
        raise ValueError("phi equation is singular")
    omega_d = 2.0 * alpha * omega / phi_denominator
    return cosine, omega_d


def rigid_precession_residuals(
    omega_e: float,
    omega_k: float,
    omega_f: float,
    eta: float,
    alpha: float,
    omega: float,
    cosine: float,
    omega_d: float,
) -> tuple[float, float]:
    """Return the divided theta and phi algebraic residuals."""

    theta = cosine * (omega * omega + (1.0 + eta) * omega_f * omega - 2.0 * omega_e * omega_k)
    theta += omega_e * (1.0 - eta) * omega_f
    phi = 2.0 * alpha * omega - omega_d * ((1.0 + eta) + (1.0 - eta) * cosine * omega / omega_e)
    return theta, phi
