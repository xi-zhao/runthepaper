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
    classify_cylinder_phase_point,
    generate_cylinder_phase_diagram_rows,
)


DATA_PATH = WORKSPACE / "outputs" / "data" / "fig3a_cylinder_phase.csv"
FIGURE_PATH = WORKSPACE / "outputs" / "figures" / "fig3a_cylinder_phase.png"
CHECK_PATH = WORKSPACE / "outputs" / "checks" / "fig3a_cylinder_phase.json"
SCORECARD_PATH = WORKSPACE / "outputs" / "checks" / "similarity_scorecard.json"

GAMMA_MIN = 0.0
GAMMA_MAX = 0.5
M_MIN = 1.3
M_MAX = 2.7
GAP_THRESHOLD = 0.02
STAR_GAMMA = 0.2
STAR_M = 1.717

FIELDNAMES = [
    "target_id",
    "series_id",
    "branch",
    "gamma",
    "m",
    "region",
    "line_gap",
    "source",
]


def main() -> int:
    result = run_cylinder_phase_diagram()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def run_cylinder_phase_diagram(
    *,
    data_path: Path = DATA_PATH,
    figure_path: Path = FIGURE_PATH,
    check_path: Path = CHECK_PATH,
    scorecard_path: Path = SCORECARD_PATH,
    gamma_points: int = 41,
    m_points: int = 81,
    kx_points: int = 41,
    ky_points: int = 41,
) -> dict[str, object]:
    gamma_values = np.linspace(GAMMA_MIN, GAMMA_MAX, gamma_points)
    m_values = np.linspace(M_MIN, M_MAX, m_points)
    rows = generate_cylinder_phase_diagram_rows(
        gamma_values=gamma_values,
        m_values=m_values,
        kx_points=kx_points,
        ky_points=ky_points,
        gap_threshold=GAP_THRESHOLD,
    )
    write_rows(rows, data_path)
    render_cylinder_phase_diagram(rows, figure_path)
    star_region = classify_cylinder_phase_point(
        gamma=STAR_GAMMA,
        m=STAR_M,
        kx_points=kx_points,
        ky_points=ky_points,
        gap_threshold=GAP_THRESHOLD,
    )
    result = {
        "status": "passed" if figure_path.exists() and data_path.exists() else "failed",
        "target_id": "T002",
        "physical_object": "cylinder phase diagram from non-Bloch band-touching boundaries",
        "rows": len(rows),
        "data_path": relative_to_workspace(data_path),
        "figure_path": relative_to_workspace(figure_path),
        "source_reference": "official paper figure, not redistributed in this public repository",
        "star_point": {"m": STAR_M, "gamma": STAR_GAMMA},
        "star_region": star_region,
        "boundary_formula": "m=1+sqrt(1±2γ+2γ^2)",
        "classification_criterion": (
            "gapless inside the two non-Bloch cylinder band-touching "
            "boundaries; chern_one to the left and chern_zero to the right"
        ),
        "grid": {
            "gamma_points": gamma_points,
            "m_points": m_points,
            "kx_points": kx_points,
            "ky_points": ky_points,
        },
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


def render_cylinder_phase_diagram(
    rows: list[dict[str, float | str]], path: Path
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    region_rows = [row for row in rows if row["series_id"] == "cylinder_phase_region"]
    gamma_values = sorted({float(row["gamma"]) for row in region_rows})
    m_values = sorted({float(row["m"]) for row in region_rows})
    gap_grid = np.full((len(gamma_values), len(m_values)), np.nan)
    gapless_grid = np.zeros((len(gamma_values), len(m_values)))
    gamma_index = {value: index for index, value in enumerate(gamma_values)}
    m_index = {value: index for index, value in enumerate(m_values)}
    for row in region_rows:
        gap_grid[gamma_index[float(row["gamma"])], m_index[float(row["m"])]] = float(
            row["line_gap"]
        )
        if row["region"] == "gapless":
            gapless_grid[gamma_index[float(row["gamma"])], m_index[float(row["m"])]] = 1.0

    m_mesh, gamma_mesh = np.meshgrid(m_values, gamma_values)
    fig, ax = plt.subplots(figsize=(3.1, 2.6), dpi=180)
    ax.set_facecolor("#f8fbfb")
    ax.axvspan(M_MIN, 2.0, color="#edf8f8", zorder=0)
    ax.axvspan(2.0, M_MAX, color="#fbfbfb", zorder=0)
    ax.contourf(
        m_mesh,
        gamma_mesh,
        gapless_grid,
        levels=[0.5, 1.5],
        colors=["#f6cda8"],
        zorder=1,
    )
    boundary_rows = [
        row for row in rows if row["series_id"] == "non_bloch_gap_boundary"
    ]
    for branch in ["lower", "upper"]:
        branch_rows = sorted(
            [row for row in boundary_rows if row.get("branch") == branch],
            key=lambda row: float(row["gamma"]),
        )
        if branch_rows:
            m_points, gamma_points = smooth_boundary_curve(branch_rows)
            ax.plot(
                m_points,
                gamma_points,
                color="#ff4e1f",
                linewidth=1.2,
                zorder=4,
            )

    lower = sorted(
        [row for row in rows if row["series_id"] == "bloch_boundary_lower"],
        key=lambda row: float(row["gamma"]),
    )
    upper = sorted(
        [row for row in rows if row["series_id"] == "bloch_boundary_upper"],
        key=lambda row: float(row["gamma"]),
    )
    ax.plot(
        [float(row["m"]) for row in lower],
        [float(row["gamma"]) for row in lower],
        color="#888888",
        linestyle=":",
        linewidth=1.0,
        zorder=3,
    )
    ax.plot(
        [float(row["m"]) for row in upper],
        [float(row["gamma"]) for row in upper],
        color="#888888",
        linestyle=":",
        linewidth=1.0,
        zorder=3,
    )
    ax.scatter([STAR_M], [STAR_GAMMA], marker="*", color="#333333", s=30, zorder=5)
    ax.text(1.52, 0.16, r"$C_y=1$", fontsize=8)
    ax.text(2.28, 0.16, r"$C_y=0$", fontsize=8)
    ax.text(1.91, 0.34, "gapless", fontsize=8, ha="center")
    ax.text(1.38, 0.34, r"$m_-$", fontsize=8)
    ax.text(2.52, 0.34, r"$m_+$", fontsize=8)
    ax.set_xlim(M_MIN, M_MAX)
    ax.set_ylim(GAMMA_MIN, GAMMA_MAX)
    ax.set_xlabel(r"$m$", fontsize=8, loc="right", labelpad=0)
    ax.set_ylabel(r"$\gamma$", fontsize=8, loc="top", rotation=0, labelpad=-6)
    ax.set_xticks(np.arange(1.4, 2.8, 0.2))
    ax.set_yticks([0.0, 0.2, 0.4])
    ax.tick_params(axis="both", labelsize=7, direction="in", pad=1)
    fig.tight_layout(pad=0.2)
    fig.savefig(path)
    plt.close(fig)


def smooth_boundary_curve(
    branch_rows: list[dict[str, float | str]],
) -> tuple[np.ndarray, np.ndarray]:
    gamma_values = np.asarray([float(row["gamma"]) for row in branch_rows])
    m_values = np.asarray([float(row["m"]) for row in branch_rows])
    if len(branch_rows) < 5:
        return m_values, gamma_values

    gamma_dense = np.linspace(float(gamma_values.min()), float(gamma_values.max()), 180)
    degree = min(4, len(branch_rows) - 1)
    coefficients = np.polyfit(gamma_values, m_values, deg=degree)
    smoothed_m = np.polyval(coefficients, gamma_dense)
    smoothed_m[0] = m_values[0]
    smoothed_m[-1] = m_values[-1]
    return smoothed_m, gamma_dense


def relative_to_workspace(path: Path) -> str:
    try:
        return str(path.relative_to(WORKSPACE))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
