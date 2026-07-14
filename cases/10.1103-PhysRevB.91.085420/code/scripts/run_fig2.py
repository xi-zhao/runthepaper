"""Fig. 2: population change Delta rho_{n,k} after one pumping cycle (bottom
Floquet band emphasised), J=K=3, T=1024.  (a) actual dynamics, (b) theory Eq. (8)."""
import sys, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "src"))
from cdhm import CDHM  # noqa: E402
from observables import evolve_fast, band_populations  # noqa: E402
from theory import initial_amplitudes, delta_rho_theory  # noqa: E402

CASE = CODE.parent
DATA = CASE / "outputs" / "data"; FIG = CASE / "outputs" / "figures"; CHK = CASE / "outputs" / "checks"
for d in (DATA, FIG, CHK):
    d.mkdir(parents=True, exist_ok=True)

BAND = 0  # bottom Floquet band (paper Fig. 2 emphasis)


def main():
    m = CDHM(J=3, K=3, n_sub=160)
    T = 1024
    Nk = 401
    k = np.linspace(-np.pi / 3, np.pi / 3, Nk, endpoint=False)

    # actual: per-k population change over one cycle
    _, phi, _ = evolve_fast(m, T=T, Nk=Nk)
    _, rho0, *_ = initial_amplitudes(m, k)
    rho1 = band_populations(m, k, phi, beta=0.0)
    drho_actual = rho1 - rho0

    # theory Eq. (8)
    drho_theory, _ = delta_rho_theory(m, k, T=T)

    hdr = "k_over_pi," + ",".join(f"drho_actual_b{b},drho_theory_b{b}" for b in range(3))
    cols = [k / np.pi]
    for b in range(3):
        cols += [drho_actual[:, b], drho_theory[:, b]]
    np.savetxt(DATA / "fig2_delta_rho.csv", np.column_stack(cols),
               delimiter=",", header=hdr, comments="")

    # 2x3 grid: rows = actual (a) / theory (b), columns = the three Floquet bands
    band_colors = ["#c81e1e", "#2ca02c", "#1f4fd8"]
    fig, axes = plt.subplots(2, 3, figsize=(12, 6), sharex=True, sharey=True)
    for b in range(3):
        axes[0, b].plot(k / np.pi, drho_actual[:, b] * 1e3, color=band_colors[b], lw=0.8)
        axes[1, b].plot(k / np.pi, drho_theory[:, b] * 1e3, color=band_colors[b], lw=0.8)
        axes[0, b].set_title(f"band {b}")
    for ax in axes.flat:
        ax.axhline(0, color="gray", lw=0.4); ax.set_xlim(-1 / 3, 1 / 3)
    for b in range(3):
        axes[1, b].set_xlabel(r"$k/\pi$")
    axes[0, 0].set_ylabel(r"(a) actual  $\Delta\rho_{n,k}\,(\times10^{-3})$")
    axes[1, 0].set_ylabel(r"(b) theory Eq.(8)  $(\times10^{-3})$")
    fig.suptitle(r"Fig. 2: population change after one cycle, CDHM $J=K=3$, $T=1024$")
    fig.tight_layout()
    fig.savefig(FIG / "fig2_reproduction.png", dpi=150, bbox_inches="tight")

    # overlay of the bottom band for auditing
    a = drho_actual[:, BAND]; t = drho_theory[:, BAND]
    fig2, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(k / np.pi, a * 1e3, color="#1f4fd8", lw=1.2, label="actual (dynamics)")
    ax.plot(k / np.pi, t * 1e3, color="#c81e1e", lw=1.0, ls="--", label="theory Eq. (8)")
    ax.set_xlabel(r"$k/\pi$"); ax.set_ylabel(r"$\Delta\rho_{0,k}\ (\times 10^{-3})$")
    ax.set_xlim(-1 / 3, 1 / 3); ax.legend(frameon=False)
    ax.set_title("Fig. 2 overlay: bottom band, $J=K=3$, $T=1024$")
    fig2.tight_layout(); fig2.savefig(FIG / "fig2_overlay.png", dpi=150)

    corr = [float(np.corrcoef(drho_actual[:, b], drho_theory[:, b])[0, 1]) for b in range(3)]
    check = {
        "target": "T201_fig2", "params": {"J": 3, "K": 3, "T": T, "Nk": Nk},
        "band_reported": BAND,
        "actual_range": [float(a.min()), float(a.max())],
        "theory_range": [float(t.min()), float(t.max())],
        "correlation_per_band": corr,
        "bottom_band_corr": corr[BAND],
        "sum_over_bands_drho_max_abs": float(np.max(np.abs(drho_actual.sum(axis=1)))),
    }
    (CHK / "fig2.json").write_text(json.dumps(check, indent=2))
    print(json.dumps(check, indent=2))


if __name__ == "__main__":
    main()
