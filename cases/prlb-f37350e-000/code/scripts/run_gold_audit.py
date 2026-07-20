#!/usr/bin/env python3
"""Generate the independent idx0 formula and polarization audit."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from vacuum_resonance import (  # noqa: E402
    B_Q_G,
    RHO_COEFF_B12,
    adiabatic_energy,
    ellipticity_branches,
    frozen_literal_adiabatic_energy,
    jump_probability,
    polarization_outcome,
    resonance_density,
    strong_field_f,
)


def outcome_dict(initial_mode: str, adiabatic: bool) -> dict[str, object]:
    row = polarization_outcome(initial_mode, adiabatic=adiabatic)
    return {
        "initial_mode": initial_mode,
        "regime": "adiabatic" if adiabatic else "nonadiabatic",
        "stokes": [row.q_over_i, row.u_over_i, row.v_over_i],
        "rotation_deg": row.rotation_deg,
    }


def build_payload() -> dict[str, object]:
    set_a = resonance_density(7.53e13, 2.37, 1.0, 1.0)
    set_b_f = strong_field_f(1.0e15)
    set_b = resonance_density(1.0e15, 0.83, 0.5, set_b_f)
    set_c = adiabatic_energy(52.0, 2.80)
    set_c_literal = frozen_literal_adiabatic_energy(52.0, 2.80)
    energies = np.array([0.5, 1.0, 2.0, 5.0])
    jumps = jump_probability(energies, set_c)

    rho_v_fig1 = resonance_density(1.0e13, 5.0, 1.0, 1.0)
    sample_rho = np.array([0.15, rho_v_fig1, 0.35])
    k_plus, k_minus, beta = ellipticity_branches(sample_rho)

    return {
        "schema_version": 1,
        "paper_id": "prlb-f37350e-000",
        "source": {
            "title": "Polarized X-Ray Emission from Magnetized Neutron Stars: Signature of Strong-Field Vacuum Polarization",
            "authors": ["Dong Lai", "Wynn C. G. Ho"],
            "arxiv": "astro-ph/0303596",
            "journal": "Phys. Rev. Lett. 91, 071101 (2003)",
            "doi": "10.1103/PhysRevLett.91.071101",
            "contract": "venue_or_date_mismatch",
        },
        "constants": {
            "B_Q_G": B_Q_G,
            "rho_coefficient_B12": RHO_COEFF_B12,
            "rho_coefficient_B14": 0.9640,
            "strong_field_kappa": 5.0,
            "E_ad_coefficient_keV": 2.520,
            "landau_zener_A_exact": "pi/2",
            "landau_zener_p": 3,
        },
        "benchmark_numeric_checks": {
            "R4_set_a_density": set_a,
            "R5_set_b_f": set_b_f,
            "R5_set_b_density": set_b,
            "R7_set_c_correct_E_ad_keV": set_c,
            "R6_literal_frozen_E_ad_keV": set_c_literal,
            "R6_relative_error_if_literal": abs(set_c_literal / set_c - 1.0),
            "R10": [
                {"energy_keV": float(e), "P_jump": float(p)}
                for e, p in zip(energies, jumps, strict=True)
            ],
        },
        "formula_audit": {
            "source_E_ad_height_power": -1.0 / 3.0,
            "frozen_displayed_E_ad_height_power": -1.0,
            "finding": "R6 omits the 1/3 exponent, while R7 and R10 use the source formula.",
        },
        "polarization_identifiability": {
            "frozen_initial_mode_specified": False,
            "high_to_low_density_outcomes": [
                outcome_dict("X", True),
                outcome_dict("O", True),
                outcome_dict("X", False),
                outcome_dict("O", False),
            ],
            "finding": "R11-R12 are conditional on an unstated initial mode; both signs are physically allowed.",
        },
        "paper_figure_1": {
            "parameter_match": "paper_exact",
            "rho_V_g_cm3": rho_v_fig1,
            "sample_density_g_cm3": sample_rho.tolist(),
            "K_plus": k_plus.tolist(),
            "K_minus": k_minus.tolist(),
            "beta": beta.tolist(),
            "invariant_max_abs_K_product_plus_one": float(np.max(np.abs(k_plus * k_minus + 1.0))),
        },
        "verdict": {
            "status": "benchmark_gold_invalid",
            "valid_rubric_ids": ["R1", "R2", "R3", "R4", "R5", "R7", "R8", "R9", "R10"],
            "invalid_rubric_ids": ["R6", "R11", "R12"],
            "valid_points": 9,
            "total_points": 12,
            "paper_figures_reproduced": ["FIG1"],
        },
    }


def main() -> None:
    output = CASE_ROOT / "outputs/data/idx0_gold_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_payload(), indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
