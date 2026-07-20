"""Quantum reservoir computing engine for arXiv:2607.02157.

Implements the paper's numerical protocol:
- reservoir Hamiltonians (disordered fully-connected TFIM; augmented cluster model),
- the thermalizing collisional CPTP map (Eq. 19),
- the binning estimator for conditional operational states (Methods Eqs. 20-21),
- Holevo capacities, coherence decomposition, QID, injection/relaxation work
  (Eqs. 8-15), multi-step capacities (S78-S80), and the ridge/NMSE readout (Eqs. 2-3).

Physics constants follow the paper: beta = 1, gamma0 = 0.1, dt = 1,
lambda = 0.05, B = 50 bins, eigenvalue truncation 1e-12.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations

import numpy as np

EIG_TRUNCATION = 1e-12

SIGMA = {
    "I": np.eye(2, dtype=np.complex128),
    "X": np.array([[0, 1], [1, 0]], dtype=np.complex128),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=np.complex128),
    "Z": np.array([[1, 0], [0, -1]], dtype=np.complex128),
}


def pauli_string(L: int, ops: dict[int, str]) -> np.ndarray:
    out = np.array([[1.0 + 0j]])
    for site in range(L):
        out = np.kron(out, SIGMA[ops.get(site, "I")])
    return out


def tfim_hamiltonian(L: int, J: float, rng: np.random.Generator) -> np.ndarray:
    """Fully connected disordered TFIM: sum_{i>j} J_ij Z_i Z_j + h sum_i X_i, h = 1."""
    H = np.zeros((2**L, 2**L), dtype=np.complex128)
    for i in range(L):
        for j in range(i):
            J_ij = rng.uniform(-J / 2.0, J / 2.0)
            H += J_ij * pauli_string(L, {i: "Z", j: "Z"})
    for i in range(L):
        H += pauli_string(L, {i: "X"})
    return H


def cluster_hamiltonian(L: int, alpha: float, J_zz: float = 0.1, pbc: bool = False) -> np.ndarray:
    """Augmented cluster model: -J_zz sum Z_i Z_{i+1} - h_x sum X_i + J_zxz sum Z_{i-1} X_i Z_{i+1}.

    J_zxz = (1 - J_zz) * alpha, h_x = (1 - J_zz) * (1 - alpha).

    Open chain (paper convention, resolved empirically): under PBC the CZ-duality
    maps H(alpha) -> H(1-alpha) exactly (X <-> ZXZ, ZZ and sum-Z invariant), which
    makes every capacity curve symmetric about alpha = 0.5 — our PBC scan confirmed
    this to machine precision, contradicting the paper's asymmetric Fig. 2 row.
    The OBC spectrum endpoints (width 10.83 at alpha=0 vs 7.24 at alpha=1, edge
    zero modes at alpha=1) match the paper's Fig. S1c; PBC does not.
    """
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


def drive_diagonal(L: int) -> np.ndarray:
    """Diagonal of H1 = sum_i sigma^z_i in the computational basis."""
    diag = np.zeros(2**L)
    for i in range(L):
        diag += np.real(np.diag(pauli_string(L, {i: "Z"})))
    return diag


@dataclass
class MapCache:
    """Propagator/Gibbs cache on a uniform s-grid.

    H(s) = H0 + s*lambda*diag(z). Caching s on a fine grid replaces one 2^L
    eigendecomposition per (sequence, step) with a lookup; the s-grid spacing
    (2/(n_grid-1)) times lambda bounds the Hamiltonian error (~2.5e-4 for
    n_grid=401), validated against the exact path by validate_cache().
    """

    s_grid: np.ndarray
    U: np.ndarray          # (n_grid, D, D)
    rho_eq: np.ndarray     # (n_grid, D, D)
    energies: np.ndarray   # (n_grid, D)
    basis: np.ndarray      # (n_grid, D, D) eigenvectors

    def index(self, s: np.ndarray) -> np.ndarray:
        n = len(self.s_grid)
        return np.clip(np.rint((s + 1.0) * (n - 1) / 2.0).astype(int), 0, n - 1)


def eig_map_pieces(H: np.ndarray, dt: float, beta: float):
    w, V = np.linalg.eigh(H)
    U = (V * np.exp(-1j * w * dt)) @ V.conj().T
    boltz = np.exp(-beta * (w - w.min()))
    boltz /= boltz.sum()
    rho_eq = (V * boltz) @ V.conj().T
    return U, rho_eq, w, V


def build_map_cache(H0: np.ndarray, lam: float, dt: float, beta: float, n_grid: int = 401) -> MapCache:
    D = H0.shape[0]
    z = drive_diagonal(int(np.log2(D)))
    s_grid = np.linspace(-1.0, 1.0, n_grid)
    U = np.empty((n_grid, D, D), dtype=np.complex128)
    rho_eq = np.empty((n_grid, D, D), dtype=np.complex128)
    energies = np.empty((n_grid, D))
    basis = np.empty((n_grid, D, D), dtype=np.complex128)
    for k, s in enumerate(s_grid):
        H = H0 + (s * lam) * np.diag(z)
        U[k], rho_eq[k], energies[k], basis[k] = eig_map_pieces(H, dt, beta)
    return MapCache(s_grid=s_grid, U=U, rho_eq=rho_eq, energies=energies, basis=basis)


def collisional_step(rho: np.ndarray, s: np.ndarray, cache: MapCache, P_th: float) -> np.ndarray:
    """Batched Eq. (19): rho' = (1-P_th) U rho U^dag + P_th rho_eq(s)."""
    idx = cache.index(s)
    U = cache.U[idx]
    evolved = U @ rho @ U.conj().transpose(0, 2, 1)
    return (1.0 - P_th) * evolved + P_th * cache.rho_eq[idx]


