from __future__ import annotations

import csv
import math
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


def f(row: dict, key: str) -> float:
    return float(row[key])


def group_by(rows: list[dict], key: str) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row[key]].append(row)
    return dict(groups)


def plot_fidelity_vs_disorder() -> None:
    rows = read_rows(DATA / "fidelity_vs_disorder_summary.csv")
    fig, axes = plt.subplots(2, 2, figsize=(12.4, 8.4), constrained_layout=True)
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(group_by(rows, "L"))))
    for color, (L, group) in zip(colors, sorted(group_by(rows, "L").items(), key=lambda item: int(item[0]))):
        group = sorted(group, key=lambda row: f(row, "W"))
        W = np.array([f(row, "W") for row in group])
        V = int(group[0]["V"])
        label = f"L={L}"
        axes[0, 0].plot(W, [f(row, "tilde_chi_typ_r") for row in group], "o-", color=color, label=label, markersize=3)
        axes[0, 1].plot(W * math.sqrt(V), [f(row, "tilde_chi_typ_r") for row in group], "o-", color=color, label=label, markersize=3)
        axes[1, 0].plot(W, [f(row, "gap_ratio") for row in group], "o-", color=color, label=label, markersize=3)
        axes[1, 1].plot(W, [f(row, "ipr") for row in group], "o-", color=color, label=label, markersize=3)
    axes[0, 0].axvline(16.5, color="crimson", linestyle="--", linewidth=1.2, label="paper W2*=16.5")
    axes[0, 1].axvline(41.0, color="crimson", linestyle="--", linewidth=1.2, label="paper W1* sqrt(V)≈41")
    axes[1, 0].axhline(0.5307, color="0.25", linestyle="--", linewidth=1.0, label="GOE 0.5307")
    axes[1, 0].axhline(0.386, color="0.25", linestyle=":", linewidth=1.0, label="Poisson 0.386")
    for ax in axes.flat:
        ax.grid(alpha=0.25)
        ax.legend(frameon=False, fontsize=8)
    axes[0, 0].set_title("Regularized typical fidelity susceptibility")
    axes[0, 0].set_xlabel("disorder W")
    axes[0, 0].set_ylabel("mu chi_typ^r")
    axes[0, 1].set_title("Weak-crossover scaling view")
    axes[0, 1].set_xlabel("W sqrt(V)")
    axes[0, 1].set_ylabel("mu chi_typ^r")
    axes[1, 0].set_title("Gap ratio: chaos window to localization")
    axes[1, 0].set_xlabel("disorder W")
    axes[1, 0].set_ylabel("<r>")
    axes[1, 1].set_title("IPR: real-space localization grows at high W")
    axes[1, 1].set_xlabel("disorder W")
    axes[1, 1].set_ylabel("central-state IPR")
    fig.savefig(FIGURES / "fig1_fidelity_vs_disorder_reproduction.png", dpi=230)
    plt.close(fig)


