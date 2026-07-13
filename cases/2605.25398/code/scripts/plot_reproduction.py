from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


WORKSPACE = Path(__file__).resolve().parents[2]
DATA = WORKSPACE / "outputs" / "data"
FIGURES = WORKSPACE / "outputs" / "figures"


COLORS = {
    "chaotic_GOE": "#0072b2",
    "integrable_Poisson": "#d55e00",
}


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def by_key(rows: list[dict], key: str) -> dict[str, list[dict]]:
    groups = defaultdict(list)
    for row in rows:
        groups[row[key]].append(row)
    return dict(groups)


def as_float(row: dict, key: str) -> float:
    return float(row[key])


def plot_main_probes() -> None:
    fig, axes = plt.subplots(3, 1, figsize=(8.8, 9.4), sharex=True, constrained_layout=True)
    for ensemble in ["chaotic_GOE", "integrable_Poisson"]:
        rows = sorted(read_rows(DATA / f"ideal_{ensemble}_metrics.csv"), key=lambda row: as_float(row, "time"))
        time = np.array([as_float(row, "time") for row in rows])
        axes[0].plot(time, [as_float(row, "pt_wasserstein") for row in rows], color=COLORS[ensemble], label=ensemble)
        axes[1].plot(time, [as_float(row, "entropy_mean") for row in rows], color=COLORS[ensemble], label=ensemble)
        axes[2].plot(time, [as_float(row, "sff4_mean") for row in rows], color=COLORS[ensemble], label=ensemble)
    axes[1].axhline(-1 + sum(1 / i for i in range(1, 29)), color="0.35", linestyle=":", label="Haar entropy, D=28")
    for ax in axes:
        ax.axvline(1.79, color="black", linestyle="--", linewidth=1.0, alpha=0.7)
        ax.set_xscale("log")
        ax.grid(alpha=0.22)
        ax.legend(frameon=False, fontsize=8)
    axes[0].set_ylabel("W1 distance to PT")
    axes[1].set_ylabel("Shannon entropy")
    axes[2].set_ylabel("4-point SFF proxy")
    axes[2].set_xlabel("evolution time")
    axes[0].set_title("Reproduced chaos probes from boson-sampling probabilities")
    fig.savefig(FIGURES / "fig3_main_probes_reproduction.png", dpi=230)
    plt.close(fig)


def plot_output_distributions() -> None:
    fig, axes = plt.subplots(2, 1, figsize=(11.0, 7.2), constrained_layout=True)
    for ax, ensemble in zip(axes, ["integrable_Poisson", "chaotic_GOE"]):
        rows = [
            row
            for row in read_rows(DATA / f"sparse_{ensemble}_output_distributions.csv")
            if abs(as_float(row, "time") - 1.79) < 1e-9 and int(row["sample_index"]) == 0
        ]
        rows = sorted(rows, key=lambda row: row["output_pair"])
        labels = [row["output_pair"] for row in rows]
        values = [as_float(row, "probability") for row in rows]
        overlaps = [int(row["overlap"]) for row in rows]
        colors = ["#4c78a8" if overlap == 0 else "#f58518" if overlap == 1 else "#54a24b" for overlap in overlaps]
        ax.bar(np.arange(len(rows)), values, color=colors, edgecolor="white", linewidth=0.4)
        ax.set_title(f"{ensemble}: conditional two-photon output distribution at t=1.79")
        ax.set_ylabel("probability")
        ax.set_xticks(np.arange(len(rows)))
        ax.set_xticklabels(labels, rotation=75, fontsize=7)
        ax.grid(axis="y", alpha=0.22)
    axes[-1].set_xlabel("collision-free output pair")
    fig.savefig(FIGURES / "fig2_output_distribution_reproduction.png", dpi=230)
    plt.close(fig)


