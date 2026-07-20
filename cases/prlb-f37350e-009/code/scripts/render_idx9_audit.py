#!/usr/bin/env python3
"""Render a compact visual summary of the idx9 gold audit."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"


def main() -> None:
    audit = json.loads(
        (CASE_ROOT / "outputs/data/idx9_gold_audit.json").read_text(encoding="utf-8")
    )["gold_audit"]
    beta = np.linspace(-3.8, 3.0, 1200)
    scalar = (beta + 7.0) / (3.0 * (beta + 1.0))
    frozen = 3.0 * (beta + 1.0) / (beta + 7.0)
    mask = np.abs(beta + 1.0) > 0.06

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.4), constrained_layout=True)
    ax = axes[0]
    ax.plot(beta[mask], scalar[mask], color="#1769aa", lw=2.0, label="derived scalar p/rho")
    ax.plot(beta[mask], frozen[mask], color="#d32f2f", lw=1.6, ls="--", label="frozen reciprocal")
    ax.axhline(1.0, color="#555555", lw=0.8)
    ax.axhline(-1.0, color="#555555", lw=0.8)
    ax.scatter([2.0, -2.5], [1.0, -1.0], color="#1769aa", zorder=3)
    ax.set_xlim(-3.8, 3.0)
    ax.set_ylim(-4.0, 4.0)
    ax.set_xlabel(r"power-law parameter $\beta$")
    ax.set_ylabel(r"$w_{\rm eff}$")
    ax.set_title("Frozen scalar ratio is inverted")
    ax.grid(alpha=0.2)
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax = axes[1]
    ax.axis("off")
    rows = [
        ("T1", "valid", "exact n_t-epsilon identity"),
        ("T2", "valid", "finite a'' jump -> |beta_k|^2 ~ k^-4"),
        ("T3.1", "error", "pressure mislabeled rho"),
        ("T3.2", "invalid", "counterterms contradict valid WKB amplitude"),
        ("T3.3", "incomplete", "rho_re and p_re not supplied"),
        ("T3.4", "invalid", f"RGW w(-2)={audit['task_3_4_rgw']['actual_at_beta_minus_2']:.3f}"),
    ]
    table = ax.table(
        cellText=rows,
        colLabels=["task", "status", "independent finding"],
        cellLoc="left",
        colLoc="left",
        loc="center",
        colWidths=[0.15, 0.19, 0.66],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.2)
    table.scale(1.0, 1.75)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("#d0d0d0")
        if row == 0:
            cell.set_facecolor("#e8eef7")
            cell.set_text_props(weight="bold")
    ax.set_title("Frozen benchmark audit", pad=12)

    output = CASE_ROOT / "outputs/figures"
    output.mkdir(parents=True, exist_ok=True)
    fig.savefig(output / "idx9_gold_audit.png", dpi=220, bbox_inches="tight")
    fig.savefig(output / "idx9_gold_audit.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