def von_neumann_entropy(rho: np.ndarray) -> np.ndarray:
    """Batched entropy with the paper's 1e-12 eigenvalue truncation (natural log)."""
    w = np.linalg.eigvalsh(rho)
    w = np.where(w > EIG_TRUNCATION, w, 1.0)
    return -np.sum(np.real(w) * np.log(np.real(w)), axis=-1)


def shannon_entropy(p: np.ndarray) -> np.ndarray:
    q = np.where(p > EIG_TRUNCATION, p, 1.0)
    return -np.sum(np.real(q) * np.log(np.real(q)), axis=-1)


def bin_indices(s: np.ndarray, n_bins: int = 50) -> np.ndarray:
    return np.clip(((s + 1.0) * 0.5 * n_bins).astype(int), 0, n_bins - 1)


def binned_states(rho: np.ndarray, s: np.ndarray, n_bins: int = 50):
    """Conditional states by binning (Methods Eq. 20): returns (P_b, rho_b, s_mean_b)."""
    idx = bin_indices(s, n_bins)
    counts = np.bincount(idx, minlength=n_bins)
    occupied = np.nonzero(counts)[0]
    D = rho.shape[-1]
    rho_flat = rho.reshape(len(s), -1)
    sums = np.zeros((n_bins, D * D), dtype=np.complex128)
    np.add.at(sums, idx, rho_flat)
    s_sums = np.bincount(idx, weights=s, minlength=n_bins)
    P_b = counts[occupied] / len(s)
    rho_b = (sums[occupied] / counts[occupied, None]).reshape(len(occupied), D, D)
    s_mean = s_sums[occupied] / counts[occupied]
    return P_b, rho_b, s_mean


def holevo_capacity(rho_bar: np.ndarray, P_b: np.ndarray, rho_b: np.ndarray) -> float:
    return float(von_neumann_entropy(rho_bar[None])[0] - np.sum(P_b * von_neumann_entropy(rho_b)))


def coherence_terms(rho_bar: np.ndarray, P_b: np.ndarray, rho_b: np.ndarray):
    """Classical MI and ensemble coherence (Eq. 11) in the computational basis."""
    diag_b = np.real(np.diagonal(rho_b, axis1=-2, axis2=-1))
    diag_bar = np.real(np.diag(rho_bar))
    I_cl = float(shannon_entropy(diag_bar) - np.sum(P_b * shannon_entropy(diag_b)))
    C_b = shannon_entropy(diag_b) - von_neumann_entropy(rho_b)
    C_bar = float(shannon_entropy(diag_bar) - von_neumann_entropy(rho_bar[None])[0])
    C_ens = float(np.sum(P_b * C_b) - C_bar)
    C_cond = float(np.sum(P_b * C_b))
    return I_cl, C_ens, C_cond


