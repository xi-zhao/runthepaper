from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


WORKSPACE = Path(__file__).resolve().parents[2]
SRC = WORKSPACE / "code" / "src"
sys.path.insert(0, str(SRC))

from nonhermitian_chern import (  # noqa: E402
    CylinderParams,
    non_bloch_cylinder_bulk_eigenvalues,
)


DATA_PATH = WORKSPACE / "outputs" / "data" / "first_target.csv"
CHECK_PATH = WORKSPACE / "outputs" / "checks" / "edge_branch_diagnostic.json"
FIGURE_PATH = WORKSPACE / "outputs" / "figures" / "edge_branch_diagnostic.png"
BULK_KY_POINTS = 720
EDGE_TRACE_RESIDUAL_TOLERANCE = 0.005
PLATEAU_IMAG_TOLERANCE = 0.006
EDGE_WEIGHT_DIAGNOSTIC_THRESHOLD = 0.35


def main() -> int:
    result = analyze_edge_branch_candidates()
    write_outputs(result)
    print(json.dumps(result["summary"], indent=2, ensure_ascii=False))
    return 0


def analyze_edge_branch_candidates(
    data_path: Path = DATA_PATH,
    params: CylinderParams | None = None,
    bulk_ky_points: int = BULK_KY_POINTS,
    edge_trace_residual_tolerance: float = EDGE_TRACE_RESIDUAL_TOLERANCE,
    plateau_imag_tolerance: float = PLATEAU_IMAG_TOLERANCE,
) -> dict[str, object]:
    params = params or CylinderParams()
    rows = read_rows(data_path)
    continuum_by_kx = build_continuum_by_kx(rows, params, bulk_ky_points)
    trace_matches = build_edge_trace_matches(
        rows, params, edge_trace_residual_tolerance
    )
    enriched_rows = []
    for row in rows:
        continuum = continuum_by_kx[int(row["kx_index"])]
        energy = complex(float(row["energy_real"]), float(row["energy_imag"]))
        distance = nearest_complex_distance(energy, continuum)
        edge_weight = max(float(row["edge_weight_left"]), float(row["edge_weight_right"]))
        on_edge_plateau = abs(abs(energy.imag) - params.gamma_x) <= plateau_imag_tolerance
        trace_match = trace_matches.get(int(row["sort_key"]))
        high_confidence = bool(trace_match) and on_edge_plateau
        enriched_rows.append(
            {
                **row,
                "bulk_continuum_distance": distance,
                "max_edge_weight": edge_weight,
                "edge_plateau_candidate": on_edge_plateau,
                "edge_branch_core_candidate": high_confidence,
                "edge_trace_label": trace_match[0] if trace_match else "",
                "edge_trace_residual": trace_match[1] if trace_match else None,
            }
        )

    distances = np.asarray(
        [float(row["bulk_continuum_distance"]) for row in enriched_rows], dtype=float
    )
    old_edge_count = sum(row["series_id"] != "bulk_spectrum_all_kx" for row in rows)
    high_confidence_count = sum(
        bool(row["edge_branch_core_candidate"]) for row in enriched_rows
    )
    summary = {
        "schema_version": 1,
        "paper_id": "1804.04672",
        "target_id": "T001",
        "status": "diagnosed",
        "physical_object": "cylinder complex spectrum edge branch classifier",
        "row_count": len(rows),
        "old_edge_localization_candidate_count": old_edge_count,
        "high_confidence_edge_core_count": high_confidence_count,
        "edge_trace_residual_tolerance": edge_trace_residual_tolerance,
        "plateau_imag_tolerance": plateau_imag_tolerance,
        "edge_weight_diagnostic_threshold": EDGE_WEIGHT_DIAGNOSTIC_THRESHOLD,
        "bulk_ky_points": bulk_ky_points,
        "bulk_distance_quantiles": quantiles(distances),
        "diagnosis": {
            "primary_suspect": "edge_state_classification",
            "interpretation": (
                "Boundary weight alone over-labels skin-localized bulk states. "
                "The red edge branch is better captured by tracing the analytic "
                "chiral edge energies E_+=sin(kx)+i gamma and E_-=-sin(kx)-i gamma; "
                "right-eigenvector edge weight and non-Bloch bulk distance are diagnostics."
            ),
            "next_step": (
                "Promote EPS/PDF point-set extraction into a quantitative validation gate "
                "for red branch cardinality, marker placement, and pixel layout."
            ),
        },
        "outputs": {
            "check": "outputs/checks/edge_branch_diagnostic.json",
            "figure": "outputs/figures/edge_branch_diagnostic.png",
        },
    }
    return {
        "summary": summary,
        "rows": enriched_rows,
        "continuum_by_kx": continuum_by_kx,
    }


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def build_continuum_by_kx(
    rows: list[dict[str, str]], params: CylinderParams, bulk_ky_points: int
) -> dict[int, np.ndarray]:
    kx_by_index: dict[int, float] = {}
    for row in rows:
        kx_by_index[int(row["kx_index"])] = float(row["kx"])
    return {
        kx_index: non_bloch_cylinder_bulk_eigenvalues(kx, params, bulk_ky_points)
        for kx_index, kx in sorted(kx_by_index.items())
    }


