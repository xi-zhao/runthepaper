from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "outputs" / "data"
FIG_DIR = ROOT / "outputs" / "figures"
CHECK_DIR = ROOT / "outputs" / "checks"


def read_rows(path: Path) -> list[dict[str, float]]:
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            converted: dict[str, float] = {}
            for key, value in row.items():
                try:
                    converted[key] = float(value)
                except (TypeError, ValueError):
                    pass
            rows.append(converted)
    return rows


def save(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def plot_infidelity(rows: list[dict[str, float]]) -> None:
    p = np.array([row["p"] for row in rows])
    exact = np.array([row["exact_infidelity"] for row in rows])
    mc = np.array([row["mc_infidelity"] for row in rows])
    se = np.array([row["infidelity_standard_error"] for row in rows])

    plt.figure(figsize=(6.2, 4.2))
    plt.loglog(p, exact, "-o", color="#1f77b4", label="reference estimator")
    plt.errorbar(p, mc, yerr=2 * se, fmt="s", color="#ff7f0e", label="propagated-error MC")
    plt.xlabel("physical error rate p")
    plt.ylabel("logical infidelity proxy")
    plt.title("Magic-state-preparation fidelity feature")
    plt.grid(True, which="both", alpha=0.25)
    plt.legend(frameon=False)
    save(FIG_DIR / "fig1_infidelity_reproduction.png")


def plot_acceptance(rows: list[dict[str, float]]) -> None:
    p = np.array([row["p"] for row in rows])
    exact = np.array([row["exact_acceptance"] for row in rows])
    mc = np.array([row["mc_acceptance"] for row in rows])
    se = np.array([row["acceptance_standard_error"] for row in rows])

    plt.figure(figsize=(6.2, 4.2))
    plt.semilogx(p, exact, "-o", color="#1f77b4", label="reference estimator")
    plt.errorbar(p, mc, yerr=2 * se, fmt="s", color="#ff7f0e", label="propagated-error MC")
    plt.xlabel("physical error rate p")
    plt.ylabel("postselection acceptance rate")
    plt.title("Acceptance decreases with circuit-level noise")
    plt.grid(True, which="both", alpha=0.25)
    plt.legend(frameon=False)
    save(FIG_DIR / "fig2_acceptance_reproduction.png")


def plot_runtime(rows: list[dict[str, float]]) -> None:
    p = np.array([row["p"] for row in rows])
    state = np.array([row["statevector_like_time_per_shot_us"] for row in rows])
    prop = np.array([row["propagated_clifford_time_per_shot_us"] for row in rows])
    speedup = np.array([row["speedup_ratio"] for row in rows])

    fig, ax1 = plt.subplots(figsize=(6.4, 4.2))
    ax1.loglog(p, state, "-o", color="#1f77b4", label="state-vector-like")
    ax1.loglog(p, prop, "-s", color="#ff7f0e", label="propagated Clifford")
    ax1.set_xlabel("physical error rate p")
    ax1.set_ylabel("time per shot (us)")
    ax1.grid(True, which="both", alpha=0.25)
    ax2 = ax1.twinx()
    ax2.semilogx(p, speedup, "--", color="#2ca02c", label="speedup")
    ax2.set_ylabel("speedup ratio")
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, frameon=False, loc="best")
    plt.title("Runtime feature: error propagation is cheap at low p")
    save(FIG_DIR / "fig3_runtime_reproduction.png")


def plot_method_checks(sampling_rows: list[dict[str, float]]) -> None:
    shots = np.array([row["shots"] for row in sampling_rows])
    std = np.array([row["estimate_std"] for row in sampling_rows])
    scaled = np.array([row["scaled_std_times_sqrt_n"] for row in sampling_rows])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.8))
    ax1.loglog(shots, std, "-o", color="#9467bd")
    ax1.set_xlabel("shots")
    ax1.set_ylabel("std. of infidelity estimate")
    ax1.set_title("Monte Carlo precision")
    ax1.grid(True, which="both", alpha=0.25)

    ax2.semilogx(shots, scaled, "-o", color="#8c564b")
    ax2.set_xlabel("shots")
    ax2.set_ylabel("std x sqrt(shots)")
    ax2.set_title("1/sqrt(N) behavior")
    ax2.grid(True, which="both", alpha=0.25)
    save(FIG_DIR / "fig4_sampling_precision_reproduction.png")


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    benchmark = read_rows(DATA_DIR / "fidelity_acceptance_benchmark.csv")
    runtime = read_rows(DATA_DIR / "runtime_proxy_benchmark.csv")
    sampling = read_rows(DATA_DIR / "sampling_scaling.csv")

    plot_infidelity(benchmark)
    plot_acceptance(benchmark)
    plot_runtime(runtime)
    plot_method_checks(sampling)

    payload = {
        "status": "passed",
        "figures": [
            "outputs/figures/fig1_infidelity_reproduction.png",
            "outputs/figures/fig2_acceptance_reproduction.png",
            "outputs/figures/fig3_runtime_reproduction.png",
            "outputs/figures/fig4_sampling_precision_reproduction.png",
        ],
    }
    (CHECK_DIR / "plot_generation_check.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