def plot_otoc_pr() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14.6, 4.6), constrained_layout=True)
    for ensemble in ["chaotic_GOE", "integrable_Poisson"]:
        rows = sorted(read_rows(DATA / f"ideal_{ensemble}_metrics.csv"), key=lambda row: as_float(row, "time"))
        time = np.array([as_float(row, "time") for row in rows])
        axes[0].plot(time, [as_float(row, "target_otoc_mean") for row in rows], color=COLORS[ensemble], label=ensemble)
        axes[2].plot(time, [as_float(row, "participation_ratio_mean") for row in rows], color=COLORS[ensemble], label=ensemble)
        sector_rows = read_rows(DATA / f"ideal_{ensemble}_otoc_sectors.csv")
        for overlap, marker in [(0, "-"), (1, "--")]:
            group = sorted([row for row in sector_rows if int(row["overlap"]) == overlap], key=lambda row: as_float(row, "time"))
            axes[1].plot(
                [as_float(row, "time") for row in group],
                [as_float(row, "probability_mean") for row in group],
                linestyle=marker,
                color=COLORS[ensemble],
                label=f"{ensemble}, overlap {overlap}",
            )
    for ax in axes:
        ax.set_xscale("log")
        ax.axvline(1.79, color="black", linestyle="--", linewidth=1.0, alpha=0.7)
        ax.grid(alpha=0.22)
        ax.legend(frameon=False, fontsize=7)
        ax.set_xlabel("evolution time")
    axes[0].set_ylabel("target output probability")
    axes[1].set_ylabel("sector-averaged probability")
    axes[2].set_ylabel("participation ratio")
    axes[0].set_title("Representative OTOC-equivalent output")
    axes[1].set_title("Overlap-sector memory")
    axes[2].set_title("Hilbert-space delocalization")
    fig.savefig(FIGURES / "fig4_otoc_pr_reproduction.png", dpi=230)
    plt.close(fig)


def plot_conditional_probability_demo() -> None:
    rows = read_rows(DATA / "appendix_conditional_probability_demo.csv")
    fig, ax = plt.subplots(figsize=(8.8, 5.2), constrained_layout=True)
    for d, group in by_key(rows, "D").items():
        group = sorted(group, key=lambda row: as_float(row, "p"))
        ax.plot(
            [as_float(row, "p") for row in group],
            [as_float(row, "conditional_density") for row in group],
            label=f"conditional D={d}",
            linewidth=1.5,
        )
    d28 = sorted([row for row in rows if row["D"] == "28"], key=lambda row: as_float(row, "p"))
    ax.plot(
        [as_float(row, "p") for row in d28],
        [as_float(row, "porter_thomas_density") for row in d28],
        color="black",
        linestyle="--",
        linewidth=1.7,
        label="PT reference for D=28",
    )
    ax.set_xlabel("conditional probability p")
    ax.set_ylabel("density")
    ax.set_title("Conditional collision-free probabilities approach Porter-Thomas at D=28")
    ax.grid(alpha=0.22)
    ax.legend(frameon=False, fontsize=8)
    fig.savefig(FIGURES / "figS1_conditional_probability_reproduction.png", dpi=230)
    plt.close(fig)


def plot_scaling_summary() -> None:
    rows = read_rows(DATA / "appendix_scaling_summary.csv")
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.4), constrained_layout=True)
    for ensemble in ["chaotic_GOE", "integrable_Poisson"]:
        group = sorted([row for row in rows if row["ensemble"] == ensemble], key=lambda row: int(row["modes"]))
        modes = [int(row["modes"]) for row in group]
        axes[0].plot(modes, [as_float(row, "time_min_pt") for row in group], "o-", color=COLORS[ensemble], label=f"{ensemble}: min PT")
        axes[0].plot(modes, [as_float(row, "time_max_entropy") for row in group], "s--", color=COLORS[ensemble], label=f"{ensemble}: max entropy")
        axes[1].plot(modes, [as_float(row, "min_pt_wasserstein") for row in group], "o-", color=COLORS[ensemble], label=ensemble)
        axes[2].plot(modes, [as_float(row, "entropy_gap_percent") for row in group], "o-", color=COLORS[ensemble], label=ensemble)
    axes[0].axhline(1.79, color="black", linestyle=":", linewidth=1.0)
    axes[0].set_ylabel("diagnostic time")
    axes[1].set_ylabel("minimum PT W1")
    axes[2].set_ylabel("entropy gap to Haar (%)")
    for ax in axes:
        ax.set_xlabel("number of optical modes M")
        ax.grid(alpha=0.22)
        ax.legend(frameon=False, fontsize=7)
    axes[0].set_title("Diagnostic times")
    axes[1].set_title("PT distance improves with scale")
    axes[2].set_title("Entropy approaches Haar prediction")
    fig.savefig(FIGURES / "figS4_scaling_reproduction.png", dpi=230)
    plt.close(fig)


