from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


WORKSPACE = Path(__file__).resolve().parents[2]
DATA = WORKSPACE / "outputs" / "data"
FIGURES = WORKSPACE / "outputs" / "figures"


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def group_rows(rows: list[dict], key: str) -> dict[str, list[dict]]:
    groups = defaultdict(list)
    for row in rows:
        groups[row[key]].append(row)
    return dict(groups)


def plot_fig1() -> None:
    peak_rows = read_rows(DATA / "fig1_peak_locking.csv")
    eps = np.array([float(row["epsilon"]) for row in peak_rows])
    nonint = np.array([float(row["noninteracting_peak"]) for row in peak_rows])
    interacting = np.array([float(row["interacting_peak"]) for row in peak_rows])

    spectra = read_rows(DATA / "fig1_fourier_spectra.csv")
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 3.8), constrained_layout=True)
    axes[0].plot(eps, nonint, "o-", color="#1f77b4", label="Jz=0")
    axes[0].plot(eps, interacting, "o-", color="black", label="Jz=0.15")
    axes[0].axhline(0.5, color="0.3", linewidth=1)
    axes[0].set_xlabel("epsilon")
    axes[0].set_ylabel("peak frequency")
    axes[0].set_title("subharmonic peak locking")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.2)

    colors = plt.cm.viridis(np.linspace(0.1, 0.9, 5))
    for ax, label, title in [(axes[1], "noninteracting", "Jz=0: peak splits"), (axes[2], "interacting", "Jz=0.15: peak remains locked")]:
        for color, eps_value in zip(colors, [0.0, 0.03, 0.06, 0.10, 0.14]):
            rows = [row for row in spectra if row["case"] == label and abs(float(row["epsilon"]) - eps_value) < 1e-9]
            f = np.array([float(row["frequency"]) for row in rows])
            a = np.array([float(row["amplitude"]) for row in rows])
            ax.plot(f, a, color=color, linewidth=1.6, label=f"{eps_value:g}")
        ax.axvline(0.5, color="red", linestyle="--", alpha=0.7)
        ax.set_xlim(0.25, 0.5)
        ax.set_ylim(0, 1.05)
        ax.set_xlabel("frequency / drive frequency")
        ax.set_title(title)
        ax.grid(alpha=0.2)
    axes[1].set_ylabel("normalized FFT")
    axes[2].legend(title="epsilon", frameon=False, fontsize=8)
    fig.savefig(FIGURES / "fig1_subharmonic_rigidity_reproduction.png", dpi=220)
    plt.close(fig)


def plot_fig2() -> None:
    r_rows = read_rows(DATA / "fig2_level_statistics.csv")
    var_rows = read_rows(DATA / "fig2_variance_h.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.0), constrained_layout=True)

    for L, rows in group_rows(r_rows, "L").items():
        rows = sorted(rows, key=lambda row: float(row["J_z"]))
        axes[0].plot([float(row["J_z"]) for row in rows], [float(row["r_mean"]) for row in rows], "o--", label=f"L={L}")
    axes[0].axhline(0.386, color="0.5", linestyle=":", label="Poisson")
    axes[0].axhline(0.527, color="0.2", linestyle=":", label="COE")
    axes[0].set_xscale("log")
    axes[0].set_xlabel("Jz")
    axes[0].set_ylabel("<r>")
    axes[0].set_title("level statistics proxy")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(alpha=0.2)

    for jz, rows in group_rows(var_rows, "J_z").items():
        rows = sorted(rows, key=lambda row: float(row["epsilon"]))
        axes[1].plot([float(row["epsilon"]) for row in rows], [float(row["var_h"]) for row in rows], "o--", label=f"Jz={float(jz):g}")
    axes[1].set_xscale("log")
    axes[1].set_xlabel("epsilon")
    axes[1].set_ylabel("Var(h)")
    axes[1].set_title("variance peak shifts with Jz")
    axes[1].legend(frameon=False)
    axes[1].grid(alpha=0.2)
    fig.savefig(FIGURES / "fig2_level_statistics_variance_reproduction.png", dpi=220)
    plt.close(fig)


def plot_fig3() -> None:
    rows = read_rows(DATA / "fig3_mutual_information_small_ed.csv")
    fig, ax = plt.subplots(figsize=(5.8, 4.0), constrained_layout=True)
    for L, group in group_rows(rows, "L").items():
        group = sorted(group, key=lambda row: float(row["epsilon"]))
        ax.plot([float(row["epsilon"]) for row in group], [float(row["endpoint_mutual_information"]) for row in group], "o--", label=f"L={L}")
    ax.set_xlabel("epsilon")
    ax.set_ylabel("endpoint mutual information")
    ax.set_title("small-ED mutual information proxy")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.savefig(FIGURES / "fig3_mutual_information_proxy_reproduction.png", dpi=220)
    plt.close(fig)


def plot_fig4() -> None:
    rows = read_rows(DATA / "fig4_long_range_variance_h.csv")
    fig, ax = plt.subplots(figsize=(6.2, 4.2), constrained_layout=True)
    for jz, group in group_rows(rows, "J_z").items():
        group = sorted(group, key=lambda row: float(row["epsilon"]))
        ax.plot([float(row["epsilon"]) for row in group], [float(row["var_h"]) for row in group], "o--", label=f"Jz={float(jz):g}")
    ax.set_xscale("log")
    ax.set_xlabel("epsilon")
    ax.set_ylabel("Var(h)")
    ax.set_title("long-range alpha=1.5 variance feature")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.savefig(FIGURES / "fig4_long_range_variance_reproduction.png", dpi=220)
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    plot_fig1()
    plot_fig2()
    plot_fig3()
    plot_fig4()


if __name__ == "__main__":
    main()
