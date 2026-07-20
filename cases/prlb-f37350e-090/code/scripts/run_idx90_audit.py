#!/usr/bin/env python3
"""Run the literal source/gold audit for PRL-Bench idx90."""

from __future__ import annotations

import json
from pathlib import Path
import sys


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from photonic_edge_audit import (  # noqa: E402
    direct_complex_kdos_component,
    exact_kdos_component,
    frozen_kdos_component,
    frozen_radial_rate_prefactor,
    radial_rate_prefactor,
    residual_after_frozen_pole_subtraction,
    toy_model_rates,
)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    point = {"epsilon0": 4.0, "omega": 0.51, "resonance": 0.47, "gamma": 0.03, "residue": [1.2, -0.4]}
    residue = complex(*point["residue"])
    exact = exact_kdos_component(4.0, 0.51, 0.47, 0.03, residue)
    direct = direct_complex_kdos_component(4.0, 0.51, 0.47, 0.03, residue)
    frozen = frozen_kdos_component(4.0, 0.51, 0.47, 0.03, residue)
    toy = {key: str(value) for key, value in toy_model_rates().items()}
    result = {
        "schema_version": 1,
        "source_contract": {
            "status": "verified_direct_prl",
            "paper": "Spontaneous Emission Decay and Excitation in Photonic Time Crystals",
            "arxiv": "2404.13287",
            "publication": "Physical Review Letters 135, 133801 (2025)",
            "doi": "10.1103/5v2w-yg7v",
            "transcription_boundary": "The paper's projected Green tensor contains an external minus sign and defines I_alpha as a normalized field intensity. The frozen prompt removes that minus while retaining the paper's positive Lorentzian decomposition.",
        },
        "task_1": {
            "verdict": "gold_invalid",
            "reason": "The explicit ansatz I/(omega-(Omega-i gamma)) gives x Im(I)-gamma Re(I); the frozen numerator is its negative.",
            "comparison_point": point,
            "direct_complex": direct,
            "exact_closed_form": exact,
            "frozen_closed_form": frozen,
        },
        "task_2": {
            "verdict": "gold_invalid",
            "reason": "The literal lossless distribution is -2 epsilon0 omega Re(I) delta(omega-Omega), not the frozen positive weight.",
        },
        "task_3": {
            "verdict": "gold_invalid",
            "reason": "Full angular integration gives |p|^2 omega/(8 pi epsilon0 hbar), four times the frozen prefactor.",
            "exact_prefactor": radial_rate_prefactor(1.0, 0.5, 4.0, 1.0),
            "frozen_prefactor": frozen_radial_rate_prefactor(1.0, 0.5, 4.0, 1.0),
        },
        "task_4": {
            "verdict": "gold_valid",
            "reason": "A nonzero simple real-axis pole makes the ordinary improper radial integral logarithmically divergent; only a separately declared principal value could cancel one-sided logs.",
        },
        "task_5": {
            "verdict": "gold_invalid",
            "reason": "The prescribed subtraction acts on rho rather than k^2 rho and leaves residue R(1-k_R^2). Even after repairing it, J_EP has unspecified sign and the literal Tasks 1-3 give a different epsilon0/Omega scaling.",
            "residual_example": {"k_pole": 1.3, "input_residue": 2.0, "remaining_residue": residual_after_frozen_pole_subtraction(1.3, 2.0)},
            "toy": toy,
        },
        "task_6": {
            "verdict": "gold_valid",
            "reason": "With a finite orthogonal-mode residue, the inverse Puiseux slope is proportional to sqrt(k_EP-k) and vanishes at the edge.",
        },
        "task_7": {
            "verdict": "gold_invalid",
            "reason": "For positive J_EP the literal delta weight is negative, so the plus branch contributes zero decay and finite excitation 0.172290279130... . Its magnitude limit is 0.172290279819..., eight times the frozen reported number and 32 times the frozen Task 5 formula at epsilon0=4.",
            "toy": toy,
        },
        "verdict": "benchmark_gold_invalid",
        "failed_tasks": [1, 2, 3, 5, 7],
        "valid_tasks": [4, 6],
    }
    write_json(CASE_ROOT / "outputs" / "data" / "idx90_gold_audit.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
