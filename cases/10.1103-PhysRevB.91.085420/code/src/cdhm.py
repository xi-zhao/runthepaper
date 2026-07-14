"""Continuously Driven Harper Model (CDHM) — core physics for reproducing
Wang, Zhou & Gong, PRB 91, 085420 (2015).

Model (Eq. 14, alpha = M/N = 1/3, tau = 2):

    H = sum_l (J/2)(a_l^dag a_{l+1} + H.c.)
        + K cos(2 pi t / tau) sum_l cos(2 pi alpha l + beta) a_l^dag a_l

Bloch reduction: lattice index l = N*n + j, j in {0,...,N-1}.  The onsite
potential depends only on the sublattice index j because
cos(2 pi (N n + j)/N + beta) = cos(2 pi j / N + beta).  The per-k Hamiltonian is
an N x N matrix (N = 3 here -> three Floquet bands).

Gauge / conventions (fixed by matching Fig. 1(a) and the reported Chern numbers):
  * atomic spacing = 1, superlattice constant a = N = 3, so k in [-pi/N, pi/N].
  * "cell" Bloch convention: the inter-cell hop (site N-1 of cell n -> site 0 of
    cell n+1) carries phase exp(i N k); intra-cell hops carry no phase.

The adiabatic pumping protocol is piecewise constant in beta: during driving
period j (j = 1..T) beta is fixed at beta_j, so one full cycle is the ordered
product of T one-period Floquet operators.  This is what makes the "actual"
wave-packet dynamics cheap.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class CDHM:
    J: float = 3.0
    K: float = 3.0
    N: int = 3            # sublattice sites per cell (alpha = 1/N)
    tau: float = 2.0      # driving period
    n_sub: int = 60       # substeps per period for the time-ordered propagator

    @property
    def a(self) -> float:
        """Superlattice constant (atomic spacing = 1)."""
        return float(self.N)

    # ---- Bloch Hamiltonian -------------------------------------------------
    def h_hop(self, k):
        """Static hopping part h_hop(k), shape (..., N, N). Vectorised over k."""
        k = np.asarray(k, dtype=float)
        N = self.N
        H = np.zeros(k.shape + (N, N), dtype=complex)
        t = self.J / 2.0
        for j in range(N - 1):
            H[..., j, j + 1] = t
            H[..., j + 1, j] = t
        # inter-cell hop: site N-1 (cell n) <-> site 0 (cell n+1), phase exp(i N k)
        phase = np.exp(1j * N * k)
        H[..., N - 1, 0] = t * phase
        H[..., 0, N - 1] = t * np.conj(phase)
        return H

    def v_diag(self, beta: float):
        """Onsite potential coefficient diag(cos(2 pi j/N + beta)) (without K, c(t))."""
        j = np.arange(self.N)
        return np.cos(2 * np.pi * j / self.N + beta)  # shape (N,)

    def hamiltonian(self, k, t: float, beta: float):
        """Full instantaneous Bloch Hamiltonian H(k, t; beta), shape (..., N, N)."""
        H = self.h_hop(k).copy()
        c = self.K * np.cos(2 * np.pi * t / self.tau)
        diag = c * self.v_diag(beta)
        idx = np.arange(self.N)
        H[..., idx, idx] += diag
        return H

    # ---- one-period Floquet operator --------------------------------------
    def floquet_operator(self, k, beta: float, n_sub: int | None = None):
        """U(k, beta) = T exp[-i \\int_0^tau H(k,t;beta) dt], shape (..., N, N).

        Time-ordered product of midpoint short-time propagators exp(-i H(t_mid) dt).
        Vectorised over k via batched Hermitian eigendecomposition.
        """
        n_sub = self.n_sub if n_sub is None else n_sub
        k = np.asarray(k, dtype=float)
        N = self.N
        dt = self.tau / n_sub
        U = np.broadcast_to(np.eye(N, dtype=complex), k.shape + (N, N)).copy()
        for s in range(n_sub):
            t_mid = (s + 0.5) * dt
            H = self.hamiltonian(k, t_mid, beta)
            step = _expm_herm(H, dt)
            U = step @ U
        return U


def _expm_herm(H, dt: float):
    """exp(-i H dt) for a batch of Hermitian matrices H (..., N, N)."""
    w, V = np.linalg.eigh(H)
    phase = np.exp(-1j * w * dt)              # (..., N)
    return (V * phase[..., None, :]) @ np.conjugate(np.swapaxes(V, -1, -2))


# ---- Floquet spectrum ------------------------------------------------------
def floquet_bands(model: CDHM, k, beta: float):
    """Return (omega, states) for the Floquet operator U(k, beta).

    omega: eigenphases in (-pi, pi], sorted ascending, shape (..., N).
    states: column eigenvectors, shape (..., N, N); states[..., :, n] is band n.
    U|psi_n> = exp(-i omega_n) |psi_n>.
    """
    U = model.floquet_operator(k, beta)
    evals, evecs = np.linalg.eig(U)
    omega = -np.angle(evals)                  # exp(-i omega) = eval
    order = np.argsort(omega, axis=-1)
    omega = np.take_along_axis(omega, order, axis=-1)
    evecs = np.take_along_axis(evecs, order[..., None, :], axis=-1)
    return omega, evecs


def initial_populations(model: CDHM, k, beta: float = 0.0):
    """rho_{n,k}(0) = |<psi_{n,k}(beta)| e_0>|^2 and C_{n,k}(0) = <psi_{n,k}|e_0>.

    Initial state = single site l=0 -> per-k sublattice vector e_0 = (1,0,...,0).
    Returns (rho, C, omega, states). C[..., n] = conj(states[..., 0, n]).
    """
    omega, states = floquet_bands(model, k, beta)
    C = np.conjugate(states[..., 0, :])       # <psi_n | e_0> = conj(psi_n[0])
    rho = np.abs(C) ** 2
    return rho, C, omega, states
