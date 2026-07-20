"""GPU (torch) port of the QRC collisional-map engine for paper-exact ensembles.

Self-contained single file (uploadable to the remote A100). Semantics mirror
qrc_engine.py exactly: same Mackey-Glass generator and seeds, same binning
estimator (B=50, 1e-12 truncation), same bin-representative work bookkeeping,
so the per-step identity beta*W_irr = chi_d holds at machine precision and CPU
vs GPU totals agree to ~1e-8 (complex128 throughout).

Usage:
  python qrc_gpu.py scan --model cluster --n-seq 5000 --n-points 21 --out fig2_cluster_scan.csv
  python qrc_gpu.py scan --model tfim --n-seq 5000 --n-points 25 --realizations 100 --out fig2_tfim_scan.csv
  python qrc_gpu.py nmse --model cluster --n-seq 500 --n-points 21 --out nmse_cluster_scan.csv

Rows are appended per (param, realization) job; completed jobs are skipped on
restart (checkpointed campaign).
"""
from __future__ import annotations

import argparse
import csv
import os
import time
from pathlib import Path

import numpy as np
import torch

# ----------------------------- Mackey-Glass (identical to mackey_glass.py) ---

BETA_MG, GAMMA_MG, TAU_MG, DT_SAMP, DT_INT = 0.2, 0.1, 18.0, 3.0, 0.1
SIGMA_S2_TARGET = 0.11


def _mg_rhs(x_now, x_delay):
    return BETA_MG * x_delay / (1.0 + x_delay**10) - GAMMA_MG * x_now


def generate_mg_sequences(n_sequences, n_samples, *, transient_samples=300, seed=0):
    rng = np.random.default_rng(seed)
    delay_steps = int(round(TAU_MG / DT_INT))
    steps_per_sample = int(round(DT_SAMP / DT_INT))
    total_samples = transient_samples + n_samples
    total_steps = total_samples * steps_per_sample
    history = np.empty((n_sequences, delay_steps + total_steps + 1), dtype=np.float64)
    history[:, : delay_steps + 1] = rng.uniform(0.8, 1.6, size=(n_sequences, 1))
    for step in range(total_steps):
        idx = delay_steps + step
        x_now = history[:, idx]
        x_del0 = history[:, idx - delay_steps]
        x_del1 = history[:, idx - delay_steps + 1]
        x_del_half = 0.5 * (x_del0 + x_del1)
        k1 = _mg_rhs(x_now, x_del0)
        k2 = _mg_rhs(x_now + 0.5 * DT_INT * k1, x_del_half)
        k3 = _mg_rhs(x_now + 0.5 * DT_INT * k2, x_del_half)
        k4 = _mg_rhs(x_now + DT_INT * k3, x_del1)
        history[:, idx + 1] = x_now + (DT_INT / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    samples = history[:, delay_steps::steps_per_sample][:, :total_samples][:, transient_samples:]
    centered = samples - samples.mean(axis=1, keepdims=True)
    rescaled = centered * np.sqrt(SIGMA_S2_TARGET / centered.var())
    if np.abs(rescaled).max() > 1.0:
        rescaled /= np.abs(rescaled).max()
    return rescaled


# ----------------------------- Hamiltonians (identical to qrc_engine.py) -----

SIGMA = {
    "I": np.eye(2, dtype=np.complex128),
    "X": np.array([[0, 1], [1, 0]], dtype=np.complex128),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=np.complex128),
    "Z": np.array([[1, 0], [0, -1]], dtype=np.complex128),
}


def pauli_string(L, ops):
    out = np.array([[1.0 + 0j]])
    for site in range(L):
        out = np.kron(out, SIGMA[ops.get(site, "I")])
    return out


def tfim_hamiltonian(L, J, rng):
    H = np.zeros((2**L, 2**L), dtype=np.complex128)
    for i in range(L):
        for j in range(i):
            H += rng.uniform(-J / 2.0, J / 2.0) * pauli_string(L, {i: "Z", j: "Z"})
    for i in range(L):
        H += pauli_string(L, {i: "X"})
    return H