def ensemble_energy(rho_b: np.ndarray, P_b: np.ndarray, s_mean: np.ndarray, H0: np.ndarray, lam: float, z: np.ndarray) -> float:
    """sum_b P_b Tr(rho_b H(s_b)) with the bin-representative Hamiltonian."""
    e0 = np.real(np.einsum("bij,ji->b", rho_b, H0))
    ez = np.real(np.einsum("bii,i->b", rho_b, z))
    return float(np.sum(P_b * (e0 + lam * s_mean * ez)))


def relative_entropy(rho: np.ndarray, sigma: np.ndarray) -> float:
    w_r, V_r = np.linalg.eigh(rho)
    w_s, V_s = np.linalg.eigh(sigma)
    w_r = np.clip(np.real(w_r), 0.0, None)
    log_sigma = (V_s * np.log(np.clip(np.real(w_s), EIG_TRUNCATION, None))) @ V_s.conj().T
    w_r_safe = np.where(w_r > EIG_TRUNCATION, w_r, 1.0)
    term1 = float(np.sum(w_r * np.log(w_r_safe)))
    term2 = float(np.real(np.trace(rho @ log_sigma)))
    return term1 - term2


@dataclass
class StepMetrics:
    chi_m: float
    chi_p: float
    chi_d: float
    I_m: float
    I_p: float
    C_m: float
    C_p: float
    beta_W_irr_inj: float
    beta_W_relax: float
    chi_m_tau: dict = field(default_factory=dict)
    chi_p_h: dict = field(default_factory=dict)


