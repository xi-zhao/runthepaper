#!/usr/bin/env python3
"""Reproduce formal Fig. 2(a,b) from independent Eq. (11) numerics."""

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
    aggregate_right_density,
    build_obc_hamiltonian,
    density_metrics,
    diamond_sites,
    full_right_eigensystem,
    model_eq11,
    spectrum_metrics,
    square_sites,
    symmetric_cloud_distance,
)

SCALES = {
    "smoke": {"square_length": 10, "rhombus_radius": 7},
    "paper": {"square_length": 40, "rhombus_radius": 30},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", choices=tuple(SCALES), default="smoke")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    params = SCALES[args.scale]
    data_dir = WORKSPACE / "outputs" / "data"
    figure_dir = WORKSPACE / "outputs" / "figures"
    check_dir = WORKSPACE / "outputs" / "checks"
    for directory in (data_dir, figure_dir, check_dir):
        directory.mkdir(parents=True, exist_ok=True)

    geometries = {
        "square": square_sites(params["square_length"]),
        "rhombus": diamond_sites(params["rhombus_radius"]),
    }
    results: dict[str, dict[str, object]] = {}
    generated: dict[str, tuple[tuple[tuple[int, int], ...], np.ndarray, np.ndarray]] = {}

    for name, sites in geometries.items():
        started = time.perf_counter()
        hamiltonian = build_obc_hamiltonian(sites, model_eq11())
        eigensystem = full_right_eigensystem(hamiltonian)
        density = aggregate_right_density(eigensystem.right_eigenvectors)
        runtime = time.perf_counter() - started

        spectrum_path = data_dir / f"fig2_{name}_spectrum_{args.scale}.csv"
        density_path = data_dir / f"fig2_{name}_density_{args.scale}.csv"
        write_spectrum(spectrum_path, eigensystem.eigenvalues)
        write_density(density_path, sites, density)

        results[name] = {
            "site_count": len(sites),
            "matrix_nonzeros": int(hamiltonian.nnz),
            "runtime_seconds": runtime,
            "spectrum": spectrum_metrics(eigensystem.eigenvalues),
            "density": density_metrics(sites, density),
            "data": {
                "spectrum": str(spectrum_path.relative_to(WORKSPACE)),
                "density": str(density_path.relative_to(WORKSPACE)),
            },
        }
        generated[name] = (sites, eigensystem.eigenvalues, density)

    cloud_distance = symmetric_cloud_distance(
        generated["square"][1], generated["rhombus"][1]
    )
    expected_counts = (
        {"square": 1600, "rhombus": 1861}
        if args.scale == "paper"
        else {name: len(sites) for name, sites in geometries.items()}
    )
    square_expected_corner = [params["square_length"] - 1, 0]
    rhombus_expected_corner = [params["rhombus_radius"], 0]
    square_max = results["square"]["density"]["max_site"]
    rhombus_max = results["rhombus"]["density"]["max_site"]
    acceptance = {
        "site_counts_match": all(
            results[name]["site_count"] == count for name, count in expected_counts.items()
        ),
        "geometry_changes_spectrum": cloud_distance["mean"] > 0.02,
        "square_localizes_lower_right": site_distance(square_max, square_expected_corner) <= 2.0,
        "rhombus_localizes_right": site_distance(rhombus_max, rhombus_expected_corner) <= 2.0,
    }

    figure_path = figure_dir / f"fig2_geometry_dependence_{args.scale}.png"
    render_figure(figure_path, generated)
    check = {
        "status": "passed" if all(acceptance.values()) else "failed",
        "target_id": "T001",
        "figure_refs": ["Fig. 2"],
        "scale": args.scale,
        "artifact_stage": "exploratory",
        "parameter_match": "paper_exact" if args.scale == "paper" else "reduced_scale",
        "generated_data_provenance": "independent_numerics",
        "formula_gate": "verified",
        "formula_dependencies": ["EQC001", "EQC003"],
        "paper_parameters": {
            "square": {"length": 40, "site_count": 1600},
            "rhombus": {"bounding_length": 61, "radius": 30, "site_count": 1861},
        },
        "generated_parameters": params,
        "panels_generated": ["a(i)", "a(ii)", "b(i)", "b(ii)"],
        "panels_not_generated": ["c(i)", "c(ii)", "d(i)", "d(ii)"],
        "geometry_cloud_distance": cloud_distance,
        "results": results,
        "acceptance": acceptance,
        "figure": str(figure_path.relative_to(WORKSPACE)),
    }
    check_path = check_dir / f"fig2_geometry_dependence_{args.scale}.json"
    check_path.write_text(json.dumps(check, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(check, indent=2))
    return 0 if check["status"] == "passed" else 1


def write_spectrum(path: Path, eigenvalues: np.ndarray) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("real_E", "imag_E"))
        writer.writerows(zip(eigenvalues.real, eigenvalues.imag, strict=True))


def write_density(path: Path, sites: tuple[tuple[int, int], ...], density: np.ndarray) -> None:
    normalized = density / density.max()
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("x", "y", "aggregate_density", "density_over_max"))
        for (x, y), value, scaled in zip(sites, density, normalized, strict=True):
            writer.writerow((x, y, value, scaled))


def render_figure(
    path: Path,
    generated: dict[str, tuple[tuple[tuple[int, int], ...], np.ndarray, np.ndarray]],
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 7.2), constrained_layout=True)
    for column, name in enumerate(("square", "rhombus")):
        sites, eigenvalues, density = generated[name]
        coords = np.asarray(sites)
        axes[0, column].scatter(
            coords[:, 0],
            coords[:, 1],
            c=density / density.max(),
            cmap="Reds",
            vmin=0,
            vmax=1,
            s=max(2.0, 1500.0 / len(sites)),
            linewidths=0,
        )
        axes[0, column].set_aspect("equal")
        axes[0, column].set_title(f"{name}: aggregate right density")
        axes[0, column].axis("off")

        axes[1, column].scatter(
            eigenvalues.real,
            eigenvalues.imag,
            color="0.25",
            alpha=0.22,
            s=4,
            linewidths=0,
        )
        axes[1, column].set_xlim(-2.1, 4.1)
        axes[1, column].set_ylim(-3.1, 3.1)
        axes[1, column].set_xlabel(r"Re $E$")
        axes[1, column].set_ylabel(r"Im $E$")
        axes[1, column].set_aspect("equal")
        axes[1, column].grid(alpha=0.15)

    fig.suptitle("Independent reproduction of formal Fig. 2(a,b) - Eq. (11)")
    fig.savefig(path, dpi=220)
    plt.close(fig)


def site_distance(first: list[int], second: list[int]) -> float:
    return float(np.linalg.norm(np.asarray(first, dtype=float) - np.asarray(second, dtype=float)))


if __name__ == "__main__":
    raise SystemExit(main())
