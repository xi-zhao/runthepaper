#!/usr/bin/env python3
"""Fig. 3(b,c,d): finite-size scaling collapse of the endpoint mutual info.

The paper collapses I_end(epsilon, L) for three couplings J_z onto a single
universal curve with

    x = (epsilon - epsilon_c) * L^{1/nu}       (horizontal rescaling)
    y = L^{beta} * I_end                        (vertical rescaling)

and reads the DTC->paramagnet critical point (epsilon_c) and exponents
(beta, nu) off the best collapse. This script consumes the merged campaign
CSV (one paper point per (panel, L, epsilon)) and does two things per panel:

1. Draws the collapse using the paper's own (epsilon_c, beta, nu) and scores
   how tightly the L curves overlap (median relative spread over the shared
   x-window). This is a generation + reference-comparison artefact.
2. Re-optimizes (epsilon_c, beta, nu) by minimizing a curve-collapse cost and
   reports the fitted values next to the paper's - the panel (d) critical
   exponent extraction, done honestly from our own small-L data.

Panel status here is *generation coverage*: producing the collapse plot and
the exponent table flips b/c/d to reproduced. The numeric agreement (spread,
|fitted-paper|) feeds parameter_match / reference_comparison, not the ledger.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA_CSV = ROOT / "outputs/data/fig3_large_ed_campaign.csv"
FIGURE_PATH = ROOT / "outputs/figures/fig3_scaling_collapse.png"
CHECK_PATH = ROOT / "outputs/checks/fig3_scaling_collapse.json"
DIFFERENCE_REASON = (
    "Difference reason: this medium campaign stops at L=12 and uses reduced "
    "disorder sampling; the paper-scale exponent fit also needs L=14 "
    "(with optional L=16/18 checks) and larger statistics."
)

# Paper Fig. 3 critical point + exponents per coupling (panel -> params).
PAPER = {
    "Fig. 3b": {"J_z": 0.05, "epsilon_c": 0.043, "beta": 0.42, "nu": 1.21},
    "Fig. 3c": {"J_z": 0.10, "epsilon_c": 0.081, "beta": 0.44, "nu": 1.24},
    "Fig. 3d": {"J_z": 0.15, "epsilon_c": 0.130, "beta": 0.47, "nu": 1.35},
}


def load_points() -> dict[str, dict[int, tuple[np.ndarray, np.ndarray]]]:
    """panel -> L -> (epsilon[], MI[]) sorted by epsilon."""

    raw: dict[str, dict[int, list[tuple[float, float]]]] = defaultdict(lambda: defaultdict(list))
    with DATA_CSV.open() as handle:
        for row in csv.DictReader(handle):
            panel = row["panel"]
            L = int(row["L"])
            raw[panel][L].append((float(row["epsilon"]), float(row["endpoint_mutual_information"])))
    out: dict[str, dict[int, tuple[np.ndarray, np.ndarray]]] = {}
    for panel, by_l in raw.items():
        out[panel] = {}
        for L, pts in by_l.items():
            pts.sort()
            eps = np.array([p[0] for p in pts])
            mi = np.array([p[1] for p in pts])
            out[panel][L] = (eps, mi)
    return out


def collapse_cost(points: dict[int, tuple[np.ndarray, np.ndarray]],
                  epsilon_c: float, beta: float, nu: float) -> float:
    """Mean squared inter-curve gap on the shared rescaled-x overlap window.

    Each L gives x = (eps-eps_c) L^{1/nu}, y = L^{beta} I. We interpolate every
    curve onto the x-range shared by all sizes and sum pairwise squared y gaps,
    normalized by the mean |y| so panels with different scales compare fairly.
    """

    curves = []
    for L, (eps, mi) in points.items():
        x = (eps - epsilon_c) * (L ** (1.0 / nu))
        y = (L ** beta) * mi
        order = np.argsort(x)
        curves.append((x[order], y[order]))
    lo = max(c[0][0] for c in curves)
    hi = min(c[0][-1] for c in curves)
    if hi <= lo:
        return np.inf
    grid = np.linspace(lo, hi, 60)
    stacked = np.array([np.interp(grid, x, y) for x, y in curves])
    scale = np.mean(np.abs(stacked)) + 1e-12
    # variance across curves at each x, averaged -> relative collapse cost
    return float(np.mean(np.var(stacked, axis=0)) / scale**2)


def relative_spread(points: dict[int, tuple[np.ndarray, np.ndarray]],
                    epsilon_c: float, beta: float, nu: float) -> float:
    """Median across the shared window of std/|mean| of the rescaled curves."""

    curves = []
    for L, (eps, mi) in points.items():
        x = (eps - epsilon_c) * (L ** (1.0 / nu))
        y = (L ** beta) * mi
        order = np.argsort(x)
        curves.append((x[order], y[order]))
    lo = max(c[0][0] for c in curves)
    hi = min(c[0][-1] for c in curves)
    grid = np.linspace(lo, hi, 60)
    stacked = np.array([np.interp(grid, x, y) for x, y in curves])
    mean = np.mean(stacked, axis=0)
    std = np.std(stacked, axis=0)
    good = np.abs(mean) > 1e-6
    return float(np.median(std[good] / np.abs(mean[good])))


def optimize_exponents(points: dict[int, tuple[np.ndarray, np.ndarray]],
                       seed: dict) -> dict:
    """Local Nelder-Mead-free coordinate descent around the paper seed."""

    ec, be, nu = seed["epsilon_c"], seed["beta"], seed["nu"]
    best = (ec, be, nu)
    best_cost = collapse_cost(points, ec, be, nu)
    steps = {"epsilon_c": 0.02, "beta": 0.06, "nu": 0.15}
    for _ in range(400):
        improved = False
        for i, name in enumerate(("epsilon_c", "beta", "nu")):
            for direction in (+1, -1):
                trial = list(best)
                trial[i] += direction * steps[name]
                if name == "nu" and trial[i] <= 0.2:
                    continue
                cost = collapse_cost(points, *trial)
                if cost < best_cost - 1e-9:
                    best, best_cost, improved = tuple(trial), cost, True
        if not improved:
            for name in steps:
                steps[name] *= 0.5
            if all(s < 1e-3 for s in steps.values()):
                break
    return {"epsilon_c": round(best[0], 4), "beta": round(best[1], 4),
            "nu": round(best[2], 4), "cost": best_cost}


def main() -> int:
    points = load_points()
    panels = [p for p in ("Fig. 3b", "Fig. 3c", "Fig. 3d") if p in points]

    fig, axes = plt.subplots(1, len(panels), figsize=(5.0 * len(panels), 4.2))
    if len(panels) == 1:
        axes = [axes]

    # Analytic anchor: at epsilon=0 the endpoint pair is a perfect Bell pair,
    # so I_end = ln 2 exactly, for every L and every coupling.
    ln2 = float(np.log(2.0))
    anchor = {"ln2": round(ln2, 6), "mi_at_epsilon_zero": {}, "deep_tail_max": {}}
    for panel, by_l in points.items():
        for L, (eps, mi) in by_l.items():
            zero = mi[np.argmin(np.abs(eps))]
            anchor["mi_at_epsilon_zero"][f"{panel}|L{L}"] = round(float(zero), 6)
            deep = mi[eps >= 0.4]
            if deep.size:
                anchor["deep_tail_max"][f"{panel}|L{L}"] = round(float(np.max(deep)), 6)
    anchor["max_abs_error_vs_ln2"] = round(
        max(abs(v - ln2) for v in anchor["mi_at_epsilon_zero"].values()), 6
    )
    anchor["deep_tail_max_over_all"] = round(
        max(anchor["deep_tail_max"].values()), 6
    )

    report = {}
    for ax, panel in zip(axes, panels):
        params = PAPER[panel]
        by_l = points[panel]
        sizes = sorted(by_l)
        # Draw the paper-parameter collapse.
        for L in sizes:
            eps, mi = by_l[L]
            x = (eps - params["epsilon_c"]) * (L ** (1.0 / params["nu"]))
            y = (L ** params["beta"]) * mi
            ax.plot(x, y, "o-", markersize=4, label=f"L={L}")
        ax.set_title(f"{panel}  ($J_z={params['J_z']}$)", fontsize=10)
        ax.set_xlabel(r"$(\epsilon-\epsilon_c)\,L^{1/\nu}$")
        ax.set_ylabel(r"$L^{\beta}\,I_{\mathrm{end}}$")
        ax.legend(fontsize=8)

        paper_spread = relative_spread(by_l, params["epsilon_c"], params["beta"], params["nu"])
        fitted = optimize_exponents(by_l, params)
        report[panel] = {
            "sizes": sizes,
            "paper_params": {k: params[k] for k in ("epsilon_c", "beta", "nu")},
            "paper_collapse_relative_spread": round(paper_spread, 4),
            "fitted_params": {k: fitted[k] for k in ("epsilon_c", "beta", "nu")},
            "fitted_collapse_cost": round(fitted["cost"], 6),
            "exponent_abs_error": {
                "epsilon_c": round(abs(fitted["epsilon_c"] - params["epsilon_c"]), 4),
                "beta": round(abs(fitted["beta"] - params["beta"]), 4),
                "nu": round(abs(fitted["nu"] - params["nu"]), 4),
            },
        }
    # Keep the qualification on the comparison figure itself so the image
    # cannot be detached from its reproduction boundary in the note.
    fig.tight_layout(rect=(0, 0.14, 1, 1))
    fig.text(0.5, 0.025, DIFFERENCE_REASON, ha="center", va="bottom", fontsize=8.5)
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_PATH, dpi=150)
    plt.close(fig)

    # Honest gates. Panel generation is unconditional here (we drew all three);
    # these flags describe the *quality* that feeds numeric/reference scoring.
    all_spreads = [r["paper_collapse_relative_spread"] for r in report.values()]
    exponent_ok = all(
        r["exponent_abs_error"]["nu"] < 0.4 and r["exponent_abs_error"]["beta"] < 0.25
        for r in report.values()
    )
    # The stronger-coupling panels (3c, 3d) are the collapse quality anchor;
    # 3b (weakest coupling) is marginal at L<=12 and tracked as a residual.
    strong = [p for p in ("Fig. 3c", "Fig. 3d") if p in report]
    gate_flags = {
        "all_panels_generated": len(panels) == 3,
        "mi_ln2_anchor_holds": bool(anchor["max_abs_error_vs_ln2"] < 1e-2),
        "strong_couplings_collapse_tight": all(
            report[p]["paper_collapse_relative_spread"] < 0.15 for p in strong
        ),
        "collapse_tight_all_panels": all(s < 0.25 for s in all_spreads),
        "fitted_exponents_near_paper": bool(exponent_ok),
    }
    status = "physically_consistent" if all(gate_flags.values()) else "partial"

    checks = {
        "target": "T003",
        "figure": "Fig. 3",
        "status": status,
        "protocol": "finite-size collapse x=(eps-eps_c)L^(1/nu), y=L^beta I_end; "
                    "paper-parameter spread + own-data exponent re-fit",
        "sizes_available": sorted({L for p in points.values() for L in p}),
        "analytic_anchor": anchor,
        "panels": report,
        "gate_flags": gate_flags,
        "difference_reason": DIFFERENCE_REASON,
        "figure_path": "outputs/figures/fig3_scaling_collapse.png",
        "data": "outputs/data/fig3_large_ed_campaign.csv",
    }
    CHECK_PATH.write_text(json.dumps(checks, indent=2) + "\n")
    print(json.dumps({"status": status, "gate_flags": gate_flags,
                      "spreads": {p: report[p]["paper_collapse_relative_spread"] for p in report},
                      "fitted": {p: report[p]["fitted_params"] for p in report}}, indent=2))
    return 0 if status == "physically_consistent" else 1


if __name__ == "__main__":
    raise SystemExit(main())
