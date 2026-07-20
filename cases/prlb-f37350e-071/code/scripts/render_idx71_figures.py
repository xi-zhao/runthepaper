#!/usr/bin/env python3
"""Render the PRL-Bench idx71 analytic gold audit."""

from __future__ import annotations

import json
from decimal import Decimal, localcontext
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from parametric_memory_audit import (  # noqa: E402
    brute_phase_gain,
    exact_optimal_gain,
    exact_transient_peak,
    frozen_optimal_gain,
    frozen_quantum_steady_occupation,
    frozen_transient_peak,
    quantum_steady_occupation,
    threshold_inversion,
)


BLUE = "#4c72b0"
ORANGE = "#dd8452"
GREEN = "#55a868"
RED = "#c44e52"
INK = "#202124"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


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
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def threshold_curve(detuning_ratio: np.ndarray) -> np.ndarray:
    with localcontext() as context:
        context.prec = 80
        n = Decimal(155)
        gamma = Decimal(10)
        alpha = gamma + Decimal(9) * n
        lam = Decimal(16) / alpha
        scale = alpha * (gamma * gamma + Decimal(200) ** 2).sqrt() / (
            n * Decimal(4) * Decimal(3)
        )
        base = float(lam * scale)
    return base * np.sqrt(1.0 + detuning_ratio * detuning_ratio)


def main() -> None:
    configure()
    audit = json.loads(
        (CASE_ROOT / "outputs" / "data" / "idx71_gold_audit.json").read_text(
            encoding="utf-8"
        )
    )
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.2), constrained_layout=True)

    time = np.linspace(0.0, 10.0, 1201)
    exact = exact_optimal_gain(1.0, 0.8, 1.2, time)
    frozen = frozen_optimal_gain(1.0, 0.8, 1.2, time)
    axes[0, 0].plot(time, exact, color=BLUE, lw=1.8, label="exact phase optimum")
    axes[0, 0].plot(time, frozen, color=RED, lw=1.4, ls="--", label="frozen formula")
    sample_time = np.linspace(0.5, 8.5, 9)
    sample_gain = [brute_phase_gain(1.0, 0.8, 1.2, value, phase_count=40_000) for value in sample_time]
    axes[0, 0].scatter(sample_time, sample_gain, s=15, color=INK, zorder=3, label="phase search")
    axes[0, 0].set(
        xlabel=r"time $T$",
        ylabel=r"optimal energy gain $\mathcal{G}$",
        title=r"(a) Task 3: oscillatory phase switches are unavoidable",
        yscale="log",
    )
    axes[0, 0].legend(fontsize=7.2)

    short_time = np.linspace(0.0, 4.0, 801)
    for coupling, color, label in (
        (0.9, ORANGE, r"$|\xi|=0.9$: no interior peak"),
        (1.1, GREEN, r"$|\xi|=1.1$: one interior peak"),
    ):
        axes[0, 1].plot(
            short_time,
            exact_optimal_gain(1.0, coupling, 0.6, short_time),
            color=color,
            lw=1.8,
            label=label,
        )
    peak = exact_transient_peak(1.0, 1.1, 0.6)
    assert peak is not None
    axes[0, 1].scatter([peak[0]], [peak[1]], color=GREEN, s=32, marker="o", zorder=4, label="exact peak")
    frozen_peak = frozen_transient_peak(1.0, 1.1, 0.6)
    axes[0, 1].scatter(
        [frozen_peak[0]],
        [float(exact_optimal_gain(1.0, 1.1, 0.6, frozen_peak[0]))],
        color=RED,
        s=38,
        marker="x",
        zorder=4,
        label=r"frozen $T_\star$",
    )
    axes[0, 1].axhline(1.0, color="#777777", lw=0.8, ls=":")
    axes[0, 1].set(
        xlabel=r"time $T$",
        ylabel=r"exact $\mathcal{G}(T)$",
        title=r"(b) Task 4: stability alone does not create a peak",
        ylim=(0.0, 1.20),
    )
    axes[0, 1].legend(fontsize=7.0)

    ratio = np.linspace(0.0, 0.96, 481)
    axes[1, 0].plot(ratio, quantum_steady_occupation(ratio), color=BLUE, lw=1.8, label="vacuum Lyapunov")
    axes[1, 0].plot(
        ratio,
        frozen_quantum_steady_occupation(ratio),
        color=RED,
        lw=1.4,
        ls="--",
        label="frozen (2x too large)",
    )
    axes[1, 0].scatter([0.5], [1.0 / 6.0], color=INK, s=25, zorder=4)
    axes[1, 0].set(
        xlabel=r"pump ratio $r=|\xi|/\lambda$",
        ylabel=r"steady occupation $n$",
        title=r"(c) Task 5: the vacuum half-factor",
        ylim=(0.0, 6.5),
    )
    axes[1, 0].legend(fontsize=7.2)

    detuning_ratio = np.linspace(0.0, 1.4, 281)
    critical = threshold_curve(detuning_ratio)
    axes[1, 1].plot(detuning_ratio, critical, color=BLUE, lw=1.8)
    exact_threshold = float(threshold_inversion())
    axes[1, 1].scatter([0.7], [exact_threshold], color=GREEN, s=36, zorder=4, label="80-digit recomputation")
    axes[1, 1].scatter(
        [0.7],
        [float(audit["task_6"]["frozen_value"])],
        color=RED,
        marker="x",
        s=42,
        zorder=5,
        label="frozen value",
    )
    axes[1, 1].annotate(
        f"difference = {float(audit['task_6']['absolute_difference_from_frozen_decimal']):.2e}",
        xy=(0.7, exact_threshold),
        xytext=(0.79, 1.85),
        arrowprops={"arrowstyle": "->", "lw": 0.8},
        fontsize=7.5,
    )
    axes[1, 1].set(
        xlabel=r"detuning ratio $|\delta|/\lambda$",
        ylabel=r"$|G_{38}\Omega_{28}|_{\rm crit}$",
        title=r"(d) Task 6: frozen digits satisfy the $10^{-12}$ tolerance",
    )
    axes[1, 1].legend(fontsize=7.2)

    stem = CASE_ROOT / "outputs" / "figures" / "idx71_gold_audit"
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
    write_json(
        CASE_ROOT / "outputs" / "checks" / "idx71_figure_check.json",
        {
            "schema_version": 1,
            "status": "passed" if all(item["bytes"] > 0 for item in outputs) else "failed",
            "outputs": outputs,
            "all_outputs_nonempty": all(item["bytes"] > 0 for item in outputs),
            "scope": "benchmark analytic audit; no source-paper panel claimed",
        },
    )


if __name__ == "__main__":
    main()
