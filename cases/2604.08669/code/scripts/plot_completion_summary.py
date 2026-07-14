#!/usr/bin/env python3
"""Plot the saved A100 GNN summary and paper-scale P2WGS check."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "outputs/data"
CHECKS = ROOT / "outputs/checks"
FIGURES = ROOT / "outputs/figures"
GNN_REASON = (
    "Difference reason: 64-instance A100 paper-geometry short probe; the "
    "million-sample training and 1024-instance evaluation were stopped because "
    "the metric-contract gate did not pass."
)
P2WGS_REASON = (
    "Difference reason: independent reconstruction; the exact Zhuifeng "
    "frame-trajectory protocol is unavailable, so the paper's 3-to-5 "
    "intensity improvement is not reproduced."
)


def plot_gnn_summary() -> None:
    with (DATA / "fig3_a100_paper_geometry_summary.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    fig, axes = plt.subplots(1, len(rows), figsize=(8.6, 4.2))
    if len(rows) == 1:
        axes = [axes]
    for ax, row in zip(axes, rows):
        paper = float(row["paper_reference"])
        reproduced = float(row["reproduced_value"])
        title = row["metric"].replace("mean_", "").replace("_", " ")
        ax.bar([0, 1], [paper, reproduced], color=["0.65", "#4c72b0"], width=0.62)
        ax.set_xticks([0, 1], ["Paper", "A100 probe"])
        ax.set_ylabel("lattice units")
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)
        ax.text(1, reproduced, f"+{reproduced - paper:.3f}", ha="center", va="bottom", fontsize=9)
    fig.suptitle("Fig. 3 paper-geometry GNN distance check (lower is better)", fontsize=11)
    fig.tight_layout(rect=(0, 0.18, 1, 0.95))
    fig.text(0.5, 0.025, GNN_REASON, ha="center", va="bottom", fontsize=8.0, wrap=True)
    fig.savefig(FIGURES / "fig3_a100_paper_geometry_gap.png", dpi=180)
    plt.close(fig)


def plot_p2wgs_summary() -> None:
    checks = json.loads((CHECKS / "p2wgs_paper_scale.json").read_text(encoding="utf-8"))
    iterations = np.array(checks["parameters"]["iterations"], dtype=int)
    summary = checks["summary_by_iteration"]
    phase = np.array([summary[str(value)]["phase_mean"] for value in iterations])
    phase_std = np.array([summary[str(value)]["phase_std"] for value in iterations])
    intensity = np.array([summary[str(value)]["intensity_mean"] for value in iterations])
    intensity_std = np.array([summary[str(value)]["intensity_std"] for value in iterations])

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.2))
    axes[0].errorbar(iterations, phase, yerr=phase_std, marker="o", capsize=3, color="#4c72b0")
    axes[0].set_title("phase continuity")
    axes[0].set_ylabel("wrapped phase change / 2π")
    axes[1].errorbar(iterations, intensity, yerr=intensity_std, marker="o", capsize=3, color="#dd8452")
    axes[1].set_title("intensity continuity")
    axes[1].set_ylabel("relative intensity change")
    for ax in axes:
        ax.set_xlabel("P2WGS iterations")
        ax.set_xticks(iterations)
        ax.grid(alpha=0.25)
    fig.suptitle("Fig. 4 paper-scale P2WGS (N=10201, 1024×1024 grid, n=3)", fontsize=11)
    fig.tight_layout(rect=(0, 0.18, 1, 0.95))
    fig.text(0.5, 0.025, P2WGS_REASON, ha="center", va="bottom", fontsize=8.0, wrap=True)
    fig.savefig(FIGURES / "fig4_paper_scale_p2wgs_summary.png", dpi=180)
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    plot_gnn_summary()
    plot_p2wgs_summary()


if __name__ == "__main__":
    main()
