#!/usr/bin/env python3
"""Render deterministic evidence for idx93 transcription/provenance failures."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from spex_audit import free_energy_x0  # noqa: E402


def main() -> None:
    alphas = np.arange(2.0, 16.0)
    x = np.linspace(-3.0, 3.0, 301)
    source_barrier = []
    frozen_barrier = []
    for alpha in alphas:
        source_barrier.append(free_energy_x0(x, alpha, n_y=4001)[len(x) // 2])
        frozen_barrier.append(free_energy_x0(x, alpha, n_y=4001, use_frozen_transcription=True)[len(x) // 2])

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.linewidth": 0.8})
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), constrained_layout=True)
    axes[0].plot(alphas, source_barrier, marker="o", ms=3, label="source SI potential")
    axes[0].plot(alphas, frozen_barrier, marker="s", ms=3, ls="--", label="frozen transcription")
    axes[0].set(xlabel=r"$\alpha$", ylabel=r"$A(0)-\min A$ ($k_BT$)", title="a  Potential transcription gate")
    axes[0].legend(frameon=False)

    labels = ["acceptance\nratio", "mechanism\nB", "channel\nratio", r"$N_s/N_{force}$", r"$R_{ex}$", "22.75×\nspeedup"]
    support = [0.5, 1.0, 1.0, 0.0, 0.0, 0.0]
    colors = ["#fdae61" if v == 0.5 else "#1a9850" if v == 1 else "#d73027" for v in support]
    axes[1].bar(np.arange(len(labels)), support, color=colors)
    axes[1].set_xticks(np.arange(len(labels)), labels, rotation=25, ha="right")
    axes[1].set(ylim=(0, 1.1), ylabel="source support", title="b  Frozen-answer provenance")
    axes[1].set_yticks([0, 0.5, 1], ["absent", "conditional", "explicit"])

    out = CASE_ROOT / "outputs/figures"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "idx93_gold_audit.png", dpi=220, facecolor="white")
    fig.savefig(out / "idx93_gold_audit.pdf", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
