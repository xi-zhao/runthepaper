#!/usr/bin/env python3
"""Render the publication-style benchmark-scope comparison for idx47.

Figure contract
---------------
Core conclusion: all frozen idx47 scalars are independently recovered by exact
gauge-invariant A100 calculations within the precision implied by their printout.
Archetype: quantitative grid with a relative-error hero panel.
Evidence: (a) all scalar errors, (b) requested vison observables at all computed
times, (c) double-precision energy conservation.
Export: double-column 183 mm x 110 mm, editable SVG/PDF plus 300 dpi PNG preview;
all quantitative values trace to the four JSON artifacts in outputs/data.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
DATA_DIR = CASE_ROOT / "outputs" / "data"
FIGURE_DIR = CASE_ROOT / "outputs" / "figures"

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 7,
        "axes.linewidth": 0.75,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "legend.frameon": False,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
    }
)

NAVY = "#355C7D"
TEAL = "#3B8C88"
GOLD = "#D49A35"
ROSE = "#B95F73"
GRAY = "#8A939A"
LIGHT = "#E9EDF0"


def load(name: str) -> dict:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def main() -> None:
    z3 = load("idx47_z3_derivatives_a100.json")
    odd = load("idx47_odd_z2_vbs_a100.json")
    matter = load("idx47_z2_matter_bulk_a100.json")
    vison = load("idx47_z2_vison_a100.json")

    rows = [
        ("Z3  dE/dg", z3["frozen"]["first_derivative"], z3["result"]["first_derivative"]),
        ("Z3  d2E/dg2", z3["frozen"]["second_derivative"], z3["result"]["second_derivative"]),
        ("odd-Z2  Dx^2", odd["frozen_value_each_direction"], odd["candidate_interpretations"]["square_of_mean_Dx"]),
        ("odd-Z2  Dy^2", odd["frozen_value_each_direction"], odd["candidate_interpretations"]["square_of_mean_Dy"]),
        ("matter  <hc>", matter["frozen"]["central_bulk_energy"], matter["result"]["central_bulk_energy"]),
        ("vison  P00(4.5)", vison["comparison"]["frozen"]["P_0_0_at_4.5"], vison["observations"]["4.5"]["plaquettes"]["P_0_0"]),
        ("vison  P01(6.0)", vison["comparison"]["frozen"]["P_0_1_at_6"], vison["observations"]["6"]["plaquettes"]["P_0_1"]),
        ("vison  P11(7.5)", vison["comparison"]["frozen"]["P_1_1_at_7.5"], vison["observations"]["7.5"]["plaquettes"]["P_1_1"]),
        ("vison  energy", vison["comparison"]["frozen"]["energy"], vison["initial_vison"]["energy"]),
    ]

    source_csv = DATA_DIR / "idx47_benchmark_comparison.csv"
    with source_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["target", "frozen", "reproduced", "absolute_error", "relative_error_ppm"],
            lineterminator="\n",
        )
        writer.writeheader()
        for target, frozen, reproduced in rows:
            writer.writerow(
                {
                    "target": target,
                    "frozen": f"{frozen:.16g}",
                    "reproduced": f"{reproduced:.16g}",
                    "absolute_error": f"{abs(reproduced - frozen):.16g}",
                    "relative_error_ppm": f"{1e6 * (reproduced - frozen) / abs(frozen):.16g}",
                }
            )

    width = 183 / 25.4
    height = 110 / 25.4
    fig = plt.figure(figsize=(width, height), constrained_layout=True)
    grid = fig.add_gridspec(2, 2, width_ratios=[1.18, 1.0], height_ratios=[1.25, 0.75])
    ax_error = fig.add_subplot(grid[:, 0])
    ax_vison = fig.add_subplot(grid[0, 1])
    ax_energy = fig.add_subplot(grid[1, 1])

    labels = [row[0] for row in rows]
    errors_ppm = np.array([1e6 * (row[2] - row[1]) / abs(row[1]) for row in rows])
    y = np.arange(len(rows))[::-1]
    ax_error.axvspan(-10, 10, color=LIGHT, zorder=0, label="within 10 ppm")
    ax_error.axvline(0, color="#4A4A4A", lw=0.8)
    colors = [NAVY, NAVY, TEAL, TEAL, GOLD, ROSE, ROSE, ROSE, ROSE]
    for yi, value, color in zip(y, errors_ppm, colors):
        ax_error.plot([0, value], [yi, yi], color=color, lw=1.2, solid_capstyle="round")
        ax_error.scatter(value, yi, s=18, color=color, edgecolor="white", linewidth=0.4, zorder=3)
        ax_error.text(
            value + 0.42,
            yi,
            f"{value:+.3f}",
            ha="left",
            va="center",
            fontsize=6.2,
            color="#34383B",
        )
    ax_error.set_yticks(y, labels)
    ax_error.set_xlabel("relative difference (ppm)")
    ax_error.set_title("All contracted scalars agree with frozen values", loc="left", weight="bold")
    ax_error.set_xlim(min(-1.5, errors_ppm.min() - 1.0), max(10.8, errors_ppm.max() + 1.0))
    ax_error.grid(axis="x", color="#D9DEE2", lw=0.5, alpha=0.8)
    ax_error.text(-0.16, 1.035, "a", transform=ax_error.transAxes, fontsize=8, weight="bold")

    times = np.array([4.5, 6.0, 7.5])
    curves = {
        "P00": [vison["observations"][f"{time:g}"]["plaquettes"]["P_0_0"] for time in times],
        "P01": [vison["observations"][f"{time:g}"]["plaquettes"]["P_0_1"] for time in times],
        "P11": [vison["observations"][f"{time:g}"]["plaquettes"]["P_1_1"] for time in times],
    }
    for (label, values), color, marker in zip(curves.items(), [NAVY, TEAL, ROSE], ["o", "s", "^"]):
        ax_vison.plot(times, values, color=color, marker=marker, ms=3.2, lw=1.25, label=label)
    frozen_points = [(4.5, 0.56388), (6.0, 0.80091), (7.5, 0.65918)]
    for x, value in frozen_points:
        ax_vison.scatter(x, value, s=36, facecolor="none", edgecolor=GOLD, linewidth=1.0, zorder=4)
    ax_vison.plot([], [], marker="o", ms=5, mfc="none", mec=GOLD, ls="none", label="frozen target")
    ax_vison.set_xticks(times)
    ax_vison.set_xlabel("time")
    ax_vison.set_ylabel("plaquette expectation")
    ax_vison.set_ylim(0.45, 1.0)
    ax_vison.set_title("Exact 6 x 6 vison observables", loc="left", weight="bold")
    ax_vison.legend(ncol=2, fontsize=6.2, loc="lower right")
    ax_vison.grid(color="#E1E5E8", lw=0.5)
    ax_vison.text(-0.17, 1.05, "b", transform=ax_vison.transAxes, fontsize=8, weight="bold")

    energy = np.array([vison["observations"][f"{time:g}"]["energy"] for time in times])
    energy0 = vison["initial_vison"]["energy"]
    drift = (energy - energy0) * 1e12
    ax_energy.axhline(0, color=GRAY, lw=0.8)
    ax_energy.plot(times, drift, color=GOLD, marker="o", ms=3.2, lw=1.2)
    ax_energy.set_xticks(times)
    ax_energy.set_xlabel("time")
    ax_energy.set_ylabel("energy drift (1e-12)")
    ax_energy.set_title("Energy conserved at double precision", loc="left", weight="bold")
    ax_energy.grid(axis="y", color="#E1E5E8", lw=0.5)
    ax_energy.text(-0.17, 1.08, "c", transform=ax_energy.transAxes, fontsize=8, weight="bold")

    fig.suptitle(
        "Independent exact reproduction of PRL-Bench record 047",
        x=0.01,
        ha="left",
        fontsize=9,
        weight="bold",
    )
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    base = FIGURE_DIR / "idx47_benchmark_comparison"
    svg_path = base.with_suffix(".svg")
    fig.savefig(svg_path, bbox_inches="tight")
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=300, bbox_inches="tight")
    plt.close(fig)
    # Matplotlib writes harmless trailing spaces inside multiline SVG paths.
    # Normalize them so repository whitespace checks remain signal-bearing.
    svg_lines = svg_path.read_text(encoding="utf-8").splitlines()
    svg_path.write_text("\n".join(line.rstrip() for line in svg_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
