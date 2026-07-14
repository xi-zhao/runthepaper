"""Analytic theory of Wang-Zhou-Gong PRB 91, 085420 (2015).

Implements, for the CDHM:
  * Berry curvature B_n(beta,k) over the (k,beta) torus and its beta-integral
    dgamma_{n,k}/dk  (Eq. 11);
  * average quasienergy E_{n,k} = int_0^1 omega_{n,k}[beta(s)] ds  (Eq. 12);
  * the interband kernel W_{nm,k}(0)  (Eq. 6);
  * the population change Delta rho_{n,k}  (Eq. 8, Fig. 2b);
  * the one-cycle displacement Delta<x> = Berry-integral term + IBC correction
    (Eq. 13, Fig. 3/4).

Unit convention.  The displacement is returned in atomic-spacing units, matching
the exact dynamics <x> from observables.py.  A filled band pumped over one cycle
gives Delta x = a * C_n (a = N = 3, C_n = Chern number); this fixes the overall
factor a/(2 pi) on both terms of Eq. (13).  See DERIVATION.md.
"""
from __future__ import annotations

import numpy as np
from cdhm import CDHM


def _floquet_eig(model: CDHM, k, beta: float):
    """Return (lam, omega, states) for U(k,beta): lam = exp(-i omega) eigenvalues,
    omega sorted ascending, states columns = right eigenvectors (orthonormal)."""
    U = model.floquet_operator(k, beta)
    lam, V = np.linalg.eig(U)
    omega = -np.angle(lam)
    order = np.argsort(omega, axis=-1)
    omega = np.take_along_axis(omega, order, axis=-1)
    lam = np.take_along_axis(lam, order, axis=-1)
    V = np.take_along_axis(V, order[..., None, :], axis=-1)
    return lam, omega, V


# ---------- initial-state amplitudes ---------------------------------------
def initial_amplitudes(model: CDHM, k):
    """C_{n,k}(0) = <psi_{n,k}(0)|e_0>, rho, omega, states at beta=0."""
    lam, omega, V = _floquet_eig(model, k, 0.0)
    C = np.conjugate(V[..., 0, :])            # <psi_n|e_0>
    return C, np.abs(C) ** 2, omega, V, lam


# ---------- W_{nm,k}(0) kernel (Eq. 6 at s=0) ------------------------------
def W0_kernel(model: CDHM, k, dbeta: float = 1e-4):
    """W_{nm,k}(0) = 2 pi <psi_n|d_beta psi_m>/(1 - exp(i(omega_n-omega_m))),
    using <psi_n|d_beta psi_m> = <psi_n|d_beta U|psi_m>/(lam_m - lam_n)  (n != m).

    Returns (W, C, rho, omega, states) with W shape (..., N, N), diagonal set to 0.
    """
    C, rho, omega, V, lam = initial_amplitudes(model, k)
    Up = model.floquet_operator(k, +dbeta)
    Um = model.floquet_operator(k, -dbeta)
    dU = (Up - Um) / (2 * dbeta)
    # <psi_n | dU | psi_m>
    M = np.conjugate(np.swapaxes(V, -1, -2)) @ dU @ V     # (..., N, N), row n col m
    N = model.N
    W = np.zeros_like(M)
    for n in range(N):
        for m in range(N):
            if n == m:
                continue
            denom_lam = lam[..., m] - lam[..., n]
            denom_ph = 1 - np.exp(1j * (omega[..., n] - omega[..., m]))
            W[..., n, m] = 2 * np.pi * M[..., n, m] / (denom_lam * denom_ph)
    return W, C, rho, omega, V, lam


# ---------- Berry phase gamma_{n,k} over the cycle -------------------------
def berry_phase(model: CDHM, k, Nbeta: int = 200):
    """gamma_{n,k} = -Im log prod_j <psi_n(beta_j)|psi_n(beta_{j+1})>  (Wilson loop
    of band n around beta in [0,2pi)).  Bands tracked by ascending-omega sort."""
    betas = np.linspace(0, 2 * np.pi, Nbeta, endpoint=False)
    prev = None
    first = None
    prod = None
    for i, b in enumerate(betas):
        _, _, V = _floquet_eig(model, k, float(b))
        if prev is None:
            first = V
            prod = np.ones(np.shape(k) + (model.N,), dtype=complex)
        else:
            ov = np.einsum("...in,...in->...n", np.conjugate(prev), V)  # <prev_n|V_n>
            prod = prod * ov
        prev = V
    # close the loop
    ov = np.einsum("...in,...in->...n", np.conjugate(prev), first)
    prod = prod * ov
    return -np.angle(prod)                     # (..., N)


# ---------- average quasienergy E_{n,k} (Eq. 12) ---------------------------
def avg_quasienergy(model: CDHM, k, Nbeta: int = 400):
    """E_{n,k} = int_0^1 omega_{n,k}[beta(s)] ds = (1/2pi) int_0^2pi omega dbeta,
    with midpoint sampling and ascending-omega band labelling."""
    betas = (np.arange(Nbeta) + 0.5) / Nbeta * 2 * np.pi
    acc = np.zeros(np.shape(k) + (model.N,))
    for b in betas:
        _, omega, _ = _floquet_eig(model, k, float(b))
        acc += omega
    return acc / Nbeta                          # average over s in [0,1]


