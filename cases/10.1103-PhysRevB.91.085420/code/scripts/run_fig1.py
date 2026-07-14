"""Fig. 1: (a) Floquet eigenphases omega_{n,k}(beta)/pi over the (k,beta) torus,
(b) initial band populations rho_{n,k}(0) for the site-0 initial state.  J=K=3."""
import sys, json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "src"))
from cdhm import CDHM, floquet_bands, initial_populations  # noqa: E402

CASE = CODE.parent
DATA = CASE / "outputs" / "data"; FIG = CASE / "outputs" / "figures"; CHK = CASE / "outputs" / "checks"
for d in (DATA, FIG, CHK):
    d.mkdir(parents=True, exist_ok=True)


def main():
    m = CDHM(J=3, K=3, n_sub=120)
    Nk, Nb = 61, 61
    kk = np.linspace(-np.pi / 3, np.pi / 3, Nk)
    bb = np.linspace(0, 2 * np.pi, Nb)
    omega = np.zeros((Nk, Nb, 3))
    for ib, b in enumerate(bb):
        om, _ = floquet_bands(m, kk, float(b))
        omega[:, ib] = om

    # Fig 1(b): rho_{n,k}(0)
    kfine = np.linspace(-np.pi / 3, np.pi / 3, 241)
    rho, C, om0, st = initial_populations(m, kfine, 0.0)

    # --- data ---
    np.savez(DATA / "fig1_spectrum.npz", k=kk, beta=bb, omega=omega)
    hdr = "k_over_pi," + ",".join(f"rho_band{n}" for n in range(3))
    np.savetxt(DATA / "fig1b_populations.csv",
               np.column_stack([kfine / np.pi, rho]), delimiter=",", header=hdr, comments="")

    # --- figure ---
    fig = plt.figure(figsize=(11, 4.2))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    KK, BB = np.meshgrid(kk / np.pi, bb / np.pi, indexing="ij")
    colors = ["#1f4fd8", "#d9c400", "#c81e1e"]
    for n in range(3):
        ax.plot_surface(KK, BB, omega[:, :, n] / np.pi, color=colors[n],
                        alpha=0.85, linewidth=0, antialiased=True, rstride=2, cstride=2)
    ax.set_xlabel(r"$k/\pi$"); ax.set_ylabel(r"$\beta/\pi$"); ax.set_zlabel(r"$\omega/\pi$")
    ax.set_title("(a) Floquet eigenphases, $J=K=3$")
    ax.view_init(elev=22, azim=-60)

    ax2 = fig.add_subplot(1, 2, 2)
    colors_b = ["#c81e1e", "#2ca02c", "#1f4fd8"]  # paper Fig 1(b) mapping: band0=red,1=green,2=blue
    for n in range(3):
        ax2.plot(kfine / np.pi, rho[:, n], color=colors_b[n], lw=2, label=f"band {n}")
    ax2.set_xlabel(r"$k/\pi$"); ax2.set_ylabel(r"$\rho_{n,k}(0)$")
    ax2.set_xlim(-1 / 3, 1 / 3); ax2.set_ylim(0, 1)
    ax2.set_title("(b) initial band populations")
    ax2.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / "fig1_reproduction.png", dpi=150)

    check = {
        "target": "T101_fig1",
        "params": {"J": 3, "K": 3, "alpha": "1/3", "tau": 2, "Nk": Nk, "Nbeta": Nb},
        "omega_over_pi_range": [float(omega.min() / np.pi), float(omega.max() / np.pi)],
        "band_omega_ranges_over_pi": [[float(omega[..., n].min() / np.pi),
                                       float(omega[..., n].max() / np.pi)] for n in range(3)],
        "rho_sum_min": float(rho.sum(axis=1).min()),
        "rho_sum_max": float(rho.sum(axis=1).max()),
        "rho_at_k0": rho[len(kfine) // 2].tolist(),
    }
    (CHK / "fig1.json").write_text(json.dumps(check, indent=2))
    print(json.dumps(check, indent=2))


if __name__ == "__main__":
    main()