def step_metrics(
    rho_next: np.ndarray,
    s_hist: np.ndarray,
    n: int,
    cache: MapCache,
    H0: np.ndarray,
    lam: float,
    beta: float,
    P_th: float,
    z: np.ndarray,
    n_bins: int = 50,
    taus: tuple[int, ...] = (),
    hs: tuple[int, ...] = (),
) -> StepMetrics:
    """All per-step observables at time t_{n+1} from the batch of states rho_next.

    rho_next: (n_seq, D, D) states after processing input s_n (i.e. rho_{t_{n+1}}).
    s_hist: (n_seq, N) full input sequences; memory bins use s_hist[:, n],
    predictive bins use s_hist[:, n+1].
    """
    rho_bar = rho_next.mean(axis=0)
    s_n = s_hist[:, n]
    s_np1 = s_hist[:, n + 1]

    S_bar = float(von_neumann_entropy(rho_bar[None])[0])
    H_bar = float(shannon_entropy(np.real(np.diag(rho_bar))))
    C_bar = H_bar - S_bar

    def binning_metrics(s_key: np.ndarray):
        """One eigendecomposition pass per binning: (P, rho, s_mean, S_b, chi, I, C_ens)."""
        P_b, rho_b, s_mean = binned_states(rho_next, s_key, n_bins)
        S_b = von_neumann_entropy(rho_b)
        H_b = shannon_entropy(np.real(np.diagonal(rho_b, axis1=-2, axis2=-1)))
        chi = float(S_bar - np.sum(P_b * S_b))
        I_cl = float(H_bar - np.sum(P_b * H_b))
        C_ens = float(np.sum(P_b * (H_b - S_b)) - C_bar)
        return P_b, rho_b, s_mean, S_b, chi, I_cl, C_ens

    P_m, rho_m, sm_mean, S_m_bins, chi_m, I_m, C_m = binning_metrics(s_n)
    P_p, rho_p, sp_mean, S_p_bins, chi_p, I_p, C_p = binning_metrics(s_np1)

    # Injection work (S62-S64): energies with bin-representative Hamiltonians;
    # beta*W_irr_inj = chi_d holds exactly with this bookkeeping (Eq. 13).
    E_p = ensemble_energy(rho_p, P_p, sp_mean, H0, lam, z)
    E_m = ensemble_energy(rho_m, P_m, sm_mean, H0, lam, z)
    S_p = float(np.sum(P_p * S_p_bins))
    S_m = float(np.sum(P_m * S_m_bins))
    W = E_p - E_m
    delta_F = (E_p - S_p / beta) - (E_m - S_m / beta)
    beta_W_irr_inj = beta * (W - delta_F)

    # Relaxation dissipation (S67-S68): predictive states relax under H(s_{n+1}).
    # Against the invariant Gibbs state, S(rho||rho_eq) = -S(rho) + beta<H> + lnZ,
    # so the lnZ terms cancel and no extra diagonalization of rho_eq is needed:
    # beta*W_relax = sum_b P_b [ (S(rho') - S(rho)) + beta(<H>_rho - <H>_rho') ].
    idx = cache.index(sp_mean)
    U = cache.U[idx]
    rho_relaxed = (1.0 - P_th) * (U @ rho_p @ U.conj().transpose(0, 2, 1)) + P_th * cache.rho_eq[idx]
    H_bins = H0[None] + (lam * sp_mean)[:, None, None] * np.diag(z)[None]
    E_bins = np.real(np.einsum("bij,bji->b", rho_p, H_bins))
    E_bins_relaxed = np.real(np.einsum("bij,bji->b", rho_relaxed, H_bins))
    S_bins_relaxed = von_neumann_entropy(rho_relaxed)
    beta_W_relax = float(np.sum(P_p * ((S_bins_relaxed - S_p_bins) + beta * (E_bins - E_bins_relaxed))))

    chi_m_tau = {}
    for tau in taus:
        if n - tau >= 0:
            chi_m_tau[tau] = binning_metrics(s_hist[:, n - tau])[4]
    chi_p_h = {}
    for h in hs:
        if n + h < s_hist.shape[1]:
            chi_p_h[h] = binning_metrics(s_hist[:, n + h])[4]

    return StepMetrics(
        chi_m=chi_m, chi_p=chi_p, chi_d=chi_m - chi_p,
        I_m=I_m, I_p=I_p, C_m=C_m, C_p=C_p,
        beta_W_irr_inj=beta_W_irr_inj, beta_W_relax=beta_W_relax,
        chi_m_tau=chi_m_tau, chi_p_h=chi_p_h,
    )


def simulate_ensemble(
    H0: np.ndarray,
    sequences: np.ndarray,
    *,
    lam: float = 0.05,
    beta: float = 1.0,
    gamma0: float = 0.1,
    dt: float = 1.0,
    n_wash: int = 500,
    n_eval: int = 2000,
    n_bins: int = 50,
    taus: tuple[int, ...] = (),
    hs: tuple[int, ...] = (),
    cache_grid: int = 401,
) -> dict:
    """Evolve an ensemble of sequences and accumulate the paper's totals.

    Returns totals summed over the evaluation window (paper convention for
    chi_tot etc.), plus the per-step identity residual max|beta*W_irr_inj - chi_d|.
    """
    D = H0.shape[0]
    L = int(np.log2(D))
    z = drive_diagonal(L)
    P_th = 1.0 - np.exp(-gamma0 * dt)
    cache = build_map_cache(H0, lam, dt, beta, cache_grid)

    n_seq, n_total = sequences.shape
    max_h = max(hs) if hs else 0
    if n_wash + n_eval + max_h + 1 > n_total:
        raise ValueError("sequences too short for wash+eval window")

    _, rho0, _, _ = eig_map_pieces(H0, dt, beta)
    rho = np.broadcast_to(rho0, (n_seq, D, D)).copy()

    totals = {k: 0.0 for k in [
        "chi_m_tot", "chi_p_tot", "chi_d_tot", "I_m_tot", "I_p_tot",
        "C_m_tot", "C_p_tot", "beta_W_irr_tot", "beta_W_relax_tot",
    ]}
    totals.update({f"chi_m_tau{t}_tot": 0.0 for t in taus})
    totals.update({f"chi_p_h{h}_tot": 0.0 for h in hs})
    identity_residual = 0.0

    for n in range(n_wash + n_eval):
        rho = collisional_step(rho, sequences[:, n], cache, P_th)
        if n < n_wash:
            continue
        m = step_metrics(rho, sequences, n, cache, H0, lam, beta, P_th, z,
                         n_bins=n_bins, taus=taus, hs=hs)
        totals["chi_m_tot"] += m.chi_m
        totals["chi_p_tot"] += m.chi_p
        totals["chi_d_tot"] += m.chi_d
        totals["I_m_tot"] += m.I_m
        totals["I_p_tot"] += m.I_p
        totals["C_m_tot"] += m.C_m
        totals["C_p_tot"] += m.C_p
        totals["beta_W_irr_tot"] += m.beta_W_irr_inj + m.beta_W_relax
        totals["beta_W_relax_tot"] += m.beta_W_relax
        for t, v in m.chi_m_tau.items():
            totals[f"chi_m_tau{t}_tot"] += v
        for h, v in m.chi_p_h.items():
            totals[f"chi_p_h{h}_tot"] += v
        identity_residual = max(identity_residual, abs(m.beta_W_irr_inj - m.chi_d))

    totals["identity_residual_max"] = identity_residual
    totals["n_eval"] = n_eval
    totals["n_seq"] = n_seq
    return totals


