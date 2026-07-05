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

from nonhermitian_chern import generate_disk_phase_diagram_rows  # noqa: E402


DATA_PATH = WORKSPACE / "outputs" / "data" / "figs3_disk_phase.csv"
FIGURE_PATH = WORKSPACE / "outputs" / "figures" / "figs3_disk_phase.png"
CHECK_PATH = WORKSPACE / "outputs" / "checks" / "figs3_disk_phase.json"
SCORECARD_PATH = WORKSPACE / "outputs" / "checks" / "similarity_scorecard.json"

FIELDNAMES = ["target_id", "series_id", "gamma", "m", "region", "source"]
GAMMA_MIN = 0.0
GAMMA_MAX = 0.5
M_MIN = 1.30
M_MAX = 2.70


def main() -> int:
    result = run_disk_phase_diagram()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def run_disk_phase_diagram(
    *,
    data_path: Path = DATA_PATH,
    figure_path: Path = FIGURE_PATH,
    check_path: Path = CHECK_PATH,
    scorecard_path: Path = SCORECARD_PATH,
    gamma_points: int = 51,
) -> dict[str, object]:
    gamma_values = np.linspace(GAMMA_MIN, GAMMA_MAX, gamma_points)
    rows = generate_disk_phase_diagram_rows(gamma_values)
    write_rows(rows, data_path)
    render_disk_phase_diagram(rows, figure_path)
    result = {
        "status": "passed" if data_path.exists() and figure_path.exists() else "failed",
        "target_id": "T006",
        "physical_object": "supplemental disk-geometry phase diagram",
        "rows": len(rows),
        "data_path": relative_to_workspace(data_path),
        "figure_path": relative_to_workspace(figure_path),
        "source_reference": "official paper figure, not redistributed in this public repository",
        "red_boundary_provenance": "supplement_disk_table_reference",
        "blue_boundary_formula": "m=2+gamma^2",
        "bloch_boundary_formula": "m=2±sqrt(2)gamma",
        "grid": {"gamma_points": gamma_points},
    }
    check_path.parent.mkdir(parents=True, exist_ok=True)
    check_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return result


def write_rows(rows: list[dict[str, float | str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDNAMES})


def render_disk_phase_diagram(rows: list[dict[str, float | str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_series = {
        series_id: sorted(
            [row for row in rows if row["series_id"] == series_id],
            key=lambda row: float(row["gamma"]),
        )
        for series_id in {row["series_id"] for row in rows}
    }
    gamma_values = np.asarray(
        [float(row["gamma"]) for row in by_series["source_disk_numerical_boundary"]]
    )
    source_boundary = np.asarray(
        [float(row["m"]) for row in by_series["source_disk_numerical_boundary"]]
    )

    fig, ax = plt.subplots(figsize=(3.45, 2.35), dpi=180)
    ax.set_facecolor("#fbfbfb")
    ax.fill_betweenx(gamma_values, M_MIN, source_boundary, color="#e9f7f7", zorder=0)
    plot_series(ax, by_series["bloch_boundary_lower"], color="#999999", linestyle=":", linewidth=1.1, zorder=2)
    plot_series(ax, by_series["bloch_boundary_upper"], color="#777777", linestyle=":", linewidth=1.1, zorder=2)
    plot_series(ax, by_series["source_disk_numerical_boundary"], color="#ff1b35", linestyle="-", linewidth=1.2, zorder=4)
    plot_series(ax, by_series["non_bloch_theory_boundary"], color="#1c49ff", linestyle="--", linewidth=1.0, zorder=5)
    ax.text(1.68, 0.38, r"$C=1$", fontsize=10)
    ax.text(2.25, 0.38, r"$C=0$", fontsize=10)
    ax.text(1.62, 0.18, r"$m_-$", fontsize=10)
    ax.text(2.42, 0.18, r"$m_+$", fontsize=10)
    ax.set_xlim(M_MIN, M_MAX)
    ax.set_ylim(GAMMA_MIN, GAMMA_MAX)
    ax.set_xlabel(r"$m$", fontsize=9, loc="right", labelpad=0)
    ax.set_ylabel(r"$\gamma$", fontsize=9, loc="top", rotation=0, labelpad=-9)
    ax.set_xticks(np.arange(1.4, 2.8, 0.2))
    ax.set_yticks([0.0, 0.2, 0.4])
    ax.tick_params(axis="both", labelsize=8, direction="in", pad=1)
    fig.tight_layout(pad=0.1)
    fig.savefig(path)
    plt.close(fig)


def plot_series(axis, rows: list[dict[str, float | str]], *, color: str, linestyle: str, linewidth: float, zorder: int) -> None:
    axis.plot(
        [float(row["m"]) for row in rows],
        [float(row["gamma"]) for row in rows],
        color=color,
        linestyle=linestyle,
        linewidth=linewidth,
        zorder=zorder,
    )


def relative_to_workspace(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(WORKSPACE.resolve()))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
