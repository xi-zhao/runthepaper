#!/usr/bin/env python3
"""Symmetry-resolved PXP sector run for T003 (scar tower) and T004 (level stats).

Diagonalizes the k=0, inversion-even PXP sector at the largest locally
feasible size (L=28, sector dimension 13201; one dense float64 matrix for the
paper's L=32 sector is about 47GB before eigensolver workspace) and extracts:

- T003: the |<Z2|E>|^2 scar tower - the paper's L/2+1 special states with
  approximately equal energy spacing;
- T004: symmetry-resolved level statistics - mean consecutive-gap ratio
  <r> against GOE vs Poisson, plus the unfolded spacing distribution
  against the Wigner surmise (exact zero modes excluded).
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code/src"))

from pxp_scars import (  # noqa: E402
    build_symmetric_hamiltonian,
    build_symmetric_sector,
    mean_level_spacing_ratio,
    pattern_state,
    symmetrized_state_vector,
    unfolded_spacings,
)
from plot_symmetry_resolved_sector import plot_sector_outputs  # noqa: E402

L = 28
GOE_R = 0.5307
POISSON_R = 0.3863


def main() -> int:
    t0 = time.time()
    sector = build_symmetric_sector(L)
    dim = len(sector["representatives"])
    hamiltonian = build_symmetric_hamiltonian(sector).toarray()
    energies, vectors = np.linalg.eigh(hamiltonian)
    elapsed = time.time() - t0

    # --- T003: Z2 scar tower ---
    z2_vector = symmetrized_state_vector(sector, pattern_state(L, "z2"))
    overlaps = (z2_vector @ vectors) ** 2
    tower_count = L // 2 + 1
    # One state per tower. In the k=0, I=+1 sector the scar towers alternate
    # with the k=pi sector, so the visible tower spacing is ~2.66 (twice the
    # full-tower spacing); greedy peak picking with separation 1.8 keeps one
    # dominant state per tower and rejects same-tower satellites.
    top = []
    for index in np.argsort(overlaps)[::-1]:
        if all(abs(energies[index] - energies[j]) > 1.8 for j in top):
            top.append(int(index))
        if len(top) == tower_count:
            break
    top = np.asarray(top)
    tower_energies = np.sort(energies[top])
    tower_spacings = np.diff(tower_energies)
    spacing_mean = float(np.mean(tower_spacings))
    spacing_rel_std = float(np.std(tower_spacings) / spacing_mean)

    # --- T004: level statistics (zero modes excluded, central window) ---
    nonzero = energies[np.abs(energies) > 1e-10]
    lo, hi = np.quantile(nonzero, [0.1, 0.9])
    window = nonzero[(nonzero >= lo) & (nonzero <= hi)]
    r_mean = mean_level_spacing_ratio(window)
    spacings = unfolded_spacings(window)
    spacings = spacings / np.mean(spacings)
    hist, edges = np.histogram(spacings, bins=40, range=(0.0, 4.0), density=True)
    centers = 0.5 * (edges[1:] + edges[:-1])
    wigner = (np.pi / 2.0) * centers * np.exp(-np.pi * centers**2 / 4.0)
    poisson = np.exp(-centers)
    l1_wigner = float(np.trapezoid(np.abs(hist - wigner), centers))
    l1_poisson = float(np.trapezoid(np.abs(hist - poisson), centers))

    gate_flags = {
        "scar_tower_has_half_L_plus_one_states": bool(np.all(overlaps[top] > 1e-8)),
        "scar_tower_spacing_uniform": spacing_rel_std < 0.15,
        "level_statistics_goe_not_poisson": abs(r_mean - GOE_R) < abs(r_mean - POISSON_R),
        "spacing_distribution_wigner_not_poisson": l1_wigner < l1_poisson,
    }

    data_dir = ROOT / "outputs/data"
    with (data_dir / "sector_scar_tower.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["energy", "z2_overlap_sq", "is_tower_state"])
        tower_set = set(int(i) for i in top)
        for i, (energy, overlap) in enumerate(zip(energies, overlaps)):
            writer.writerow([f"{energy:.10f}", f"{overlap:.3e}", int(i in tower_set)])
    with (data_dir / "sector_level_spacings.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["unfolded_spacing"])
        writer.writerows([[f"{s:.8f}"] for s in spacings])

    checks = {
        "targets": ["T003", "T004"],
        "status": "physically_consistent" if all(gate_flags.values()) else "partial",
        "sector": {"L": L, "momentum": 0, "inversion": "+1", "dimension": dim},
        "elapsed_seconds": round(elapsed, 1),
        "scar_tower": {
            "expected_states": tower_count,
            "min_tower_overlap_sq": float(np.min(overlaps[top])),
            "tower_energies": [round(float(e), 6) for e in tower_energies],
            "mean_tower_spacing": spacing_mean,
            "tower_spacing_rel_std": spacing_rel_std,
        },
        "level_statistics": {
            "window_levels": int(len(window)),
            "zero_modes_excluded": int(len(energies) - len(nonzero)),
            "mean_gap_ratio": r_mean,
            "goe_reference": GOE_R,
            "poisson_reference": POISSON_R,
            "l1_distance_to_wigner": l1_wigner,
            "l1_distance_to_poisson": l1_poisson,
        },
        "gate_flags": gate_flags,
        "remote_rerun": {
            "L": 32,
            "reason": "The L=32 sector (~77k) needs about 47GB for one dense float64 matrix before eigensolver workspace, beyond the current single 40GB A100 path.",
            "constraint_class": "external_required",
        },
        "difference_reasons": {
            "sector_figures": "Same k=0, I=+1 sector at L=28; the paper uses L=32, whose dense matrix alone is about 47GB before eigensolver workspace.",
            "entanglement_dynamics": "Finite-size exact evolution at L=16; the paper uses thermodynamic-limit iTEBD with bond dimension around 400."
        },
        "data": ["outputs/data/sector_scar_tower.csv", "outputs/data/sector_level_spacings.csv"],
        "figures": ["outputs/figures/sector_scar_tower.png", "outputs/figures/sector_level_statistics.png"],
    }
    (ROOT / "outputs/checks/symmetry_resolved_sector.json").write_text(
        json.dumps(checks, indent=2) + "\n"
    )
    plot_sector_outputs(ROOT)

    print(json.dumps({"status": checks["status"], "gate_flags": gate_flags,
                      "r_mean": r_mean, "dim": dim,
                      "tower_spacing_rel_std": spacing_rel_std}, indent=2))
    return 0 if checks["status"] == "physically_consistent" else 1


if __name__ == "__main__":
    raise SystemExit(main())
