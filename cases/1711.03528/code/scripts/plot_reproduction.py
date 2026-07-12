from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


WORKSPACE = Path(__file__).resolve().parents[2]
DATA = WORKSPACE / "outputs" / "data"
FIGURES = WORKSPACE / "outputs" / "figures"


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def groups(rows: list[dict], key: str) -> dict[str, list[dict]]:
    out = defaultdict(list)
    for row in rows:
        out[row[key]].append(row)
    return dict(out)


def plot_fig1_graph() -> None:
    nodes = read_rows(DATA / "fig1_graph_nodes.csv")
    edges = read_rows(DATA / "fig1_graph_edges.csv")
    by_state = {row["state"]: row for row in nodes}
    fig, ax = plt.subplots(figsize=(8.8, 4.6), constrained_layout=True)
    for edge in edges:
        source = by_state[edge["source"]]
        target = by_state[edge["target"]]
        ax.plot(
            [float(source["x"]), float(target["x"])],
            [float(source["y"]), float(target["y"])],
            color="0.72",
            linewidth=1.0,
            zorder=1,
        )
    xs = np.array([float(row["x"]) for row in nodes])
    ys = np.array([float(row["y"]) for row in nodes])
    colors = np.array([float(row["hamming_distance_from_z2"]) for row in nodes])
    ax.scatter(xs, ys, c=colors, cmap="viridis", s=140, edgecolors="black", linewidths=0.8, zorder=2)
    for row in nodes:
        ax.text(float(row["x"]), float(row["y"]), row["state"], ha="center", va="center", fontsize=6, color="white", zorder=3)
    ax.set_xlabel("Hamming distance from Z2")
    ax.set_ylabel("allowed product states")
    ax.set_title("PXP Hamiltonian graph, L=6")
    ax.set_yticks([])
    ax.grid(axis="x", alpha=0.18)
    fig.savefig(FIGURES / "fig1_hilbert_graph_reproduction.png", dpi=220)
    plt.close(fig)


def plot_dynamics() -> None:
    rows = read_rows(DATA / "fig_ent_dynamics.csv")
    fig, axes = plt.subplots(1, 3, figsize=(14.2, 4.2), constrained_layout=True)
    palette = {"z2": "black", "z3": "#1f77b4", "z4": "#2ca02c", "vacuum": "#d62728"}
    for name, group in groups(rows, "initial_state").items():
        group = sorted(group, key=lambda row: float(row["time"]))
        time = np.array([float(row["time"]) for row in group])
        entropy = np.array([float(row["entanglement_entropy"]) for row in group])
        zz = np.array([float(row["nearest_neighbor_zz"]) for row in group])
        ret = np.array([float(row["return_probability"]) for row in group])
        axes[0].plot(time, entropy, color=palette.get(name), label=name)
        axes[1].plot(time, zz, color=palette.get(name), label=name)
        axes[2].plot(time, ret, color=palette.get(name), label=name)
    axes[0].set_title("entanglement growth")
    axes[0].set_ylabel("S_half")
    axes[1].set_title("local ZZ oscillations")
    axes[1].set_ylabel("<Zi Zi+1>")
    axes[2].set_title("return probability")
    axes[2].set_ylabel("|<psi(0)|psi(t)>|^2")
    for ax in axes:
        ax.set_xlabel("time")
        ax.grid(alpha=0.2)
        ax.legend(frameon=False, fontsize=8)
    fig.savefig(FIGURES / "fig_ent_dynamics_reproduction.png", dpi=220)
    plt.close(fig)


