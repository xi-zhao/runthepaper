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

from nonhermitian_chern import generate_open_boundary_phase_diagram_rows  # noqa: E402


DATA_PATH = WORKSPACE / "outputs" / "data" / "fig1_open_boundary_phase.csv"
FIGURE_PATH = WORKSPACE / "outputs" / "figures" / "fig1_open_boundary_phase.png"
CHECK_PATH = WORKSPACE / "outputs" / "checks" / "fig1_open_boundary_phase.json"
SCORECARD_PATH = WORKSPACE / "outputs" / "checks" / "similarity_scorecard.json"

GAMMA_MIN = 0.0
GAMMA_MAX = 0.5
M_MIN = 1.25
M_MAX = 2.70

FIELDNAMES = [
    "target_id",
    "series_id",
    "gamma",
    "m",
    "region",
    "source",
]


def main() -> int:
    result = run_open_boundary_phase_diagram()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def run_open_boundary_phase_diagram(
    *,
    data_path: Path = DATA_PATH,
    figure_path: Path = FIGURE_PATH,
    check_path: Path = CHECK_PATH,
    scorecard_path: Path = SCORECARD_PATH,
    gamma_points: int = 51,
) -> dict[str, object]:
    gamma_values = np.linspace(GAMMA_MIN, GAMMA_MAX, gamma_points)
    rows = generate_open_boundary_phase_diagram_rows(gamma_values)
    write_rows(rows, data_path)
    render_open_boundary_phase_diagram(rows, figure_path)
    result = {
        "status": "passed" if data_path.exists() and figure_path.exists() else "failed",
        "target_id": "T003",
        "physical_object": "open-boundary phase diagram for the square geometry",
        "rows": len(rows),
        "data_path": relative_to_workspace(data_path),
        "figure_path": relative_to_workspace(figure_path),
        "source_reference": "official paper figure, not redistributed in this public repository",
        "red_boundary_provenance": "source_table_reference",
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


def render_open_boundary_phase_diagram(
    rows: list[dict[str, float | str]], path: Path
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_series = {
        series_id: sorted(
            [row for row in rows if row["series_id"] == series_id],
            key=lambda row: float(row["gamma"]),
        )
        for series_id in {row["series_id"] for row in rows}
    }
    gamma_values = np.asarray(
        [float(row["gamma"]) for row in by_series["source_numerical_boundary"]]
    )
    source_boundary = np.asarray(
        [float(row["m"]) for row in by_series["source_numerical_boundary"]]
    )

    fig, ax = plt.subplots(figsize=(3.35, 2.3), dpi=180)
    ax.set_facecolor("#fbfbfb")
    ax.fill_betweenx(
        gamma_values,
        M_MIN,
        source_boundary,
        color="#e9f7f7",
        zorder=0,
    )

    plot_series(
        ax,
        by_series["bloch_boundary_lower"],
        color="#999999",
        linestyle=":",
        linewidth=1.1,
        zorder=2,
    )
    plot_series(
        ax,
        by_series["bloch_boundary_upper"],
        color="#777777",
        linestyle=":",
        linewidth=1.1,
        zorder=2,
    )
    plot_series(
        ax,
        by_series["source_numerical_boundary"],
        color="#ff1b35",
        linestyle="-",
        linewidth=1.2,
        zorder=4,
    )
    plot_series(
        ax,
        by_series["non_bloch_theory_boundary"],
        color="#1c49ff",
        linestyle="--",
        linewidth=1.0,
        zorder=5,
    )

    star = by_series["fig2_marker_star"][0]
    square = by_series["fig2_marker_square"][0]
    ax.scatter([float(star["m"])], [float(star["gamma"])], marker="*", s=28, color="#333333", zorder=6)
    ax.scatter([float(square["m"])], [float(square["gamma"])], marker="s", s=14, color="#333333", zorder=6)

    ax.text(1.75, 0.38, r"$C=1$", fontsize=9)
    ax.text(2.23, 0.38, r"$C=0$", fontsize=9)
    ax.text(1.50, 0.25, r"$m_-$", fontsize=8)
    ax.text(2.42, 0.25, r"$m_+$", fontsize=8)
    ax.set_xlim(M_MIN, M_MAX)
    ax.set_ylim(GAMMA_MIN, GAMMA_MAX)
    ax.set_xlabel(r"$m$", fontsize=8, loc="right", labelpad=0)
    ax.set_ylabel(r"$\gamma$", fontsize=8, loc="top", rotation=0, labelpad=-8)
    ax.set_xticks(np.arange(1.4, 2.8, 0.2))
    ax.set_yticks([0.0, 0.2, 0.4])
    ax.tick_params(axis="both", labelsize=7, direction="in", pad=1)
    fig.tight_layout(pad=0.15)
    fig.savefig(path)
    plt.close(fig)


def plot_series(
    axis,
    rows: list[dict[str, float | str]],
    *,
    color: str,
    linestyle: str,
    linewidth: float,
    zorder: int,
) -> None:
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
        return str(path.relative_to(WORKSPACE))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
