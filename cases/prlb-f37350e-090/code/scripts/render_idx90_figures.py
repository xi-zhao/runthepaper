#!/usr/bin/env python3
"""Render the PRL-Bench idx90 source/gold consistency audit."""

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

from photonic_edge_audit import (  # noqa: E402
    exact_kdos_component,
    frozen_edge_formula,
    frozen_kdos_component,
    frozen_radial_rate_prefactor,
    radial_rate_prefactor,
    residual_after_frozen_pole_subtraction,
    toy_model_rates,
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

    omega = np.linspace(0.34, 0.66, 801)
    residue = complex(1.2, -0.4)
    exact = np.asarray([exact_kdos_component(4.0, value, 0.47, 0.03, residue) for value in omega])
    frozen = np.asarray([frozen_kdos_component(4.0, value, 0.47, 0.03, residue) for value in omega])
    axes[0, 0].plot(omega, exact, color=BLUE, lw=1.8, label="literal complex ansatz")
    axes[0, 0].plot(omega, frozen, color=RED, lw=1.4, ls="--", label="frozen Task 1")
    axes[0, 0].axhline(0.0, color="#777777", lw=0.8)
    axes[0, 0].set(
        xlabel=r"frequency $\omega$",
        ylabel=r"component $\rho_p$",
        title="(a) Tasks 1–2: the frozen line shape has the opposite sign",
    )
    axes[0, 0].legend(fontsize=7.3)

    exact_prefactor = radial_rate_prefactor(1.0, 0.5, 4.0, 1.0)
    frozen_prefactor = frozen_radial_rate_prefactor(1.0, 0.5, 4.0, 1.0)
    axes[0, 1].bar([0, 1], [exact_prefactor, frozen_prefactor], color=[BLUE, RED], width=0.62)
    axes[0, 1].set_xticks([0, 1], ["full $4\\pi$ angle", "frozen"])
    axes[0, 1].text(0, exact_prefactor * 1.03, f"{exact_prefactor:.6f}", ha="center", fontsize=8)
    axes[0, 1].text(1, frozen_prefactor * 1.10, f"{frozen_prefactor:.6f}", ha="center", fontsize=8)
    axes[0, 1].set(
        ylabel="radial-rate prefactor",
        title="(b) Task 3: angular reduction is low by a factor of four",
        ylim=(0.0, exact_prefactor * 1.22),
    )

    k_pole = np.linspace(0.2, 1.8, 401)
    remaining = np.asarray([residual_after_frozen_pole_subtraction(value, 1.0) for value in k_pole])
    axes[1, 0].plot(k_pole, remaining, color=PURPLE, lw=1.8)
    axes[1, 0].axhline(0.0, color="#777777", lw=0.8)
    axes[1, 0].axvline(1.0, color=ORANGE, lw=1.0, ls=":", label="accidental cancellation at $k_R=1$")
    axes[1, 0].scatter([1.3], [residual_after_frozen_pole_subtraction(1.3, 1.0)], color=RED, s=28, zorder=3)
    axes[1, 0].set(
        xlabel=r"real pole $k_R$",
        ylabel=r"remaining residue / input residue",
        title=r"(c) Task 5: prescribed subtraction leaves $1-k_R^2$",
    )
    axes[1, 0].legend(fontsize=7.2)

    detuning = np.logspace(-9, -1, 240)
    omega_toy = 0.5 - detuning
    root = 1.0 - (detuning / 2.0) ** 2
    residue_jacobian = 5.0 * np.sqrt(3.0)
    excitation = omega_toy**2 / (4.0 * np.pi) * root**2 * residue_jacobian
    toy = toy_model_rates()
    limit = float(toy["literal_magnitude_limit"])
    reported = float(toy["frozen_task7_reported"])
    frozen_closed = frozen_edge_formula(omega_drive=1.0, epsilon0=4.0, a=2.0, b=3.0, j_edge=5.0)
    axes[1, 1].semilogx(detuning, excitation, color=GREEN, lw=1.8, label="literal excitation magnitude")
    axes[1, 1].axhline(limit, color=INK, lw=1.0, ls=":", label=f"correct magnitude limit {limit:.6f}")
    axes[1, 1].axhline(reported, color=RED, lw=1.3, ls="--", label=f"frozen reported {reported:.6f}")
    axes[1, 1].axhline(frozen_closed, color=ORANGE, lw=1.2, ls="-.", label=f"frozen Task 5 formula {frozen_closed:.6f}")
    axes[1, 1].invert_xaxis()
    axes[1, 1].set(
        xlabel=r"edge detuning $\Omega/2-\omega$",
        ylabel="rate magnitude",
        title="(d) Task 7: literal decay is zero; excitation is finite",
        ylim=(0.0, limit * 1.12),
    )
    axes[1, 1].legend(fontsize=6.8, loc="upper right")

    stem = CASE_ROOT / "outputs" / "figures" / "idx90_gold_audit"
    save_all(fig, stem)
    outputs = []
    for suffix in (".png", ".svg", ".pdf"):
        path = stem.with_suffix(suffix)
        outputs.append(
            {
                "path": str(path.relative_to(CASE_ROOT)),
                "exists": path.exists(),
                "bytes": path.stat().st_size if path.exists() else 0,
            }
        )
    check = {
        "schema_version": 1,
        "status": "passed" if all(item["bytes"] > 0 for item in outputs) else "failed",
        "outputs": outputs,
        "all_outputs_nonempty": all(item["bytes"] > 0 for item in outputs),
        "scope": "benchmark analytic audit; no source-paper panel claimed",
    }
    path = CASE_ROOT / "outputs" / "checks" / "idx90_figure_check.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(check, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
