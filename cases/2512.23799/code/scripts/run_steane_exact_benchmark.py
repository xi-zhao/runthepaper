#!/usr/bin/env python3
"""Run the reconstructed Steane |Hbar> preparation protocol.

The default smoke profile verifies that the exact circuit executes without
overwriting the published paper-profile artifacts.  The paper profile uses
the shot counts behind the public benchmark and can take hours on a laptop.

This script deliberately generates only independent numerical data.  Paper
curves digitized for internal validation are not distributed by RunThePaper.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


CASE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CASE_ROOT / "code/src"))

import steane_h_prep as sim  # noqa: E402


PAPER_P_GRID = [
    0.001,
    0.002125,
    0.00325,
    0.004375,
    0.0055,
    0.006625,
    0.00775,
    0.008875,
    0.01,
    0.02,
    0.035,
    0.05,
]
CONFIG = {
    "stab_schedule": "asap",
    "idle_policy": "active_window",
    "encoding": "explicit_no_idle",
}
FIELDS = [
    "p",
    "shots",
    "error_shots",
    "accepted",
    "acceptance_rate",
    "acceptance_se",
    "fidelity",
    "infidelity",
    "infidelity_se",
    "locations",
]


def paper_shots(p: float) -> int:
    if p < 0.006:
        return 100_000
    if p < 0.02:
        return 50_000
    return 30_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("smoke", "paper"), default="smoke")
    parser.add_argument("--seed", type=int, default=2512)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sim.set_protocol_config(
        CONFIG["stab_schedule"], CONFIG["idle_policy"], CONFIG["encoding"]
    )
    if args.profile == "paper":
        p_grid = PAPER_P_GRID
        shots_for = paper_shots
        stem = "steane_exact_benchmark"
    else:
        p_grid = [0.001, 0.01, 0.05]
        shots_for = lambda _p: 200
        stem = "steane_exact_smoke"

    started = time.perf_counter()
    rows = []
    for index, p in enumerate(p_grid):
        result = sim.run_point(p, shots_for(p), seed=args.seed + index)
        rows.append(result)
        print(
            json.dumps(
                {
                    key: result[key]
                    for key in ("p", "shots", "acceptance_rate", "infidelity")
                }
            ),
            flush=True,
        )

    data_path = CASE_ROOT / f"outputs/data/{stem}.csv"
    check_path = CASE_ROOT / f"outputs/checks/{stem}.json"
    figure_path = CASE_ROOT / f"outputs/figures/{stem}_reproduction.png"
    for path in (data_path, check_path, figure_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    with data_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    checks = {
        "schema_version": 1,
        "status": "completed",
        "profile": args.profile,
        "protocol": "exact_fig_ch_meas_circ_state_vector_monte_carlo",
        "configuration": CONFIG,
        "seed": args.seed,
        "p_grid": p_grid,
        "shots_total": sum(int(row["shots"]) for row in rows),
        "locations": len(sim.LOCATIONS),
        "runtime_seconds": round(time.perf_counter() - started, 3),
        "data_path": str(data_path.relative_to(CASE_ROOT)),
        "reference_policy": (
            "Independent results only. Digitized paper point sets are not distributed."
        ),
    }
    check_path.write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
    plot_generated(rows, figure_path)
    print(json.dumps(checks, indent=2))
    return 0


def plot_generated(rows: list[dict], output: Path) -> None:
    ps = [float(row["p"]) for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.4))
    axes[0].errorbar(
        ps,
        [float(row["acceptance_rate"]) for row in rows],
        yerr=[float(row["acceptance_se"]) for row in rows],
        fmt="o-",
        color="tab:green",
    )
    axes[0].set_ylabel("acceptance rate")
    axes[0].set_title("Exact-circuit acceptance")
    axes[1].errorbar(
        ps,
        [float(row["infidelity"]) for row in rows],
        yerr=[float(row["infidelity_se"]) for row in rows],
        fmt="o-",
        color="tab:green",
    )
    axes[1].set_yscale("log")
    axes[1].set_ylabel("logical infidelity")
    axes[1].set_title("Exact-circuit infidelity")
    for axis in axes:
        axis.set_xscale("log")
        axis.set_xlabel("physical error rate p")
        axis.grid(alpha=0.3, which="both")
    fig.suptitle("Independent Steane |Hbar> state-vector Monte Carlo")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    raise SystemExit(main())
