#!/usr/bin/env python3
"""Evaluate the frozen idx9 answers against independent formulas."""

from __future__ import annotations

import json
import sys
from pathlib import Path


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from power_law_audit import (  # noqa: E402
    correct_counterterm_brackets,
    frozen_counterterm_brackets,
    frozen_scalar_high_frequency_w,
    rgw_high_frequency_w,
    scalar_high_frequency_w,
)


def main() -> None:
    counterterm_point = {"beta": -2.2, "mass": 0.3, "t_minus_tau": 0.8, "k": 7.0}
    args = tuple(counterterm_point.values())
    correct_rho, correct_pressure = correct_counterterm_brackets(*args)
    frozen_rho, frozen_pressure = frozen_counterterm_brackets(*args)
    payload = {
        "schema_version": 1,
        "benchmark_record": "prlb-f37350e-009",
        "source_contract": {
            "status": "mismatch",
            "reason": "The frozen record is a composite of three older non-PRL papers, not one in-window PRL.",
            "sources": [
                {
                    "scope": "Tasks 1-2 and RGW comparison",
                    "source": "arXiv:1512.03134v2 / Phys. Rev. D 94, 044033 (2016)",
                },
                {
                    "scope": "Massive minimally coupled scalar stress tensor and adiabatic-order discussion in de Sitter",
                    "source": "arXiv:1903.10115v4",
                },
                {
                    "scope": "General power-law Robertson-Walker analysis, but massless scalar only",
                    "source": "arXiv:1909.13010v2 / Chin. Phys. C 44, 095104 (2020)",
                },
            ],
        },
        "gold_audit": {
            "task_1": {"status": "valid", "finding": "n_t=-2 epsilon/(1-epsilon)"},
            "task_2_1": {"status": "valid", "finding": "beta_k=Delta(a''/a)e^{i phi}/(4k^2)+O(k^-3)"},
            "task_2_2": {"status": "valid", "finding": "|beta_k|^2 proportional to k^-4"},
            "task_2_3": {"status": "valid", "finding": "finite jump in a'' (equivalently a''/a for continuous nonzero a)"},
            "task_3_1": {
                "status": "semantic_error",
                "finding": "The two displayed formulas are energy density and pressure, but both are labeled rho_k.",
            },
            "task_3_2_amplitude": {
                "status": "valid",
                "finding": "The printed |u_k^(4)|^2 equals the general (2k)^-1[1-V/(2k^2)+(3V^2+V'')/(8k^4)].",
            },
            "task_3_2_counterterms": {
                "status": "invalid",
                "finding": "The printed rho/p counterterms do not follow from that amplitude and the prompt's own stress tensor.",
                "counterexample_parameters": counterterm_point,
                "correct_brackets": {"rho": correct_rho, "pressure": correct_pressure},
                "frozen_brackets": {"rho": frozen_rho, "pressure": frozen_pressure},
                "absolute_difference": {
                    "rho": abs(correct_rho - frozen_rho),
                    "pressure": abs(correct_pressure - frozen_pressure),
                },
            },
            "task_3_3": {
                "status": "incomplete",
                "finding": "The task requests separate leading rho_re and p_re, but the frozen answer supplies only one ratio.",
            },
            "task_3_4_scalar": {
                "status": "invalid",
                "correct": "(beta+7)/(3(beta+1))",
                "frozen": "3(beta+1)/(beta+7)",
                "counterexample_beta": -3.0,
                "correct_value": scalar_high_frequency_w(-3.0),
                "frozen_value": frozen_scalar_high_frequency_w(-3.0),
                "fixed_points": {"w=1": 2.0, "w=-1": -2.5},
            },
            "task_3_4_rgw": {
                "status": "invalid_conclusion",
                "formula_status": "valid",
                "formula": "(beta-2)/(3(beta+4))",
                "correct_fixed_points": {"w=1": -7.0, "w=-1": -2.5},
                "frozen_claim_at_beta_minus_2": 1.0,
                "actual_at_beta_minus_2": rgw_high_frequency_w(-2.0),
            },
        },
        "paper_figure_observation": {
            "target": "2016 PRD Fig. 2",
            "parameter_match": "paper_exact",
            "closed_forms": {
                "n_t": "2x^2/(1+x^2)",
                "alpha_t": "4x^2/(1+x^2)^2",
            },
            "landmarks": {"x=0": [0.0, 0.0], "x=1": [1.0, 1.0], "x=3": [1.8, 0.36]},
        },
        "verdict": "benchmark_gold_invalid",
    }
    output = CASE_ROOT / "outputs/data/idx9_gold_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
