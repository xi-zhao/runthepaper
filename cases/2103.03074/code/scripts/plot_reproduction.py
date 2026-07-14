from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


WORKSPACE = Path(__file__).resolve().parents[2]
DATA = WORKSPACE / "outputs" / "data"
FIGURES = WORKSPACE / "outputs" / "figures"
FEATURE_DIFFERENCE_REASON = (
    "Difference reason: 18-qubit random-circuit feature check; the paper uses "
    "a 53-qubit Sycamore tensor-network contraction."
)
TABLE_DIFFERENCE_REASON = (
    "Difference reason: paper-reported estimates only; the 53-qubit contraction "
    "was not rerun (reported: 149 days on one A100)."
)


def read_probability_csv(path: Path) -> tuple[np.ndarray, np.ndarray]:
    scaled = []
    conditional_scaled = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scaled.append(float(row["scaled_Np"]))
            conditional_scaled.append(float(row["scaled_conditional_Lp"]))
    return np.asarray(scaled), np.asarray(conditional_scaled)


def read_curve_csv(path: Path) -> tuple[np.ndarray, np.ndarray]:
    fractions = []
    xeb = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            fractions.append(float(row["fraction"]))
            xeb.append(float(row["xeb"]))
    return np.asarray(fractions), np.asarray(xeb)


def plot_histogram(ax: plt.Axes, scaled: np.ndarray, xmax: float, title: str) -> None:
    bins = np.linspace(0.0, xmax, 64)
    ax.hist(scaled, bins=bins, density=True, color="#1f77b4", edgecolor="#1f77b4")
    xs = np.linspace(0.0, xmax, 400)
    ax.plot(xs, np.exp(-xs), color="red", linewidth=2.5)
    ax.set_yscale("log")
    ax.set_ylim(1e-4, 1.05)
    ax.set_xlim(0, xmax)
    ax.set_xlabel("Np")
    ax.set_ylabel("Prob(Np)")
    ax.set_title(title)
    ax.grid(alpha=0.18, linewidth=0.5)


def plot_postselection(ax: plt.Axes, fractions: np.ndarray, xeb: np.ndarray, title: str) -> None:
    ax.plot(100 * fractions, xeb, "o--", color="red", linewidth=2.5, markersize=6)
    ax.plot(100 * fractions, -np.log(fractions), color="#444444", alpha=0.35, linewidth=1.5)
    ax.set_xlabel("Percentage of bitstrings")
    ax.set_ylabel("XEB")
    ax.set_title(title)
    ax.set_xlim(5, 105)
    ax.set_ylim(-0.1, max(2.45, float(np.max(xeb)) + 0.15))
    ax.grid(alpha=0.18, linewidth=0.5)


def plot_depth(label: str, title: str, output_name: str) -> None:
    scaled, _ = read_probability_csv(DATA / f"{label}_big_batch_probabilities.csv")
    fractions, xeb = read_curve_csv(DATA / f"{label}_postselection_xeb.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6))
    plot_histogram(axes[0], scaled, 8.0, f"{title}: batch probabilities")
    plot_postselection(axes[1], fractions, xeb, f"{title}: post-selected XEB")
    fig.tight_layout(rect=(0, 0.14, 1, 1))
    fig.text(0.5, 0.025, FEATURE_DIFFERENCE_REASON, ha="center", va="bottom", fontsize=8.2)
    fig.savefig(FIGURES / output_name, dpi=220)
    plt.close(fig)


def plot_conditional() -> None:
    _, cond20 = read_probability_csv(DATA / "depth20_big_batch_probabilities.csv")
    _, cond14 = read_probability_csv(DATA / "depth14_big_batch_probabilities.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6))
    plot_histogram(axes[0], cond20, 8.0, "depth 20: conditional probabilities")
    plot_histogram(axes[1], cond14, 8.0, "depth 14: conditional probabilities")
    fig.tight_layout(rect=(0, 0.14, 1, 1))
    fig.text(0.5, 0.025, FEATURE_DIFFERENCE_REASON, ha="center", va="bottom", fontsize=8.2)
    fig.savefig(FIGURES / "fig6_conditional_probability_reproduction.png", dpi=220)
    plt.close(fig)


def plot_table_summary() -> None:
    methods = []
    bitstrings = []
    time_complexity = []
    with (DATA / "table2_method_comparison_arxiv.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row["time_complexity"]:
                methods.append(row["method"])
                bitstrings.append(float(row["bitstrings"]))
                time_complexity.append(float(row["time_complexity"]))

    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.5))
    axes[0].bar(methods, bitstrings, color=["#8da0cb", "#66c2a5", "#fc8d62"])
    axes[0].set_yscale("log")
    axes[0].set_ylabel("# bitstrings")
    axes[0].set_title("Reported batch size")
    axes[0].grid(axis="y", alpha=0.2)

    axes[1].bar(methods, time_complexity, color=["#8da0cb", "#66c2a5", "#fc8d62"])
    axes[1].set_yscale("log")
    axes[1].set_ylabel("time complexity")
    axes[1].set_title("Reported contraction cost")
    axes[1].grid(axis="y", alpha=0.2)
    fig.tight_layout(rect=(0, 0.16, 1, 1))
    fig.text(0.5, 0.025, TABLE_DIFFERENCE_REASON, ha="center", va="bottom", fontsize=8.0)
    fig.savefig(FIGURES / "table2_method_comparison_reproduction.png", dpi=220)
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    plot_depth("depth20", "Fig. 2 feature reproduction", "fig2_depth20_reproduction.png")
    plot_depth("depth14", "Fig. 5 feature reproduction", "fig5_depth14_reproduction.png")
    plot_conditional()
    plot_table_summary()


if __name__ == "__main__":
    main()
