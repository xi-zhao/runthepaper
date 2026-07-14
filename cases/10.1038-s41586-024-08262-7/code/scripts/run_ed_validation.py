#!/usr/bin/env python3
"""Exact-diagonalize the 1D solvable spin model and check it is free paraparticles.

Validates the paper's central physical claim (free paraparticles emerge as
quasiparticle excitations) and, as a by-product, the single-mode partition
function z_R(x)=1+m x that Fig. 2 rests on.  Writes a JSON check.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))
from spin_model_1d import (  # noqa: E402
    build_hamiltonian,
    free_paraparticle_spectrum,
    number_operator,
    single_particle_matrix,
)

OUT = Path(__file__).resolve().parents[2] / "outputs" / "checks"


def run_case(N: int, m: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    J = rng.uniform(0.5, 1.5, size=N)
    J[-1] = 0.0  # open boundary
    mu = rng.uniform(-1.0, 1.0, size=N)

    H = build_hamiltonian(J, mu, m)
    Nop = number_operator(m, N)
    commutator = float(np.max(np.abs(H @ Nop - Nop @ H)))

    ed_spectrum = np.sort(np.linalg.eigvalsh(H))
    eps = np.linalg.eigvalsh(single_particle_matrix(J, mu))
    pred_spectrum = free_paraparticle_spectrum(eps, m)

    same_dim = ed_spectrum.size == pred_spectrum.size == (m + 1) ** N
    max_dev = float(np.max(np.abs(ed_spectrum - pred_spectrum))) if same_dim else float("inf")

    return {
        "N": N,
        "m": m,
        "seed": seed,
        "hilbert_dim": (m + 1) ** N,
        "single_particle_levels": [round(float(e), 8) for e in np.sort(eps)],
        "commutator_H_n_maxabs": commutator,
        "spectrum_dim_match": bool(same_dim),
        "max_spectrum_deviation": max_dev,
        "passed": bool(same_dim and max_dev < 1e-9 and commutator < 1e-10),
    }


def main() -> int:
    cases = [
        run_case(N=4, m=2, seed=1),
        run_case(N=5, m=2, seed=7),
        run_case(N=4, m=3, seed=3),
    ]
    result = {
        "target": "ed_validation_1d_solvable_model",
        "claim": "1D spin model (Ex.3) spectrum == free-paraparticle spectrum "
        "sum_{k in S} eps_k with multiplicity m^{|S|}; verifies z_R(x)=1+m x.",
        "tol_spectrum": 1e-9,
        "cases": cases,
        "all_passed": all(c["passed"] for c in cases),
    }
    result["status"] = "passed" if result["all_passed"] else "failed"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ed_validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
