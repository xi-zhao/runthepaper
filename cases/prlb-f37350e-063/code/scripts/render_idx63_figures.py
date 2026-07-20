#!/usr/bin/env python3
"""Render source-curve and benchmark-gold figures for PRL-Bench idx63."""

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

from nonreciprocal_cep_audit import (  # noqa: E402
    eigenpair_residuals,
    exact_obc_eigenpairs,
    frozen_obc_eigenpairs,
    obc_linear_matrix,
)


BLUE = "#8da0cb"
GREEN = "#66c2a5"
ORANGE = "#fc8d62"
RED = "#d75452"
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


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


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


def load_table(path: Path) -> dict[str, np.ndarray]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    table: dict[str, np.ndarray] = {}
    for index, column in enumerate(payload["columns"]):
        values = [row[index] for row in payload["rows"]]
        if column == "accepted":
            table[column] = np.asarray(values, dtype=bool)
        else:
            table[column] = np.asarray(
                [np.nan if value is None else value for value in values], dtype=float
            )
    return table


def draw_source_overlay(ax: plt.Axes, features: dict[str, object]) -> None:
    source = features["digitized_source"]
    generated = features["a100_generated"]
    source_x = np.asarray(source["x"], dtype=float)
    source_y = np.asarray(source["lambda_2"], dtype=float)
    generated_x = np.asarray(generated["x"], dtype=float)
    generated_y = np.asarray(generated["lambda_2"], dtype=float)
    keep = generated_x <= 0.015
    ax.plot(
        source_x,
        source_y,
        color=INK,
        lw=2.8,
        alpha=0.24,
        label="source S1(a), digitized",
    )
    ax.plot(
        generated_x[keep],
        generated_y[keep],
        color=BLUE,
        lw=1.8,
        marker="o",
        ms=2.5,
        markevery=4,
        label="A100, independent RK4",
    )
    ax.set(
        xlim=(0.0, 0.015),
        ylim=(-0.25, 0.0),
        xlabel=r"$\kappa-\kappa_c$",
        ylabel=r"$\mathrm{Re}\,\lambda_2$",
    )
    ax.set_xticks(np.linspace(0.0, 0.015, 6))
    ax.legend(loc="lower left", fontsize=7.6)


def render_source_reproduction(features: dict[str, object]) -> None:
    source = features["digitized_source"]
    generated = features["a100_generated"]
    source_x = np.asarray(source["x"], dtype=float)
    source_y = np.asarray(source["lambda_2"], dtype=float)
    generated_x = np.asarray(generated["x"], dtype=float)
    generated_y = np.asarray(generated["lambda_2"], dtype=float)
    overlap = (
        (source_x >= generated_x.min())
        & (source_x <= min(0.015, generated_x.max()))
    )
    error = np.interp(source_x[overlap], generated_x, generated_y) - source_y[overlap]
    metrics = features["comparison"]

    fig, axes = plt.subplots(1, 2, figsize=(9.1, 3.45), constrained_layout=True)
    draw_source_overlay(axes[0], features)
    axes[0].set_title(r"(a) Source CEP branch, $\gamma=0.3$", loc="left")
    axes[1].plot(source_x[overlap], error, color=ORANGE, lw=1.45)
    axes[1].axhline(0.0, color="0.25", lw=0.8)
    axes[1].axhspan(
        -float(metrics["rmse"]),
        float(metrics["rmse"]),
        color=GREEN,
        alpha=0.16,
        label=f"RMSE = {metrics['rmse']:.2e}",
    )
    axes[1].set(
        xlim=(0.0, 0.015),
        xlabel=r"$\kappa-\kappa_c$",
        ylabel="A100 − source",
        title="(b) Digitized curve residual",
    )
    axes[1].ticklabel_format(axis="y", style="sci", scilimits=(-2, 2))
    axes[1].legend(loc="upper right", fontsize=7.8)
    save_all(
        fig,
        CASE_ROOT / "outputs" / "figures" / "idx63_cep_gamma03_reproduction",
    )


