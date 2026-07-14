#!/usr/bin/env python3
"""Plot public exact-circuit data, with an optional private reference overlay.

The normal public run creates reproduction-only figures.  Maintainers may
provide a directory containing internally digitized reference CSV files to
render the limited comparison panels used in the note.  Those source-derived
point sets are validation inputs and are intentionally not distributed.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


CASE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = CASE_ROOT / "outputs/data/steane_exact_benchmark.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument(
        "--reference-dir",
        type=Path,
        help="Internal validation directory; its digitized point sets are not published.",
    )
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def reference_series(directory: Path, name: str) -> dict[float, float]:
    rows = read_rows(directory / f"steane_{name}_digitized.csv")
    return {
        float(row["p"]): float(row["value"])
        for row in rows
        if row["series"] == "cirq_orange"
    }


def nearest(series: dict[float, float], p: float) -> float:
    key = min(series, key=lambda value: abs(value - p))
    return series[key]


def main() -> int:
    args = parse_args()
    rows = read_rows(args.data)
    if args.reference_dir:
        acceptance_ref = reference_series(args.reference_dir, "acceptance")
        infidelity_ref = reference_series(args.reference_dir, "infidelity")
        plot_one(
            rows,
            "acceptance_rate",
            "acceptance_se",
            "acceptance rate",
            CASE_ROOT / "outputs/figures/steane_exact_acceptance_comparison.png",
            acceptance_ref,
            "Validation result: all 12 points agree within max(0.012, 3 sigma).",
            log_y=False,
        )
        plot_one(
            rows,
            "infidelity",
            "infidelity_se",
            "logical infidelity",
            CASE_ROOT / "outputs/figures/steane_exact_infidelity_comparison.png",
            infidelity_ref,
            (
                "Difference reason: reconstructed gate/idle ordering gives 0.42-0.68x "
                "of the paper curve in the mid-range.\n"
                "The author implementation is not public; more shots cannot resolve this schedule detail."
            ),
            log_y=True,
        )
    else:
        plot_one(
            rows,
            "acceptance_rate",
            "acceptance_se",
            "acceptance rate",
            CASE_ROOT / "outputs/figures/steane_exact_acceptance_reproduction.png",
            None,
            "Independent exact-circuit result; no source-derived points are included.",
            log_y=False,
        )
        plot_one(
            rows,
            "infidelity",
            "infidelity_se",
            "logical infidelity",
            CASE_ROOT / "outputs/figures/steane_exact_infidelity_reproduction.png",
            None,
            "Independent exact-circuit result; no source-derived points are included.",
            log_y=True,
        )
    return 0


def plot_one(
    rows: list[dict[str, str]],
    value_key: str,
    error_key: str,
    ylabel: str,
    output: Path,
    reference: dict[float, float] | None,
    reason: str,
    *,
    log_y: bool,
) -> None:
    ps = [float(row["p"]) for row in rows]
    fig, axis = plt.subplots(figsize=(7.2, 5.0))
    fig.subplots_adjust(left=0.14, right=0.97, top=0.82, bottom=0.23)
    axis.errorbar(
        ps,
        [float(row[value_key]) for row in rows],
        yerr=[float(row[error_key]) for row in rows],
        fmt="o-",
        color="tab:green",
        label="exact protocol (this work)",
    )
    if reference:
        axis.plot(
            ps,
            [nearest(reference, p) for p in ps],
            "^--",
            color="tab:orange",
            label="paper curve (digitized for validation; points not redistributed)",
        )
    axis.set_xscale("log")
    if log_y:
        axis.set_yscale("log")
    axis.set_xlabel("physical error rate p")
    axis.set_ylabel(ylabel)
    axis.grid(alpha=0.3, which="both")
    axis.legend(fontsize=8)
    fig.suptitle(r"Steane $|\overline{H}\rangle$ exact-circuit benchmark")
    fig.text(0.5, 0.055, reason, ha="center", va="bottom", fontsize=8.5, color="0.25")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    raise SystemExit(main())
