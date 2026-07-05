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
    fig2_square_parameter_sets,
    generate_square_spectrum_rows,
    square_wavepacket_snapshots,
)


SPECTRUM_PATH = WORKSPACE / "outputs" / "data" / "fig2_square_spectrum.csv"
WAVEPACKET_PATH = WORKSPACE / "outputs" / "data" / "fig2_wavepacket.csv"
FIGURE_PATH = WORKSPACE / "outputs" / "figures" / "fig2_square_dynamics.png"
CHECK_PATH = WORKSPACE / "outputs" / "checks" / "fig2_square_dynamics.json"
SCORECARD_PATH = WORKSPACE / "outputs" / "checks" / "similarity_scorecard.json"

SPECTRUM_FIELDS = [
    "target_id",
    "series_id",
    "parameter_set",
    "eigen_index",
    "energy_real",
    "energy_imag",
    "source",
]

WAVEPACKET_FIELDS = [
    "target_id",
    "series_id",
    "parameter_set",
    "time",
    "x",
    "y",
    "intensity",
    "source",
]


def main() -> int:
    result = run_square_dynamics()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def run_square_dynamics(
    *,
    spectrum_path: Path = SPECTRUM_PATH,
    wavepacket_path: Path = WAVEPACKET_PATH,
    figure_path: Path = FIGURE_PATH,
    check_path: Path = CHECK_PATH,
    scorecard_path: Path = SCORECARD_PATH,
    L: int = 30,
    eigen_count: int = 22,
    times: list[float] | tuple[float, ...] = (0.0, 5.0, 20.0),
) -> dict[str, object]:
    parameter_sets = fig2_square_parameter_sets(L=L)
    spectrum_rows = generate_square_spectrum_rows(parameter_sets, eigen_count=eigen_count)
    wavepacket_rows = []
    for params in parameter_sets.values():
        wavepacket_rows.extend(square_wavepacket_snapshots(params, times=times))

    write_rows(spectrum_rows, spectrum_path, SPECTRUM_FIELDS)
    write_rows(wavepacket_rows, wavepacket_path, WAVEPACKET_FIELDS)
    render_square_dynamics(
        spectrum_rows=spectrum_rows,
        wavepacket_rows=wavepacket_rows,
        path=figure_path,
        L=L,
        times=[float(value) for value in times],
    )
    result = {
        "status": "passed" if spectrum_path.exists() and wavepacket_path.exists() and figure_path.exists() else "failed",
        "target_id": "T004",
        "physical_object": "square low-energy spectra and wave-packet dynamics",
        "parameter_sets": list(parameter_sets),
        "spectrum_rows": len(spectrum_rows),
        "wavepacket_rows": len(wavepacket_rows),
        "spectrum_path": relative_to_workspace(spectrum_path),
        "wavepacket_path": relative_to_workspace(wavepacket_path),
        "figure_path": relative_to_workspace(figure_path),
        "source_reference": "official paper figure, not redistributed in this public repository",
        "grid": {"L": L, "eigen_count": eigen_count, "times": list(times)},
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


def render_square_dynamics(
    *,
    spectrum_rows: list[dict[str, object]],
    wavepacket_rows: list[dict[str, object]],
    path: Path,
    L: int,
    times: list[float],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(
        2,
        4,
        figsize=(9.4, 4.2),
        dpi=170,
        gridspec_kw={"width_ratios": [1.0, 1.0, 1.0, 1.0], "wspace": 0.28, "hspace": 0.34},
        constrained_layout=True,
    )
    vmax = max(float(row["intensity"]) for row in wavepacket_rows)
    for row_index, label in enumerate(["fig2a", "fig2b"]):
        render_spectrum_panel(axes[row_index, 0], spectrum_rows, label)
        for time_index, time in enumerate(times[:3]):
            render_wavepacket_panel(
                axes[row_index, time_index + 1],
                wavepacket_rows,
                label,
                time,
                L,
                vmax=max(vmax, 1e-12),
            )
        axes[row_index, 0].text(
            -0.32,
            1.05,
            "(a)" if label == "fig2a" else "(b)",
            transform=axes[row_index, 0].transAxes,
            fontsize=10,
            va="bottom",
        )
    fig.savefig(path)
    plt.close(fig)


def render_spectrum_panel(axis, rows: list[dict[str, object]], label: str) -> None:
    selected = [row for row in rows if row["parameter_set"] == label]
    selected = sorted(selected, key=lambda row: float(row["energy_real"]))
    x_values = np.arange(len(selected))
    y_values = [float(row["energy_real"]) for row in selected]
    axis.scatter(x_values, y_values, s=10, color="black")
    axis.set_ylim(-0.45, 0.45)
    axis.set_xticks([])
    axis.set_yticks([-0.4, 0.0, 0.4])
    axis.set_ylabel("E", rotation=0, labelpad=8)
    axis.tick_params(axis="both", labelsize=8, direction="in", pad=1)
    marker = "■" if label == "fig2a" else "*"
    mass = "2.2121" if label == "fig2a" else "1.7879"
    axis.text(0.05, 0.92, f"{marker} m={mass}", transform=axis.transAxes, fontsize=8)


def render_wavepacket_panel(
    axis,
    rows: list[dict[str, object]],
    label: str,
    time: float,
    L: int,
    *,
    vmax: float,
) -> None:
    panel_rows = [
        row
        for row in rows
        if row["parameter_set"] == label and abs(float(row["time"]) - time) < 1e-9
    ]
    grid = np.zeros((L, L), dtype=float)
    for row in panel_rows:
        x = int(float(row["x"])) - 1
        y = int(float(row["y"])) - 1
        grid[y, x] = float(row["intensity"])
    axis.imshow(
        grid,
        origin="lower",
        extent=(1, L, 1, L),
        cmap="Blues",
        vmin=0.0,
        vmax=vmax,
        interpolation="bilinear",
        aspect="equal",
    )
    axis.scatter(*np.meshgrid(np.arange(1, L + 1), np.arange(1, L + 1)), s=1.0, color="#b5b5b5", alpha=0.55)
    axis.set_xlim(1, L)
    axis.set_ylim(1, L)
    axis.set_xticks([L // 2, L])
    axis.set_yticks([L // 2, L])
    axis.set_xlabel("x", fontsize=8, loc="right", labelpad=-1)
    axis.set_ylabel("y", fontsize=8, rotation=0, labelpad=6)
    axis.tick_params(axis="both", labelsize=8, direction="in", pad=1)
    mass = "2.2121" if label == "fig2a" else "1.7879"
    axis.text(0.06, 0.92, f"t={time:g}", transform=axis.transAxes, fontsize=8)
    if abs(time) < 1e-12:
        axis.text(0.57, 0.92, f"m={mass}", transform=axis.transAxes, fontsize=8)


def relative_to_workspace(path: Path) -> str:
    try:
        return str(path.relative_to(WORKSPACE))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
