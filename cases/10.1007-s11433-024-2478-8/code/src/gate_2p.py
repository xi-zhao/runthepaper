"""Integrate the two-photon BAM sectors and evaluate the CZ gate metrics.

Reuses the CZ metric definitions from ``gate`` (conditional phase and Pedersen
average gate error) but drives the two-photon sector Hamiltonians of
``hamiltonians_2p``.  hbar = 1; time in us, frequencies in rad/us.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

import hamiltonians_2p as h2
from waveforms import TWO_PI, TAU_US


@dataclass
class SectorResult:
    population: np.ndarray
    phase: np.ndarray
    amp_final: complex


def _params(proto, t):
    def w(f):
        return float(np.asarray(f(t)))
    return {
        "omega1p": w(proto.omega1p), "omega1s": proto.omega1s,
        "omega2p": w(proto.omega2p), "omega2s": proto.omega2s,
        "delta1": w(proto.delta1), "delta2": w(proto.delta2),
        "delta_0": TWO_PI * proto.delta0_mhz,
        "B": TWO_PI * proto.B_mhz, "delta_q": TWO_PI * proto.delta_q_mhz,
    }


def _evolve_sector(proto, sector, n_out, tau):
    spec = h2.SECTORS[sector]
    n = spec["n"]
    dim = h2.D ** n
    i0 = h2.init_index(n)

    def rhs(t, y):
        H = h2.build_sector(n, spec["roles"], spec["adjacency"], _params(proto, t))
        psi = y[:dim] + 1j * y[dim:]
        d = -1j * (H @ psi)
        return np.concatenate([d.real, d.imag])

    y0 = np.zeros(2 * dim)
    y0[i0] = 1.0
    t_eval = np.linspace(0.0, tau, n_out)
    # Delta_0 ~ 2*pi*5 GHz drives fast intermediate-state oscillations -> tight steps.
    sol = solve_ivp(rhs, (0.0, tau), y0, t_eval=t_eval, method="DOP853",
                    rtol=1e-10, atol=1e-12, max_step=tau / 4000.0)
    amp = sol.y[i0] + 1j * sol.y[dim + i0]
    # population of the initial all-|1> state and its phase
    pop = np.abs(amp) ** 2
    phase = np.unwrap(np.angle(amp))
    return SectorResult(pop, phase, complex(amp[-1]))


def run_protocol(proto, n_out: int = 401, tau: float = TAU_US):
    return {
        "00": _evolve_sector(proto, "00", n_out, tau),
        "01": _evolve_sector(proto, "01", n_out, tau),
        "11": _evolve_sector(proto, "11", n_out, tau),
    }
