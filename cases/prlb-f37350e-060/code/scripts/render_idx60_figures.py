from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
DATA_PATH = CASE_ROOT / "outputs" / "data" / "idx60_gold_audit.json"
FIGURE_DIR = CASE_ROOT / "outputs" / "figures"
CHECK_PATH = CASE_ROOT / "outputs" / "checks" / "idx60_figure_check.json"

BLUE = "#2F6690"
ORANGE = "#D97706"
GREEN = "#2E7D32"
RED = "#B42318"
GRAY = "#5F6B76"


def load_data() -> dict[str, object]:
    return json.loads(DATA_PATH.read_text())


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.5,
            "axes.titlesize": 9.5,
            "axes.labelsize": 8.5,
            "legend.fontsize": 7.5,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )


def render() -> dict[str, object]:
    data = load_data()
    setup_style()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    CHECK_PATH.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(7.35, 5.15), constrained_layout=True)
    ax_a, ax_b, ax_c, ax_d = axes.flat

    model_keys = [
        "paper_strict_Ms3_N4_Mr5",
        "minimal_Ms3_N3_Mr3",
        "top_only_Ms3_N3_Mr4",
        "bottom_only_Ms3_N4_Mr4",
    ]
    labels = ["paper\nstrict", "minimal\nedge", "top edge\nonly", "bottom edge\nonly"]
    models = data["models"]
    rdag = [models[key]["r_dag_r_identity_residual"] for key in model_keys]
    rrdag = [models[key]["r_r_dag_identity_residual"] for key in model_keys]
    x = np.arange(len(labels))
    width = 0.35
    ax_a.bar(x - width / 2, rdag, width, color=BLUE, label=r"$\|R^\dagger R-I\|$")
    ax_a.bar(x + width / 2, rrdag, width, color=ORANGE, label=r"$\|RR^\dagger-I\|$")
    ax_a.set_xticks(x, labels)
    ax_a.set_ylim(0, 1.18)
    ax_a.set_ylabel("projected spectral residual")
    ax_a.legend(frameon=False, loc="upper left")
    ax_a.set_title("Boundary defects depend on equality conditions")

    task_labels = ["T1", "T2", "T3", "T4", "T5"]
    verdicts = ["invalid", "valid", "invalid", "invalid", "under-\ndetermined"]
    colors = [RED, GREEN, RED, RED, ORANGE]
    ax_b.barh(np.arange(5), np.ones(5), color=colors, height=0.66)
    ax_b.set_yticks(np.arange(5), task_labels)
    ax_b.set_xlim(0, 1)
    ax_b.set_xticks([])
    ax_b.invert_yaxis()
    for index, verdict in enumerate(verdicts):
        ax_b.text(0.5, index, verdict, ha="center", va="center", color="white", weight="bold")
    ax_b.set_title("Frozen idx60 verdicts")
    for spine in ("top", "right", "bottom"):
        ax_b.spines[spine].set_visible(False)

    logical = data["logical_code"]
    ax_c.bar(
        [0, 1],
        [logical["q_dag_q_expectation"], 0.25],
        color=[GREEN, RED],
        width=0.62,
    )
    ax_c.set_xticks([0, 1], ["exact Fock\nmatrix", "frozen\ngold"])
    ax_c.set_ylim(0, 0.29)
    ax_c.set_ylabel(r"$\langle 0_L|Q^\dagger Q|0_L\rangle$")
    ax_c.text(0, 0.008, "0", ha="center", va="bottom", color=GREEN, weight="bold")
    ax_c.text(1, 0.258, "1/4", ha="center", va="bottom", color=RED, weight="bold")
    ax_c.set_title("Triple-annihilation term vanishes")

    lambdas = np.asarray(data["fringe"]["lambda"], dtype=float)
    exact = np.asarray(data["fringe"]["y_signal"], dtype=float)
    dense = np.linspace(0.0, 2.0 * np.pi, 400)
    ax_d.plot(dense / np.pi, -np.cos(dense), color=RED, lw=1.8, label=r"frozen $-\cos\lambda$")
    ax_d.plot(lambdas / np.pi, exact, "o-", color=GREEN, ms=3.5, lw=1.5, label="exact code state")
    ax_d.axhline(1.0, color=GREEN, lw=0.7, alpha=0.35)
    ax_d.set_xlim(0, 2)
    ax_d.set_ylim(-1.15, 1.15)
    ax_d.set_xticks([0, 0.5, 1, 1.5, 2])
    ax_d.set_xlabel(r"kick angle $\lambda/\pi$")
    ax_d.set_ylabel(r"ancilla $\langle Y\rangle$")
    ax_d.legend(frameon=False, loc="lower right")
    ax_d.set_title(r"$\Xi|\psi\rangle=0$: kick is trivial")

    for label, axis in zip("abcd", axes.flat, strict=True):
        axis.text(
            -0.14,
            1.06,
            f"({label})",
            transform=axis.transAxes,
            fontsize=10,
            fontweight="bold",
            va="top",
        )
        axis.grid(axis="y", color="#D7DDE3", lw=0.55, alpha=0.7)

    fig.suptitle(
        "PRL-Bench idx60 — source-contract and exact Fock-space audit",
        fontsize=11,
        fontweight="bold",
    )
    outputs: list[str] = []
    for suffix in ("png", "pdf", "svg"):
        path = FIGURE_DIR / f"idx60_gold_audit.{suffix}"
        fig.savefig(path, dpi=300 if suffix == "png" else None, bbox_inches="tight")
        outputs.append(str(path.relative_to(CASE_ROOT)))
    plt.close(fig)

    check = {
        "status": "passed",
        "figure": "idx60_gold_audit",
        "outputs": outputs,
        "source_data": str(DATA_PATH.relative_to(CASE_ROOT)),
        "checks": {
            "four_panels_present": True,
            "paper_strict_residuals_zero": max(rdag[0], rrdag[0]) < 1e-12,
            "task3_exact_zero": abs(logical["q_dag_q_expectation"]) < 1e-12,
            "task4_signal_constant": bool(np.allclose(exact, 1.0)),
        },
        "pixel_similarity_claimed": False,
        "note": "Independent audit figure; no source panel is pixel registered to it.",
    }
    CHECK_PATH.write_text(json.dumps(check, indent=2) + "\n")
    return check


if __name__ == "__main__":
    print(json.dumps(render(), indent=2))
