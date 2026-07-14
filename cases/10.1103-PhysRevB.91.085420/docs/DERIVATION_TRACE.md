# Derivation Trace

Human-readable walk-through of the derivation behind the four reproduced
figures. The equation-level view is in `DERIVATION.md`.

## 0. Physical question

For a periodically driven closed system taken adiabatically around a pumping
cycle (beta: 0 -> 2 pi over duration T tau), what is the displacement Delta<x> of
the wave-packet center when the initial state is a general superposition across
Floquet bands (not a single Floquet band)?

## 1. Floquet setup (Eqs. 1-3)

- One-period evolution operator U(beta); Floquet eigenstates psi_{n,k}(beta) with
  eigenphases omega_{n,k}(beta): U(beta) psi_{n,k} = exp(-i omega_{n,k}) psi_{n,k}
  (Eq. 1).
- Parallel-transport gauge `<psi | d psi/d beta> = 0`, so psi(2 pi) = exp(-i gamma) psi(0),
  gamma = Berry phase.
- Accumulated dynamical phase Omega_{n,k}(s_j) = sum_{j' <= j} omega_{n,k}[beta(s_j')]
  (Eq. 2).
- State expansion Psi(s) = sqrt(a/2 pi) integral dk sum_n C_{n,k}(s) exp(-i Omega_{n,k}(s)) psi_{n,k}[beta(s)]
  (Eq. 3); rho_{n,k}(0) = |C_{n,k}(0)|^2 are the initial band populations.

## 2. First-order adiabatic perturbation theory (Eqs. 4-8, App. 1)

- Projecting Psi(s + ds) = U Psi(s) gives the transition equation for dC_n/ds
  (Eq. 4 / A4).
- Integrating by parts and keeping O(1/T):
  C_{n,k}(1) = C_{n,k}(0) + (1/T) sum_{m != n} C_{m,k}(0) times the boundary term of
  the kernel W_{nm,k}(s) (Eqs. 5-6 / A11).
- Population change:
  Delta rho_{n,k} = |C_{n,k}(1)|^2 - rho_{n,k}(0)
  = (2/T) Re[ sum_{m != n} C*_n(0) C_m(0) (W_{nm,k} evaluated 0..1) ] (Eq. 8).
- Key scaling: for a single-band initial state the cross term C*_n C_m vanishes so
  Delta rho ~ 1/T^2; for a general multi-band initial state the interband-coherence
  (IBC) cross term is nonzero so Delta rho ~ 1/T. This 1/T versus 1/T^2 split is
  what makes the correction survive.

Numerical realisation of W(0): using U psi_m = lam_m psi_m and <psi_n| U = lam_n <psi_n|
(U unitary, hence normal with orthonormal eigenvectors),
`<psi_n | d_beta psi_m> = <psi_n | d_beta U | psi_m> / (lam_m - lam_n)` for n != m.
This avoids any beta-gauge fixing; the physical combination C*_n C_m W_{nm} is
gauge-invariant.

## 3. Wave-packet displacement (Eqs. 9-13, App. 2)

- The position operator in the Floquet-Bloch basis (App. A12-A19) gives <x> as an
  intraband-Berry-connection plus amplitude-derivative integral; the interband
  ("third") term A19/A20 is rapidly oscillating and drops out.
- Subtracting initial from final (A22 versus A25):
  Delta<x> = sum_n integral dk [ d gamma_{n,k}/dk + d Omega_{n,k}(1)/dk ] |C_{n,k}(1)|^2
  (Eq. 9 / A26).
- Of the resulting terms: the d gamma/dk times Delta rho term vanishes (gamma is
  T-independent, Delta rho ~ 1/T); the d Omega(1)/dk times rho(0) term is odd in k
  under k-reflection symmetry and integrates to zero. The surviving pieces are the
  weighted Berry-curvature integral
  sum_n integral dk (d gamma/dk) rho_{n,k}(0) = sum_n double-integral B_n(beta,k) rho_{n,k}(0) d beta dk
  (Eq. 11), plus the IBC correction from d Omega(1)/dk times Delta rho. Because
  Omega(1) = T E (Eq. 12) is proportional to T while Delta rho ~ 1/T, their product
  is T-independent and non-vanishing.
- Final result (Eq. 13):
  Delta<x> = sum_n integral dk integral d beta B_n(beta,k) rho_{n,k}(0)
           - 2 sum_{m != n} integral dk Re[ C*_n(0) C_m(0) (dE_{n,k}/dk) W_{nm,k}(0) ].
  Both terms are independent of T. Only W(0) survives the k-integration (the
  W(1)-part self-averages away), which is why Eq. 13 needs only static beta=0
  quantities.

## 4. Unit / prefactor bookkeeping

<x> is computed exactly from the dynamics in atomic-spacing units (x = 3n + j). For
a filled single band the Berry term reduces to the Thouless result Delta x = a C_n
with a = N = 3 (one Wannier center per pumped charge per cell). This fixes the
overall a/(2 pi) prefactor carried by both terms of Eq. 13, and it is independently
confirmed by the exact dynamics (theory total 3.08 versus dynamics 3.10 at
J = K = 4). The (k, beta)-torus orientation is a gauge choice; the physical
displacement is reported with the paper's positive sign, aligned to the dynamics.

## 5. What the model calculation shows (Sec. IV, Figs. 1-4)

- Fig. 1: Floquet spectrum and initial populations for J = K = 3.
- Fig. 2: Eq. 8 reproduces the actual one-cycle Delta rho (feature level).
- Fig. 3: Delta<x> is T-independent; the Berry-only term (4.32) is far from the
  true displacement (3.10); the IBC correction (-1.24) closes the gap.
- Fig. 4: scanning J = K across the Floquet-Chern transition (~5.14), the corrected
  theory tracks the actual displacement and both jump at the transition, while the
  Berry-only term does not follow the actual result -- a topological-transition
  probe from a trivial site-0 initial state.
