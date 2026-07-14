"""Consistency checks for the CDHM reproduction.

These are the limiting-case, conservation, and cross-validation checks that gate
the physics before any figure is trusted:

  * Floquet operator unitarity;
  * undriven (K=0) analytic band limit;
  * initial band populations sum to one;
  * k-reflection symmetry of populations and eigenphases (Eq. 10 assumption);
  * Fukui-Hatsugai-Suzuki Chern numbers are integers summing to zero, |C|=(4,8,4)
    near J=K=4;
  * the fast Strang-split evolver matches the exact eigendecomposition propagator;
  * the initial <x> vanishes;
  * Eq. (13) total tracks the exact one-cycle displacement (central claim);
  * Eq. (8) reproduces the actual population-change structure (feature level).

Run:  python scripts/qa_cdhm.py
Writes: ../outputs/checks/qa_cdhm.json
"""
import sys, json
from pathlib import Path
import numpy as np

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE / "src"))
from cdhm import CDHM, floquet_bands, initial_populations  # noqa: E402
from observables import evolve, evolve_fast, x_expectation, band_populations  # noqa: E402
from theory import initial_amplitudes, delta_x_theory, delta_rho_theory, berry_flux_strips  # noqa: E402

CASE = CODE.parent
CHK = CASE / "outputs" / "checks"
CHK.mkdir(parents=True, exist_ok=True)


def check_floquet_unitary():
    m = CDHM(J=3, K=3)
    k = np.linspace(-np.pi / 3, np.pi / 3, 11, endpoint=False)
    U = m.floquet_operator(k, beta=0.7)
    ident = np.conjugate(np.swapaxes(U, -1, -2)) @ U
    err = float(np.max(np.abs(ident - np.eye(3))))
    return err < 1e-10, {"max_unitarity_error": err}


def check_undriven_analytic_band():
    """K=0: U = exp(-i h_hop(k) tau), so Floquet eigenphases = eps(k)*tau mod 2pi."""
    m = CDHM(J=3, K=0, n_sub=120)
    k = np.array([0.2, -0.5, 0.9])
    omega, _ = floquet_bands(m, k, beta=0.0)
    eps = np.linalg.eigvalsh(m.h_hop(k))
    expected = -np.angle(np.exp(-1j * eps * m.tau))
    got = np.sort(np.mod(omega + np.pi, 2 * np.pi) - np.pi, axis=-1)
    exp_s = np.sort(expected, axis=-1)
    err = float(np.max(np.abs(got - exp_s)))
    return err < 1e-4, {"max_band_error": err}


def check_populations_sum_to_one():
    m = CDHM(J=3, K=3)
    k = np.linspace(-np.pi / 3, np.pi / 3, 25, endpoint=False)
    rho, *_ = initial_populations(m, k, beta=0.0)
    err = float(np.max(np.abs(rho.sum(axis=-1) - 1.0)))
    return err < 1e-10, {"max_sum_deviation": err}


def check_k_reflection_symmetry():
    m = CDHM(J=4, K=4)
    k = np.linspace(0.02, np.pi / 3 - 0.02, 20)
    rp, _, op, _ = initial_populations(m, k, 0.0)
    rm, _, om, _ = initial_populations(m, -k, 0.0)
    e_rho = float(np.max(np.abs(np.sort(rp, -1) - np.sort(rm, -1))))
    e_om = float(np.max(np.abs(np.sort(op, -1) - np.sort(om, -1))))
    return (e_rho < 1e-6 and e_om < 1e-6), {"rho_asym": e_rho, "omega_asym": e_om}


def check_chern_sum_and_magnitude():
    m = CDHM(J=4, K=4, n_sub=80)
    k = np.linspace(-np.pi / 3, np.pi / 3, 61, endpoint=False)
    F = berry_flux_strips(m, k, Nbeta=61)
    chern = F.sum(axis=0) / (2 * np.pi)
    ints = sorted(np.abs(np.round(chern)).astype(int).tolist())
    ok = (np.allclose(chern, np.round(chern), atol=1e-6) and abs(chern.sum()) < 1e-6
          and ints == [4, 4, 8])
    return ok, {"chern": chern.tolist(), "abs_int_sorted": ints, "chern_sum": float(chern.sum())}


def check_fast_matches_exact():
    m = CDHM(J=4, K=4, n_sub=160)
    _, pe, _ = evolve(m, T=48, Nk=192)
    _, pf, _ = evolve_fast(m, T=48, Nk=192)
    err = float(np.max(np.abs(pe - pf)))
    return err < 2e-2, {"max_abs_diff": err}


def check_initial_x_zero():
    m = CDHM(J=4, K=4)
    _, phi, _ = evolve_fast(m, T=0, Nk=256)
    val = float(abs(x_expectation(m, phi)))
    return val < 1e-9, {"initial_x": val}


def check_theory_matches_dynamics_dx():
    """Central claim: Eq. (13) total ~ exact one-cycle displacement (J=K=4)."""
    m = CDHM(J=4, K=4, n_sub=120)
    th = delta_x_theory(m, Nk=301, Nbeta_F=100, Nbeta_E=300)
    _, phi, _ = evolve_fast(m, T=1024, Nk=4096)
    dx_actual = x_expectation(m, phi)
    ok = abs(th["total"] - dx_actual) < 0.15 and (th["berry"] - th["total"]) > 0.8
    return ok, {"theory_total": th["total"], "berry_only": th["berry"],
                "actual": float(dx_actual)}


def check_delta_rho_tracks_actual():
    """Eq. (8) reproduces the actual population change structure (feature level)."""
    m = CDHM(J=3, K=3, n_sub=200)
    Nk = 121
    k = np.linspace(-np.pi / 3, np.pi / 3, Nk, endpoint=False)
    _, rho0, *_ = initial_amplitudes(m, k)
    _, phi, _ = evolve_fast(m, T=256, Nk=Nk)
    drho_a = band_populations(m, k, phi, 0.0) - rho0
    drho_t, _ = delta_rho_theory(m, k, T=256)
    corr = [float(np.corrcoef(drho_a[:, b], drho_t[:, b])[0, 1]) for b in range(3)]
    return all(c > 0.75 for c in corr), {"correlation_per_band": corr}


CHECKS = [
    ("floquet_unitary", check_floquet_unitary),
    ("undriven_analytic_band", check_undriven_analytic_band),
    ("populations_sum_to_one", check_populations_sum_to_one),
    ("k_reflection_symmetry", check_k_reflection_symmetry),
    ("chern_sum_and_magnitude", check_chern_sum_and_magnitude),
    ("fast_matches_exact_evolution", check_fast_matches_exact),
    ("initial_x_is_zero", check_initial_x_zero),
    ("theory_matches_dynamics_dx", check_theory_matches_dynamics_dx),
    ("delta_rho_theory_tracks_actual", check_delta_rho_tracks_actual),
]


def main():
    results = {}
    all_ok = True
    for name, fn in CHECKS:
        ok, detail = fn()
        all_ok = all_ok and ok
        results[name] = {"passed": bool(ok), **detail}
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    report = {"status": "passed" if all_ok else "failed",
              "checks_total": len(CHECKS),
              "checks_passed": sum(1 for r in results.values() if r["passed"]),
              "checks": results}
    (CHK / "qa_cdhm.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({"status": report["status"],
                      "checks_passed": report["checks_passed"],
                      "checks_total": report["checks_total"]}, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
