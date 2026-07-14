"""Fig. 3: position expectation <x>(t) during one adiabatic cycle for six
durations T, J=K=4.  Solid curves = exact dynamics; horizontal dashed lines =
theory Eq. (13) total (filled circle) and Berry-only term (triangle).

The abscissa "t" is the number of elapsed driving periods j (curve for duration
T ends at t=T).  The one-cycle displacement is T-independent, so all curves end
near the theory total; the Berry-only value sits well above -- the gap is the
interband-coherence (IBC) correction."""
import sys, json, time
from pathlib import Path
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

T_LIST = [1024, 2048, 3072, 4096, 5120, 6144]
N_SAMPLE = 40


def nk_for(T):
    # Nk ~ 2T resolves the packet (verified converged at T=6144, Nk=12288);
    # floor 4096 for small T, cap 12288.
    return int(min(12288, max(4096, 2 * T)))


def run_curve(m, T, Nk):
    # sample <x> at N_SAMPLE period indices along the cycle
    samples = sorted(set(np.linspace(0, T, N_SAMPLE, dtype=int).tolist()))
    _, _, snaps = evolve_fast(m, T=T, Nk=Nk, sample_periods=samples)
    js = sorted(snaps)
    xs = [x_expectation(m, snaps[j]) for j in js]
    return np.array(js), np.array(xs)


def main():
    m = CDHM(J=4, K=4, n_sub=100)
    # theory (scalars) for J=K=4
    th = delta_x_theory(m, Nk=401, Nbeta_F=120, Nbeta_E=400)
    print("theory:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in th.items()})

    curves = {}
    colors = plt.cm.viridis(np.linspace(0, 0.85, len(T_LIST)))
    fig, ax = plt.subplots(figsize=(7.2, 5))
    for T, col in zip(T_LIST, colors):
        Nk = nk_for(T)
        t0 = time.time()
        js, xs = run_curve(m, T, Nk)
        curves[T] = {"j": js.tolist(), "x": xs.tolist(), "Nk": Nk, "end": float(xs[-1])}
        ax.plot(js, xs, color=col, lw=1.3)
        ax.plot(js[-1], xs[-1], "o", mfc="white", mec=col, ms=7)
        print(f"  T={T} Nk={Nk}: <x>(end)={xs[-1]:.4f}  ({time.time()-t0:.0f}s)")

    jmax = max(T_LIST)
    ax.hlines(th["total"], 0, jmax, color="k", ls="--", lw=1)
    ax.plot(jmax, th["total"], "o", color="k", ms=6, label=f"theory Eq.(13) = {th['total']:.2f}")
    ax.hlines(th["berry"], 0, jmax, color="gray", ls="--", lw=1)
    ax.plot(jmax, th["berry"], "v", color="gray", ms=7, label=f"Berry-only = {th['berry']:.2f}")
    ax.set_xlabel(r"$t$ (driving periods)"); ax.set_ylabel(r"$\langle x\rangle$")
    ax.set_xlim(0, jmax + 100); ax.set_ylim(bottom=0)
    ax.set_title(r"Fig. 3: $\langle x\rangle$ over one cycle, CDHM $J=K=4$")
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout(); fig.savefig(FIG / "fig3_reproduction.png", dpi=150)

    for T, c in curves.items():
        np.savetxt(DATA / f"fig3_xt_T{T}.csv", np.column_stack([c["j"], c["x"]]),
                   delimiter=",", header="period_j,x_expectation", comments="")

    check = {
        "target": "T301_fig3", "params": {"J": 4, "K": 4, "n_sub": 100, "T_list": T_LIST},
        "theory": th,
        "actual_end_per_T": {str(T): curves[T]["end"] for T in T_LIST},
        "actual_end_mean": float(np.mean([curves[T]["end"] for T in T_LIST])),
        "actual_end_std": float(np.std([curves[T]["end"] for T in T_LIST])),
        "nk_per_T": {str(T): curves[T]["Nk"] for T in T_LIST},
    }
    (CHK / "fig3.json").write_text(json.dumps(check, indent=2))
    print(json.dumps({k: check[k] for k in ("actual_end_mean", "actual_end_std")}, indent=2))


if __name__ == "__main__":
    main()
