# Lessons Learned

Durable, forward-looking lessons from reproducing the CDHM interband-coherence
pumping paper. These are written as guidance for the next driven-lattice /
transport reproduction, not as a log of this case.

## Method lessons

1. **Measure the packet center in k-space, not real space.** During a pumping
   cycle the wave packet spreads ballistically (~2T sites) while its center moves
   only a few sites. The robust observable is the gauge-free k-space mean position
   `<x> = i integral dk sum_j phi_j* d_k phi_j + sum_j j |phi_j|^2` (spectral
   k-derivative by FFT). It equals sum_l l |<l|Psi>|^2 exactly and stays
   well-conditioned when the packet width far exceeds the displacement. Resolve
   phi(k) with Nk ~ 2T and confirm by convergence (T=6144 converges at Nk=12288).

2. **A piecewise-constant adiabatic protocol is a product of Floquet operators.**
   Because beta is held fixed for each driving period, one cycle is the ordered
   product of T one-period 3x3 operators. Using this structure turns the dynamics
   into a minutes-long laptop job and makes T=1024..6144 and a 61-point J-scan
   feasible.

3. **Split the propagator when only part of H is time-dependent.** With
   H = A(k) + c(t) V(beta) and only the diagonal V time-dependent, a Strang split
   precomputes exp(-i A dt) once per k (independent of beta and t), so each period
   is a few cheap batched matrix-vector products (~30x speedup over rebuilding U).

4. **Accumulate the dynamical phase on the exact discrete protocol.** The W(1)
   term in Eq. (8) carries exp(-i(Omega_n - Omega_m)) with Omega ~ 10^2 rad at
   T=1024, so Delta rho is intrinsically phase-sensitive and reproduces at
   feature level (correlation ~0.9), not pixel. Evaluate Omega_n(1) as the exact
   discrete sum sum_j omega_n(beta_j) rather than the large-T integral T E, and
   keep the phase convention Phi_{nm} = (gamma_n - gamma_m) - (Omega_n - Omega_m)
   consistent with the exp(-i omega) eigenphase convention used everywhere.

5. **Compute interband matrix elements from a single diagonalization.** For n != m,
   `<psi_n | d_beta psi_m> = <psi_n | d_beta U | psi_m> / (lam_m - lam_n)` (from
   d_beta of the eigen-equation and <psi_n| U = lam_n <psi_n| for unitary U). This
   avoids beta-gauge fixing; only the gauge-invariant combination
   C*_n C_m W_{nm} enters the physics.

6. **Gate the model with topological invariants before trusting dynamics.** The
   Fukui-Hatsugai-Suzuki Chern numbers are (2,-4,2) at J=K=3 and jump
   (4,-8,4) -> (-8,16,-8) across J=K ~ 5.14 (up to an overall orientation sign).
   The transition location and jump magnitude validate the Bloch and gauge
   conventions independently of any figure.

## What worked well

- Deriving and gating the physics first (Floquet spectrum, Chern numbers,
  k-reflection symmetry, undriven analytic limit) before writing figure code keeps
  convention choices cheap to verify.
- Cross-validating the analytic theory (Eq. 13) against the exact dynamics -- not
  just against the paper figure -- gives an internal, unit-independent correctness
  check (theory total 3.08 versus dynamics 3.10).

## Reusable checks and tools

- Gauge-free k-space mean-position estimator for any k-conserving lattice
  evolution (`code/src/observables.py`, `x_expectation`).
- Strang-split fast Floquet evolver for H = A(k) + c(t) V with only the diagonal
  part time-dependent (`code/src/observables.py`, `evolve_fast`).
- Fukui-Hatsugai-Suzuki plaquette Chern / Berry-flux on a (k, parameter) torus as a
  model-convention gate (`code/src/theory.py`, `berry_flux_strips`).
- A standalone consistency suite covering unitarity, the undriven limit,
  conservation, symmetry, Chern integers, evolver agreement, and the central
  theory-vs-dynamics claim (`code/scripts/qa_cdhm.py`).
