"""Observables for the CDHM reproduction: exact wave-packet dynamics, band
populations after a cycle, and the analytic theory of Eq. (8)/(13).

Actual dynamics
---------------
The initial state is a single site l = 0.  Because k is conserved, each k-channel
is a 3-vector phi(k) evolving as phi <- U(k, beta_j) phi, with the initial
phi(k) = e_0 = (1,0,0) for every k.  Since the adiabatic protocol holds beta
fixed for a whole driving period, one cycle is the ordered product of T
one-period Floquet operators.

Position expectation.  The real-space cell amplitude is the inverse Bloch
transform of phi over the BZ; |psi(cell n, sublattice j)|^2 = |IFFT_k phi_j|^2.
With x = N*n + j (atomic spacing 1) and cell index folded to a signed range, the
exact position expectation is <x> = sum (N n + j)|psi|^2 / sum |psi|^2.  This is
the true <x> = sum_l l |<l|Psi>|^2, not the paper's leading-order approximation.
"""
from __future__ import annotations

import numpy as np
from cdhm import CDHM, floquet_bands


def beta_schedule(T: int, offset: float = 0.5) -> np.ndarray:
    """beta values held during each of the T driving periods.

    beta(s)=2 pi s, s_j=j/T.  offset selects where in [j-1, j] we sample beta:
    0.5 = midpoint of the j-th period (default).  The O(1/T) choice is immaterial
    for the large T used in the paper.
    """
    j = np.arange(T)
    return 2 * np.pi * (j + offset) / T


def evolve(model: CDHM, T: int, Nk: int, sample_periods=None, offset: float = 0.5):
    """Evolve phi(k) through T driving periods.

    Returns (k_grid, phi_final, samples) where samples is a dict
    {period_index: phi(k) copy} for the requested sample_periods (period 0 is the
    initial state).  phi has shape (Nk, N).
    """
    k = np.linspace(-np.pi / model.N, np.pi / model.N, Nk, endpoint=False)
    phi = np.zeros((Nk, model.N), dtype=complex)
    phi[:, 0] = 1.0
    betas = beta_schedule(T, offset)
    sample_set = set(sample_periods or [])
    samples = {}
    if 0 in sample_set:
        samples[0] = phi.copy()
    for j in range(T):
        U = model.floquet_operator(k, float(betas[j]))
        phi = np.einsum("kij,kj->ki", U, phi)
        if (j + 1) in sample_set:
            samples[j + 1] = phi.copy()
    return k, phi, samples


def evolve_fast(model: CDHM, T: int, Nk: int, sample_periods=None, offset: float = 0.5,
                n_sub: int | None = None):
    """Fast wave-packet evolution using a Strang split of the hopping (fixed) and
    the time-dependent diagonal potential.

    H(k,t;beta) = A(k) + c(t) V(beta), A = h_hop(k) fixed, V diagonal, c(t)=K
    cos(2 pi t/tau).  exp(-i A dt) is precomputed once per k (independent of beta
    and t); the diagonal factor is a cheap elementwise phase.  Reproduces
    evolve() to Strang order O(dt^2) but is orders of magnitude faster for large T.

    Returns (k_grid, phi_final, samples) exactly like evolve().
    """
    n_sub = model.n_sub if n_sub is None else n_sub
    k = np.linspace(-np.pi / model.N, np.pi / model.N, Nk, endpoint=False)
    A = model.h_hop(k)                                   # (Nk, N, N)
    dt = model.tau / n_sub
    Uf = _expm_from_herm(A, dt)                          # exp(-i A dt)
    Uh = _expm_from_herm(A, dt / 2)                      # exp(-i A dt/2)
    t_s = (np.arange(n_sub) + 0.5) * dt
    c = model.K * np.cos(2 * np.pi * t_s / model.tau)    # (n_sub,)

    phi = np.zeros((Nk, model.N), dtype=complex)
    phi[:, 0] = 1.0
    betas = beta_schedule(T, offset)
    sample_set = set(sample_periods or [])
    samples = {0: phi.copy()} if 0 in sample_set else {}

    for j in range(T):
        vdiag = model.v_diag(float(betas[j]))            # (N,)
        phi = np.einsum("kij,kj->ki", Uh, phi)
        for s in range(n_sub):
            phase = np.exp(-1j * c[s] * vdiag * dt)      # (N,)
            phi = phase[None, :] * phi
            if s < n_sub - 1:
                phi = np.einsum("kij,kj->ki", Uf, phi)
        phi = np.einsum("kij,kj->ki", Uh, phi)
        if (j + 1) in sample_set:
            samples[j + 1] = phi.copy()
    return k, phi, samples


def _expm_from_herm(H, dt: float):
    w, V = np.linalg.eigh(H)
    phase = np.exp(-1j * w * dt)
    return (V * phase[..., None, :]) @ np.conjugate(np.swapaxes(V, -1, -2))


def x_expectation(model: CDHM, phi: np.ndarray) -> float:
    """Exact <x> (atomic-spacing units) from the k-space 3-vector field phi(k).

    Gauge-free position expectation in the fixed sublattice basis:

        <x> = ( i sum_k sum_j conj(phi_j) d/dk phi_j + sum_k sum_j j |phi_j|^2 )
              / ( sum_k sum_j |phi_j|^2 )

    The N*n ("cell") part is captured by the spectral k-derivative; the j
    (sublattice offset) part is the diagonal term.  phi_j(k) is smooth and
    periodic over the BZ (U(k,beta) is periodic and the initial state is
    k-independent), so the FFT spectral derivative is exact once Nk resolves the
    packet.  This equals sum_l l |<l|Psi>|^2 without band decomposition or gauge
    fixing, and stays well-conditioned even when the packet width >> <x>.
    """
    Nk, N = phi.shape
    L = 2 * np.pi / model.N                         # BZ width
    dk = L / Nk
    freq = np.fft.fftfreq(Nk, d=dk)                 # cycles per unit k
    dphi = np.fft.ifft(1j * 2 * np.pi * freq[:, None] * np.fft.fft(phi, axis=0), axis=0)
    j_idx = np.arange(N)
    total = np.abs(phi) ** 2
    cell_part = 1j * np.conjugate(phi) * dphi        # i phi* d/dk phi
    sub_part = j_idx[None, :] * total
    num = np.real(cell_part.sum() + sub_part.sum())
    den = total.sum()
    return float(num / den)


def x_width(model: CDHM, phi: np.ndarray) -> float:
    """RMS spread of the packet (atomic units) — for diagnosing required Nk."""
    Nk, N = phi.shape
    psi = np.fft.ifft(phi, axis=0)
    prob = np.abs(psi) ** 2
    n_idx = np.fft.fftfreq(Nk) * Nk
    j_idx = np.arange(N)
    x = model.N * n_idx[:, None] + j_idx[None, :]
    total = prob.sum()
    mean = (x * prob).sum() / total
    return float(np.sqrt(((x - mean) ** 2 * prob).sum() / total))


def band_populations(model: CDHM, k: np.ndarray, phi: np.ndarray, beta: float):
    """rho_{n,k} = |<psi_{n,k}(beta)|phi(k)>|^2, shape (Nk, N)."""
    _, states = floquet_bands(model, k, beta)     # states[...,:,n] = band n
    amp = np.einsum("kin,ki->kn", np.conjugate(states), phi)
    return np.abs(amp) ** 2
