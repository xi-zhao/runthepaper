# Derivation: fixed-sector Bose–Hubbard quantum walks

## 1. Hamiltonian and units

The twelve-site processor is represented by an open Bose–Hubbard chain,

\[
H=\sum_{j=1}^{11}J_j(a_j^\dagger a_{j+1}+a_{j+1}^\dagger a_j)
 +\frac{1}{2}\sum_{j=1}^{12}U_j n_j(n_j-1)+\sum_{j=1}^{12}h_jn_j.
\]

The published coupling and anharmonicity parameters are quoted as ordinary
frequencies in MHz. The propagator uses radians per nanosecond, so every
frequency is converted with `2*pi*1e-3`. This conversion is part of the domain
model rather than a plotting adjustment.

## 2. Conserved particle-number sectors

Because `[H, sum_j n_j] = 0`, the one-photon calculation needs only 12 basis
states. The two-photon bosonic basis contains

\[
\binom{12+2-1}{2}=78
\]

states, while the hard-core sector contains `C(12,2)=66` states. In an
occupation basis, moving one boson from site `j` to `j+1` contributes

\[
J_j\sqrt{n_j(n_{j+1}+1)}.
\]

This fixed-sector construction in `code/src/quantum_walk.py` is the main reason
the complete case is inexpensive and deterministic.

## 3. Exact propagation

For a time-independent calibrated Hamiltonian,

\[
|\psi(t)\rangle = V\,\mathrm{diag}(e^{-iE_kt})V^\dagger|\psi(0)\rangle,
\]

where `E_k` and `V` come from a Hermitian eigendecomposition. One
diagonalization therefore serves every requested time point. The implementation
checks state norm and total density throughout the trajectory.

## 4. Observables

The site density is `p_j=<n_j>`. In the one-particle sector the reduced state of
one site has probabilities `(1-p_j,p_j)`, hence

\[
S_j=-(1-p_j)\ln(1-p_j)-p_j\ln p_j.
\]

The connected spin correlation and one-particle concurrence are

\[
C^z_{ij}=\langle\sigma_i^z\sigma_j^z\rangle
-\langle\sigma_i^z\rangle\langle\sigma_j^z\rangle,
\qquad
\mathcal C_{ij}=2|\psi_i\psi_j^*|.
\]

For two particles, the normally ordered correlator is

\[
G_{ij}=\langle a_i^\dagger a_j^\dagger a_i a_j\rangle.
\]

Its sum is `N(N-1)=2`, providing a global invariant independent of the figure
style. The double-occupancy probability is the weight of basis states with two
bosons on the same site.

## 5. Fermionization test

The strong attractive interaction, free-boson control (`U=0`), and hard-core
limit all use the same Hamiltonian builder. The normalized matrix distance
between their two-particle correlators tests the paper's central qualitative
claim: the calibrated strong-interaction pattern is much closer to the
hard-core pattern than to the free-boson pattern.
