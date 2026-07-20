#!/usr/bin/env python3
"""Write the machine-readable idx16 source and gold audit."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from dwave_impurity_audit import (  # noqa: E402
    clean_green_matrix,
    d_wave_gap,
    frozen_fixed_log_pole,
    frozen_resonance_energy,
    local_green_low_energy,
    low_branch_real_axis_root,
    pole_residual_at_frozen_energy,
    rmp_logarithmic_pole,
    width_to_energy,
)


def complex_payload(value: complex) -> dict[str, float]:
    return {"real": value.real, "imag": value.imag, "abs": abs(value)}


def main() -> None:
    delta_0 = 30.0
    c = 0.3
    gap = d_wave_gap(delta_0, math.pi / 8.0)
    matrix = clean_green_matrix(50.0, 15.0, gap)
    local_frozen = local_green_low_energy(1.2, delta_0, cutoff_factor=2.0)
    local_rmp = local_green_low_energy(
        1.2, delta_0, cutoff_factor=4.0, imaginary_sign=1.0
    )
    frozen_energy = frozen_resonance_energy(c, delta_0)
    frozen_proxy = frozen_fixed_log_pole(c, delta_0)
    source_pole = rmp_logarithmic_pole(c, delta_0)
    residual = pole_residual_at_frozen_energy(c, delta_0)
    real_root = low_branch_real_axis_root(c, delta_0, cutoff_factor=2.0)

    payload = {
        "schema_version": 1,
        "paper_id": "prlb-f37350e-016",
        "source_contract": {
            "status": "source_contract_mismatch",
            "frozen_candidate": {
                "title": "Probing Sign-Changing Order Parameters via Impurity States in unconventional superconductors",
                "venue": "Phys. Rev. B 111, 174525 (2025)",
                "arxiv": "2501.01155v3",
                "match": "general T-matrix and d-wave sign-cancellation narrative only",
            },
            "direct_formula_source": {
                "title": "Impurity-induced states in conventional and unconventional superconductors",
                "venue": "Rev. Mod. Phys. 78, 373 (2006)",
                "arxiv": "cond-mat/0411318",
                "match": "pole condition, normalized local Green function, and logarithmic pole formula",
            },
            "reason": "No recovered PRL source satisfies the benchmark identity; the closest 2025 PRB cites the older 2006 RMP that actually contains the frozen formulas.",
        },
        "task_1": {
            "status": "valid",
            "delta_phi_mev": gap,
            "green_matrix_per_mev": [list(matrix[0]), list(matrix[1])],
        },
        "task_2": {
            "status": "valid_with_declared_cutoff_and_normalization",
            "frozen_cutoff_2": complex_payload(local_frozen),
            "rmp_cutoff_4_as_printed": complex_payload(local_rmp),
            "normalization": "dimensionless density-of-states-normalized local propagator",
            "caveat": "The cutoff constant and printed imaginary-part sign differ between the frozen answer and the RMP convention; off-diagonal cancellation is exact only under the stated C4-symmetric integration/patch contract.",
        },
        "task_3": {
            "status": "invalid",
            "frozen_reported_energy_mev": frozen_energy,
            "correct_unit": "meV",
            "frozen_printed_unit": "meV^-1",
            "pole_residual": complex_payload(residual),
            "frozen_fixed_log_complex_proxy_mev": complex_payload(frozen_proxy),
            "frozen_width_to_energy": width_to_energy(frozen_proxy),
            "rmp_logarithmic_pole_mev": complex_payload(source_pole),
            "rmp_width_to_energy": width_to_energy(source_pole),
            "rmp_logarithm": math.log(8.0 / (math.pi * c)),
            "real_axis_low_branch_diagnostic_mev": real_root,
            "reason": "The frozen number is only the real part of a fixed-log approximation, does not solve G0(Omega)=c, discards a width larger than the energy, and is called exact outside the controlled log>>1 regime.",
        },
        "verdict": {
            "status": "benchmark_gold_invalid",
            "source_gate": "failed",
            "formula_gate": "failed_for_task_3",
            "tasks_valid": [1, 2],
            "tasks_invalid": [3],
        },
    }

    output = CASE_ROOT / "outputs" / "data" / "idx16_gold_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["verdict"], indent=2))


if __name__ == "__main__":
    main()
