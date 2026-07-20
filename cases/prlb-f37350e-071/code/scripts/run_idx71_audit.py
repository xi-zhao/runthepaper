#!/usr/bin/env python3
"""Run the complete frozen-gold audit for PRL-Bench idx71."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
import sys

import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from parametric_memory_audit import (  # noqa: E402
    brute_phase_gain,
    exact_optimal_gain,
    exact_transient_peak,
    frozen_optimal_gain,
    frozen_quantum_steady_occupation,
    frozen_transient_peak,
    quantum_steady_occupation,
    threshold_inversion,
)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    comparison_point = {"lambda": 1.0, "coupling": 1.1, "delta": 0.6, "time": 0.7}
    exact_gain = float(exact_optimal_gain(1.0, 1.1, 0.6, 0.7))
    frozen_gain = float(frozen_optimal_gain(1.0, 1.1, 0.6, 0.7))
    sampled_gain = brute_phase_gain(1.0, 1.1, 0.6, 0.7)

    no_peak_frozen = frozen_transient_peak(1.0, 0.9, 0.6)
    peak = exact_transient_peak(1.0, 1.1, 0.6)
    assert peak is not None
    frozen_peak = frozen_transient_peak(1.0, 1.1, 0.6)

    ratio = 0.5
    result = {
        "schema_version": 1,
        "source_contract": {
            "status": "verified_direct_prl",
            "paper": "Unwanted Couplings Can Induce Amplification in Quantum Memories despite Negligible Apparent Noise",
            "arxiv": "2411.15362",
            "publication": "Physical Review Letters 135, 070802 (2025)",
            "doi": "10.1103/pz34-47pw",
            "benchmark_extension": "Tasks 1-5 add a damped classical/quantum parametric-amplifier model. The paper supplies the undamped semiclassical growth form and explicitly leaves a full quantum treatment for future work.",
        },
        "task_1": {
            "verdict": "gold_valid",
            "reason": "The detuning rotation gives the stated principal-branch exponents; arg(xi) is removable by a constant gauge.",
        },
        "task_2": {
            "verdict": "gold_valid",
            "reason": "Positive real Floquet growth occurs exactly when coupling^2 > lambda^2 + delta^2; |delta| >= coupling is uniformly stable.",
        },
        "task_3": {
            "verdict": "gold_invalid",
            "reason": "The physical phase optimization is the largest singular value on the conjugacy-constrained input, not the frozen cosh+(lambda/chi)sinh expression. Oscillatory splitting necessarily introduces phase-switch cusps.",
            "comparison_point": comparison_point,
            "exact_gain": exact_gain,
            "brute_phase_gain": sampled_gain,
            "frozen_gain": frozen_gain,
            "absolute_frozen_error": abs(exact_gain - frozen_gain),
        },
        "task_4": {
            "verdict": "gold_invalid",
            "reason": "The stated assumptions do not guarantee a positive interior maximum; one exists only when coupling > lambda in addition to chi < lambda.",
            "counterexample_without_peak": {
                "lambda": 1.0,
                "coupling": 0.9,
                "delta": 0.6,
                "exact_peak": None,
                "frozen_peak": {"time": no_peak_frozen[0], "gain": no_peak_frozen[1]},
            },
            "interior_peak_example": {
                "lambda": 1.0,
                "coupling": 1.1,
                "delta": 0.6,
                "exact_peak": {"time": peak[0], "gain": peak[1]},
                "frozen_peak": {"time": frozen_peak[0], "gain": frozen_peak[1]},
                "exact_gain_at_frozen_time": float(exact_optimal_gain(1.0, 1.1, 0.6, frozen_peak[0])),
            },
        },
        "task_5": {
            "verdict": "gold_invalid",
            "reason": "Vacuum Lyapunov equations give n=r^2/[2(1-r^2)]; the frozen answer is too large by exactly two.",
            "ratio": ratio,
            "exact_occupation": float(quantum_steady_occupation(ratio)),
            "frozen_occupation": float(frozen_quantum_steady_occupation(ratio)),
        },
        "task_6": {
            "verdict": "gold_valid",
            "critical_value": str(threshold_inversion()),
            "frozen_value": "2.10267600615632986004",
            "absolute_difference_from_frozen_decimal": str(
                abs(threshold_inversion() - Decimal("2.10267600615632986004"))
            ),
        },
        "verdict": "benchmark_gold_invalid",
        "failed_tasks": [3, 4, 5],
        "valid_tasks": [1, 2, 6],
    }
    write_json(CASE_ROOT / "outputs" / "data" / "idx71_gold_audit.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
