# Derivation Trace

Every implemented equation maps back to a source equation. Machine-readable cards
are in `EQUATION_CARDS.json`; the reader-facing rendering is `DERIVATION.md`
(generated — do not hand-edit). Formula gate: `outputs/checks/formula_verification.json`.

> **Pedagogical, self-contained walk-through (first-year-grad level, in Chinese):**
> `DERIVATION_WALKTHROUGH.zh-CN.md` — derives everything behind Fig. 2 from the
> definition of the R-matrix through the exclusion statistics `d_n`, the
> thermodynamics `<n>=x z'/z`, and the 1D-model ED validation, step by step.

## Formula Lane Rule

Every formula used by numerical code has a card, a derivation here, a formula gate
result, and a code pointer. All three cards below are `verified` with an open
numeric gate.

## EQ001 — Single-mode partition function / Hilbert series

- Source: Eq. `single_mode_Z`, Table 1, SI "Calculation of exclusion statistics".
- Latex: `z_R(x) = Tr[e^{-beta eps n}] = sum_{n>=0} d_n x^n`, `x = e^{-beta eps}`.
- Role: defines the generalized exclusion statistics `{d_n}` (Fig. 2 left) and
  is the generating function for the thermodynamics (Fig. 2 right).
- Derived from: the definition of `d_n` = dim of the n-particle single-mode space,
  solved for each R-matrix via the SI's `V_n_basis` condition.
- Steps:
  - `d_0=1`, `d_1=m` for all R-matrices (no constraint at `n=0,1`).
  - Ex.1/Ex.2: antisymmetry under neighbour exchange ⇒ `d_n = C(m,n)` ⇒ `z=(1+x)^m`.
  - Ex.3 (`R=-delta_ac delta_bd`): `Psi=-Psi` for `n>=2` ⇒ `d_{n>=2}=0` ⇒ `z=1+m x`.
  - Ex.4: `n=2` gives a unique `Psi=lambda` (uses `Tr(lambda xi^T)=2`) ⇒ `d_2=1`;
    `n>=3` has no solution ⇒ `z=1+m x+x^2`.
  - Fermion (`m=1`, `-`): `z=1+x`. Boson (`+`): `z=1/(1-x)` (`d_n=1`).
- Numerical form: `d_n` are the Taylor coefficients of `z_R(x)`; coded directly.
- Code pointer: `src/paraparticles.py::Species.degeneracies`, `species_table`.
- Status: verified. Independently confirmed by ED (EQ003): the Ex.3 chain's
  single-mode factor is exactly `(1+m x)`.
- Open questions: text says `m=5`, figure legend says `m=2/3` (see FIGURE_CLASSIFICATION.md).

## EQ002 — Free-paraparticle thermal occupation

- Source: Eq. `n_k_expectation`.
- Latex: `<n_k>_beta = z'_R(x) x / z_R(x)`, `x = e^{-beta eps_k}`.
- Role: the observable plotted in Fig. 2 (right).
- Derived from: `<n> = Tr[n e^{-beta eps n}]/Tr[e^{-beta eps n}]
  = sum_n n d_n x^n / sum_n d_n x^n = x d/dx ln z_R(x) = x z'_R(x)/z_R(x)`.
  This independent derivation reproduces the paper's formula exactly.
- Numerical form: evaluate `sum_n n d_n x^n / sum_n d_n x^n` (finite polynomials
  for Ex.*; closed form `x/(1-x)` for the boson tower).
- Code pointer: `src/paraparticles.py::Species.occupation`.
- Status: verified. Limits at `x=1` and `x->inf` checked in `outputs/checks/fig2.json`.

## EQ003 — 1D solvable spin model = free paraparticles

- Source: Eq. `Hamil1Dspin`, SI "Details on the 1D spin model and the MPO JWT".
- Latex: `H = sum_{i,a} J_i(x^+_{i,a} y^-_{i+1,a}+h.c.) - sum_{i,a} mu_i y^+_{i,a}y^-_{i,a}`.
- Role: a physical (local, Hermitian) spin model whose quasiparticles are the
  Ex.3 paraparticles; validates that `z_R=1+m x` describes an actual system.
- Derived from: the generalized Jordan-Wigner transformation maps the on-site
  ladder operators to paraparticle operators, giving `H=sum_{ij} h_{ij} e_{ij}`,
  `h` tridiagonal (`h_{i,i+1}=h_{i+1,i}=J_i`, `h_{ii}=-mu_i`). Being an algebra
  isomorphism, it preserves the spectrum, so the many-body levels are
  `sum_{k in S} eps_k` with multiplicity `m^{|S|}` (`eps_k=eig(h)`).
- Numerical form: brute-force build `H` on `(m+1)^N` states, diagonalize, and
  compare to the free-paraparticle prediction; also `[H, n_hat]=0`.
- Code pointer: `src/spin_model_1d.py`, `scripts/run_ed_validation.py`.
- Status: verified. Max spectrum deviation ~1e-14 for N=4,5 (m=2), N=4 (m=3).