def cluster_hamiltonian(L, alpha, J_zz=0.1, pbc=False):
    J_zxz = (1.0 - J_zz) * alpha
    h_x = (1.0 - J_zz) * (1.0 - alpha)
    H = np.zeros((2**L, 2**L), dtype=np.complex128)
    bonds = range(L) if pbc else range(L - 1)
    for i in bonds:
        H -= J_zz * pauli_string(L, {i: "Z", (i + 1) % L: "Z"})
    for i in range(L):
        H -= h_x * pauli_string(L, {i: "X"})
    triples = range(L) if pbc else range(1, L - 1)
    for i in triples:
        H += J_zxz * pauli_string(L, {(i - 1) % L: "Z", i: "X", (i + 1) % L: "Z"})
    return H


def drive_diagonal(L):
    diag = np.zeros(2**L)
    for i in range(L):
        diag += np.real(np.diag(pauli_string(L, {i: "Z"})))
    return diag


# ----------------------------- torch engine ----------------------------------

EIG_TRUNC = 1e-12
N_BINS = 50


def device_auto():
    return torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


def build_cache(H0_np, lam, dt, beta, n_grid, device):
    D = H0_np.shape[0]
    z = drive_diagonal(int(np.log2(D)))
    H0 = torch.as_tensor(H0_np, dtype=torch.complex128, device=device)
    zt = torch.as_tensor(z, dtype=torch.float64, device=device)
    s_grid = torch.linspace(-1.0, 1.0, n_grid, dtype=torch.float64, device=device)
    H = H0.unsqueeze(0) + (s_grid[:, None] * lam * zt[None, :]).to(torch.complex128).diag_embed()
    w, V = _eigh(H)
    U = (V * torch.exp(-1j * w * dt).unsqueeze(1)) @ V.conj().transpose(-2, -1)
    boltz = torch.exp(-beta * (w - w.min(dim=1, keepdim=True).values))
    boltz = boltz / boltz.sum(dim=1, keepdim=True)
    rho_eq = (V * boltz.to(torch.complex128).unsqueeze(1)) @ V.conj().transpose(-2, -1)
    rho0 = rho_eq[(n_grid - 1) // 2] if n_grid % 2 == 1 else None
    # unperturbed (s=0) Gibbs state for the initial condition
    w0, V0 = torch.linalg.eigh(H0)
    b0 = torch.exp(-beta * (w0 - w0.min()))
    b0 = b0 / b0.sum()
    rho0 = (V0 * b0.to(torch.complex128)) @ V0.conj().transpose(-2, -1)
    return {"U": U, "rho_eq": rho_eq, "s_grid": s_grid, "n_grid": n_grid,
            "H0": H0, "z": zt, "rho0": rho0}


def cache_index(cache, s):
    n = cache["n_grid"]
    return torch.clamp(torch.round((s + 1.0) * (n - 1) / 2.0).long(), 0, n - 1)


# torch routes batched complex128 eigvalsh through a slow cusolver path
# (~0.6 ms/matrix even on an idle A100). cupy.linalg.eigvalsh uses
# syevjBatched (Jacobi), measured 28x faster at (6000,64,64) c128.
# torch<->cupy exchange is zero-copy dlpack on the shared legacy default
# stream. --real-embed (real-symmetric 128x128 embedding) was benchmarked
# slower than c128 and is kept only as a fallback.
REAL_EMBED = False
CUPY_EIG = False
_cupy = None


def _eigvalsh(herm):
    if CUPY_EIG and herm.is_cuda:
        w_cp = _cupy.linalg.eigvalsh(_cupy.from_dlpack(herm.contiguous()))
        return torch.from_dlpack(w_cp)
    return torch.linalg.eigvalsh(herm)


def _eigh(herm):
    """Batched Hermitian eigendecomposition with the same cupy fast path."""
    if CUPY_EIG and herm.is_cuda and herm.dim() > 2:
        w_cp, v_cp = _cupy.linalg.eigh(_cupy.from_dlpack(herm.contiguous()))
        return torch.from_dlpack(w_cp), torch.from_dlpack(v_cp)
    return torch.linalg.eigh(herm)


def entropy(rho):
    herm = (rho + rho.conj().transpose(-2, -1)) / 2
    if REAL_EMBED:
        re, im = herm.real, herm.imag
        top = torch.cat([re, -im], dim=-1)
        bot = torch.cat([im, re], dim=-1)
        w = _eigvalsh(torch.cat([top, bot], dim=-2))
        w_safe = torch.where(w > EIG_TRUNC, w, torch.ones_like(w))
        return -0.5 * (w_safe * torch.log(w_safe)).sum(dim=-1)
    w = _eigvalsh(herm)
    w_safe = torch.where(w > EIG_TRUNC, w, torch.ones_like(w))
    return -(w_safe * torch.log(w_safe)).sum(dim=-1)


def shannon(p):
    q = torch.where(p > EIG_TRUNC, p, torch.ones_like(p))
    return -(q * torch.log(q)).sum(dim=-1)


def binned(rho, s):
    """(P_b, rho_b, s_mean) over occupied bins."""
    idx = torch.clamp(((s + 1.0) * 0.5 * N_BINS).long(), 0, N_BINS - 1)
    counts = torch.bincount(idx, minlength=N_BINS)
    occ = counts > 0
    D = rho.shape[-1]
    sums = torch.zeros(N_BINS, D * D, dtype=rho.dtype, device=rho.device)
    sums.index_add_(0, idx, rho.reshape(len(s), -1))
    s_sums = torch.zeros(N_BINS, dtype=torch.float64, device=rho.device)
    s_sums.index_add_(0, idx, s)
    P_b = counts[occ].double() / len(s)
    rho_b = (sums[occ] / counts[occ].to(rho.dtype)[:, None]).reshape(-1, D, D)
    s_mean = s_sums[occ] / counts[occ].double()
    return P_b, rho_b, s_mean


def simulate_ensemble_gpu(H0_np, sequences_np, *, lam=0.05, beta=1.0, gamma0=0.1,
                          dt=1.0, n_wash=500, n_eval=2000, taus=(1, 2), hs=(2, 3),
                          cache_grid=401, device=None):
    device = device or device_auto()
    P_th = 1.0 - np.exp(-gamma0 * dt)
    cache = build_cache(H0_np, lam, dt, beta, cache_grid, device)
    H0, z = cache["H0"], cache["z"]
    seqs = torch.as_tensor(sequences_np, dtype=torch.float64, device=device)
    n_seq = seqs.shape[0]
    rho = cache["rho0"].unsqueeze(0).expand(n_seq, -1, -1).clone()

    keys = ["chi_m_tot", "chi_p_tot", "chi_d_tot", "I_m_tot", "I_p_tot", "C_m_tot",
            "C_p_tot", "beta_W_irr_tot", "beta_W_relax_tot"]
    keys += [f"chi_m_tau{t}_tot" for t in taus] + [f"chi_p_h{h}_tot" for h in hs]
    totals = {k: 0.0 for k in keys}
    identity_residual = 0.0

    def bin_metrics(s_key, S_bar, H_bar, C_bar):
        P_b, rho_b, s_mean = binned(rho, s_key)
        S_b = entropy(rho_b)
        diag = torch.diagonal(rho_b, dim1=-2, dim2=-1).real
        H_b = shannon(diag)
        chi = (S_bar - (P_b * S_b).sum()).item()
        I_cl = (H_bar - (P_b * H_b).sum()).item()
        C_ens = ((P_b * (H_b - S_b)).sum() - C_bar).item()
        return P_b, rho_b, s_mean, S_b, chi, I_cl, C_ens

    for n in range(n_wash + n_eval):
        idx = cache_index(cache, seqs[:, n])
        U = cache["U"][idx]
        rho = (1.0 - P_th) * (U @ rho @ U.conj().transpose(-2, -1)) + P_th * cache["rho_eq"][idx]
        if n < n_wash:
            continue

        rho_bar = rho.mean(dim=0)
        S_bar = entropy(rho_bar.unsqueeze(0))[0]
        H_bar = shannon(torch.diagonal(rho_bar, dim1=-2, dim2=-1).real)
        C_bar = H_bar - S_bar

        P_m, rho_m, sm_mean, S_m_b, chi_m, I_m, C_m = bin_metrics(seqs[:, n], S_bar, H_bar, C_bar)
        P_p, rho_p, sp_mean, S_p_b, chi_p, I_p, C_p = bin_metrics(seqs[:, n + 1], S_bar, H_bar, C_bar)

        def energy(P_b, rho_b, s_mean):
            e0 = torch.einsum("bij,ji->b", rho_b, H0).real
            ez = (torch.diagonal(rho_b, dim1=-2, dim2=-1).real * z[None, :]).sum(dim=-1)
            return (P_b * (e0 + lam * s_mean * ez)).sum()

        E_p, E_m = energy(P_p, rho_p, sp_mean), energy(P_m, rho_m, sm_mean)
        S_p, S_m = (P_p * S_p_b).sum(), (P_m * S_m_b).sum()
        W = E_p - E_m
        delta_F = (E_p - S_p / beta) - (E_m - S_m / beta)
        beta_W_irr_inj = (beta * (W - delta_F)).item()

        idx_b = cache_index(cache, sp_mean)
        U_b = cache["U"][idx_b]
        rho_relaxed = (1.0 - P_th) * (U_b @ rho_p @ U_b.conj().transpose(-2, -1)) + P_th * cache["rho_eq"][idx_b]
        H_bins = H0.unsqueeze(0) + (lam * sp_mean[:, None] * z[None, :]).to(torch.complex128).diag_embed()
        E_bins = torch.einsum("bij,bji->b", rho_p, H_bins).real
        E_rel = torch.einsum("bij,bji->b", rho_relaxed, H_bins).real
        S_rel = entropy(rho_relaxed)
        beta_W_relax = (P_p * ((S_rel - S_p_b) + beta * (E_bins - E_rel))).sum().item()

        totals["chi_m_tot"] += chi_m
        totals["chi_p_tot"] += chi_p
        totals["chi_d_tot"] += chi_m - chi_p
        totals["I_m_tot"] += I_m
        totals["I_p_tot"] += I_p
        totals["C_m_tot"] += C_m
        totals["C_p_tot"] += C_p
        totals["beta_W_irr_tot"] += beta_W_irr_inj + beta_W_relax
        totals["beta_W_relax_tot"] += beta_W_relax
        for t in taus:
            if n - t >= 0:
                totals[f"chi_m_tau{t}_tot"] += bin_metrics(seqs[:, n - t], S_bar, H_bar, C_bar)[4]
        for h in hs:
            if n + h < seqs.shape[1]:
                totals[f"chi_p_h{h}_tot"] += bin_metrics(seqs[:, n + h], S_bar, H_bar, C_bar)[4]
        identity_residual = max(identity_residual, abs(beta_W_irr_inj - (chi_m - chi_p)))

    totals["identity_residual_max"] = identity_residual
    totals["n_eval"] = n_eval
    totals["n_seq"] = n_seq
    return totals


# ----------------------------- packed multi-realization engine ---------------

def simulate_packed_gpu(H0_list, seq_list, *, lam=0.05, beta=1.0, gamma0=0.1,
                        dt=1.0, n_wash=500, n_eval=2000, taus=(1, 2), hs=(2, 3),
                        cache_grid=401, device=None):
    """Evolve R disorder realizations (each with its own H0 and MG batch) in one
    packed trajectory batch. Semantics per realization identical to
    simulate_ensemble_gpu; returns a list of R totals dicts.

    Zero per-step host synchronization: all R*N_BINS bins keep a fixed shape
    (empty bins carry P_b = 0 and a zero state, which contributes nothing),
    and per-step results accumulate into GPU tensors that are read out once
    at the end.
    """
    device = device or device_auto()
    R = len(H0_list)
    S = seq_list[0].shape[0]
    P_th = 1.0 - np.exp(-gamma0 * dt)
    caches = [build_cache(H, lam, dt, beta, cache_grid, device) for H in H0_list]
    U_flat = torch.stack([c["U"] for c in caches]).reshape(-1, H0_list[0].shape[0], H0_list[0].shape[0])
    EQ_flat = torch.stack([c["rho_eq"] for c in caches]).reshape_as(U_flat)
    H0_all = torch.stack([c["H0"] for c in caches])
    z = caches[0]["z"]
    G = cache_grid
    D = H0_all.shape[-1]

    seqs = torch.as_tensor(np.stack(seq_list), dtype=torch.float64, device=device)  # (R, S, N)
    n_total = seqs.shape[2]
    r_idx = torch.arange(R, device=device).repeat_interleave(S)                     # (R*S,)
    rho = torch.stack([c["rho0"] for c in caches]).repeat_interleave(S, dim=0).clone()

    NB = R * N_BINS
    owner = torch.arange(R, device=device).repeat_interleave(N_BINS)                # static (NB,)
    H0_bins = H0_all.repeat_interleave(N_BINS, dim=0)                               # static (NB, D, D)
    ones = torch.ones(R * S, dtype=torch.float64, device=device)

    keys = ["chi_m_tot", "chi_p_tot", "chi_d_tot", "I_m_tot", "I_p_tot", "C_m_tot",
            "C_p_tot", "beta_W_irr_tot", "beta_W_relax_tot"]
    keys += [f"chi_m_tau{t}_tot" for t in taus] + [f"chi_p_h{h}_tot" for h in hs]
    acc = {k: torch.zeros(R, dtype=torch.float64, device=device) for k in keys}
    identity_residual = torch.zeros(R, dtype=torch.float64, device=device)

    def grid_index(s_flat):
        return torch.clamp(torch.round((s_flat + 1.0) * (G - 1) / 2.0).long(), 0, G - 1)

    def packed_bins(s_flat):
        """Fixed-shape (NB,) binning; empty bins have P_b = 0 and zero state."""
        b = torch.clamp(((s_flat + 1.0) * 0.5 * N_BINS).long(), 0, N_BINS - 1)
        gidx = r_idx * N_BINS + b
        counts = torch.zeros(NB, dtype=torch.float64, device=device)
        counts.index_add_(0, gidx, ones)
        safe = torch.clamp(counts, min=1.0)
        sums = torch.zeros(NB, D * D, dtype=rho.dtype, device=device)
        sums.index_add_(0, gidx, rho.reshape(R * S, -1))
        s_sums = torch.zeros(NB, dtype=torch.float64, device=device)
        s_sums.index_add_(0, gidx, s_flat)
        P_b = counts / S
        rho_b = (sums / safe.to(rho.dtype)[:, None]).reshape(NB, D, D)
        s_mean = s_sums / safe
        return P_b, rho_b, s_mean

    def per_r_sum(values):
        return values.reshape(R, N_BINS).sum(dim=1)

    def bin_metrics(s_flat, S_bar_r, H_bar_r, C_bar_r):
        P_b, rho_b, s_mean = packed_bins(s_flat)
        S_b = entropy(rho_b)
        H_b = shannon(torch.diagonal(rho_b, dim1=-2, dim2=-1).real)
        chi_r = S_bar_r - per_r_sum(P_b * S_b)
        I_r = H_bar_r - per_r_sum(P_b * H_b)
        C_r = per_r_sum(P_b * (H_b - S_b)) - C_bar_r
        return P_b, rho_b, s_mean, S_b, chi_r, I_r, C_r

    for n in range(n_wash + n_eval):
        s_flat = seqs[:, :, n].reshape(-1)
        flat_idx = r_idx * G + grid_index(s_flat)
        U = U_flat[flat_idx]
        rho = (1.0 - P_th) * (U @ rho @ U.conj().transpose(-2, -1)) + P_th * EQ_flat[flat_idx]
        if n < n_wash:
            continue

        rho_bar = torch.zeros(R, D * D, dtype=rho.dtype, device=device)
        rho_bar.index_add_(0, r_idx, rho.reshape(R * S, -1))
        rho_bar = (rho_bar / S).reshape(R, D, D)
        S_bar_r = entropy(rho_bar)
        H_bar_r = shannon(torch.diagonal(rho_bar, dim1=-2, dim2=-1).real)
        C_bar_r = H_bar_r - S_bar_r

        P_m, rho_m, sm_mean, S_m_b, chi_m_r, I_m_r, C_m_r = bin_metrics(s_flat, S_bar_r, H_bar_r, C_bar_r)
        P_p, rho_p, sp_mean, S_p_b, chi_p_r, I_p_r, C_p_r = bin_metrics(
            seqs[:, :, n + 1].reshape(-1), S_bar_r, H_bar_r, C_bar_r)

        def energy_r(P_b, rho_b, s_mean):
            e0 = torch.einsum("bij,bji->b", rho_b, H0_bins).real
            ez = (torch.diagonal(rho_b, dim1=-2, dim2=-1).real * z[None, :]).sum(dim=-1)
            return per_r_sum(P_b * (e0 + lam * s_mean * ez))

        E_p_r, E_m_r = energy_r(P_p, rho_p, sp_mean), energy_r(P_m, rho_m, sm_mean)
        S_p_r = per_r_sum(P_p * S_p_b)
        S_m_r = per_r_sum(P_m * S_m_b)
        W_r = E_p_r - E_m_r
        delta_F_r = (E_p_r - S_p_r / beta) - (E_m_r - S_m_r / beta)
        beta_W_irr_r = beta * (W_r - delta_F_r)

        flat_b = owner * G + grid_index(sp_mean)
        U_b = U_flat[flat_b]
        rho_relaxed = (1.0 - P_th) * (U_b @ rho_p @ U_b.conj().transpose(-2, -1)) + P_th * EQ_flat[flat_b]
        H_b_dyn = H0_bins + (lam * sp_mean[:, None] * z[None, :]).to(torch.complex128).diag_embed()
        E_bins = torch.einsum("bij,bji->b", rho_p, H_b_dyn).real
        E_rel = torch.einsum("bij,bji->b", rho_relaxed, H_b_dyn).real
        S_rel = entropy(rho_relaxed)
        beta_W_relax_r = per_r_sum(P_p * ((S_rel - S_p_b) + beta * (E_bins - E_rel)))

        chi_d_r = chi_m_r - chi_p_r
        identity_residual = torch.maximum(identity_residual, (beta_W_irr_r - chi_d_r).abs())

        acc["chi_m_tot"] += chi_m_r
        acc["chi_p_tot"] += chi_p_r
        acc["chi_d_tot"] += chi_d_r
        acc["I_m_tot"] += I_m_r
        acc["I_p_tot"] += I_p_r
        acc["C_m_tot"] += C_m_r
        acc["C_p_tot"] += C_p_r
        acc["beta_W_irr_tot"] += beta_W_irr_r + beta_W_relax_r
        acc["beta_W_relax_tot"] += beta_W_relax_r
        for t in taus:
            if n - t >= 0:
                acc[f"chi_m_tau{t}_tot"] += bin_metrics(
                    seqs[:, :, n - t].reshape(-1), S_bar_r, H_bar_r, C_bar_r)[4]
        for h in hs:
            if n + h < n_total:
                acc[f"chi_p_h{h}_tot"] += bin_metrics(
                    seqs[:, :, n + h].reshape(-1), S_bar_r, H_bar_r, C_bar_r)[4]

    acc_host = {k: v.cpu().numpy() for k, v in acc.items()}
    resid_host = identity_residual.cpu().numpy()
    totals = []
    for r in range(R):
        row = {k: float(v[r]) for k, v in acc_host.items()}
        row["identity_residual_max"] = float(resid_host[r])
        row["n_eval"] = n_eval
        row["n_seq"] = S
        totals.append(row)
    return totals


# ----------------------------- NMSE (full Pauli readout) ---------------------

def full_pauli_observables(L):
    """All 4^L - 1 nontrivial Pauli strings, stacked (K, D, D)."""
    labels = ["I", "X", "Y", "Z"]
    ops = []
    for code in range(1, 4**L):
        digits, c = [], code
        for _ in range(L):
            digits.append(labels[c % 4])
            c //= 4
        ops.append(pauli_string(L, {i: digits[i] for i in range(L) if digits[i] != "I"}))
    return np.stack(ops)


def nmse_gpu(H0_np, sequences_np, *, horizons=(1, 2, 3), lam=0.05, beta=1.0,
             gamma0=0.1, dt=1.0, n_wash=500, n_train=2000, n_test=2000,
             eta=1e-5, cache_grid=401, device=None, obs_batch=512):
    """Ridge/NMSE with the full Pauli basis; per-sequence Gram accumulation.

    H0_np is either one Hamiltonian shared by all sequences, or a list with
    one Hamiltonian per sequence (the paper's disordered-TFIM NMSE protocol).
    The train window accumulates per-sequence Gram matrices and X^T y online;
    the test window caches float32 features, so n_seq must be modest (e.g. 50).
    """
    device = device or device_auto()
    P_th = 1.0 - np.exp(-gamma0 * dt)
    seqs = torch.as_tensor(sequences_np, dtype=torch.float64, device=device)
    n_seq = seqs.shape[0]
    H0_list = list(H0_np) if isinstance(H0_np, (list, tuple)) else [H0_np]
    per_seq_H = len(H0_list) > 1
    if per_seq_H and len(H0_list) != n_seq:
        raise ValueError("H0 list must have one entry per sequence")
    caches = [build_cache(H, lam, dt, beta, cache_grid, device) for H in H0_list]
    U_all = torch.stack([c["U"] for c in caches]).reshape(-1, H0_list[0].shape[0], H0_list[0].shape[0])
    EQ_all = torch.stack([c["rho_eq"] for c in caches]).reshape_as(U_all)
    G = cache_grid
    h_idx = (torch.arange(n_seq, device=device) if per_seq_H
             else torch.zeros(n_seq, dtype=torch.long, device=device))
    D = H0_list[0].shape[0]
    L = int(np.log2(D))
    obs_np = full_pauli_observables(L)
    K = obs_np.shape[0]
    obs = torch.as_tensor(obs_np.reshape(K, D * D), dtype=torch.complex128, device=device)

    F = K + 1  # + bias
    gram = torch.zeros(n_seq, F, F, dtype=torch.float64, device=device)
    xty = {h: torch.zeros(n_seq, F, dtype=torch.float64, device=device) for h in horizons}
    test_feats = torch.zeros(n_seq, n_test, F, dtype=torch.float32, device=device)

    if per_seq_H:
        rho = torch.stack([c["rho0"] for c in caches]).clone()
    else:
        rho = caches[0]["rho0"].unsqueeze(0).expand(n_seq, -1, -1).clone()
    for n in range(n_wash + n_train + n_test):
        gi = torch.clamp(torch.round((seqs[:, n] + 1.0) * (G - 1) / 2.0).long(), 0, G - 1)
        flat = h_idx * G + gi
        U = U_all[flat]
        rho = (1.0 - P_th) * (U @ rho @ U.conj().transpose(-2, -1)) + P_th * EQ_all[flat]
        if n < n_wash:
            continue
        # x = Tr(rho P_k), computed as obs @ vec(rho^T)
        rho_vec = rho.transpose(-2, -1).reshape(n_seq, D * D)
        x = torch.empty(n_seq, F, dtype=torch.float64, device=device)
        for k0 in range(0, K, obs_batch):
            k1 = min(k0 + obs_batch, K)
            x[:, k0:k1] = (rho_vec @ obs[k0:k1].transpose(0, 1)).real
        x[:, K] = 1.0
        m = n - n_wash
        if m < n_train:
            gram += x.unsqueeze(-1) * x.unsqueeze(-2)
            for h in horizons:
                xty[h] += x * seqs[:, n + h].unsqueeze(-1)
        else:
            test_feats[:, m - n_train] = x.float()

    results = {}
    eye = torch.eye(F, dtype=torch.float64, device=device)
    for h in horizons:
        w = torch.linalg.solve(gram + eta * eye, xty[h].unsqueeze(-1)).squeeze(-1)
        preds = torch.einsum("qtf,qf->qt", test_feats.double(), w)
        targets = torch.stack([seqs[q, n_wash + n_train + h: n_wash + n_train + n_test + h]
                               for q in range(n_seq)])
        nmse = ((preds - targets) ** 2).sum(dim=1) / (targets ** 2).sum(dim=1)
        results[f"nmse_h{h}"] = nmse.mean().item()
    return results


# ----------------------------- campaign driver -------------------------------

N_WASH, N_EVAL, MAX_H = 500, 2000, 3


def existing_jobs(out_path):
    done = set()
    if out_path.exists():
        for row in csv.DictReader(open(out_path)):
            done.add((row["model"], float(row["param"]), int(row["realization"])))
    return done


def append_row(out_path, row):
    exists = out_path.exists()
    with out_path.open("a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(row.keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def cmd_scan(args):
    device = device_auto()
    params = (np.linspace(0.0, 1.0, args.n_points) if args.model == "cluster"
              else np.logspace(-1, 2, args.n_points))
    out_path = Path(args.out)
    done = existing_jobs(out_path)
    pack = max(1, args.pack)
    print(f"device={device}, points={len(params)}, realizations={args.realizations}, "
          f"pack={pack}, done_rows={len(done)}", flush=True)
    for i, p in enumerate(params):
        p = float(p)
        for r0 in range(0, args.realizations, pack):
            reals = [r for r in range(r0, min(r0 + pack, args.realizations))
                     if (args.model, p, r) not in done]
            if not reals:
                continue
            t0 = time.time()
            seq_list, H0_list = [], []
            for r in reals:
                seq_seed = 1000 * i + r + 1
                seq_list.append(generate_mg_sequences(args.n_seq, N_WASH + N_EVAL + MAX_H + 1, seed=seq_seed))
                if args.model == "cluster":
                    H0_list.append(cluster_hamiltonian(6, p))
                else:
                    H0_list.append(tfim_hamiltonian(6, p, np.random.default_rng(10_000 + r)))
            if len(reals) == 1:
                totals_list = [simulate_ensemble_gpu(H0_list[0], seq_list[0], n_wash=N_WASH,
                                                     n_eval=N_EVAL, device=device)]
            else:
                totals_list = simulate_packed_gpu(H0_list, seq_list, n_wash=N_WASH,
                                                  n_eval=N_EVAL, device=device)
            dt_s = round(time.time() - t0, 1)
            for r, totals in zip(reals, totals_list):
                row = {"model": args.model, "param": p, "realization": r, "runtime_s": dt_s}
                row.update(totals)
                append_row(out_path, row)
            print(f"[point {i + 1}/{len(params)}] param={p:.4g} reals={reals[0]}-{reals[-1]} "
                  f"chi_m~{totals_list[0]['chi_m_tot']:.3f} "
                  f"resid={max(t['identity_residual_max'] for t in totals_list):.1e} ({dt_s}s)", flush=True)


def cmd_nmse(args):
    device = device_auto()
    params = (np.linspace(0.0, 1.0, args.n_points) if args.model == "cluster"
              else np.logspace(-1, 2, args.n_points))
    out_path = Path(args.out)
    done = existing_jobs(out_path)
    jobs = [(float(p), r) for i, p in enumerate(params) for r in range(args.realizations)]
    print(f"device={device}, NMSE jobs={len(jobs)}, done={len(done)}", flush=True)
    chunk = args.chunk
    for i, (p, r) in enumerate(jobs):
        if (args.model, p, r) in done:
            continue
        t0 = time.time()
        acc = {f"nmse_h{h}": [] for h in (1, 2, 3)}
        for c0 in range(0, args.n_seq, chunk):
            n_c = min(chunk, args.n_seq - c0)
            p_idx = int(np.where(np.isclose(params, p))[0][0])
            seq_seed = 7000 + 100 * p_idx + r + 100_000 * c0
            seqs = generate_mg_sequences(n_c, N_WASH + 2000 + 2000 + MAX_H, seed=seq_seed)
            if args.model == "cluster":
                H0 = cluster_hamiltonian(6, p)
            else:
                # paper protocol: each NMSE sequence uses a distinct disorder realization
                H0 = [tfim_hamiltonian(6, p, np.random.default_rng(500_000 + 1000 * p_idx + c0 + q))
                      for q in range(n_c)]
            res = nmse_gpu(H0, seqs, device=device)
            for k, v in res.items():
                acc[k].append((v, n_c))
        row = {"model": args.model, "param": p, "realization": r}
        for k, pairs in acc.items():
            row[k] = float(sum(v * w for v, w in pairs) / sum(w for _, w in pairs))
        row["runtime_s"] = round(time.time() - t0, 1)
        append_row(out_path, row)
        print(f"[{i + 1}/{len(jobs)}] param={p:.4g} real={r} nmse_h1={row['nmse_h1']:.4g} "
              f"({row['runtime_s']}s)", flush=True)


def main():
    global REAL_EMBED
    parser = argparse.ArgumentParser()
    parser.add_argument("--real-embed", action="store_true",
                        help="entropy via real-symmetric 128x128 embedding (benchmarked slower; fallback only)")
    parser.add_argument("--cupy-eig", action="store_true",
                        help="batched eigvalsh via cupy syevjBatched (28x faster than torch c128 path)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    scan = sub.add_parser("scan")
    scan.add_argument("--model", choices=["cluster", "tfim"], required=True)
    scan.add_argument("--n-seq", type=int, default=5000)
    scan.add_argument("--n-points", type=int, default=21)
    scan.add_argument("--realizations", type=int, default=1)
    scan.add_argument("--pack", type=int, default=1, help="realizations packed per GPU batch")
    scan.add_argument("--out", required=True)
    scan.set_defaults(func=cmd_scan)
    nmse = sub.add_parser("nmse")
    nmse.add_argument("--model", choices=["cluster", "tfim"], required=True)
    nmse.add_argument("--n-seq", type=int, default=500)
    nmse.add_argument("--n-points", type=int, default=21)
    nmse.add_argument("--realizations", type=int, default=1)
    nmse.add_argument("--chunk", type=int, default=50)
    nmse.add_argument("--out", required=True)
    nmse.set_defaults(func=cmd_nmse)
    args = parser.parse_args()
    REAL_EMBED = args.real_embed
    if args.cupy_eig:
        global _cupy, CUPY_EIG
        import cupy as _cupy_mod
        _cupy = _cupy_mod
        CUPY_EIG = True
    torch.set_grad_enabled(False)
    args.func(args)


if __name__ == "__main__":
    main()