# ---------- Berry curvature integral dgamma/dk via Fukui plaquettes --------
def berry_flux_strips(model: CDHM, k_grid, Nbeta: int = 120):
    """Return F[i,n] = flux of band n through the k-strip at k_grid[i]
    (integrated over beta in [0,2pi)) via the Fukui-Hatsugai-Suzuki method.
    sum_i F[i,n] = 2 pi C_n.  k_grid must be a uniform periodic BZ grid.
    """
    Nk = len(k_grid)
    betas = np.linspace(0, 2 * np.pi, Nbeta, endpoint=False)
    V = np.zeros((Nk, Nbeta, model.N, model.N), dtype=complex)
    for jb, b in enumerate(betas):
        _, _, Vb = _floquet_eig(model, k_grid, float(b))
        V[:, jb] = Vb
    F = np.zeros((Nk, model.N))
    for n in range(model.N):
        v = V[..., n]                            # (Nk, Nbeta, N)
        for i in range(Nk):
            ip = (i + 1) % Nk
            for jb in range(Nbeta):
                jp = (jb + 1) % Nbeta
                u00 = v[i, jb]; u10 = v[ip, jb]; u11 = v[ip, jp]; u01 = v[i, jp]
                link = (np.vdot(u00, u10) * np.vdot(u10, u11)
                        * np.vdot(u11, u01) * np.vdot(u01, u00))
                F[i, n] += np.angle(link)
    return F


# ---------- Delta rho_{n,k} theory (Eq. 8, Fig. 2b) ------------------------
def accumulated_Omega(model: CDHM, k, T: int, offset: float = 0.5):
    """Omega_{n,k}(1) = sum_{j=1}^T omega_{n,k}(beta_j)  (Eq. 2), evaluated on the
    exact discrete protocol beta_j = 2 pi (j+offset)/T used by the dynamics.

    This exact discrete sum (not the large-T integral T*E) is required because the
    W(1) term carries exp(-i(Omega_n-Omega_m)), a phase of hundreds of radians at
    the paper's T=1024.  Returns (Nk, N)."""
    betas = 2 * np.pi * (np.arange(T) + offset) / T
    acc = np.zeros(np.shape(k) + (model.N,))
    for b in betas:
        _, om, _ = _floquet_eig(model, k, float(b))
        acc += om
    return acc


def delta_rho_theory(model: CDHM, k, T: int, dbeta: float = 1e-4, Nbeta_g: int = 360,
                     offset: float = 0.5):
    """Delta rho_{n,k} = (2/T) Re[ sum_{m!=n} C*_n C_m (W_{nm}|_0^1) ]  (Eq. 8), with
    W_{nm}|_0^1 = W_{nm}(0) [ exp(i Phi_{nm}) - 1 ],
    Phi_{nm} = (gamma_n - gamma_m) - (Omega_n(1) - Omega_m(1)).

    The -(Omega_n-Omega_m) sign matches the e^{-i omega} eigenphase convention of
    this code (an overall omega-sign choice); it is fixed against the exact
    dynamics.  Returns (Delta rho, rho(0)), both (Nk, N)."""
    W, C, rho, omega, V, lam = W0_kernel(model, k, dbeta)
    gamma = berry_phase(model, k, Nbeta_g)
    Omega = accumulated_Omega(model, k, T, offset)
    Nk = W.shape[0]
    N = model.N
    drho = np.zeros((Nk, N))
    for n in range(N):
        acc = np.zeros(Nk, dtype=complex)
        for m in range(N):
            if m == n:
                continue
            Phi = (gamma[..., n] - gamma[..., m]) - (Omega[..., n] - Omega[..., m])
            Wloop = W[..., n, m] * (np.exp(1j * Phi) - 1)
            acc += np.conjugate(C[..., n]) * C[..., m] * Wloop
        drho[..., n] = (2.0 / T) * np.real(acc)
    return drho, rho


# ---------- Delta<x> theory (Eq. 13, Fig. 3/4) -----------------------------
def delta_x_theory(model: CDHM, Nk: int = 401, Nbeta_F: int = 120,
                   Nbeta_E: int = 400, dbeta: float = 1e-4, dk_E: float = 1e-3):
    """Return dict with 'berry' (term 1), 'ibc' (term 2), 'total', in atomic
    units, plus per-band Chern numbers.  k on a uniform periodic BZ grid."""
    a = model.a
    k = np.linspace(-np.pi / model.N, np.pi / model.N, Nk, endpoint=False)
    dk = (2 * np.pi / model.N) / Nk

    # --- term 1: (a/2pi) sum_n sum_i rho_{n,i} * (beta-flux strip) ---
    F = berry_flux_strips(model, k, Nbeta_F)          # (Nk, N), sum_i F = 2pi C_n
    C, rho, omega0, V0, lam0 = initial_amplitudes(model, k)
    term1_bands = (a / (2 * np.pi)) * np.sum(rho * F, axis=0)   # per band
    term1 = float(term1_bands.sum())
    chern = F.sum(axis=0) / (2 * np.pi)

    # --- term 2 (IBC): -(a/2pi) * 2 * dk * sum_i sum_{m!=n} Re[C*_n C_m (dE_n/dk) W_nm(0)] ---
    W, C, rho, omega, V, lam = W0_kernel(model, k, dbeta)
    # dE_n/dk via central difference of the average quasienergy
    Ep = avg_quasienergy(model, k + dk_E, Nbeta_E)
    Em = avg_quasienergy(model, k - dk_E, Nbeta_E)
    dEdk = (Ep - Em) / (2 * dk_E)                     # (Nk, N)
    N = model.N
    acc = 0.0
    for n in range(N):
        for m in range(N):
            if m == n:
                continue
            integ = np.conjugate(C[..., n]) * C[..., m] * dEdk[..., n] * W[..., n, m]
            acc += np.sum(np.real(integ))
    term2 = -(a / (2 * np.pi)) * 2 * dk * acc

    return {
        "berry": term1,
        "berry_bands": term1_bands.tolist(),
        "ibc": float(term2),
        "total": float(term1 + term2),
        "chern": chern.tolist(),
    }
