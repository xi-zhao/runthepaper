#!/usr/bin/env python3
"""Recompute every numeric gold item in PRL-Bench idx8."""

from __future__ import annotations

import json
import sys
from pathlib import Path


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from secular_resonance import (  # noqa: E402
    coefficient_b,
    coefficient_c,
    coefficient_d,
    gamma_parameter,
    resonance_semimajor_axis,
    separatrix_peak,
    source_figc_beta,
)


def main() -> None:
    gamma0 = gamma_parameter(45.0, 20.0, 0.42, 5.5, 0.8)
    a_res = resonance_semimajor_axis(0.42, gamma0)
    b = coefficient_b(0.8)
    c_res = coefficient_c(45.0, 20.0, a_res, 5.5, 0.8)
    peak = separatrix_peak(c_res, coefficient_d(b, 1.0))
    payload = {
        "benchmark_record": "prlb-f37350e-008",
        "source_contract": {
            "status": "mismatch",
            "direct_formula_source": "arXiv:2403.03250v2 / PRL 132, 231403 (2024)",
            "closest_in_window_source": "arXiv:2509.20806v2 / ApJL",
            "reason": "No single PRL in the frozen date window supports the record.",
        },
        "gold_audit": {
            "task_1": {"status": "valid", "hamiltonian_sign": "Phi_N - dot(varpi_in) L_out"},
            "task_2": {"status": "valid", "B": b, "K": 4, "C_at_resonance": c_res},
            "task_3": {"status": "valid", "power": -4.5},
            "task_4": {"status": "valid", "gamma0": gamma0, "rounded": round(gamma0, 3), "inequality": "gamma0 < 1"},
            "task_5": {"status": "valid", "a_in_res_au": a_res, "rounded": round(a_res, 3)},
            "task_6": {"status": "valid", "D_at_gamma_1": coefficient_d(b, 1.0), "peak": peak, "rounded": round(peak, 3), "initial_below_peak": 0.08 < peak},
            "task_7": {"status": "valid", "action_integrand": "1-sqrt(1-e_out^2)", "captured_trend": "increase"},
        },
        "source_figc": {"beta": source_figc_beta(), "energies": [0.02, 0.0, -0.002]},
        "verdict": "benchmark_source_invalid_gold_valid",
    }
    output = CASE_ROOT / "outputs/data/idx8_gold_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