def build_edge_trace_matches(
    rows: list[dict[str, str]],
    params: CylinderParams,
    edge_trace_residual_tolerance: float,
) -> dict[int, tuple[str, float]]:
    rows_by_kx: dict[int, list[dict[str, str]]] = {}
    for row in rows:
        rows_by_kx.setdefault(int(row["kx_index"]), []).append(row)

    matches: dict[int, tuple[str, float]] = {}
    for kx_rows in rows_by_kx.values():
        kx = float(kx_rows[0]["kx"])
        targets = {
            "upper_chiral_edge": complex(np.sin(kx), params.gamma_x),
            "lower_chiral_edge": complex(-np.sin(kx), -params.gamma_x),
        }
        for trace_label, target in targets.items():
            nearest_row = min(
                kx_rows,
                key=lambda row: abs(
                    complex(float(row["energy_real"]), float(row["energy_imag"]))
                    - target
                ),
            )
            residual = abs(
                complex(
                    float(nearest_row["energy_real"]),
                    float(nearest_row["energy_imag"]),
                )
                - target
            )
            if residual <= edge_trace_residual_tolerance:
                matches[int(nearest_row["sort_key"])] = (trace_label, float(residual))
    return matches


def nearest_complex_distance(value: complex, candidates: np.ndarray) -> float:
    return float(np.min(np.abs(candidates - value)))


def quantiles(values: np.ndarray) -> dict[str, float]:
    return {
        "min": float(np.min(values)),
        "p50": float(np.quantile(values, 0.50)),
        "p90": float(np.quantile(values, 0.90)),
        "p95": float(np.quantile(values, 0.95)),
        "p99": float(np.quantile(values, 0.99)),
        "max": float(np.max(values)),
    }


def write_outputs(result: dict[str, object]) -> None:
    CHECK_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHECK_PATH.write_text(
        json.dumps(result["summary"], indent=2, ensure_ascii=False) + "\n"
    )
    write_figure(result, FIGURE_PATH)


def write_figure(result: dict[str, object], path: Path) -> None:
    rows = result["rows"]
    continuum_by_kx = result["continuum_by_kx"]
    path.parent.mkdir(parents=True, exist_ok=True)

    all_energy = np.asarray(
        [
            complex(float(row["energy_real"]), float(row["energy_imag"]))
            for row in rows
        ],
        dtype=np.complex128,
    )
    edge_core = np.asarray(
        [
            complex(float(row["energy_real"]), float(row["energy_imag"]))
            for row in rows
            if row["edge_branch_core_candidate"]
        ],
        dtype=np.complex128,
    )
    continuum = np.concatenate(list(continuum_by_kx.values()))

    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.8), dpi=160)
    ax = axes[0]
    ax.scatter(all_energy.real, all_energy.imag, s=1.2, color="0.78", linewidths=0)
    ax.scatter(
        continuum.real,
        continuum.imag,
        s=0.25,
        color="#2f5f9f",
        alpha=0.16,
        linewidths=0,
    )
    if len(edge_core):
        ax.scatter(
            edge_core.real,
            edge_core.imag,
            s=5.0,
            color="#c73e3a",
            linewidths=0,
        )
    ax.set_xlabel("Re(E)")
    ax.set_ylabel("Im(E)")
    ax.set_title("Finite strip, non-Bloch bulk, edge-core candidates", fontsize=8)
    ax.tick_params(direction="in", labelsize=8)

    distances = np.asarray(
        [float(row["bulk_continuum_distance"]) for row in rows], dtype=float
    )
    axes[1].hist(distances, bins=80, color="0.35", alpha=0.85)
    axes[1].axvline(
        np.quantile(distances, 0.99), color="#c73e3a", linewidth=1.2
    )
    axes[1].set_xlabel("distance to non-Bloch bulk continuum")
    axes[1].set_ylabel("state count")
    axes[1].set_title("Separation from bulk continuum", fontsize=8)
    axes[1].tick_params(direction="in", labelsize=8)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


if __name__ == "__main__":
    raise SystemExit(main())