def plot_a100_paper_subset() -> None:
    rows = read_rows(DATA / "remote_campaign_summary.csv")
    fig, axes = plt.subplots(1, 3, figsize=(15.2, 5.3))
    fig.subplots_adjust(left=0.06, right=0.985, top=0.82, bottom=0.21, wspace=0.27)
    colors = plt.cm.viridis(np.linspace(0.12, 0.88, len(group_by(rows, "L"))))
    for color, (L, group) in zip(
        colors,
        sorted(group_by(rows, "L").items(), key=lambda item: int(item[0])),
    ):
        group = sorted(group, key=lambda row: f(row, "W"))
        W = [f(row, "W") for row in group]
        label = f"L={L}"
        axes[0].plot(
            W,
            [f(row, "tilde_chi_typ_r_mu0.001") for row in group],
            "o-",
            color=color,
            label=label,
            markersize=3,
        )
        axes[1].errorbar(
            W,
            [f(row, "gap_ratio_mean") for row in group],
            yerr=[f(row, "gap_ratio_sem") for row in group],
            fmt="o-",
            color=color,
            label=label,
            markersize=3,
            capsize=2,
        )
        axes[2].plot(
            W,
            [f(row, "ipr_mean") for row in group],
            "o-",
            color=color,
            label=label,
            markersize=3,
        )

    for ax in axes:
        ax.axvline(16.5, color="crimson", linestyle="--", linewidth=1.1, label="paper Wc=16.5")
        ax.set_xlabel("disorder W")
        ax.grid(alpha=0.25)
    axes[0].set_title("Fidelity susceptibility (mu=0.001)")
    axes[0].set_ylabel("mu chi_typ^r")
    axes[1].axhline(0.5307, color="0.3", linestyle=":", linewidth=1.0, label="GOE")
    axes[1].axhline(0.386, color="0.3", linestyle="-.", linewidth=1.0, label="Poisson")
    axes[1].set_title("GOE-to-Poisson crossover")
    axes[1].set_ylabel("mean gap ratio")
    axes[2].set_title("Real-space localization")
    axes[2].set_ylabel("mean IPR")
    for ax in axes:
        ax.legend(frameon=False, fontsize=8)
    fig.suptitle("A100 paper-size subset: L=24/28/31, 605 disorder realizations")
    fig.text(
        0.5,
        0.035,
        "Difference reason: L=32-38 are absent because the available single-A100 dense eigensolver is memory/workspace limited.",
        ha="center",
        va="bottom",
        fontsize=9,
        color="0.25",
    )
    fig.savefig(FIGURES / "fig1_a100_subset_reproduction.png", dpi=230, bbox_inches="tight")
    plt.close(fig)


def plot_weak_crossover() -> None:
    rows = read_rows(DATA / "fidelity_vs_disorder_summary.csv")
    peak_rows = []
    for L, group in sorted(group_by(rows, "L").items(), key=lambda item: int(item[0])):
        group = [row for row in group if 0.2 <= f(row, "W") <= 8.0]
        best = max(group, key=lambda row: f(row, "tilde_chi_typ_r"))
        peak_rows.append({"L": int(L), "V": int(best["V"]), "W_peak": f(best, "W"), "height": f(best, "tilde_chi_typ_r"), "mu_inv": 1.0 / f(best, "mu_star")})
    x = np.array([1.0 / math.sqrt(row["V"]) for row in peak_rows])
    y = np.array([row["W_peak"] for row in peak_rows])
    coeff = float(np.dot(x, y) / np.dot(x, x))

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.6), constrained_layout=True)
    axes[0].plot(x, y, "o", label="local extracted W1*")
    xx = np.linspace(0, max(x) * 1.08, 100)
    axes[0].plot(xx, coeff * xx, label=f"local fit c={coeff:.1f}")
    axes[0].plot(xx, 41.0 * xx, "--", label="paper c≈41")
    axes[0].set_xlabel("1 / sqrt(V)")
    axes[0].set_ylabel("weak peak W1*")
    axes[0].set_title("Weak-disorder peak drifts toward W=0")

    axes[1].loglog([row["mu_inv"] for row in peak_rows], [row["height"] for row in peak_rows], "o-", label="local peak heights")
    axes[1].set_xlabel("mu_star^-1")
    axes[1].set_ylabel("peak mu chi_typ^r")
    axes[1].set_title("Local peak-height trend")
    for ax in axes:
        ax.grid(alpha=0.25)
        handles, _labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend(frameon=False, fontsize=8)
    fig.savefig(FIGURES / "fig2_weak_crossover_scaling_reproduction.png", dpi=230)
    plt.close(fig)