def local_pauli_observables(L: int, max_weight: int = 2) -> np.ndarray:
    """Stack of 1- and 2-body Pauli strings (reduced readout basis for local runs)."""
    ops = []
    for i in range(L):
        for a in "XYZ":
            ops.append(pauli_string(L, {i: a}))
    if max_weight >= 2:
        for i, j in combinations(range(L), 2):
            for a in "XYZ":
                for b in "XYZ":
                    ops.append(pauli_string(L, {i: a, j: b}))
    return np.stack(ops)


def nmse_readout(
    H0: np.ndarray,
    sequences: np.ndarray,
    *,
    horizon: int = 1,
    lam: float = 0.05,
    beta: float = 1.0,
    gamma0: float = 0.1,
    dt: float = 1.0,
    n_wash: int = 500,
    n_train: int = 2000,
    n_test: int = 2000,
    eta: float = 1e-5,
    observables: np.ndarray | None = None,
    cache_grid: int = 401,
) -> float:
    """Ridge readout NMSE (Eqs. 2-3), target s_{n+horizon}, averaged over sequences."""
    D = H0.shape[0]
    L = int(np.log2(D))
    if observables is None:
        observables = local_pauli_observables(L)
    P_th = 1.0 - np.exp(-gamma0 * dt)
    cache = build_map_cache(H0, lam, dt, beta, cache_grid)
    _, rho0, _, _ = eig_map_pieces(H0, dt, beta)

    n_seq, n_total = sequences.shape
    needed = n_wash + n_train + n_test + horizon
    if needed > n_total:
        raise ValueError("sequences too short for NMSE protocol")

    rho = np.broadcast_to(rho0, (n_seq, D, D)).copy()
    n_obs = observables.shape[0]
    feats = np.empty((n_seq, n_train + n_test, n_obs))
    for n in range(n_wash + n_train + n_test):
        rho = collisional_step(rho, sequences[:, n], cache, P_th)
        if n >= n_wash:
            feats[:, n - n_wash] = np.real(np.einsum("kab,nba->nk", observables, rho))

    nmse_values = []
    for q in range(n_seq):
        X = np.concatenate([feats[q], np.ones((feats.shape[1], 1))], axis=1)
        X_train, X_test = X[:n_train], X[n_train:]
        targets = sequences[q, n_wash + horizon: n_wash + n_train + n_test + horizon]
        y_train, y_test = targets[:n_train], targets[n_train:]
        gram = X_train.T @ X_train + eta * np.eye(X.shape[1])
        w = np.linalg.solve(gram, X_train.T @ y_train)
        y_pred = X_test @ w
        nmse_values.append(float(np.sum((y_pred - y_test) ** 2) / np.sum(y_test**2)))
    return float(np.mean(nmse_values))
