#!/usr/bin/env python3
"""Compute the idx40 source/frozen-definition audit."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from scipy.optimize import brentq


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from mi_wedge_audit import (  # noqa: E402
    background_terms,
    frozen_claimed_speed,
    minority_coefficients,
    source_edge_speed,
    source_edge_wavenumber,
    stationarity,
    unstable_endpoint,
)


def main() -> None:
    x_star = brentq(stationarity, 0.4, 0.6, xtol=1e-15)
    s_star = float(background_terms(x_star)[2])
    source_a1, source_a3 = minority_coefficients(source_definition=True)
    frozen_a1, frozen_a3 = minority_coefficients(source_definition=False)
    payload = {
        "benchmark_record": "prlb-f37350e-040",
        "source": {
            "arxiv": "2412.17083v2",
            "publication": "Phys. Rev. Lett. 135, 113401 (2025)",
            "doi": "10.1103/6jsr-f8q1",
            "contract": "verified",
        },
        "task_1": {"verdict": "valid", "reason": "The symmetric dispersion and immiscibility condition match source Eqs. S10-S12."},
        "task_2": {
            "verdict": "invalid",
            "frozen_definition": "d Im(omega_-)/dk on 0<k<sqrt(S) is positive and strictly decreases to zero; no minimum positive value exists.",
            "source_definition": "d Re(omega_-)/dk on k>sqrt(2S) has its minimum at k=sqrt(3S), with V=4sqrt(S).",
        },
        "task_3": {
            "verdict": "partially_valid",
            "x_star": x_star,
            "q1_star": (1.0 - x_star) ** 0.5,
            "q2_star": x_star**0.5,
            "s_star": s_star,
            "frozen_formula_value": frozen_claimed_speed(s_star),
            "frozen_reported_value": 0.250370248905988,
            "source_speed": source_edge_speed(s_star),
        },
        "task_4": {
            "verdict": "partially_valid",
            "kmax_valid": unstable_endpoint(s_star),
            "frozen_kmin_invalid": 0.0885103478486455,
            "source_kmin": source_edge_wavenumber(s_star),
        },
        "task_5": {
            "verdict": "invalid",
            "source_coefficients": {"a1": source_a1, "a3": source_a3},
            "coefficients_for_frozen_prefactor": {"a1": frozen_a1, "a3": frozen_a3},
            "note": "The displayed frozen a3 expression is smaller by another factor of two; its printed decimals also miss the stated couplings.",
        },
        "verdict": "benchmark_gold_invalid",
    }
    output = CASE_ROOT / "outputs/data/idx40_gold_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
