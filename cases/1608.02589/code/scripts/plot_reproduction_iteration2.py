#!/usr/bin/env python3
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
    grouped = defaultdict(list)
    for row in rows:
        grouped[row[key]].append(row)
    return dict(grouped)


def plot_fig1_l14() -> None:
    peak_rows = read_rows(DATA / "iteration2_fig1_peak_locking_L14.csv")
    spectra_rows = read_rows(DATA / "iteration2_fig1_fourier_spectra_L14.csv")

    fig, axes = plt.subplots(1, 3, figsize=(13.6, 3.8), constrained_layout=True)
    eps = np.array([float(row["epsilon"]) for row in peak_rows])
    nonint = np.array([float(row["noninteracting_peak_signed"]) for row in peak_rows])
    interacting = np.array([float(row["interacting_peak"]) for row in peak_rows])
    axes[0].plot(eps, nonint, "o-", color="#1f77b4", label="Jz=0 analytic")
    axes[0].plot(eps, interacting, "o-", color="black", label="Jz=0.15, L=14")
    axes[0].axhline(0.5, color="0.35", linewidth=1)
    axes[0].set_xlabel("epsilon")
    axes[0].set_ylabel("peak frequency")
    axes[0].set_title("rigid half-frequency peak")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(alpha=0.2)

    colors = plt.cm.plasma(np.linspace(0.08, 0.86, 5))
    for ax, label, title in [
        (axes[1], "noninteracting", "free spins: detuning splits the peak"),
        (axes[2], "interacting", "interacting DTC: peak stays at 1/2"),
    ]:
        for color, eps_value in zip(colors, [0.0, 0.03, 0.06, 0.10, 0.14]):
            rows = [
                row
                for row in spectra_rows
                if row["case"] == label and abs(float(row["epsilon"]) - eps_value) < 1e-12
            ]
            f = np.array([float(row["frequency"]) for row in rows])
            amp = np.array([float(row["amplitude"]) for row in rows])
            ax.plot(f, amp, color=color, linewidth=1.7, label=f"{eps_value:g}")
        ax.axvline(0.5, color="#d62728", linestyle="--", alpha=0.75)
        ax.set_xlim(0.25, 0.5)
        ax.set_ylim(0, 1.05)
        ax.set_xlabel("frequency / drive frequency")
        ax.set_title(title)
        ax.grid(alpha=0.2)
    axes[1].set_ylabel("normalized FFT")
    axes[2].legend(title="epsilon", frameon=False, fontsize=8)
    fig.savefig(FIGURES / "iteration2_fig1_L14_subharmonic_rigidity.png", dpi=230)
    plt.close(fig)


def plot_phase_proxy() -> None:
    rows = sorted(read_rows(DATA / "iteration2_fig1_phase_boundary_proxy.csv"), key=lambda row: float(row["J_z"]))
    fig, ax = plt.subplots(figsize=(5.8, 4.0), constrained_layout=True)
    ax.plot(
        [float(row["J_z"]) for row in rows],
        [float(row["epsilon_peak"]) for row in rows],
        "o-",
        color="#2ca02c",
        label="variance-peak boundary proxy",
    )
    ax.set_xlabel("Jz")
    ax.set_ylabel("epsilon at max Var(h)")
    ax.set_title("local phase-boundary proxy")
    ax.grid(alpha=0.2)
    ax.legend(frameon=False)
    fig.savefig(FIGURES / "iteration2_fig1_phase_boundary_proxy.png", dpi=230)
    plt.close(fig)


def plot_fig2() -> None:
    level_rows = read_rows(DATA / "iteration2_fig2_level_statistics_L6_L8_L10.csv")
    variance_rows = read_rows(DATA / "iteration2_fig2_variance_L10.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.0), constrained_layout=True)

    for l_value, rows in sorted(group_rows(level_rows, "L").items(), key=lambda item: int(item[0])):
        rows = sorted(rows, key=lambda row: float(row["J_z"]))
        axes[0].plot(
            [float(row["J_z"]) for row in rows],
            [float(row["r_mean"]) for row in rows],
            "o--",
            label=f"L={l_value}",
        )
    axes[0].axhline(0.386, color="0.55", linestyle=":", label="Poisson")
    axes[0].axhline(0.527, color="0.25", linestyle=":", label="COE")
    axes[0].set_xscale("log")
    axes[0].set_xlabel("Jz")
    axes[0].set_ylabel("<r>")
    axes[0].set_title("Floquet level statistics")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(alpha=0.2)

    for j_z, rows in sorted(group_rows(variance_rows, "J_z").items(), key=lambda item: float(item[0])):
        rows = sorted(rows, key=lambda row: float(row["epsilon"]))
        axes[1].plot(
            [float(row["epsilon"]) for row in rows],
            [float(row["var_h"]) for row in rows],
            "o--",
            label=f"Jz={float(j_z):g}",
        )
    axes[1].set_xscale("log")
    axes[1].set_xlabel("epsilon")
    axes[1].set_ylabel("Var(h)")
    axes[1].set_title("transition from variance of h")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(alpha=0.2)
    fig.savefig(FIGURES / "iteration2_fig2_level_statistics_variance_L10.png", dpi=230)
    plt.close(fig)


def plot_fig3() -> None:
    rows = read_rows(DATA / "iteration2_fig3_mutual_information_corrected.csv")
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 3.8), sharey=True, constrained_layout=True)
    for ax, j_z in zip(axes, ["0.050000000000", "0.100000000000", "0.150000000000"]):
        group = [row for row in rows if row["J_z"] == j_z]
        for l_value, l_rows in sorted(group_rows(group, "L").items(), key=lambda item: int(item[0])):
            l_rows = sorted(l_rows, key=lambda row: float(row["epsilon"]))
            ax.plot(
                [float(row["epsilon"]) for row in l_rows],
                [float(row["endpoint_mutual_information"]) for row in l_rows],
                "o--",
                label=f"L={l_value}",
            )
        ax.axhline(np.log(2), color="0.35", linestyle=":", label="log 2" if ax is axes[0] else None)
        ax.set_title(f"Jz={float(j_z):g}")
        ax.set_xlabel("epsilon")
        ax.grid(alpha=0.2)
    axes[0].set_ylabel("endpoint mutual information")
    axes[0].legend(frameon=False, fontsize=8)
    fig.suptitle("corrected mutual-information flow")
    fig.savefig(FIGURES / "iteration2_fig3_mutual_information_corrected.png", dpi=230)
    plt.close(fig)


def plot_fig4() -> None:
    rows = read_rows(DATA / "iteration2_fig4_long_range_variance_L10.csv")
    fig, ax = plt.subplots(figsize=(6.4, 4.2), constrained_layout=True)
    for j_z, group in sorted(group_rows(rows, "J_z").items(), key=lambda item: float(item[0])):
        group = sorted(group, key=lambda row: float(row["epsilon"]))
        ax.plot(
            [float(row["epsilon"]) for row in group],
            [float(row["var_h"]) for row in group],
            "o--",
            label=f"Jz={float(j_z):g}",
        )
    ax.set_xscale("log")
    ax.set_xlabel("epsilon")
    ax.set_ylabel("Var(h)")
    ax.set_title("long-range alpha=1.5 DTC transition proxy")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.2)
    fig.savefig(FIGURES / "iteration2_fig4_long_range_variance_L10.png", dpi=230)
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    plot_fig1_l14()
    plot_phase_proxy()
    plot_fig2()
    plot_fig3()
    plot_fig4()


if __name__ == "__main__":
    main()
