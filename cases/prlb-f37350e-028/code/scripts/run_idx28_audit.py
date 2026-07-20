#!/usr/bin/env python3
"""Run the independent source/gold audit for PRL-Bench idx28."""

from __future__ import annotations

import json
from pathlib import Path
import sys


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from neel_macrospin_audit import (  # noqa: E402
    frozen_mep_barrier,
    frozen_task3_response,
    mep_barrier,
    rigid_precession_residuals,
    rigid_precession_solution,
    stationary_points,
    tracked_interior_response,
)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    lam = 1.8
    cosine, omega_d = rigid_precession_solution(100.0, 1.0, 1.0, 0.0, 0.1, 20.0)
    theta_residual, phi_residual = rigid_precession_residuals(
        100.0, 1.0, 1.0, 0.0, 0.1, 20.0, cosine, omega_d
    )
    result = {
        "schema_version": 1,
        "source_contract": {
            "status": "verified_direct_prl",
            "paper": "Deterministic Switching of the Neel Vector by Asymmetric Spin Torque",
            "arxiv": "2506.10786",
            "publication": "Physical Review Letters 136, 096702 (2026)",
            "doi": "10.1103/fkyr-z5b8",
            "source_equations": "Accepted-paper Eqs. (7)-(8) reproduce the benchmark Lagrange-Rayleigh pair.",
            "source_observation": "The paper explicitly lists a third beta=pi stationary solution with 0<Theta<pi and constant azimuthal motion.",
        },
        "task_1": {
            "verdict": "gold_invalid",
            "reason": "For lambda<1 the y-positive point is a saddle and the two off-axis points are global minima; at lambda=1 the merged minimum is degenerate.",
            "lambda_0_4": [point.to_dict() for point in stationary_points(0.4)],
            "lambda_1": [point.to_dict() for point in stationary_points(1.0)],
            "lambda_1_8": [point.to_dict() for point in stationary_points(lam)],
        },
        "task_2": {
            "verdict": "gold_invalid",
            "reason": "The minimax arc is y>=0, but max-minus-min changes at lambda=1/2 and lambda=1.",
            "exact_piecewise": ["omega_K(1-lambda)^2", "omega_K lambda^2", "omega_K(2lambda-1)"],
            "comparison": {
                str(value): {"exact": mep_barrier(value), "frozen": frozen_mep_barrier(value)}
                for value in (0.2, 0.7, 1.8)
            },
        },
        "task_3": {
            "verdict": "gold_invalid_ill_posed",
            "reason": "For lambda>1 the interior theta=pi/2 point is a local minimum; the MEP maximum occurs at an endpoint, so the requested unique 1D saddle does not exist.",
            "tracked_non_saddle_response": tracked_interior_response(lam),
            "frozen_response": frozen_task3_response(lam),
        },
        "task_4": {
            "verdict": "gold_invalid",
            "reason": "The exact theta and phi equations admit interior rigid precession. The paper also explicitly describes this constant-oscillation branch.",
            "solvability_condition": {
                "theta": "c[Omega^2+(1+eta)omega_F Omega-2 omega_E omega_K]+omega_E(1-eta)omega_F=0",
                "phi": "2 alpha Omega-omega_D[(1+eta)+(1-eta)c Omega/omega_E]=0",
            },
            "counterexample": {
                "omega_E": 100.0,
                "omega_K": 1.0,
                "omega_F": 1.0,
                "eta": 0.0,
                "alpha": 0.1,
                "Omega": 20.0,
                "cos_theta": cosine,
                "omega_D": omega_d,
                "theta_residual": theta_residual,
                "phi_residual": phi_residual,
            },
            "answer": "Yes",
        },
        "verdict": "benchmark_gold_invalid",
        "failed_tasks": [1, 2, 3, 4],
        "valid_tasks": [],
    }
    write_json(CASE_ROOT / "outputs" / "data" / "idx28_gold_audit.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
