#!/usr/bin/env python3
"""Render the idx28 benchmark-gold diagnostic figure."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from neel_macrospin_audit import (  # noqa: E402
    frozen_mep_barrier,
    frozen_task3_response,
    mep_barrier,
    rigid_precession_solution,
    tracked_interior_response,
)


BLUE = "#4c72b0"
ORANGE = "#dd8452"
GREEN = "#55a868"
RED = "#c44e52"
PURPLE = "#8172b3"
INK = "#202124"


def configure() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "mathtext.fontset": "stix",
            "font.size": 9,
            "axes.linewidth": 0.85,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "legend.frameon": False,
        }
    )


def save_all(fig: plt.Figure, stem: Path) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".png"), dpi=260, bbox_inches="tight", facecolor="white")
    svg_path = stem.with_suffix(".svg")
    fig.savefig(svg_path, bbox_inches="tight", facecolor="white")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    configure()
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.2), constrained_layout=True)

    lam = np.linspace(0.02, 2.2, 800)
    energy_y_plus = -2.0 * lam
    energy_y_minus = 2.0 * lam
    energy_off_axis = -(1.0 + lam**2)
    axes[0, 0].plot(lam, energy_y_plus, color=BLUE, lw=1.8, label=r"$+\hat y$: saddle $\to$ min")
    axes[0, 0].plot(lam, energy_y_minus, color=RED, lw=1.5, label=r"$-\hat y$: maximum")
    mask = lam < 1.0
    axes[0, 0].plot(lam[mask], energy_off_axis[mask], color=GREEN, lw=2.0, label="two off-axis minima")
    axes[0, 0].axvline(1.0, color=INK, ls=":", lw=1.0)
    axes[0, 0].set(xlabel=r"$\lambda$", ylabel=r"$U/\omega_K$", title="(a) Task 1: frozen Morse indices are reversed")
    axes[0, 0].legend(fontsize=7.2)

    exact = np.asarray([mep_barrier(value) for value in lam])
    frozen = np.asarray([frozen_mep_barrier(value) for value in lam])
    axes[0, 1].plot(lam, exact, color=BLUE, lw=2.0, label="exact minimax arc")
    axes[0, 1].plot(lam, frozen, color=RED, lw=1.5, ls="--", label="frozen Task 2")
    axes[0, 1].axvline(0.5, color=INK, ls=":", lw=0.9)
    axes[0, 1].axvline(1.0, color=INK, ls=":", lw=0.9)
    axes[0, 1].set(xlabel=r"$\lambda$", ylabel=r"$\Delta U/\omega_K$", title="(b) Task 2: the real breakpoints are 1/2 and 1")
    axes[0, 1].legend(fontsize=7.4)

    lam_response = np.linspace(1.03, 4.0, 600)
    tracked = np.asarray([tracked_interior_response(value) for value in lam_response])
    frozen_response = np.asarray([frozen_task3_response(value) for value in lam_response])
    axes[1, 0].plot(lam_response, tracked, color=PURPLE, lw=1.9, label="tracked interior minimum")
    axes[1, 0].plot(lam_response, frozen_response, color=ORANGE, lw=1.5, ls="--", label="frozen claimed saddle")
    axes[1, 0].axhline(0.0, color=INK, lw=0.8)
    axes[1, 0].set(xlabel=r"$\lambda>1$", ylabel=r"$\partial_\delta n_z$", ylim=(-35, 6), title="(c) Task 3: no interior MEP saddle exists")
    axes[1, 0].legend(fontsize=7.2)

    omega = np.linspace(12.0, 50.0, 500)
    cosine = []
    omega_d = []
    for value in omega:
        try:
            c_value, d_value = rigid_precession_solution(100.0, 1.0, 1.0, 0.0, 0.1, value)
        except ValueError:
            cosine.append(np.nan)
            omega_d.append(np.nan)
        else:
            cosine.append(c_value)
            omega_d.append(d_value)
    axes[1, 1].plot(omega, cosine, color=BLUE, lw=1.9, label=r"$\cos\theta$")
    twin = axes[1, 1].twinx()
    twin.plot(omega, omega_d, color=GREEN, lw=1.6, label=r"$\omega_D$")
    axes[1, 1].scatter([20.0], [-5.0 / 11.0], color=RED, s=28, zorder=4)
    twin.scatter([20.0], [4.4], color=RED, s=28, zorder=4)
    axes[1, 1].set(xlabel=r"precession $\Omega$", ylabel=r"$\cos\theta$", title="(d) Task 4: an exact interior precession family")
    twin.set_ylabel(r"required $\omega_D$", color=GREEN)
    lines = axes[1, 1].lines + twin.lines
    axes[1, 1].legend(lines, [line.get_label() for line in lines], fontsize=7.2, loc="upper right")

    stem = CASE_ROOT / "outputs" / "figures" / "idx28_gold_audit"
    save_all(fig, stem)
    outputs = []
    for suffix in (".png", ".svg", ".pdf"):
        path = stem.with_suffix(suffix)
        outputs.append({"path": str(path.relative_to(CASE_ROOT)), "exists": path.exists(), "bytes": path.stat().st_size if path.exists() else 0})
    check = {
        "schema_version": 1,
        "status": "passed" if all(item["bytes"] > 0 for item in outputs) else "failed",
        "outputs": outputs,
        "all_outputs_nonempty": all(item["bytes"] > 0 for item in outputs),
        "scope": "benchmark analytic audit; no source-paper panel claimed",
    }
    path = CASE_ROOT / "outputs" / "checks" / "idx28_figure_check.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(check, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