def render_gold_audit(features: dict[str, object]) -> None:
    transition = load_table(
        CASE_ROOT / "outputs" / "a100" / "idx63_transition_summary.json"
    )
    audit = json.loads(
        (CASE_ROOT / "outputs" / "data" / "idx63_gold_audit.json").read_text()
    )
    accepted = transition["accepted"] & np.isfinite(transition["lambda_2"])
    kappa = transition["kappa"]
    residual = transition["residual"]
    frozen_index = int(np.argmin(np.abs(kappa - 2.38930)))
    first_static = int(np.flatnonzero(accepted)[0])

    fig, axes = plt.subplots(2, 2, figsize=(10.2, 7.25), constrained_layout=True)

    axes[0, 0].semilogy(kappa, residual, color=INK, lw=1.35)
    axes[0, 0].axhline(1.0e-8, color=GREEN, ls="--", lw=1.1, label=r"static gate $10^{-8}$")
    axes[0, 0].scatter(
        [kappa[frozen_index]],
        [residual[frozen_index]],
        color=RED,
        marker="x",
        s=58,
        lw=1.8,
        zorder=4,
        label=r"frozen $\kappa=2.38930$",
    )
    axes[0, 0].scatter(
        [kappa[first_static]],
        [residual[first_static]],
        color=GREEN,
        s=38,
        zorder=4,
        label=r"first accepted $2.38937$",
    )
    axes[0, 0].set(
        xlabel=r"$\kappa$",
        ylabel=r"$\|\dot\alpha\|_2$",
        title="(a) Task 4 fails before Jacobian evaluation",
    )
    axes[0, 0].legend(fontsize=7.1, loc="lower left")

    x = kappa[accepted] - 2.38930
    y = transition["lambda_2"][accepted]
    y_half = transition["half_lambda_2"][accepted]
    axes[0, 1].plot(x, y, color=BLUE, lw=1.7, marker="o", ms=2.8, label=r"$\varepsilon=10^{-7}$")
    axes[0, 1].plot(x, y_half, color=ORANGE, lw=1.1, ls="--", label=r"$\varepsilon/2$")
    axes[0, 1].axhspan(-1.0e-5, 1.0e-5, color=GREEN, alpha=0.22, label="CEP eigenvalue band")
    axes[0, 1].axhline(0.0, color="0.25", lw=0.8)
    axes[0, 1].text(
        0.96,
        0.10,
        r"all accepted points: $\nu_1=1,\ \nu_2=1$",
        transform=axes[0, 1].transAxes,
        ha="right",
        fontsize=7.8,
    )
    axes[0, 1].set(
        xlabel=r"$\kappa-2.38930$",
        ylabel=r"$\mathrm{Re}\,\lambda_2$",
        title="(b) No CEP point after the static gate",
    )
    axes[0, 1].legend(fontsize=7.2, loc="lower left")

    modes = np.arange(1, 41)
    for gamma, color in ((0.3, GREEN), (1.7, ORANGE)):
        matrix = obc_linear_matrix(40, 2.1, gamma)
        exact_values, exact_vectors = exact_obc_eigenpairs(40, 2.1, gamma)
        frozen_values, frozen_vectors = frozen_obc_eigenpairs(40, 2.1, gamma)
        exact_residual = eigenpair_residuals(matrix, exact_values, exact_vectors)
        frozen_residual = eigenpair_residuals(matrix, frozen_values, frozen_vectors)
        axes[1, 0].semilogy(modes, exact_residual, color=color, lw=1.4, label=fr"correct $\gamma={gamma}$")
        axes[1, 0].semilogy(modes, frozen_residual, color=color, lw=1.25, ls="--", label=fr"frozen pair $\gamma={gamma}$")
    axes[1, 0].set(
        xlabel="mode $m$",
        ylabel="relative eigenpair residual",
        title="(c) Task 1: spectra survive, printed eigenpairs do not",
        ylim=(1.0e-17, 2.0),
    )
    axes[1, 0].legend(fontsize=6.9, ncol=2, loc="upper center")

    solutions = audit["task_3"]["solutions"]
    q = np.asarray([item["q_over_pi"] for item in solutions], dtype=float)
    density = np.asarray([item["density"] for item in solutions], dtype=float)
    axes[1, 1].bar(q, density, width=0.20, color=[BLUE, GREEN], edgecolor="white")
    for q_value, density_value in zip(q, density, strict=True):
        axes[1, 1].text(q_value, density_value + 0.12, "PH: yes", ha="center", fontsize=8)
    axes[1, 1].annotate(
        "valid branch omitted by\nfrozen uniqueness claim",
        xy=(-0.5, density[1]),
        xytext=(-0.12, 3.4),
        arrowprops={"arrowstyle": "->", "lw": 0.8, "color": RED},
        color=RED,
        fontsize=7.6,
        ha="center",
    )
    axes[1, 1].set(
        xlim=(-0.75, 0.75),
        ylim=(0.0, 6.8),
        xticks=[-0.5, 0.5],
        xticklabels=[r"$-\pi/2$", r"$+\pi/2$"],
        xlabel="bulk wavevector $q$",
        ylabel=r"density $\rho^2$",
        title=r"(d) Task 3: both static waves are PH-compatible",
    )
    save_all(fig, CASE_ROOT / "outputs" / "figures" / "idx63_gold_audit")


def main() -> None:
    configure()
    feature_path = CASE_ROOT / "outputs" / "data" / "idx63_source_figure_features.json"
    features = json.loads(feature_path.read_text(encoding="utf-8"))
    render_source_reproduction(features)
    render_gold_audit(features)
    outputs = []
    for stem in ("idx63_cep_gamma03_reproduction", "idx63_gold_audit"):
        for suffix in (".png", ".svg", ".pdf"):
            path = CASE_ROOT / "outputs" / "figures" / f"{stem}{suffix}"
            outputs.append(
                {
                    "path": str(path.relative_to(CASE_ROOT)),
                    "exists": path.exists(),
                    "bytes": path.stat().st_size if path.exists() else 0,
                }
            )
    write_json(
        CASE_ROOT / "outputs" / "checks" / "idx63_figure_check.json",
        {
            "schema_version": 1,
            "status": "passed" if all(item["bytes"] > 0 for item in outputs) else "failed",
            "outputs": outputs,
            "all_outputs_nonempty": all(item["bytes"] > 0 for item in outputs),
            "source_curve_comparison": features["comparison"],
            "scope": "Supplemental Fig. S1(a) gamma=0.3 plus benchmark audit",
        },
    )


if __name__ == "__main__":
    main()
