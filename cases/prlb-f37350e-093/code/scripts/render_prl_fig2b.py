#!/usr/bin/env python3
"""Reconstruct the deterministic free-energy curves of PRL Fig. 2B."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from spex_audit import free_energy_x0  # noqa: E402


def main() -> None:
    x = np.linspace(-3.0, 3.0, 401)
    barriers = np.arange(2.0, 16.0)
    curves = {float(a): free_energy_x0(x, float(a), n_y=8001) for a in barriers}

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.linewidth": 1.5})
    fig, ax = plt.subplots(figsize=(4.0, 4.35), dpi=180)
    colors = plt.cm.Blues(np.linspace(0.18, 0.95, len(barriers)))
    for color, a in zip(colors, barriers, strict=True):
        ax.plot(x, curves[float(a)], color=color, lw=1.0)
    ax.set(xlim=(-3.2, 3.2), ylim=(-2, 42), xlabel=r"$x^{(0)}$", ylabel=r"$A[x^{(0)}]$ [$k_{\rm B}T$]")
    ax.set_xticks([-3, 0, 3])
    ax.set_yticks([0, 10, 20, 30, 40])
    ax.tick_params(direction="out", length=5, width=1.3)
    ax.text(-3.0, 39.5, "B", fontsize=28, va="top")
    ax.text(-1.45, 33.5, r"$A_{\rm barrier}$ [$k_{\rm B}T$]", fontsize=11)
    gradient = np.linspace(0, 1, 256)[None, :]
    inset = ax.inset_axes([0.25, 0.68, 0.55, 0.045])
    inset.imshow(gradient, aspect="auto", cmap="Blues", extent=(0, 15, 0, 1), origin="lower")
    inset.set(xticks=[0, 7.5, 15], yticks=[])
    inset.tick_params(length=5, width=1.2)
    for spine in inset.spines.values():
        spine.set_linewidth(1.3)
    ax.text(-2.15, 5.2, "A", fontsize=15, ha="center", va="center", bbox={"boxstyle": "circle,pad=0.2", "fc": "white", "ec": "black", "lw": 1.2})
    ax.text(2.15, 5.2, "B", fontsize=15, ha="center", va="center", bbox={"boxstyle": "circle,pad=0.2", "fc": "white", "ec": "black", "lw": 1.2})

    out = CASE_ROOT / "outputs/figures"
    out.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / "prl_fig2b_reproduced.png", dpi=180, facecolor="white")
    fig.savefig(out / "prl_fig2b_reproduced.pdf", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
