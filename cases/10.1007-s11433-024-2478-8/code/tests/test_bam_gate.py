"""Sanity checks for the single-photon BAM/ORMD CZ reproduction.

Run:  PYTHONPATH=src python -m pytest tests/ -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import coefficients as C  # noqa: E402
import gate  # noqa: E402
import hamiltonians as ham  # noqa: E402
from waveforms import TWO_PI, fourier_waveform  # noqa: E402


def test_fourier_turn_on_and_peak():
    """Fig. 3(a) source trace: hybrid Omega_2 starts ~0 and peaks ~2*pi*16.4 MHz."""
    coeffs = (112.83, -46.32, -11.51, 2.35, 0.193, -1.14)
    v0 = fourier_waveform(coeffs, 0.0) / TWO_PI
    v_mid = fourier_waveform(coeffs, 0.125) / TWO_PI  # t = tau/2
    assert abs(v0) < 0.05            # smooth turn-on at t=0
    assert abs(v_mid - 16.4) < 0.2   # centre peak matches Fig. 3(a) blue/cyan curves


def test_rabi_analytic_limit():
    """Sector-00 with constant Omega, Delta=0 reduces to a textbook Rabi oscillation."""
    omega = TWO_PI * 10.0  # rad/us
    tau = 0.037
    n = 2000
    dt = tau / n
    psi = np.array([1.0 + 0j, 0.0])
    for _ in range(n):
        h = ham.h_sector00(omega, 0.0)
        # 2nd-order (midpoint) unitary step, H time-independent here
        from scipy.linalg import expm
        psi = expm(-1j * h * dt) @ psi
    p_excited = abs(psi[1]) ** 2
    assert abs(p_excited - np.sin(omega * tau / 2) ** 2) < 1e-6


def test_unitarity_and_dark_states():
    res = gate.run_protocol(C.FIG3_HYBRID, n_out=101)
    assert res["11"].norm_drift < 1e-9          # norm conserved (unitary evolution)
    assert res["11"].max_dark < 1e-10           # antisymmetric combos stay dark (Morris-Shore)


def test_product_and_bright_sector11_agree():
    """Cross-validate the reconstructed 9-state product H_d against the verbatim
    Morris-Shore 6-state form of eq. (a4): the |111> amplitude must be identical."""
    from scipy.integrate import solve_ivp

    proto = C.FIG3_HYBRID
    B = 2 * np.pi * proto.B_mhz
    tau = 0.25

    def amps(hfun, dim):
        def rhs(t, y):
            psi = y[:dim] + 1j * y[dim:]
            d = -1j * (hfun(t) @ psi)
            return np.concatenate([d.real, d.imag])
        y0 = np.zeros(2 * dim)
        y0[0] = 1.0
        t_eval = np.linspace(0, tau, 120)
        sol = solve_ivp(rhs, (0, tau), y0, t_eval=t_eval, method="DOP853",
                        rtol=1e-11, atol=1e-12, max_step=tau / 400)
        return (sol.y[0] + 1j * sol.y[dim])  # amplitude on state 0 = |111>

    def w(f, t):
        return float(np.asarray(f(t)))

    a_prod = amps(lambda t: ham.h_sector11(
        w(proto.omega1, t), w(proto.omega2, t), w(proto.delta1, t), w(proto.delta2, t), B, 0.0), 9)
    a_bright = amps(lambda t: ham.h_sector11_bright(
        w(proto.omega1, t), w(proto.omega2, t), w(proto.delta1, t), w(proto.delta2, t), B, 0.0), 6)
    assert np.max(np.abs(a_prod - a_bright)) < 1e-8


def test_fig3_hybrid_is_cz_below_1e4():
    res = gate.run_protocol(C.FIG3_HYBRID, n_out=201)
    s = gate.summarize(res)
    assert s["gate_error"] < 1e-4
    assert abs(abs(s["conditional_phase_over_pi"]) - 1.0) < 5e-3
    assert s["max_leakage"] < 5e-4


def test_fig3_amplitude_is_cz_below_1e4():
    res = gate.run_protocol(C.FIG3_AMPLITUDE, n_out=201)
    s = gate.summarize(res)
    assert s["gate_error"] < 1e-4
    assert abs(abs(s["conditional_phase_over_pi"]) - 1.0) < 5e-3


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([str(Path(__file__)), "-q"]))


def test_fig7_ratio_scan_structure():
    """Fig. 7: gate error is minimal at unit ratio and grows toward the
    anti-diagonal corners; the +/-1% window keeps error near 1e-4."""
    import dataclasses

    base = C.FIG3_HYBRID
    o1, o2 = base.omega1, base.omega2

    def err(rb, rq):
        proto = dataclasses.replace(
            base,
            omega1=lambda t, r=rb: r * np.asarray(o1(t)),
            omega2=lambda t, r=rq: r * np.asarray(o2(t)),
        )
        return gate.average_gate_error(gate.run_protocol(proto, n_out=2))["gate_error"]

    e_center = err(1.0, 1.0)
    e_tl = err(0.99, 1.01)   # anti-diagonal corner (buffer low, qubit high)
    e_br = err(1.01, 0.99)   # anti-diagonal corner (buffer high, qubit low)
    e_tr = err(1.01, 1.01)   # main-diagonal corner
    assert e_center < 1e-5                       # matches Fig. 3(a)
    assert e_tl > 5e-5 and e_br > 5e-5           # bright anti-diagonal corners
    assert e_tl > e_tr and e_br > e_tr           # anti-diagonal brighter than diagonal
    assert e_tl < 1.5e-4                         # within the paper's colorbar scale


def test_fig5_single_pulse_is_half_cz():
    """One pulse of the dual-pulse waveform returns all populations and imparts
    half the CZ conditional phase (pi/2); two pulses compose to a full CZ."""
    res = gate.run_protocol(C.FIG5_SINGLE_PULSE, n_out=101)
    for s in ("00", "01", "11"):
        assert res[s].population[-1] > 0.9999
    assert abs(abs(gate.conditional_phase(res)) - np.pi / 2) < 0.02


def test_twophoton_model_is_hermitian_and_reduces():
    """The two-photon sector Hamiltonians are Hermitian and, with the drive off,
    leave the register state stationary (only |e>,|r>,|q> carry energy)."""
    import hamiltonians_2p as h2
    params = dict(omega1p=0.0, omega1s=0.0, omega2p=0.0, omega2s=0.0,
                  delta1=1.0, delta2=2.0, delta_0=5.0, B=3.0, delta_q=0.0)
    for sec in ("00", "01", "11"):
        spec = h2.SECTORS[sec]
        H = h2.build_sector(spec["n"], spec["roles"], spec["adjacency"], params)
        assert np.allclose(H, H.conj().T)          # Hermitian
        assert abs(H[0, 0]) < 1e-12                # all-|1> state has zero energy
        assert np.allclose(H[0, 1:], 0.0)          # drive off -> |1...1> decoupled
