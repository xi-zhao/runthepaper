#!/usr/bin/env python3
"""Render an equation-level comparison of the source and frozen selection rules."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from mi_wedge_audit import (  # noqa: E402
    background_terms,
    frozen_claimed_speed,
    frozen_growth_derivative,
    source_edge_speed,
    source_group_velocity,
    stationarity,
)


def main() -> None:
    x_star = brentq(stationarity, 0.4, 0.6, xtol=1e-15)
    s_star = float(background_terms(x_star)[2])
    root_s = np.sqrt(s_star)

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.25), constrained_layout=True)
    ax = axes[0]
    ku = np.linspace(0.001, 0.9999, 700) * root_s
    ks = np.linspace(np.sqrt(2.0) + 0.005, 2.6, 900) * root_s
    ax.plot(ku / root_s, frozen_growth_derivative(ku, s_star) / root_s, color="#D55E00", lw=2.0, label=r"frozen: $d\gamma/dk$")
    ax.plot(ks / root_s, source_group_velocity(ks, s_star) / root_s, color="#0072B2", lw=2.0, label=r"PRL: $d\omega/dk$")
    ax.axvline(np.sqrt(2.0), color="0.45", ls="--", lw=1.0, label=r"$k_{\max}$")
    ax.scatter([np.sqrt(3.0)], [4.0], color="#0072B2", zorder=4)
    ax.annotate("source minimum", (np.sqrt(3.0), 4.0), xytext=(1.85, 5.25), arrowprops={"arrowstyle": "->", "lw": 0.9}, fontsize=8)
    ax.annotate("infimum 0\n(no minimum)", (1.0, 0.0), xytext=(0.45, 1.25), arrowprops={"arrowstyle": "->", "lw": 0.9}, fontsize=8)
    ax.set(xlabel=r"$k/\sqrt{S}$", ylabel=r"velocity $/\sqrt{S}$", xlim=(0, 2.6), ylim=(0, 8.0))
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    ax.text(0.02, 0.96, "a", transform=ax.transAxes, va="top", fontweight="bold")

    ax = axes[1]
    x = np.linspace(0.0, 1.0, 800)
    s = np.maximum(background_terms(x)[2], 0.0)
    source = 4.0 * np.sqrt(s)
    frozen = 4.0 / np.sqrt(3.0) * np.sqrt(s)
    ax.plot(x, source, color="#0072B2", lw=2.2, label="PRL stable-branch speed")
    ax.plot(x, frozen, color="#D55E00", lw=1.8, ls="--", label="frozen claimed formula")
    ax.axvline(x_star, color="0.45", lw=1.0, ls=":")
    ax.scatter([x_star], [source_edge_speed(s_star)], color="#0072B2", zorder=4)
    ax.scatter([x_star], [frozen_claimed_speed(s_star)], color="#D55E00", zorder=4)
    ax.set(xlabel=r"population fraction $x=Q_2^2$", ylabel="edge-speed proxy", xlim=(0, 1), ylim=(0, 0.48))
    ax.legend(frameon=False, fontsize=7.5, loc="lower center")
    ax.text(0.02, 0.96, "b", transform=ax.transAxes, va="top", fontweight="bold")

    for axis in axes:
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.tick_params(direction="out")

    out = CASE_ROOT / "outputs/figures"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "idx40_selection_rule_audit.png", dpi=240, bbox_inches="tight")
    fig.savefig(out / "idx40_selection_rule_audit.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
