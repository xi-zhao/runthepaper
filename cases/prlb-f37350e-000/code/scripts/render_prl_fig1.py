#!/usr/bin/env python3
"""Independently render the data and layout of Lai--Ho PRL Fig. 1."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from matplotlib.ticker import AutoMinorLocator


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from vacuum_resonance import ellipticity_branches  # noqa: E402


def add_ellipse(ax: plt.Axes, x: float, y: float, w: float, h: float, color: str) -> None:
    ax.add_patch(Ellipse((x, y), width=w, height=h, fill=False, lw=1.7, ec=color))
    ax.plot([x, x + 0.18 * w], [y + 0.05 * h, y + 0.32 * h], color=color, lw=1.2)
    ax.plot([x + 0.18 * w, x + 0.10 * w], [y + 0.32 * h, y + 0.25 * h], color=color, lw=1.2)


def main() -> None:
    rho = np.linspace(0.12, 0.38, 1000)
    k_plus, k_minus, _ = ellipticity_branches(rho)

    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "stix",
        "font.size": 8,
        "axes.linewidth": 0.8,
    })
    fig = plt.figure(figsize=(3.3, 3.2), dpi=100)
    ax = fig.add_axes([0.06, 0.05, 0.87, 0.91])
    ax.plot(rho, k_plus, color="black", lw=0.8)
    ax.plot(rho, k_minus, color="black", lw=0.8, ls=(0, (8, 3)))
    ax.set_xlim(0.12, 0.38)
    ax.set_ylim(-8.8, 8.0)
    ax.set_xticks([0.15, 0.20, 0.25, 0.30, 0.35])
    ax.set_xticklabels(["0.15", "0.2", "0.25", "0.3", "0.35"])
    ax.set_yticks([-5, 0, 5])
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.tick_params(which="major", direction="in", top=True, right=True, length=4, width=0.7, pad=2)
    ax.tick_params(which="minor", direction="in", top=True, right=True, length=2.2, width=0.6)
    ax.set_xlabel(r"$\rho$ (g/cm$^3$)", labelpad=1)
    ax.set_ylabel(r"$K=-iE_x/E_y$", labelpad=1)

    ax.text(0.258, 0.8, r"$K_+$", color="black")
    ax.text(0.215, -1.45, r"$K_-$", color="black")
    ax.text(0.127, -0.75, "X-mode", color="red")
    ax.text(0.325, -0.05, "X-mode", color="red")
    ax.text(0.128, -6.55, "O-mode", color="blue")
    ax.text(0.324, 3.05, "O-mode", color="blue")

    add_ellipse(ax, 0.145, 2.15, 0.015, 2.9, "red")
    add_ellipse(ax, 0.315, 6.0, 0.048, 1.0, "blue")
    add_ellipse(ax, 0.215, 2.25, 0.032, 2.0, "#00aa22")
    add_ellipse(ax, 0.25, -2.9, 0.031, 2.0, "#00aa22")
    add_ellipse(ax, 0.35, -2.45, 0.015, 2.9, "red")
    add_ellipse(ax, 0.20, -7.05, 0.048, 1.0, "blue")

    out = CASE_ROOT / "outputs/figures"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "prl_fig1_reproduced.png", dpi=100, facecolor="white")
    fig.savefig(out / "prl_fig1_reproduced.pdf", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
