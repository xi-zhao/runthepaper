#!/usr/bin/env python3
"""Render the independent frozen-gold and source-lineage audit for idx8."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"


def main() -> None:
    audit = json.loads(
        (CASE_ROOT / "outputs/data/idx8_gold_audit.json").read_text(encoding="utf-8")
    )
    gold = audit["gold_audit"]

    labels = [r"$\gamma_0$", r"$a_{\rm res}$ [AU]", r"$e_{\rm peak}$"]
    computed = np.array(
        [gold["task_4"]["gamma0"], gold["task_5"]["a_in_res_au"], gold["task_6"]["peak"]]
    )
    frozen = np.array([0.648, 0.381, 0.082])

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.3), constrained_layout=True)
    ax = axes[0]
    x = np.arange(len(labels))
    ax.plot(x, computed, "o", ms=9, color="#1769aa", label="independent")
    ax.plot(x, frozen, "x", ms=9, mew=2, color="#d32f2f", label="frozen (3 d.p.)")
    for index, value in enumerate(computed):
        ax.annotate(f"{value:.9f}", (index, value), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=8)
    ax.set_xticks(x, labels)
    ax.set_ylim(0.0, 0.72)
    ax.set_ylabel("value")
    ax.set_title("All frozen scalar answers survive")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, loc="upper right")

    ax = axes[1]
    ax.axis("off")
    ax.set_title("Source contract does not", pad=12)
    rows = [
        ("Formula source", "PRL 132, 231403 (2024)", "outside window"),
        ("In-window candidate", "ApJL 2025 / 2509.20806", "not PRL"),
        (r"Rate ratio", r"$\gamma_{\rm PRL}=\dot\varpi_{\rm in}/\dot\varpi_{\rm out}$", "reciprocal"),
        ("Frozen tasks", "7 / 7 independently valid", "gold valid"),
    ]
    table = ax.table(
        cellText=rows,
        colLabels=["check", "evidence", "verdict"],
        cellLoc="left",
        colLoc="left",
        loc="center",
        colWidths=[0.29, 0.48, 0.23],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.0)
    table.scale(1.0, 1.8)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("#d0d0d0")
        if row == 0:
            cell.set_facecolor("#e8eef7")
            cell.set_text_props(weight="bold")

    out = CASE_ROOT / "outputs/figures"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "idx8_source_gold_audit.png", dpi=220, bbox_inches="tight")
    fig.savefig(out / "idx8_source_gold_audit.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
