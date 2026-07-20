#!/usr/bin/env python3
"""Independently regenerate Supplemental Fig. C of PRL 132, 231403."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from secular_resonance import phase_curve, source_figc_beta  # noqa: E402


def main() -> None:
    beta = source_figc_beta()
    phi = np.linspace(-math.pi, math.pi, 5001)
    fig, ax = plt.subplots(figsize=(5.2, 5.0), constrained_layout=True)

    blue = phase_curve(phi, beta, 0.02, 1)
    ax.plot(phi, blue, color="#0000ff", lw=2.1)

    separatrix = np.maximum(beta * np.cos(phi), 0.0)
    ax.plot(phi, separatrix, color="black", lw=2.1)

    red_plus = phase_curve(phi, beta, -0.002, 1)
    red_minus = phase_curve(phi, beta, -0.002, -1)
    ax.plot(phi, red_plus, color="#ff0000", lw=2.1)
    ax.plot(phi, red_minus, color="#ff0000", lw=2.1)

    ax.set_xlim(-math.pi, math.pi)
    ax.set_ylim(-0.01, 0.30)
    ax.set_xticks([-math.pi, -math.pi / 2, 0, math.pi / 2, math.pi], [r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    ax.set_xlabel(r"$\Delta\varpi$ [Rad]")
    ax.set_ylabel(r"$e_{\rm out}$")
    ax.tick_params(direction="in", top=True, right=True)
    for spine in ax.spines.values():
        spine.set_linewidth(1.2)

    out = CASE_ROOT / "outputs/figures"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "prl_figC_reproduced.png", dpi=240, bbox_inches="tight")
    fig.savefig(out / "prl_figC_reproduced.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
