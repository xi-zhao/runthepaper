#!/usr/bin/env python3
"""Render source-calibration and frozen-gold audit figures for idx58."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
DATA = CASE_ROOT / "outputs" / "data"
FIGURES = CASE_ROOT / "outputs" / "figures"
COMPARISONS = CASE_ROOT / "outputs" / "comparisons"
REFERENCES = CASE_ROOT / "references" / "original_figures"

BLUE = "#0072B2"
ORANGE = "#D55E00"
GREEN = "#009E73"
PURPLE = "#7A3E9D"
GRAY = "#5B6573"
RED = "#B2182B"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.0,
            "axes.labelsize": 8.0,
            "axes.titlesize": 8.5,
            "axes.linewidth": 0.8,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "legend.fontsize": 6.8,
            "legend.frameon": False,
            "lines.linewidth": 1.4,
            "savefig.bbox": "tight",
        }
    )


def panel_label(axis: plt.Axes, label: str) -> None:
    axis.text(
        -0.14,
        1.06,
        label,
        transform=axis.transAxes,
        fontsize=10,
        fontweight="bold",
        va="top",
    )


def plot_fixed_window(axis: plt.Axes, source: dict[str, object]) -> None:
    table = source["fixed_window_refits"]["10"]
    sizes = np.asarray(table["half_intervals"], dtype=float)
    values = np.asarray(table["top_eigenvalues"], dtype=float)
    fit = table["fit"]
    x = 1.0 / sizes
    xline = np.linspace(0.0, x.max() * 1.03, 200)
    axis.scatter(x, values, s=19, color=ORANGE, edgecolor="white", linewidth=0.45, label="paper table")
    axis.plot(xline, fit["intercept"] + fit["slope"] * xline, color=BLUE, label="linear refit")
    calibration = source["independent_matrix_calibration"]
    cx = np.array([1.0 / row["half_intervals"] for row in calibration])
    cy = np.array([row["computed"] for row in calibration])
    axis.scatter(cx, cy, s=35, facecolors="none", edgecolors=GREEN, linewidth=1.1, label="independent matrix")
    axis.set_xlabel(r"$1/N$")
    axis.set_ylabel(r"$\lambda_{10,N}^{\max}$")
    axis.set_title(r"Fixed window $L=10$")
    axis.legend(loc="lower left")
    axis.grid(alpha=0.18, linewidth=0.6)


def plot_final_fit(axis: plt.Axes, source: dict[str, object]) -> None:
    limits = source["fixed_window_refits"]
    windows = np.array(sorted(int(key) for key in limits), dtype=float)
    values = np.array([limits[str(int(window))]["fit"]["intercept"] for window in windows])
    errors = np.array([limits[str(int(window))]["fit"]["intercept_std"] for window in windows])
    fit = source["final_fit"]
    x = 1.0 / windows
    xline = np.linspace(0.0, x.max() * 1.03, 200)
    axis.errorbar(x, values, yerr=errors, fmt="o", ms=4.0, color=ORANGE, ecolor=GRAY, capsize=2, label="fixed-$L$ limits")
    axis.plot(xline, fit["intercept"] + fit["slope"] * xline, color=BLUE, label="weighted refit")
    axis.scatter([0.0], [fit["intercept"]], marker="D", s=25, color=GREEN, zorder=3, label=r"$L\to\infty$")
    axis.set_xlabel(r"$1/L$")
    axis.set_ylabel(r"$\sup\lambda_L$")
    axis.set_title("Final window extrapolation")
    axis.legend(loc="lower left")
    axis.grid(alpha=0.18, linewidth=0.6)


def save_all(figure: plt.Figure, stem: Path) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(stem.with_suffix(".png"), dpi=400)
    figure.savefig(stem.with_suffix(".pdf"))
    figure.savefig(stem.with_suffix(".svg"))


def render_source(source: dict[str, object]) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(7.1, 2.75), constrained_layout=True)
    plot_fixed_window(axes[0], source)
    plot_final_fit(axes[1], source)
    panel_label(axes[0], "a")
    panel_label(axes[1], "b")
    save_all(figure, FIGURES / "idx58_source_extrapolation")
    plt.close(figure)


def render_audit(audit: dict[str, object]) -> None:
    scan = audit["task_3"]["scan"]
    figure, axes = plt.subplots(2, 2, figsize=(7.1, 5.0), constrained_layout=True)

    ax = axes[0, 0]
    lower, upper = audit["task_2"]["rigorous_norm_bounds_from_source"]
    ax.hlines(1.0, lower, upper, color=BLUE, linewidth=8, label="rigorous interval")
    ax.scatter([audit["task_2"]["paper_estimate"]], [1.0], marker="D", s=35, color=GREEN, label="paper estimate")
    ax.scatter([audit["task_2"]["frozen_value"]], [1.0], marker="x", s=55, color=RED, linewidth=2, label="frozen gold")
    ax.set_xlim(1.05, 2.08)
    ax.set_yticks([])
    ax.set_xlabel(r"operator norm $\|K\|$")
    ax.set_title(r"Parity: $\inf\sigma(K)=-1-\sup\sigma(K)$")
    ax.legend(loc="upper center", ncol=2)

    ax = axes[0, 1]
    windows = np.array([row["window"] for row in scan], dtype=float)
    lambdas = np.array([row["lambda_at_half"] for row in scan], dtype=float)
    resolutions = np.array([row["half_intervals"] / row["window"] for row in scan])
    points = ax.scatter(windows, lambdas, c=resolutions, cmap="viridis", s=30, edgecolor="white", linewidth=0.4)
    ax.axhline(audit["task_3"]["frozen_lambda_half"], color=RED, linestyle="--", label="frozen 0.06405")
    ax.set_xlabel(r"window $L$")
    ax.set_ylabel(r"$\Lambda_{L,N}(1/2)$")
    ax.set_title("Constrained spectral flow")
    ax.grid(alpha=0.18, linewidth=0.6)
    ax.legend(loc="lower right")
    colorbar = figure.colorbar(points, ax=ax, fraction=0.05, pad=0.03)
    colorbar.set_label(r"$N/L$")

    ax = axes[1, 0]
    growth = audit["task_4"]["window_growth"]
    gx = np.array([row["window"] for row in growth], dtype=float)
    gy = np.array([row["c2_finite_window"] for row in growth], dtype=float)
    ax.plot(gx, gy, "o-", color=PURPLE, label="finite-window quadratic form")
    ax.axhline(audit["task_4"]["frozen_c2"], color=RED, linestyle="--", label="frozen 0.3210")
    ax.set_xlabel(r"window $L$")
    ax.set_ylabel(r"$c_2(L,N)$")
    ax.set_title("No full-line convergence")
    ax.grid(alpha=0.18, linewidth=0.6)
    ax.legend(loc="upper left")

    ax = axes[1, 1]
    ax.axis("off")
    rows = [
        ("Task 1", "valid", "direct source identity"),
        ("Task 2", "invalid", r"$\|K\|<1.193$, not 2"),
        ("Task 3", "invalid", r"$\Lambda(1/2)\approx0.11$"),
        ("Task 4", "invalid", r"$c_2(L)$ grows with $L$"),
    ]
    table = ax.table(
        cellText=rows,
        colLabels=["Task", "Verdict", "Decisive check"],
        loc="center",
        cellLoc="left",
        colLoc="left",
        colWidths=[0.23, 0.22, 0.55],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7.2)
    table.scale(1.0, 1.55)
    for (row, column), cell in table.get_celld().items():
        cell.set_linewidth(0.5)
        cell.set_edgecolor("#C8CDD3")
        if row == 0:
            cell.set_facecolor("#E9EEF3")
            cell.set_text_props(weight="bold")
        elif column == 1:
            cell.get_text().set_color(GREEN if row == 1 else RED)
            cell.get_text().set_weight("bold")
    ax.set_title("Terminal verdict: benchmark gold invalid", pad=2)

    for label, axis in zip("abcd", axes.flat):
        panel_label(axis, label)
    save_all(figure, FIGURES / "idx58_gold_audit")
    plt.close(figure)


def render_feature_comparison(source: dict[str, object]) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(7.1, 5.1), constrained_layout=True)
    reference_paths = [
        REFERENCES / "SM_fig_lambda_10.png",
        REFERENCES / "SM_fig_sup_Delta.png",
    ]
    for row, reference in enumerate(reference_paths):
        axes[row, 0].imshow(mpimg.imread(reference))
        axes[row, 0].axis("off")
        axes[row, 0].set_title("Paper source reference")
    plot_fixed_window(axes[0, 1], source)
    plot_final_fit(axes[1, 1], source)
    axes[0, 1].set_title("Independent matrix calibration + refit")
    axes[1, 1].set_title("Independent weighted refit")
    for label, axis in zip("abcd", axes.flat):
        panel_label(axis, label)
    figure.suptitle("Feature-level comparison (not pixel registered)", fontsize=9.5)
    COMPARISONS.mkdir(parents=True, exist_ok=True)
    figure.savefig(COMPARISONS / "idx58_source_extrapolation_comparison.png", dpi=300)
    plt.close(figure)


def main() -> None:
    style()
    source = load_json(DATA / "idx58_source_extrapolation.json")
    audit = load_json(DATA / "idx58_gold_audit.json")
    render_source(source)
    render_audit(audit)
    render_feature_comparison(source)
    artifacts = [
        FIGURES / "idx58_source_extrapolation.png",
        FIGURES / "idx58_source_extrapolation.pdf",
        FIGURES / "idx58_source_extrapolation.svg",
        FIGURES / "idx58_gold_audit.png",
        FIGURES / "idx58_gold_audit.pdf",
        FIGURES / "idx58_gold_audit.svg",
        COMPARISONS / "idx58_source_extrapolation_comparison.png",
    ]
    check = {
        "status": "passed" if all(path.exists() and path.stat().st_size > 1000 for path in artifacts) else "failed",
        "artifacts": [str(path.relative_to(CASE_ROOT)) for path in artifacts],
        "comparison_type": "feature_level_not_pixel_registered",
        "pixel_diff_generated": False,
    }
    output = CASE_ROOT / "outputs" / "checks" / "idx58_figure_check.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(check, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(check, indent=2))


if __name__ == "__main__":
    main()
