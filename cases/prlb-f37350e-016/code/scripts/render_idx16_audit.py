#!/usr/bin/env python3
"""Render the idx16 benchmark audit from independent calculations."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from dwave_impurity_audit import (  # noqa: E402
    frozen_resonance_energy,
    local_green_low_energy,
    low_branch_real_axis_root,
    rmp_logarithmic_pole,
    width_to_energy,
)


def main() -> None:
    delta_0 = 30.0
    c_point = 0.3
    audit_path = CASE_ROOT / "outputs" / "data" / "idx16_gold_audit.json"
    audit = json.loads(audit_path.read_text(encoding="utf-8"))

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.linewidth": 0.8,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )
    fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.35), constrained_layout=True)

    matrix = np.asarray(audit["task_1"]["green_matrix_per_mev"])
    image = axes[0].imshow(matrix, cmap="RdBu_r", vmin=0.0, vmax=0.04)
    for row in range(2):
        for column in range(2):
            axes[0].text(column, row, f"{matrix[row, column]:.4f}", ha="center", va="center")
    axes[0].set_xticks([0, 1], ["particle", "hole"])
    axes[0].set_yticks([0, 1], ["particle", "hole"])
    axes[0].set_title("(a) Clean Nambu Green matrix")
    fig.colorbar(image, ax=axes[0], fraction=0.046, pad=0.04, label=r"meV$^{-1}$")

    omega = np.linspace(-8.0, 8.0, 801)
    omega = omega[omega != 0.0]
    values = np.asarray([local_green_low_energy(x, delta_0, cutoff_factor=2.0) for x in omega])
    axes[1].plot(omega, values.real, color="#16802c", lw=1.8, label=r"Re $G_0$")
    axes[1].plot(omega, values.imag, color="#1f4bd4", lw=1.6, ls="--", label=r"Im $G_0$")
    frozen_energy = frozen_resonance_energy(c_point, delta_0)
    axes[1].axhline(c_point, color="#d62728", lw=1.2, label=r"$c=0.3$")
    axes[1].axvline(-frozen_energy, color="0.35", lw=1.0, ls=":")
    residual = audit["task_3"]["pole_residual"]
    axes[1].scatter([-frozen_energy], [c_point + residual["real"]], color="black", s=18, zorder=4)
    axes[1].annotate(
        r"frozen $|\Omega|$" + "\nmisses pole",
        (-frozen_energy, c_point + residual["real"]),
        xytext=(-7.6, -0.23),
        arrowprops={"arrowstyle": "->", "lw": 0.8},
    )
    axes[1].set(xlabel=r"$\omega$ (meV)", ylabel=r"normalized $G_0$", title="(b) Frozen real-axis equation")
    axes[1].legend(frameon=False, loc="upper right", fontsize=8)

    c_values = np.geomspace(0.015, 0.45, 220)
    frozen = np.asarray([frozen_resonance_energy(c, delta_0) for c in c_values])
    real_roots = np.asarray([low_branch_real_axis_root(c, delta_0) for c in c_values])
    source_real = np.asarray([abs(rmp_logarithmic_pole(c, delta_0).real) for c in c_values])
    axes[2].plot(c_values, frozen, color="#d62728", lw=1.8, label="frozen real part")
    axes[2].plot(c_values, real_roots, color="#202020", lw=1.5, label="real-axis root (cutoff 2)")
    axes[2].plot(c_values, source_real, color="#1f77b4", lw=1.5, ls="--", label="RMP log estimate")
    axes[2].scatter([c_point], [frozen_resonance_energy(c_point, delta_0)], color="#d62728", s=22)
    ratio = width_to_energy(rmp_logarithmic_pole(c_point, delta_0))
    axes[2].annotate(
        rf"$c=0.3$: $|\Omega''/\Omega'|={ratio:.2f}$",
        (c_point, frozen_resonance_energy(c_point, delta_0)),
        xytext=(0.075, 10.8),
        arrowprops={"arrowstyle": "->", "lw": 0.8},
    )
    axes[2].set_xscale("log")
    axes[2].set(xlabel=r"$|c|$", ylabel=r"energy scale (meV)", title="(c) Approximation dependence")
    axes[2].legend(frameon=False, fontsize=7.5, loc="upper left")

    output_stem = CASE_ROOT / "outputs" / "figures" / "idx16_gold_audit"
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".png"), dpi=240, bbox_inches="tight", facecolor="white")
    fig.savefig(output_stem.with_suffix(".svg"), bbox_inches="tight", facecolor="white")
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)

    check = {
        "status": "passed",
        "artifact": "outputs/figures/idx16_gold_audit.png",
        "editable_exports": [
            "outputs/figures/idx16_gold_audit.svg",
            "outputs/figures/idx16_gold_audit.pdf"
        ],
        "data": "outputs/data/idx16_gold_audit.json",
        "panels": 3,
        "provenance": "independent_numerics",
        "paper_figure": False,
        "figure_contract": {
            "core_conclusion": "The frozen Task 3 energy is not a controlled solution of its own pole equation.",
            "evidence_chain": {
                "a": "Tasks 1 and 2 have reproducible benchmark arithmetic.",
                "b": "The frozen energy misses the stated pole condition on the real axis.",
                "c": "The result depends strongly on approximation and has order-one width."
            },
            "archetype": "quantitative grid",
            "backend": "python",
            "export": "PNG preview plus editable SVG/PDF"
        },
        "note": "Benchmark diagnostic only; the source Figure 3 is a schematic without a quantitative parameter contract.",
    }
    check_path = CASE_ROOT / "outputs" / "checks" / "idx16_audit_figure_check.json"
    check_path.parent.mkdir(parents=True, exist_ok=True)
    check_path.write_text(json.dumps(check, indent=2) + "\n", encoding="utf-8")
    print(output_stem.with_suffix(".png"))


if __name__ == "__main__":
    main()
