"""Time evolution and CZ gate metrics for the single-photon BAM/ORMD protocol.

Given a fully specified protocol (waveforms + B + delta_q), integrate the
Schroedinger equation i dpsi/dt = H(t) psi (hbar = 1) for each of the three
register sectors over t in [0, tau], then evaluate:

  * per-sector return population P_k(t) = |<init|psi(t)>|^2  (Fig. 3b/e),
  * per-sector accumulated phase phi_k(t) = arg(<init|psi(t)>)  (Fig. 3c/f),
  * the conditional (entangling) phase  Phi = phi_11 + phi_00 - 2 phi_01,
  * the leakage 1 - P_k(tau),
  * the average gate error 1 - F_avg against the ideal CZ, optimised over
    single-qubit Z rotations and global phase (Pedersen et al., PRA 2007 -
    the paper's "typical way" of evaluating CZ fidelity, refs [48,49]).

The scipy ODE integrator (Dormand-Prince RK45, tight tolerances) provides an
independent numerical solution of the same physics.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

import hamiltonians as ham
from waveforms import TAU_US, TWO_PI


@dataclass
class SectorResult:
    name: str
    t: np.ndarray            # time grid (us)
    population: np.ndarray   # P(t) = |<init|psi(t)>|^2
    phase: np.ndarray        # unwrapped arg(<init|psi(t)>)
    amp_final: complex       # <init|psi(tau)>
    max_dark: float          # max population in dark subspace (|11> sector only)
    norm_drift: float        # max |<psi|psi> - 1| over the trajectory


def _evolve(h_of_t, dim, init_index, tau, n_out):
    """Integrate one sector; return (t grid, state trajectory [n_out, dim])."""
    psi0 = np.zeros(dim, dtype=complex)
    psi0[init_index] = 1.0

    def rhs(t, y):
        psi = y[:dim] + 1j * y[dim:]
        dpsi = -1j * (h_of_t(t) @ psi)
        return np.concatenate([dpsi.real, dpsi.imag])

    t_eval = np.linspace(0.0, tau, n_out)
    y0 = np.concatenate([psi0.real, psi0.imag])
    sol = solve_ivp(
        rhs, (0.0, tau), y0, t_eval=t_eval,
        method="DOP853", rtol=1e-11, atol=1e-12, max_step=tau / 400.0,
    )
    if not sol.success:
        raise RuntimeError(f"integration failed: {sol.message}")
    states = sol.y[:dim].T + 1j * sol.y[dim:].T
    return sol.t, states


def _sector_metrics(name, t, states, init_index, dark_pairs=None):
    amps = states[:, init_index]
    population = np.abs(amps) ** 2
    phase = np.unwrap(np.angle(amps))
    norm = np.sum(np.abs(states) ** 2, axis=1)
    max_dark = 0.0
    if dark_pairs:
        for i, j in dark_pairs:
            dark = (states[:, i] - states[:, j]) / np.sqrt(2.0)
            max_dark = max(max_dark, float(np.max(np.abs(dark) ** 2)))
    return SectorResult(
        name=name, t=t, population=population, phase=phase,
        amp_final=complex(amps[-1]), max_dark=max_dark,
        norm_drift=float(np.max(np.abs(norm - 1.0))),
    )


def run_protocol(proto, n_out: int = 401, tau: float = TAU_US):
    """Evolve all three sectors of a SinglePhotonProtocol."""
    B = TWO_PI * proto.B_mhz
    dq = TWO_PI * proto.delta_q_mhz

    def w(f, t):
        return float(np.asarray(f(t)))

    def h00(t):
        return ham.h_sector00(w(proto.omega1, t), w(proto.delta1, t))

    def h01(t):
        return ham.h_sector01(
            w(proto.omega1, t), w(proto.omega2, t),
            w(proto.delta1, t), w(proto.delta2, t), B, dq,
        )

    def h11(t):
        return ham.h_sector11(
            w(proto.omega1, t), w(proto.omega2, t),
            w(proto.delta1, t), w(proto.delta2, t), B, dq,
        )

    t0, s0 = _evolve(h00, 2, ham.SECTOR00_INIT, tau, n_out)
    t1, s1 = _evolve(h01, 5, ham.SECTOR01_INIT, tau, n_out)
    t2, s2 = _evolve(h11, 9, ham.SECTOR11_INIT, tau, n_out)

    r00 = _sector_metrics("00", t0, s0, ham.SECTOR00_INIT)
    r01 = _sector_metrics("01", t1, s1, ham.SECTOR01_INIT)
    r11 = _sector_metrics("11", t2, s2, ham.SECTOR11_INIT, ham.SECTOR11_DARK_PAIRS)
    return {"00": r00, "01": r01, "11": r11}


def conditional_phase(results) -> float:
    """Entangling phase Phi = phi_11 + phi_00 - 2 phi_01, wrapped to (-pi, pi]."""
    a00 = results["00"].amp_final
    a01 = results["01"].amp_final
    a11 = results["11"].amp_final
    phi = np.angle(a11) + np.angle(a00) - 2.0 * np.angle(a01)
    return float((phi + np.pi) % (2 * np.pi) - np.pi)


def average_gate_error(results) -> dict:
    """Pedersen average gate error 1 - F_avg vs. ideal CZ, optimised over local Z.

    Realised computational gate is diagonal U = diag(a00, a01, a10, a11) with
    a10 = a01 by symmetry; leakage makes it sub-unitary.  The target family is
    e^{i theta} (Z_c(alpha) x Z_t(beta)) CZ.  For a diagonal U the optimum over
    (theta, alpha, beta) maximises |a00 + e^{-i beta} a01 + e^{-i alpha} a10
    - e^{-i(alpha+beta)} a11|; we optimise (alpha, beta) numerically.
    """
    a00 = results["00"].amp_final
    a01 = results["01"].amp_final
    a10 = a01
    a11 = results["11"].amp_final
    amps = np.array([a00, a01, a10, a11])
    d = 4

    def neg_overlap(x):
        alpha, beta = x
        target = np.array([1.0, np.exp(1j * beta), np.exp(1j * alpha),
                           -np.exp(1j * (alpha + beta))])
        return -abs(np.vdot(target, amps))

    # coarse grid then local polish
    best = None
    grid = np.linspace(-np.pi, np.pi, 73)
    for al in grid:
        for be in grid:
            v = neg_overlap((al, be))
            if best is None or v < best[0]:
                best = (v, al, be)
    from scipy.optimize import minimize
    res = minimize(neg_overlap, [best[1], best[2]], method="Nelder-Mead",
                   options={"xatol": 1e-10, "fatol": 1e-14})
    tr_overlap = -res.fun  # |tr(U_target^dagger U)|
    tr_uu = float(np.sum(np.abs(amps) ** 2))  # tr(U^dagger U)
    f_avg = (tr_overlap ** 2 + tr_uu) / (d * (d + 1))
    return {
        "f_avg": float(f_avg),
        "gate_error": float(1.0 - f_avg),
        "tr_overlap": float(tr_overlap),
        "tr_uu": tr_uu,
    }


def summarize(results) -> dict:
    phi = conditional_phase(results)
    err = average_gate_error(results)
    leak = {k: float(1.0 - results[k].population[-1]) for k in ("00", "01", "11")}
    return {
        "conditional_phase_rad": phi,
        "conditional_phase_over_pi": phi / np.pi,
        "leakage": leak,
        "max_leakage": max(leak.values()),
        "max_dark_population_11": results["11"].max_dark,
        "max_norm_drift": max(results[k].norm_drift for k in results),
        **err,
    }
