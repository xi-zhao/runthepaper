#!/usr/bin/env python3
"""Render the saved L=28 symmetry-sector outputs without rerunning ED."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIFFERENCE_REASON = (
    "Difference reason: same k=0, I=+1 sector at L=28; the paper uses L=32, "
    "whose dense matrix alone is about 47GB before eigensolver workspace."
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def plot_sector_outputs(root: Path = ROOT) -> None:
    data_dir = root / "outputs/data"
    check_path = root / "outputs/checks/symmetry_resolved_sector.json"
    figure_dir = root / "outputs/figures"
    checks = json.loads(check_path.read_text(encoding="utf-8"))
    reason = checks.get("difference_reasons", {}).get(
        "sector_figures", DEFAULT_DIFFERENCE_REASON.removeprefix("Difference reason: ")
    )
    footnote = reason if reason.startswith("Difference reason:") else f"Difference reason: {reason}"

    tower_rows = _read_csv(data_dir / "sector_scar_tower.csv")
    energies = np.array([float(row["energy"]) for row in tower_rows])
    overlaps = np.array([float(row["z2_overlap_sq"]) for row in tower_rows])
    is_tower = np.array([bool(int(row["is_tower_state"])) for row in tower_rows])
    sector = checks["sector"]

    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    ax.semilogy(energies, np.maximum(overlaps, 1e-16), ".", markersize=2, color="0.6")
    ax.semilogy(
        energies[is_tower],
        overlaps[is_tower],
        "o",
        markersize=5,
        color="tab:red",
        label=f"top {int(np.count_nonzero(is_tower))} tower states",
    )
    ax.set_xlabel("E")
    ax.set_ylabel(r"$|\langle Z_2|E\rangle|^2$")
    ax.set_ylim(1e-10, 1.0)
    ax.set_title(
        f"PXP L={sector['L']}, k=0, I=+1 sector (dim {sector['dimension']})",
        fontsize=10,
    )
    ax.legend(fontsize=8)
    fig.tight_layout(rect=(0, 0.18, 1, 1))
    fig.text(0.5, 0.025, footnote, ha="center", va="bottom", fontsize=7.4, wrap=True)
    fig.savefig(figure_dir / "sector_scar_tower.png", dpi=150)
    plt.close(fig)

    spacing_rows = _read_csv(data_dir / "sector_level_spacings.csv")
    spacings = np.array([float(row["unfolded_spacing"]) for row in spacing_rows])
    hist, edges = np.histogram(spacings, bins=40, range=(0.0, 4.0), density=True)
    centers = 0.5 * (edges[1:] + edges[:-1])
    wigner = (np.pi / 2.0) * centers * np.exp(-np.pi * centers**2 / 4.0)
    poisson = np.exp(-centers)
    stats = checks["level_statistics"]

    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    ax.bar(centers, hist, width=centers[1] - centers[0], color="#9fc5e8", label="unfolded spacings")
    ax.plot(centers, wigner, "-", color="tab:red", label="Wigner surmise (GOE)")
    ax.plot(centers, poisson, "--", color="0.4", label="Poisson")
    ax.set_xlabel("s")
    ax.set_ylabel("P(s)")
    ax.set_title(
        f"<r> = {stats['mean_gap_ratio']:.4f}  "
        f"(GOE {stats['goe_reference']}, Poisson {stats['poisson_reference']})",
        fontsize=10,
    )
    ax.legend(fontsize=8)
    fig.tight_layout(rect=(0, 0.19, 1, 1))
    fig.text(0.5, 0.025, footnote, ha="center", va="bottom", fontsize=7.4, wrap=True)
    fig.savefig(figure_dir / "sector_level_statistics.png", dpi=150)
    plt.close(fig)


def main() -> None:
    plot_sector_outputs(ROOT)


if __name__ == "__main__":
    main()
