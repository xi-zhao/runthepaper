"""Geometry-adaptive generalized Brillouin-zone extraction.

The core object is a GBZ point: an OBC energy, two inverse localization
lengths selected by the hierarchical potential, and a momentum pair solving
the analytically continued characteristic equation.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping

import numpy as np
from scipy.optimize import least_squares

from src.geometry_adaptive import (
    HoppingModel,
    basis_hopping_model,
    geometry_adaptive_potential,
)


@dataclass(frozen=True)
class GBZPoint:
    energy: complex
    mu_1: float
    mu_2: float
    k_1: float
    k_2: float
    residual: float

    @property
    def beta_1(self) -> complex:
        return complex(np.exp(self.mu_1 + 1j * self.k_1))

    @property
    def beta_2(self) -> complex:
        return complex(np.exp(self.mu_2 + 1j * self.k_2))


def laurent_energy(
    beta_1: complex,
    beta_2: complex,
    hoppings: Mapping[tuple[int, int], complex],
) -> complex:
    """Evaluate a scalar two-variable Laurent Hamiltonian."""

    return complex(
        sum(
            amplitude * beta_1**power_1 * beta_2**power_2
            for (power_1, power_2), amplitude in hoppings.items()
        )
    )


def solve_phase_pairs(
    energy: complex,
    hoppings: Mapping[tuple[int, int], complex],
    deformations: tuple[float, float],
    *,
    seed_count: int = 6,
    residual_tolerance: float = 1e-7,
    duplicate_tolerance: float = 1e-3,
) -> tuple[tuple[float, float, float], ...]:
    """Solve H(exp(mu1+ik1), exp(mu2+ik2)) = E from periodic grid seeds."""

    if seed_count < 2:
        raise ValueError("seed_count must be at least 2")
    mu_1, mu_2 = deformations

    def residual(momentum: np.ndarray) -> np.ndarray:
        value = laurent_energy(
            np.exp(mu_1 + 1j * momentum[0]),
            np.exp(mu_2 + 1j * momentum[1]),
            hoppings,
        ) - energy
        return np.asarray((value.real, value.imag), dtype=np.float64)

    solutions: list[tuple[float, float, float]] = []
    seeds = np.linspace(-np.pi, np.pi, seed_count, endpoint=False)
    for seed_1 in seeds:
        for seed_2 in seeds:
            result = least_squares(
                residual,
                np.asarray((seed_1, seed_2)),
                method="lm",
                xtol=1e-10,
                ftol=1e-10,
                gtol=1e-10,
                max_nfev=100,
            )
            norm = float(np.linalg.norm(result.fun))
            if not result.success or norm > residual_tolerance:
                continue
            folded = (np.asarray(result.x) + np.pi) % (2.0 * np.pi) - np.pi
            if any(
                _periodic_distance(folded, np.asarray(existing[:2]))
                <= duplicate_tolerance
                for existing in solutions
            ):
                continue
            solutions.append((float(folded[0]), float(folded[1]), norm))
    return tuple(solutions)


def solve_gbz_for_energy(
    energy: complex,
    hoppings: HoppingModel,
    *,
    basis: str,
    momentum_samples: int = 64,
    deformation_bounds: tuple[float, float] = (-1.5, 1.5),
    minimization_tolerance: float = 2e-4,
    seed_count: int = 6,
) -> tuple[GBZPoint, ...]:
    """Execute Supplementary Note 3 Steps 1-2 for one OBC energy."""

    potential = geometry_adaptive_potential(
        energy,
        hoppings,
        basis=basis,
        momentum_samples=momentum_samples,
        deformation_bounds=deformation_bounds,
        tolerance=minimization_tolerance,
    )
    deformations = (
        potential.cylinder_1.deformation,
        potential.cylinder_2.deformation,
    )
    transformed = basis_hopping_model(hoppings, basis)
    phase_pairs = solve_phase_pairs(
        energy,
        transformed,
        deformations,
        seed_count=seed_count,
    )
    return tuple(
        GBZPoint(
            energy=energy,
            mu_1=deformations[0],
            mu_2=deformations[1],
            k_1=k_1,
            k_2=k_2,
            residual=residual,
        )
        for k_1, k_2, residual in phase_pairs
    )


def _periodic_distance(first: np.ndarray, second: np.ndarray) -> float:
    difference = np.angle(np.exp(1j * (first - second)))
    return float(np.linalg.norm(difference))
