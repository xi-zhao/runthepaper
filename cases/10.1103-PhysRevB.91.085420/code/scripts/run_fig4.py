"""Fig. 4: one-cycle displacement Delta<x> vs J (=K) across the Floquet-Chern
topological transition (paper: (4,-8,4)->(-8,16,-8) near J=K~5.14).

For each J: actual displacement from exact dynamics (T=2560), theory Eq. (13)
total, and the Berry-curvature-only term.  The actual and full theory track each
other and jump at the transition; the Berry-only term does not follow the actual
displacement -- so a trivial site-0 initial state detects the transition.
Parallelised over J.
"""
import sys, json, time
from pathlib import Path
from multiprocessing import Pool
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "src"))
from cdhm import CDHM  # noqa: E402
from observables import evolve_fast, x_expectation  # noqa: E402
from theory import delta_x_theory  # noqa: E402

CASE = CODE.parent
DATA = CASE / "outputs" / "data"; FIG = CASE / "outputs" / "figures"; CHK = CASE / "outputs" / "checks"
for d in (DATA, FIG, CHK):
    d.mkdir(parents=True, exist_ok=True)

J_MIN, J_MAX, N_J = 5.0, 5.3, 61
T_ACTUAL = 2560
N_SUB = 100


def worker(J):
    m = CDHM(J=J, K=J, n_sub=N_SUB)
    th = delta_x_theory(m, Nk=301, Nbeta_F=90, Nbeta_E=240)
    Nk = int(min(8192, max(4096, 2 * T_ACTUAL)))
    _, phi, _ = evolve_fast(m, T=T_ACTUAL, Nk=Nk)
    dx = x_expectation(m, phi)
    return {"J": float(J), "actual": float(dx), "berry": th["berry"],
            "ibc": th["ibc"], "total": th["total"], "chern": th["chern"]}


def main():
    Js = np.linspace(J_MIN, J_MAX, N_J)
    t0 = time.time()
    with Pool(processes=8) as pool:
        results = pool.map(worker, Js.tolist())
    print(f"scan done in {time.time()-t0:.0f}s")

    J = np.array([r["J"] for r in results])
    actual = np.array([r["actual"] for r in results])
    berry = np.array([r["berry"] for r in results])
    total = np.array([r["total"] for r in results])

    np.savetxt(DATA / "fig4_scan.csv",
               np.column_stack([J, actual, berry, np.array([r["ibc"] for r in results]), total]),
               delimiter=",", header="J,actual_dx,berry_only,ibc,theory_total", comments="")

    fig, ax = plt.subplots(figsize=(7.4, 5))
    ax.plot(J, actual, "o", mfc="white", mec="#1f4fd8", ms=6, label="actual dynamics ($T=2560$)")
    ax.plot(J, total, "o", color="k", ms=4, label="theory Eq. (13)")
    ax.plot(J, berry, "v", color="gray", ms=5, label="Berry-only term")
    ax.axvline(5.14, color="red", ls=":", lw=1, alpha=0.7)
    ax.text(5.145, ax.get_ylim()[1] * 0.05, "Chern jump\n$\\sim$5.14", color="red", fontsize=8)
    ax.set_xlabel(r"$J\ (=K)$"); ax.set_ylabel(r"$\Delta\langle x\rangle$")
    ax.set_title("Fig. 4: topological-transition probe, CDHM")
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout(); fig.savefig(FIG / "fig4_reproduction.png", dpi=150)

    # locate transition from theory sign/jump
    dtot = np.abs(np.diff(total))
    j_jump = float(J[np.argmax(dtot)])
    check = {
        "target": "T401_fig4",
        "params": {"J_range": [J_MIN, J_MAX], "N_J": N_J, "T": T_ACTUAL, "n_sub": N_SUB},
        "transition_J_theory_jump": j_jump,
        "chern_below": results[0]["chern"], "chern_above": results[-1]["chern"],
        "actual_range": [float(actual.min()), float(actual.max())],
        "berry_range": [float(berry.min()), float(berry.max())],
        "theory_total_range": [float(total.min()), float(total.max())],
        "mean_abs_actual_minus_total": float(np.mean(np.abs(actual - total))),
        "mean_abs_actual_minus_berry": float(np.mean(np.abs(actual - berry))),
    }
    (CHK / "fig4.json").write_text(json.dumps(check, indent=2))
    print(json.dumps(check, indent=2))


if __name__ == "__main__":
    main()
