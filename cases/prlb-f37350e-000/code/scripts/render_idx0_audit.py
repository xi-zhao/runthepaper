#!/usr/bin/env python3
"""Render a compact diagnostic for the frozen-gold audit."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from vacuum_resonance import (  # noqa: E402
    adiabatic_energy,
    frozen_literal_adiabatic_energy,
    jump_probability,
)


def main() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 9,
        "axes.linewidth": 0.8,
        "legend.fontsize": 7,
    })
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), constrained_layout=True)

    h = np.geomspace(0.4, 12.0, 300)
    correct = np.array([adiabatic_energy(52.0, x) for x in h])
    frozen = np.array([frozen_literal_adiabatic_energy(52.0, x) for x in h])
    axes[0].loglog(h, correct, lw=1.8, label=r"source: $H_\rho^{-1/3}$")
    axes[0].loglog(h, frozen, lw=1.5, ls="--", label=r"frozen R6: $H_\rho^{-1}$")
    axes[0].scatter([2.8], [adiabatic_energy(52.0, 2.8)], s=24, color="black", zorder=3)
    axes[0].set(xlabel=r"$H_\rho$ (cm)", ylabel=r"$E_{\rm ad}$ (keV)", title="a  Scale-height exponent")
    axes[0].legend(frameon=False)

    e_ad = adiabatic_energy(52.0, 2.8)
    energy = np.linspace(0, 5.3, 400)
    axes[1].semilogy(energy, jump_probability(energy, e_ad), color="#b2182b", lw=1.8)
    sample = np.array([0.5, 1.0, 2.0, 5.0])
    axes[1].scatter(sample, jump_probability(sample, e_ad), color="black", s=18, zorder=3)
    axes[1].axvline(e_ad, color="0.5", lw=0.8, ls=":")
    axes[1].set(xlabel="Photon energy (keV)", ylabel=r"$P_{\rm jump}$", title="b  Landau–Zener table", ylim=(1e-10, 1.2))

    out = CASE_ROOT / "outputs/figures"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "idx0_gold_audit.png", dpi=220, facecolor="white")
    fig.savefig(out / "idx0_gold_audit.pdf", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