def plot_spectral_function() -> None:
    rows = read_rows(DATA / "spectral_function_summary.csv")
    fig, ax = plt.subplots(figsize=(8.2, 5.4), constrained_layout=True)
    for W, group in sorted(group_by(rows, "W").items(), key=lambda item: float(item[0])):
        group = sorted(group, key=lambda row: f(row, "omega"))
        ax.loglog([f(row, "omega") for row in group], [f(row, "spectral_weight") for row in group], "o-", label=f"W={float(W):g}")
    ax.axvline(1e-2, color="0.4", linestyle=":", linewidth=1.0)
    ax.set_xlabel("energy mismatch omega")
    ax.set_ylabel("binned spectral weight")
    ax.set_title("Spectral-function object used in the paper")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)
    fig.savefig(FIGURES / "fig3_spectral_function_reproduction.png", dpi=230)
    plt.close(fig)


def plot_typical_average() -> None:
    rows = read_rows(DATA / "mu_sweep_summary.csv")
    fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.8), constrained_layout=True)
    for mu, group in sorted(group_by(rows, "mu").items(), key=lambda item: float(item[0])):
        group = sorted(group, key=lambda row: f(row, "W"))
        axes[0].plot([f(row, "W") for row in group], [f(row, "av_typ_ratio") for row in group], "o-", label=f"mu={float(mu):g}", markersize=3)
        axes[1].plot([f(row, "W") for row in group], [f(row, "tilde_chi_typ_r") for row in group], "o-", label=f"mu={float(mu):g}", markersize=3)
    for ax in axes:
        ax.axvline(16.5, color="crimson", linestyle="--", linewidth=1.0, label="W2*=16.5")
        ax.axvline(27.92, color="purple", linestyle=":", linewidth=1.0, label="paper W3≈27.92")
        ax.set_xlabel("disorder W")
        ax.grid(alpha=0.25)
        ax.legend(frameon=False, fontsize=7)
    axes[0].set_ylabel("chi_av^r / chi_typ^r")
    axes[0].set_title("Average and typical separate in localized regime")
    axes[1].set_ylabel("mu chi_typ^r")
    axes[1].set_title("Frequency-cutoff dependence")
    fig.savefig(FIGURES / "fig8_typical_average_reproduction.png", dpi=230)
    plt.close(fig)


def plot_perturbation() -> None:
    rows = read_rows(DATA / "perturbation_theory_summary.csv")
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.7), constrained_layout=True)
    for mu, group in sorted(group_by(rows, "mu").items(), key=lambda item: float(item[0])):
        group = sorted(group, key=lambda row: f(row, "W"))
        label = "mu=0 proxy" if float(mu) == 0 else f"mu={float(mu):g}"
        axes[0].loglog([f(row, "W") for row in group], [f(row, "chi_typ_numeric") for row in group], "o-", label=f"numeric {label}")
        axes[0].loglog([f(row, "W") for row in group], [f(row, "chi_typ_perturbative") for row in group], "--", label=f"perturbative {label}")
        axes[1].plot([f(row, "W") for row in group], [f(row, "scaled_W2_numeric") for row in group], "o-", label=f"numeric {label}")
        axes[1].plot([f(row, "W") for row in group], [f(row, "scaled_W2_perturbative") for row in group], "--", label=f"perturbative {label}")
    axes[0].set_xlabel("disorder W")
    axes[0].set_ylabel("chi_typ^r or chi_typ")
    axes[0].set_title("Strong-disorder perturbative trend")
    axes[1].set_xlabel("disorder W")
    axes[1].set_ylabel("W^2 times susceptibility")
    axes[1].set_title("1/W^2 expectation becomes flatter at large W")
    for ax in axes:
        ax.axvspan(20, 28, color="purple", alpha=0.08)
        ax.grid(alpha=0.25, which="both")
        ax.legend(frameon=False, fontsize=7)
    fig.savefig(FIGURES / "fig10_perturbation_reproduction.png", dpi=230)
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    plot_fidelity_vs_disorder()
    plot_a100_paper_subset()
    plot_weak_crossover()
    plot_spectral_function()
    plot_typical_average()
    plot_perturbation()
    print("figures generated")


if __name__ == "__main__":
    main()
