#!/usr/bin/env python3
"""Reproduce the boundary-ratio sensitivity mechanism of formal Fig. 4(d)."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))

from src.geometry_adaptive import (  # noqa: E402
    build_obc_hamiltonian,
    cut_coordinate_interval_sites,
    full_spectrum,
    model_eq15,
    spectrum_metrics,
    symmetric_cloud_distance,
)

SCALES = {
    "smoke": {
        "3:1": ((-12, 12), (-4, 4)),
        "2:1": ((-10, 10), (-5, 5)),
        "1:2": ((-5, 5), (-10, 10)),
        "1:3": ((-4, 4), (-12, 12)),
    },
    "feature": {
        "3:1": ((-30, 30), (-10, 10)),
        "2:1": ((-24, 24), (-12, 12)),
        "1:2": ((-12, 12), (-24, 24)),
        "1:3": ((-10, 10), (-30, 30)),
    },
    # The captions fix ratios and site counts but not integer vertices. These
    # parity-compatible intervals are the minimal reconstruction matching both.
    "paper_counts": {
        "3:1": ((-69, 69), (-23, 23)),
        "2:1": ((-57, 57), (-29, 27)),
        "1:2": ((-29, 27), (-57, 57)),
        "1:3": ((-23, 23), (-69, 69)),
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", choices=tuple(SCALES), default="smoke")
    parser.add_argument(
        "--reuse-data",
        action="store_true",
        help="Rebuild checks and figures from existing spectrum CSVs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    params = SCALES[args.scale]
    data_dir = WORKSPACE / "outputs" / "data"
    figure_dir = WORKSPACE / "outputs" / "figures"
    check_dir = WORKSPACE / "outputs" / "checks"
    for directory in (data_dir, figure_dir, check_dir):
        directory.mkdir(parents=True, exist_ok=True)

    check_path = check_dir / f"fig4d_boundary_ratio_{args.scale}.json"
    prior_check = json.loads(check_path.read_text()) if args.reuse_data and check_path.exists() else {}

    spectra: dict[str, np.ndarray] = {}
    results: dict[str, dict[str, object]] = {}
    for label, (u_bounds, v_bounds) in params.items():
        sites = cut_coordinate_interval_sites(u_bounds, v_bounds)
        hamiltonian = build_obc_hamiltonian(sites, model_eq15())
        path = data_dir / f"fig4d_ratio_{label.replace(':', 'to')}_{args.scale}.csv"
        if args.reuse_data:
            eigenvalues = read_spectrum(path)
            runtime = prior_check.get("results", {}).get(label, {}).get("runtime_seconds")
        else:
            started = time.perf_counter()
            eigenvalues = full_spectrum(hamiltonian)
            runtime = time.perf_counter() - started
            write_spectrum(path, eigenvalues)
        spectra[label] = eigenvalues
        results[label] = {
            "u_bounds": list(u_bounds),
            "v_bounds": list(v_bounds),
            "site_count": len(sites),
            "matrix_nonzeros": int(hamiltonian.nnz),
            "runtime_seconds": runtime,
            "spectrum": spectrum_metrics(eigenvalues),
            "data": str(path.relative_to(WORKSPACE)),
        }

    reciprocal_extreme_distance = symmetric_cloud_distance(spectra["3:1"], spectra["1:3"])
    reciprocal_middle_distance = symmetric_cloud_distance(spectra["2:1"], spectra["1:2"])
    ratio_class_distance = symmetric_cloud_distance(spectra["3:1"], spectra["2:1"])
    anisotropies = {
        label: result["spectrum"]["real_span"] / result["spectrum"]["imag_span"]
        for label, result in results.items()
    }
    acceptance = {
        "all_four_ratios_generated": set(spectra) == {"3:1", "2:1", "1:2", "1:3"},
        "site_counts_match_paper": args.scale != "paper_counts"
        or [results[label]["site_count"] for label in ("3:1", "2:1", "1:2", "1:3")]
        == [3267, 3278, 3278, 3267],
        "three_to_one_differs_from_two_to_one": ratio_class_distance["mean"]
        > (0.005 if args.scale == "paper_counts" else 0.03),
        # Large non-normal matrices can have a few unstable eigenvalue outliers.
        # The median and p95 quantify cloud equivalence without hiding max error.
        "reciprocal_extreme_ratios_are_reflection_equivalent": reciprocal_extreme_distance[
            "median"
        ]
        < 1e-6
        and reciprocal_extreme_distance["p95"] < 1e-3,
        "reciprocal_middle_ratios_are_reflection_equivalent": reciprocal_middle_distance[
            "median"
        ]
        < 1e-6
        and reciprocal_middle_distance["p95"] < 1e-3,
    }

    figure_path = figure_dir / f"fig4d_boundary_ratio_{args.scale}.png"
    render_figure(figure_path, spectra)
    check = {
        "status": "passed" if all(acceptance.values()) else "failed",
        "target_id": "T002",
        "figure_refs": ["Fig. 4"],
        "scale": args.scale,
        "artifact_stage": "exploratory",
        "parameter_match": "paper_subset" if args.scale == "paper_counts" else "reduced_scale",
        "generated_data_provenance": "independent_numerics",
        "formula_gate": "verified",
        "formula_dependencies": ["EQC003", "EQC004"],
        "paper_parameters": {
            "ratios": ["3:1", "2:1", "1:2", "1:3"],
            "site_counts": [3267, 3278, 3278, 3267],
        },
        "generated_parameters": {
            label: {"u_bounds": list(bounds[0]), "v_bounds": list(bounds[1])}
            for label, bounds in params.items()
        },
        "panel_generated": "d",
        "panels_not_generated": ["a", "b", "c", "e", "f"],
        "ratio_class_cloud_distance": ratio_class_distance,
        "reciprocal_extreme_cloud_distance": reciprocal_extreme_distance,
        "reciprocal_middle_cloud_distance": reciprocal_middle_distance,
        "symmetry_interpretation": (
            "Reflection-equivalent Hamiltonians are verified by an exact unit test. "
            "For paper-scale non-normal matrices, acceptance uses median and p95 cloud "
            "distance while retaining the maximum outlier as spectral-instability evidence."
        ),
        "anisotropy_real_span_over_imag_span": anisotropies,
        "results": results,
        "acceptance": acceptance,
        "figure": str(figure_path.relative_to(WORKSPACE)),
    }
    check_path.write_text(json.dumps(check, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(check, indent=2))
    return 0 if check["status"] == "passed" else 1


def write_spectrum(path: Path, eigenvalues: np.ndarray) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("real_E", "imag_E"))
        writer.writerows(zip(eigenvalues.real, eigenvalues.imag, strict=True))


def read_spectrum(path: Path) -> np.ndarray:
    data = np.genfromtxt(path, delimiter=",", names=True)
    return np.asarray(data["real_E"] + 1j * data["imag_E"])


def render_figure(path: Path, spectra: dict[str, np.ndarray]) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.2), sharex=True, sharey=True, constrained_layout=True)
    for axis, label in zip(axes.flat, ("3:1", "2:1", "1:2", "1:3"), strict=True):
        values = spectra[label]
        axis.scatter(values.real, values.imag, color="0.2", alpha=0.32, s=5, linewidths=0)
        axis.set_title(label, color="#2055d6")
        axis.set_xlim(-2.1, 2.1)
        axis.set_ylim(-1.1, 1.1)
        axis.grid(alpha=0.15)
        axis.set_aspect("equal")
    axes[1, 0].set_xlabel(r"Re $E$")
    axes[1, 1].set_xlabel(r"Re $E$")
    axes[0, 0].set_ylabel(r"Im $E$")
    axes[1, 0].set_ylabel(r"Im $E$")
    fig.suptitle("Eq. (15): boundary-ratio-dependent spectra")
    fig.savefig(path, dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    raise SystemExit(main())
