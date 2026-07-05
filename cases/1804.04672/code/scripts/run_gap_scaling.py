from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


WORKSPACE = Path(__file__).resolve().parents[2]
SRC = WORKSPACE / "code" / "src"
sys.path.insert(0, str(SRC))

from nonhermitian_chern import (  # noqa: E402
    fig_s2_gap_scaling_parameter_sets,
    fit_gap_scaling_by_mass,
    generate_disk_gap_scaling_rows,
)


DATA_PATH = WORKSPACE / "outputs" / "data" / "figs2_gap_scaling.csv"
FIT_PATH = WORKSPACE / "outputs" / "data" / "figs2_gap_scaling_fit.csv"
FIGURE_PATH = WORKSPACE / "outputs" / "figures" / "figs2_gap_scaling.png"
CHECK_PATH = WORKSPACE / "outputs" / "checks" / "figs2_gap_scaling.json"
SCORECARD_PATH = WORKSPACE / "outputs" / "checks" / "similarity_scorecard.json"

DATA_FIELDS = [
    "target_id",
    "series_id",
    "parameter_set",
    "m",
    "radius",
    "inverse_radius_square",
    "gap_square",
    "source",
]

FIT_FIELDS = [
    "target_id",
    "parameter_set",
    "m",
    "intercept",
    "slope",
    "source",
]


def main() -> int:
    result = run_gap_scaling()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def run_gap_scaling(
    *,
    data_path: Path = DATA_PATH,
    fit_path: Path = FIT_PATH,
    figure_path: Path = FIGURE_PATH,
    check_path: Path = CHECK_PATH,
    scorecard_path: Path = SCORECARD_PATH,
    radii: list[int] | tuple[int, ...] = (20, 24, 28, 32),
    eigen_count: int = 8,
) -> dict[str, object]:
    parameter_sets = fig_s2_gap_scaling_parameter_sets()
    rows = generate_disk_gap_scaling_rows(
        parameter_sets,
        radii=radii,
        eigen_count=eigen_count,
    )
    fits_by_label = fit_gap_scaling_by_mass(rows)
    fit_rows = [fits_by_label[label] for label in sorted(fits_by_label)]

    write_rows(rows, data_path, DATA_FIELDS)
    write_rows(fit_rows, fit_path, FIT_FIELDS)
    render_gap_scaling(rows=rows, fits_by_label=fits_by_label, path=figure_path)
    result = {
        "status": "passed" if data_path.exists() and fit_path.exists() and figure_path.exists() else "failed",
        "target_id": "T005",
        "physical_object": "supplemental finite-size gap-square extrapolation",
        "rows": len(rows),
        "fit_rows": len(fit_rows),
        "data_path": relative_to_workspace(data_path),
        "fit_path": relative_to_workspace(fit_path),
        "figure_path": relative_to_workspace(figure_path),
        "source_reference": "official paper figure, not redistributed in this public repository",
        "grid": {"radii": [int(value) for value in radii], "eigen_count": eigen_count},
        "fit_summary": {
            label: {
                "m": float(fit["m"]),
                "intercept": float(fit["intercept"]),
                "slope": float(fit["slope"]),
            }
            for label, fit in fits_by_label.items()
        },
    }
    check_path.parent.mkdir(parents=True, exist_ok=True)
    check_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return result


def write_rows(rows: list[dict[str, object]], path: Path, fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def render_gap_scaling(
    *,
    rows: list[dict[str, object]],
    fits_by_label: dict[str, dict[str, object]],
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    labels = ["fig_s2a", "fig_s2b", "fig_s2c"]
    masses = {"fig_s2a": "2.2000", "fig_s2b": "2.0800", "fig_s2c": "2.0400"}
    y_limits = {"fig_s2a": (0.0, 0.05), "fig_s2b": (0.0, 0.010), "fig_s2c": (0.0, 0.006)}
    fig, axes = plt.subplots(3, 1, figsize=(2.7, 7.2), dpi=180, constrained_layout=True)
    for index, label in enumerate(labels):
        axis = axes[index]
        selected = sorted(
            [row for row in rows if row["parameter_set"] == label],
            key=lambda row: float(row["inverse_radius_square"]),
        )
        x_values = np.asarray([float(row["inverse_radius_square"]) for row in selected])
        y_values = np.asarray([float(row["gap_square"]) for row in selected])
        fit = fits_by_label[label]
        x_fit = np.linspace(0.0, max(x_values) * 1.04, 100)
        y_fit = float(fit["intercept"]) + float(fit["slope"]) * x_fit
        axis.plot(x_fit, y_fit, color="#ff5533", linestyle="-.", linewidth=0.9)
        axis.scatter(x_values, y_values, s=12, facecolors="white", edgecolors="#4f8bd6", linewidths=0.8, zorder=3)
        axis.annotate(
            r"$|\Delta|^2(L\to\infty)$",
            xy=(0.0, float(fit["intercept"])),
            xytext=(max(x_values) * 0.22, max(float(fit["intercept"]) * 1.12, y_limits[label][1] * 0.10)),
            arrowprops={"arrowstyle": "->", "linewidth": 0.6, "color": "#666666"},
            fontsize=7,
        )
        axis.text(0.66, 0.84, f"m={masses[label]}", transform=axis.transAxes, fontsize=8)
        axis.text(
            -0.22,
            1.02,
            f"({chr(ord('a') + index)})",
            transform=axis.transAxes,
            fontsize=9,
            clip_on=False,
        )
        axis.set_xlim(0.0, max(x_values) * 1.08)
        axis.set_ylim(*y_limits[label])
        axis.set_xlabel(r"$1/L^2$", fontsize=8)
        set_milli_axis(axis, axis_name="x")
        if label in {"fig_s2b", "fig_s2c"}:
            set_milli_axis(axis, axis_name="y")
        if index == 0:
            axis.set_ylabel(r"$|\Delta|^2$", fontsize=8)
        else:
            axis.set_ylabel("")
        axis.tick_params(axis="both", labelsize=7, direction="in", pad=1)
        axis.grid(False)
    fig.savefig(path)
    plt.close(fig)


def set_milli_axis(axis, *, axis_name: str) -> None:
    if axis_name == "x":
        ticks = np.arange(0.0, 0.00251, 0.0005)
        axis.set_xticks(ticks)
        axis.set_xticklabels([f"{value / 1e-3:g}" for value in ticks])
        axis.text(0.98, -0.19, r"$\times 10^{-3}$", transform=axis.transAxes, ha="right", va="top", fontsize=7)
        return
    if axis_name == "y":
        upper = axis.get_ylim()[1]
        ticks = np.arange(0.0, upper + 1e-12, 0.002 if upper > 0.008 else 0.001)
        axis.set_yticks(ticks)
        axis.set_yticklabels([f"{value / 1e-3:g}" for value in ticks])
        axis.text(0.00, 1.02, r"$\times 10^{-3}$", transform=axis.transAxes, ha="left", va="bottom", fontsize=7)
        return
    raise ValueError("axis_name must be x or y")


def relative_to_workspace(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(WORKSPACE.resolve()))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
