#!/usr/bin/env python3
"""Reproduce Fig. 2 of Wang & Hazzard (Nature 637, 314): exclusion statistics
(left, level degeneracy d_n) and free-particle thermodynamics (right, thermal
occupation <n>_beta).

Paper-exact parameters (from the published figure legend): fermion, boson,
Ex.2 (m=2), Ex.3 (m=2), Ex.4 (m=3).  All curves are closed-form; no fitting.
Emits CSV data, a JSON check of the d_n against the SI values, and the figure.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

CASE = Path(__file__).resolve().parents[2]
CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "src"))
from paraparticles import species_table  # noqa: E402

DATA = CASE / "outputs" / "data"
CHECKS = CASE / "outputs" / "checks"
FIGS = CASE / "outputs" / "figures"

# Reference d_n straight from SI Sec. "Calculation of exclusion statistics".
EXPECTED_D = {
    "fermion": [1, 1, 0, 0, 0],
    "boson": [1, 1, 1, 1, 1],
    "ex2": [1, 2, 1, 0, 0],   # (1+x)^2
    "ex3": [1, 2, 0, 0, 0],   # 1+2x
    "ex4": [1, 3, 1, 0, 0],   # 1+3x+x^2
}

COLORS = {
    "fermion": "#1f2ad0",
    "boson": "#e01111",
    "ex2": "#000000",
    "ex3": "#f39019",
    "ex4": "#7a4a1e",
}
STYLES = {"fermion": "-", "boson": "--", "ex2": "-.", "ex3": (0, (5, 3)), "ex4": (0, (6, 3))}


def main() -> int:
    for d in (DATA, CHECKS, FIGS):
        d.mkdir(parents=True, exist_ok=True)
    species = species_table(m3=2, m4=3)

    # ---- left panel data: level degeneracies d_n ----
    n_max = 4
    deg_rows = []
    deg_check = {}
    for sp in species:
        d = sp.degeneracies(n_max).astype(int).tolist()
        deg_rows.append([sp.key] + d)
        deg_check[sp.key] = {
            "d_n": d,
            "expected": EXPECTED_D[sp.key],
            "match": d == EXPECTED_D[sp.key],
        }
    with (DATA / "fig2_left_degeneracies.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["species"] + [f"d{n}" for n in range(n_max + 1)])
        w.writerows(deg_rows)

    # ---- right panel data: thermal occupation <n>_beta vs beta*eps ----
    be = np.linspace(-4.0, 4.0, 401)
    occ = {sp.key: sp.occupation(be) for sp in species}
    with (DATA / "fig2_right_occupation.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["beta_eps"] + [sp.key for sp in species])
        for j, x in enumerate(be):
            w.writerow([f"{x:.5f}"] + [f"{occ[sp.key][j]:.8f}" for sp in species])

    # ---- sanity checks on known limits ----
    idx0 = int(np.argmin(np.abs(be)))  # beta*eps = 0 -> x = 1
    # T -> infinity limit (beta*eps -> -inf): <n> -> n_max, the largest n with d_n>0.
    sat = {sp.key: float(sp.occupation(np.array([-30.0]))[0]) for sp in species}
    limit_checks = {
        "fermion_at_0_is_0.5": bool(abs(occ["fermion"][idx0] - 0.5) < 1e-9),
        "ex2_at_0_is_1.0": bool(abs(occ["ex2"][idx0] - 1.0) < 1e-9),        # 2x/(1+x)|_{x=1}=1
        "ex3_at_0_is_2/3": bool(abs(occ["ex3"][idx0] - 2.0 / 3.0) < 1e-9),  # 2x/(1+2x)|_{x=1}
        "ex4_at_0_is_1.0": bool(abs(occ["ex4"][idx0] - 1.0) < 1e-9),        # (3x+2x^2)/(1+3x+x^2)|_{x=1}=5/5
        "fermion_saturates_to_1": bool(abs(sat["fermion"] - 1.0) < 1e-6),   # d_1 highest
        "ex3_saturates_to_1": bool(abs(sat["ex3"] - 1.0) < 1e-6),           # d_2=0 -> max n=1
        "ex2_saturates_to_2": bool(abs(sat["ex2"] - 2.0) < 1e-6),           # d_2=1 -> max n=2
        "ex4_saturates_to_2": bool(abs(sat["ex4"] - 2.0) < 1e-6),           # d_2=1,d_3=0 -> max n=2
    }
    check = {
        "target": "fig2_exclusion_and_thermodynamics",
        "parameters": {"ex2_m": 2, "ex3_m": 2, "ex4_m": 3, "source": "Fig. 2 legend"},
        "degeneracies": deg_check,
        "degeneracies_all_match": all(v["match"] for v in deg_check.values()),
        "limit_checks": limit_checks,
        "limit_checks_all_pass": all(limit_checks.values()),
    }
    check["passed"] = check["degeneracies_all_match"] and check["limit_checks_all_pass"]
    check["status"] = "passed" if check["passed"] else "failed"
    (CHECKS / "fig2.json").write_text(json.dumps(check, indent=2) + "\n")

    # ---- figure ----
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (axl, axr) = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [1, 1.25]})

    # left: level degeneracy, dash width encodes d_n (as the paper draws it)
    order = ["fermion", "boson", "ex2", "ex3", "ex4"]
    colmap = {"fermion": "(f)", "boson": "(b)", "ex2": "(2)", "ex3": "(3)", "ex4": "(4)"}
    for col, key in enumerate(order):
        sp = next(s for s in species if s.key == key)
        d = sp.degeneracies(n_max)
        for n, dn in enumerate(d):
            if dn <= 0:
                continue
            half = 0.12 + 0.10 * (dn - 1)  # wider dash = larger degeneracy
            axl.hlines(n, col - half, col + half, color=COLORS[key], lw=5)
        axl.text(col, -0.75, colmap[key], ha="center", va="top", color=COLORS[key], fontsize=12)
    axl.set_ylim(-1.1, 4.8)
    axl.set_xlim(-0.6, 4.6)
    axl.set_ylabel(r"$n$", fontsize=13)
    axl.set_yticks(range(5))
    axl.set_xticks([])
    axl.set_title("level degeneracy $\\{d_n\\}$", fontsize=12)
    for s in ("top", "right", "bottom"):
        axl.spines[s].set_visible(False)

    # right: thermal occupation
    labels = {"fermion": "(f) fermion", "boson": "(b) boson", "ex2": "(2) Ex.2 (m=2)",
              "ex3": "(3) Ex.3 (m=2)", "ex4": "(4) Ex.4 (m=3)"}
    for key in order:
        axr.plot(be, occ[key], linestyle=STYLES[key], color=COLORS[key], lw=2.4, label=labels[key])
    axr.set_xlabel(r"$\beta\epsilon$", fontsize=13)
    axr.set_ylabel(r"$\langle \hat n\rangle_\beta$", fontsize=13)
    axr.set_xlim(-4, 4)
    axr.set_ylim(0, 2.2)
    axr.axvline(0, color="0.5", lw=0.8)
    axr.grid(alpha=0.2)
    axr.legend(fontsize=9, loc="upper right")
    axr.set_title("free-particle thermodynamics", fontsize=12)

    fig.suptitle("Fig. 2 reproduction — generalized exclusion statistics & paraparticle thermodynamics",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(FIGS / "fig2_reproduction.png", dpi=150)
    print(json.dumps(check, indent=2))
    return 0 if check["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
