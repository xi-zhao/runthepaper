#!/usr/bin/env python3
"""Regenerate Fig. 2 of Wang, Zhang, and Chen, PRD 94, 044033."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from power_law_audit import fig2_running, fig2_tensor_index  # noqa: E402


def main() -> None:
    x = np.linspace(0.0, 3.0, 3001)
    tensor_index = np.array([fig2_tensor_index(value) for value in x])
    running = np.array([fig2_running(value) for value in x])

    with plt.rc_context(
        {
            "font.family": "serif",
            "font.size": 12,
            "axes.labelsize": 19,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
        }
    ):
        fig, ax = plt.subplots(figsize=(6.4, 4.8), constrained_layout=True)
        ax.plot(x, tensor_index, color="#0000cc", lw=1.55)
        ax.plot(x, running, color="#990000", lw=1.25, ls=(0, (5.0, 4.0)))
        ax.set_xlim(0.0, 3.2)
        ax.set_ylim(0.0, 2.0)
        ax.set_xticks([0, 1, 2, 3])
        ax.set_yticks(np.arange(0.0, 2.01, 0.2))
        ax.grid(color="#b8b8b8", linewidth=0.55)
        ax.set_xlabel(r"$|k\tau|$")
        ax.set_ylabel("spectral  indices", labelpad=12)
        ax.text(1.60, 1.82, r"$\mathrm{n}_{\mathrm{t}}$", color="#0000ff", fontsize=24)
        ax.text(1.78, 0.96, r"$\alpha_{\mathrm{t}}$", color="#990000", fontsize=21)
        ax.tick_params(direction="out", width=1.0, length=5.0)
        for spine in ax.spines.values():
            spine.set_linewidth(0.8)

        output = CASE_ROOT / "outputs/figures"
        output.mkdir(parents=True, exist_ok=True)
        fig.savefig(output / "rgw_fig2_reproduced.png", dpi=220, bbox_inches="tight")
        fig.savefig(output / "rgw_fig2_reproduced.pdf", bbox_inches="tight")
        plt.close(fig)


if __name__ == "__main__":
    main()