def plot_ideal_otocs_full() -> None:
    rows = read_rows(DATA / "appendix_ideal_otocs_full.csv")
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), sharey=True, constrained_layout=True)
    for ax, ensemble in zip(axes, ["chaotic_GOE", "integrable_Poisson"]):
        group = [row for row in rows if row["ensemble"] == ensemble]
        for output_pair, curve in by_key(group, "output_pair").items():
            curve = sorted(curve, key=lambda row: as_float(row, "time"))
            overlap = int(curve[0]["overlap"])
            color = "#4c78a8" if overlap == 0 else "#e45756"
            ax.plot(
                [as_float(row, "time") for row in curve],
                [as_float(row, "otoc") for row in curve],
                color=color,
                alpha=0.22,
                linewidth=0.8,
            )
        for overlap, color in [(0, "#4c78a8"), (1, "#e45756")]:
            by_time = defaultdict(list)
            for row in group:
                if int(row["overlap"]) == overlap:
                    by_time[as_float(row, "time")].append(as_float(row, "otoc"))
            times = np.array(sorted(by_time.keys()))
            values = np.array([np.mean(by_time[time]) for time in times])
            ax.plot(times, values, color=color, linewidth=2.4, label=f"overlap {overlap} sector average")
        ax.axvline(1.79, color="black", linestyle="--", linewidth=1.0, alpha=0.7)
        ax.set_xscale("log")
        ax.set_xlabel("evolution time")
        ax.set_title(ensemble)
        ax.grid(alpha=0.22)
        ax.legend(frameon=False, fontsize=8)
    axes[0].set_ylabel("OTOC-equivalent probability")
    fig.suptitle("Ideal OTOCs for all collision-free output configurations")
    fig.savefig(FIGURES / "figS5_ideal_otocs_reproduction.png", dpi=230)
    plt.close(fig)


def plot_extra_otoc() -> None:
    short_rows = read_rows(DATA / "appendix_otoc_short_time.csv")
    spectrum_rows = read_rows(DATA / "appendix_otoc_fft_spectrum.csv")
    fft_pr_rows = read_rows(DATA / "appendix_otoc_fft_pr.csv")
    fig, axes = plt.subplots(1, 3, figsize=(14.8, 4.5), constrained_layout=True)

    for overlap in [0, 1]:
        group = [row for row in short_rows if row["ensemble"] == "chaotic_GOE" and int(row["overlap"]) == overlap]
        by_time = defaultdict(list)
        for row in group:
            by_time[as_float(row, "time")].append(as_float(row, "otoc"))
        times = np.array(sorted(by_time.keys()))
        values = np.array([np.mean(by_time[time]) for time in times])
        axes[0].loglog(times, values, label=f"overlap {overlap}")
        mask = (times < 0.08) & (values > 0)
        slope, intercept = np.polyfit(np.log(times[mask]), np.log(values[mask]), 1)
        axes[0].loglog(times[mask], np.exp(intercept) * times[mask] ** slope, "--", color="0.35")
        axes[0].text(times[mask][-1], np.exp(intercept) * times[mask][-1] ** slope, f"{slope:.1f}", fontsize=8)

    for ensemble in ["chaotic_GOE", "integrable_Poisson"]:
        group = sorted([row for row in spectrum_rows if row["ensemble"] == ensemble], key=lambda row: as_float(row, "frequency"))
        axes[1].plot(
            [as_float(row, "frequency") for row in group],
            [as_float(row, "normalized_power") for row in group],
            color=COLORS[ensemble],
            label=ensemble,
        )

    for x, ensemble in enumerate(["integrable_Poisson", "chaotic_GOE"]):
        values = [as_float(row, "fft_participation_ratio") for row in fft_pr_rows if row["ensemble"] == ensemble]
        axes[2].scatter(np.full(len(values), x) + np.linspace(-0.16, 0.16, len(values)), values, s=18, alpha=0.75, color=COLORS[ensemble])
        axes[2].plot([x - 0.22, x + 0.22], [np.mean(values), np.mean(values)], color="black", linewidth=2)

    axes[0].set_xlabel("short time")
    axes[0].set_ylabel("averaged OTOC-equivalent probability")
    axes[0].set_title("Short-time power laws")
    axes[1].set_xlabel("frequency")
    axes[1].set_ylabel("normalized FFT power")
    axes[1].set_title("Late-time fluctuation spectrum")
    axes[2].set_xticks([0, 1])
    axes[2].set_xticklabels(["integrable", "chaotic"])
    axes[2].set_ylabel("FFT participation ratio")
    axes[2].set_title("Frequency-space delocalization")
    for ax in axes:
        ax.grid(alpha=0.22)
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend(frameon=False, fontsize=8)
    fig.savefig(FIGURES / "figS6_extra_otoc_reproduction.png", dpi=230)
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    plot_output_distributions()
    plot_main_probes()
    plot_otoc_pr()
    plot_conditional_probability_demo()
    plot_scaling_summary()
    plot_ideal_otocs_full()
    plot_extra_otoc()


if __name__ == "__main__":
    main()
