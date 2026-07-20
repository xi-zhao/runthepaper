#!/usr/bin/env python3
"""Generate the hierarchical potential and derived density for formal Fig. 2(c)."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys
import time

import matplotlib.pyplot as plt
import numpy as np


WORKSPACE = Path(__file__).resolve().parents[1]
CASE_PATH = WORKSPACE.parent
sys.path.insert(0, str(WORKSPACE))

from src.geometry_adaptive import (  # noqa: E402
    geometry_adaptive_potential,
    model_eq11,
    spectral_density_from_potential,
    spectral_potential_grid,
)


SCALE_CONFIG = {
    "smoke": {"grid_size": 11, "momentum_samples": 32, "tolerance": 2e-3},
    "feature": {"grid_size": 31, "momentum_samples": 96, "tolerance": 5e-4},
    "paper": {"grid_size": 101, "momentum_samples": 200, "tolerance": 1e-5},
}


def _load_spectrum(path: Path) -> np.ndarray:
    table = np.loadtxt(path, delimiter=",", skiprows=1)
    if table.ndim != 2 or table.shape[1] != 2:
        raise ValueError(f"expected real_E,imag_E columns in {path}")
    return np.asarray(table[:, 0] + 1j * table[:, 1], dtype=np.complex128)


def _write_grid_csv(
    path: Path,
    geometry: str,
    real_axis: np.ndarray,
    imaginary_axis: np.ndarray,
    arrays: dict[str, np.ndarray],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("geometry", "real_energy", "imag_energy", *arrays.keys()))
        for row, imaginary in enumerate(imaginary_axis):
            for column, real in enumerate(real_axis):
                writer.writerow(
                    (
                        geometry,
                        f"{real:.17g}",
                        f"{imaginary:.17g}",
                        *(f"{values[row, column]:.17g}" for values in arrays.values()),
                    )
                )


def _render(results: dict[str, dict[str, np.ndarray]], output: Path, scale: str) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(9.2, 4.0), constrained_layout=True)
    vmax = max(
        float(np.quantile(np.clip(item["density"], 0, None), 0.995))
        for item in results.values()
    )
    vmax = max(vmax, np.finfo(float).eps)
    image = None
    for axis, name in zip(axes, ("square", "rhombus"), strict=True):
        image = axis.imshow(
            np.clip(results[name]["density"], 0, None),
            origin="lower",
            extent=(-2, 4, -3, 3),
            cmap="magma",
            vmin=0,
            vmax=vmax,
            interpolation="nearest",
            aspect="equal",
        )
        axis.set_title(name)
        axis.set_xlabel("Re E")
        axis.set_ylabel("Im E")
    if image is None:
        raise AssertionError("no geometry was rendered")
    figure.colorbar(image, ax=axes, label="rho(E), clipped at zero")
    figure.suptitle(f"Eq. (10) geometry-adaptive density — {scale} grid")
    figure.savefig(output, dpi=240)
    plt.close(figure)


def run(
    scale: str,
    output_root: Path,
    *,
    reuse_potential: bool = False,
) -> dict[str, object]:
    config = SCALE_CONFIG[scale]
    grid_size = int(config["grid_size"])
    momentum_samples = int(config["momentum_samples"])
    tolerance = float(config["tolerance"])
    real_axis = np.linspace(-2.0, 4.0, grid_size)
    imaginary_axis = np.linspace(-3.0, 3.0, grid_size)
    real_step = float(real_axis[1] - real_axis[0])
    imaginary_step = float(imaginary_axis[1] - imaginary_axis[0])

    data_dir = output_root / "data"
    figure_dir = output_root / "figures"
    checks_dir = output_root / "checks"
    for directory in (data_dir, figure_dir, checks_dir):
        directory.mkdir(parents=True, exist_ok=True)

    results: dict[str, dict[str, np.ndarray]] = {}
    previous_check_path = checks_dir / f"fig2_hierarchical_potential_{scale}.json"
    previous_check = (
        json.loads(previous_check_path.read_text(encoding="utf-8"))
        if reuse_potential and previous_check_path.exists()
        else {}
    )
    check: dict[str, object] = {
        "schema_version": 1,
        "paper_id": CASE_PATH.name,
        "target_id": "T001",
        "figure_refs": ["Fig. 2(c)"],
        "scale": scale,
        "artifact_stage": "final_reproduction" if scale == "paper" else "exploratory",
        "parameter_match": "paper_exact" if scale == "paper" else "reduced_scale",
        "generated_data_provenance": "independent_numerics",
        "formula_gate": "verified",
        "formula_dependencies": ["EQC001", "EQC002", "EQC003", "EQC006"],
        "grid_size": grid_size,
        "momentum_samples": momentum_samples,
        "minimizer_tolerance": tolerance,
        "geometries": {},
    }

    for basis in ("square", "rhombus"):
        started = time.perf_counter()
        npz_path = data_dir / f"fig2_{basis}_potential_{scale}.npz"
        if reuse_potential:
            if not npz_path.exists():
                raise FileNotFoundError(f"stored potential is missing: {npz_path}")
            stored = np.load(npz_path)
            np.testing.assert_allclose(stored["x"], real_axis)
            np.testing.assert_allclose(stored["y"], imaginary_axis)
            potential = np.asarray(stored["potential"], dtype=np.float64)
            phi_1 = np.asarray(stored["phi_1"], dtype=np.float64)
            phi_2 = np.asarray(stored["phi_2"], dtype=np.float64)
            mu_1 = np.asarray(stored["mu_1"], dtype=np.float64)
            mu_2 = np.asarray(stored["mu_2"], dtype=np.float64)
            previous_geometry = previous_check.get("geometries", {}).get(basis, {})
            evaluations = int(previous_geometry.get("objective_evaluations", 0))
            potential_runtime = float(previous_geometry.get("runtime_seconds", 0.0))
        else:
            potential = np.empty((grid_size, grid_size), dtype=np.float64)
            phi_1 = np.empty_like(potential)
            phi_2 = np.empty_like(potential)
            mu_1 = np.empty_like(potential)
            mu_2 = np.empty_like(potential)
            evaluations = 0
            for row, imaginary in enumerate(imaginary_axis):
                for column, real in enumerate(real_axis):
                    value = geometry_adaptive_potential(
                        complex(real, imaginary),
                        model_eq11(),
                        basis=basis,
                        momentum_samples=momentum_samples,
                        tolerance=tolerance,
                    )
                    potential[row, column] = value.potential
                    phi_1[row, column] = value.cylinder_1.potential
                    phi_2[row, column] = value.cylinder_2.potential
                    mu_1[row, column] = value.cylinder_1.deformation
                    mu_2[row, column] = value.cylinder_2.deformation
                    evaluations += (
                        value.cylinder_1.evaluations
                        + value.cylinder_2.evaluations
                    )
            potential_runtime = time.perf_counter() - started

        density = spectral_density_from_potential(
            potential,
            real_step=real_step,
            imaginary_step=imaginary_step,
        )
        refresh_runtime = time.perf_counter() - started

        spectrum_path = data_dir / f"fig2_{basis}_spectrum_paper.csv"
        finite_comparison: dict[str, float] | None = None
        if spectrum_path.exists():
            energy_grid = real_axis[None, :] + 1j * imaginary_axis[:, None]
            finite_potential = spectral_potential_grid(_load_spectrum(spectrum_path), energy_grid)
            absolute_error = np.abs(finite_potential - potential)
            finite_comparison = {
                "mean_abs_potential_error": float(np.mean(absolute_error)),
                "median_abs_potential_error": float(np.median(absolute_error)),
                "max_abs_potential_error": float(np.max(absolute_error)),
            }

        _write_grid_csv(
            data_dir / f"fig2_{basis}_potential_{scale}.csv",
            basis,
            real_axis,
            imaginary_axis,
            {
                "potential": potential,
                "density_raw": density,
                "density_clipped": np.clip(density, 0, None),
                "phi_cylinder_1": phi_1,
                "phi_cylinder_2": phi_2,
                "mu_1": mu_1,
                "mu_2": mu_2,
            },
        )
        np.savez_compressed(
            npz_path,
            x=real_axis,
            y=imaginary_axis,
            potential=potential,
            density=density,
            phi_1=phi_1,
            phi_2=phi_2,
            mu_1=mu_1,
            mu_2=mu_2,
        )
        positive_mass = float(np.sum(np.clip(density, 0, None)) * real_step * imaginary_step)
        check["geometries"][basis] = {
            "runtime_seconds": potential_runtime,
            "artifact_refresh_seconds": refresh_runtime if reuse_potential else 0.0,
            "potential_source": "stored_paper_grid" if reuse_potential else "fresh_compute",
            "objective_evaluations": evaluations,
            "potential_finite": bool(np.all(np.isfinite(potential))),
            "density_finite": bool(np.all(np.isfinite(density))),
            "positive_density_mass_in_plot_window": positive_mass,
            "negative_density_fraction": float(np.mean(density < 0)),
            "finite_size_potential_comparison": finite_comparison,
        }
        results[basis] = {"potential": potential, "density": density}

    check["status"] = "passed" if all(
        item["potential_finite"]
        and item["density_finite"]
        and 0.5 < item["positive_density_mass_in_plot_window"] < 2.0
        and item["finite_size_potential_comparison"] is not None
        and item["finite_size_potential_comparison"]["mean_abs_potential_error"] < 0.01
        for item in check["geometries"].values()
    ) else "failed"
    figure_path = figure_dir / f"fig2_hierarchical_potential_{scale}.png"
    _render(results, figure_path, scale)
    payload = json.dumps(check, indent=2, ensure_ascii=False) + "\n"
    (checks_dir / f"fig2_hierarchical_potential_{scale}.json").write_text(payload, encoding="utf-8")
    print(json.dumps(check, indent=2, ensure_ascii=False))
    return check


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scale", choices=tuple(SCALE_CONFIG), default="smoke")
    parser.add_argument("--output-root", type=Path, default=WORKSPACE / "outputs")
    parser.add_argument(
        "--reuse-potential",
        action="store_true",
        help="rebuild density/check/figure artifacts from an existing potential grid",
    )
    args = parser.parse_args()
    result = run(args.scale, args.output_root, reuse_potential=args.reuse_potential)
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