def plot_special_states() -> None:
    scatter = read_rows(DATA / "fig2a_scar_overlaps.csv")
    overlaps = read_rows(DATA / "fig2bc_fsa_basis_overlaps.csv")
    pr_rows = read_rows(DATA / "fig2d_participation_ratio.csv")
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 9.0), constrained_layout=True)

    exact = [row for row in scatter if not str(row["eigen_index"]).startswith("fsa")]
    fsa = [row for row in scatter if str(row["eigen_index"]).startswith("fsa")]
    axes[0, 0].scatter(
        [float(row["energy"]) for row in exact],
        [float(row["z2_overlap"]) for row in exact],
        s=8,
        alpha=0.42,
        color="0.2",
        label="exact ED",
    )
    axes[0, 0].scatter(
        [float(row["energy"]) for row in fsa],
        [float(row["z2_overlap"]) for row in fsa],
        marker="x",
        s=46,
        color="#d62728",
        label="FSA",
    )
    axes[0, 0].set_yscale("log")
    axes[0, 0].set_xlabel("energy")
    axes[0, 0].set_ylabel("overlap with Z2")
    axes[0, 0].set_title("scar tower from Z2 overlaps")
    axes[0, 0].legend(frameon=False)
    axes[0, 0].grid(alpha=0.2)

    for panel, ax in [("ground_state", axes[0, 1]), ("near_zero_scar", axes[1, 0])]:
        group = sorted([row for row in overlaps if row["panel"] == panel], key=lambda row: int(row["n"]))
        n = [int(row["n"]) for row in group]
        exact_projection = [float(row["exact_projection"]) for row in group]
        fsa_projection = [float(row["fsa_projection"]) for row in group]
        ax.plot(n, exact_projection, "o-", color="black", label="exact projected on FSA basis")
        ax.plot(n, fsa_projection, "s--", color="#d62728", label="FSA eigenstate")
        ax.set_xlabel("FSA basis index n")
        ax.set_ylabel("|projection|^2")
        ax.set_title(panel.replace("_", " "))
        ax.grid(alpha=0.2)
        ax.legend(frameon=False, fontsize=8)

    pr_rows = sorted(pr_rows, key=lambda row: int(row["L"]))
    L = [int(row["L"]) for row in pr_rows]
    axes[1, 1].plot(L, [float(row["average_pr2_middle"]) for row in pr_rows], "o-", color="0.35", label="middle-spectrum average")
    axes[1, 1].plot(L, [float(row["special_pr2_average"]) for row in pr_rows], "o-", color="#d62728", label="high-Z2-overlap states")
    axes[1, 1].plot(L, [float(row["inverse_dimension"]) for row in pr_rows], "k:", label="1 / constrained dimension")
    axes[1, 1].set_yscale("log")
    axes[1, 1].set_xlabel("L")
    axes[1, 1].set_ylabel("PR2")
    axes[1, 1].set_title("participation-ratio enhancement")
    axes[1, 1].grid(alpha=0.2)
    axes[1, 1].legend(frameon=False, fontsize=8)

    fig.savefig(FIGURES / "fig2_special_states_reproduction.png", dpi=220)
    plt.close(fig)


def plot_level_statistics() -> None:
    spacing = read_rows(DATA / "fig4_level_spacing_distribution.csv")
    density = read_rows(DATA / "fig4_density_of_states.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.2), constrained_layout=True)
    for L, group in groups(spacing, "L").items():
        group = sorted(group, key=lambda row: float(row["s_over_mean"]))
        axes[0].plot([float(row["s_over_mean"]) for row in group], [float(row["probability_density"]) for row in group], label=f"L={L}")
    s = np.linspace(0, 4, 300)
    axes[0].plot(s, np.exp(-s), ":", color="0.45", label="Poisson")
    axes[0].plot(s, (np.pi / 2) * s * np.exp(-np.pi * s**2 / 4), "--", color="black", label="WD GOE")
    axes[0].plot(s, 4 * s * np.exp(-2 * s), "-.", color="#d62728", label="Semi-Poisson")
    axes[0].set_xlabel("s / <s>")
    axes[0].set_ylabel("P(s)")
    axes[0].set_title("level-spacing distribution")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(alpha=0.2)

    for L, group in groups(density, "L").items():
        group = sorted(group, key=lambda row: float(row["energy"]))
        axes[1].plot([float(row["energy"]) for row in group], [float(row["density"]) for row in group], label=f"L={L}")
    axes[1].set_xlabel("energy")
    axes[1].set_ylabel("density")
    axes[1].set_title("density of states")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(alpha=0.2)
    fig.savefig(FIGURES / "fig4_level_statistics_reproduction.png", dpi=220)
    plt.close(fig)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    plot_fig1_graph()
    plot_dynamics()
    plot_special_states()
    plot_level_statistics()


if __name__ == "__main__":
    main()
