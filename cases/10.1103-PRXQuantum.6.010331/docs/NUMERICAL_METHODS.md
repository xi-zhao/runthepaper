# Numerical Methods

## Core Reproduction Model

The clean core object is a **physical target** with three explicit inputs:
`equations + parameters + solver`. It emits a numerical table first and a plot
second. Source-figure pixels are outside this object and may enter only the
post-computation comparison renderer.

There are three numerical routes:

1. analytic evaluation (`T001-T004`, `T006-T008`), where published formulas or
   anchor-constrained scaling laws are sampled directly;
2. independent two-atom Hamiltonian propagation (`T005` and diagnostic D001);
3. independent seven-site state-vector/tangent propagation (`T009`).

Missing PSDs, pulse metadata, geometry or calibration arrays remain explicit
missing inputs. The implementation does not estimate them from source curves.

## Paper-Parameter Card: T001 / Fig. 15

| Field | Paper value | Generated value | Match |
| --- | --- | --- | --- |
| Response form | Appendix-L Gaussian pair for frequency noise; logistic/tanh form for intensity noise | Same | exact |
| Coefficients | Four six-parameter coefficient sets | Same printed coefficients | exact |
| Metrics | Haar and symmetric-Haar | Both | exact |
| Noise channels | Frequency and relative intensity | Both | exact |
| Plot range | `x=2*pi*f/Omega` from 0 to 3 | 0 to 3 inclusive | exact |
| Evaluation range | Must cover Fig. 6(a) rescaling | 0 to 5, no extrapolation at 15 MHz / 7.7 MHz | sufficient |
| Frequency grid | Not reported | 1001 deterministic points | implementation tolerance |

- Parameter match: `paper_exact`.
- Artifact stage: `final_reproduction`.
- Generated-data provenance: `analytic_reference`.
- Formula dependencies: `EQ005`, `EQ006`.
- Acceptance: nonnegative response, published `I_I(1.5 MHz)` sanity value at
  `Omega/(2*pi)=3 MHz`, and the second frequency-response peak in `x=1.0-1.4`.
- Known residual: Appendix L is explicitly approximate and its intensity form
  omits the small side peaks visible in Fig. 15(b) near `x=1.5` and `x=2.5`.

## Method Card NUM002: Fig. 6(a) Scaling

- Apply `I_nu(f;Omega)=Omega^-2 g_nu(2*pi*f/Omega)` and
  `I_I(f;Omega)=g_I(2*pi*f/Omega)`.
- Use paper Rabi frequencies `Omega/(2*pi)=3.0 MHz` and `7.7 MHz`.
- Evaluate `f=0-15 MHz`; frequency response is in `MHz^-2`, intensity response
  is dimensionless.
- Collapse both dimensional curves back to the universal functions. The
  measured maximum round-trip error is `1.42e-14`.
- This verifies the scaling law and dominant envelope, while inheriting the
  Appendix-L intensity fine-structure limitation.

## Diagnostic Method D001: Direct Hamiltonian Integration

This lane tests the FRT machinery without making a paper-exact claim.

- Hilbert space: two three-level atoms in basis `{0,1,r}`, with `|rr>` removed
  for infinite blockade (dimension 8).
- Pulse: generic sinusoidal parameters printed by the cited Evered source.
- Evolution: midpoint piecewise-constant Hamiltonian and matrix exponential.
- Response: Appendix Eq. (G7), factorized through the Fourier-transformed
  Heisenberg operator.
- Grid: 4001 time samples and 1001 normalized-frequency samples; convergence is
  checked against 2001 time samples.
- Result: unitarity error `3.05e-13`, CZ phase error `1.33e-4 rad`, maximum
  computational return leakage `2.33e-5`, and convergence NRMSE below `5e-7`.
- Limitation: response NRMSE against Appendix L is `0.084-0.411`, proving that
  the cited generic pulse is not enough to identify the paper's Fig. 15
trajectory. Therefore this lane is `exploratory / reconstructed / partial`.

## Formula-Theory Targets T003-T008

- `T003`: evaluates `epsilon_j = integral S_j I_j df` in the quasistatic/public
  limits, preserving unpublished frequency/Doppler variances as `None` rather
  than inventing values.
- `T004`: solves power-law exponents from the two Rabi/spacing anchors printed
  for `n=61` and `n=44`.
- `T005`: constructs piecewise or continuously phased control segments and
  propagates the common 8D infinite-blockade Hamiltonian. Acceptance uses
  Hermiticity, unitarity, computational return, leakage and controlled phase.
- `T006`: samples the exact finite-time Appendix-H sinc-squared filter.
- `T007`: samples a disclosed single-pole cavity **power** transfer; this is a
  convention reconstruction, not a claim about an unreleased PSD.
- `T008`: evaluates the Appendix-D phase-flip polynomials and first-order SSB
  slope/cancellation over the printed ranges.

## Many-Body Method T009

- Hilbert space: seven two-level sites, dimension `2^7=128`.
- Hamiltonian: printed transverse-field/detuning/density-interaction form.
- Quench: exact spectral decomposition.
- Quasi-adiabatic path: unitary diagonal/X split-step propagation plus midpoint
  first-order complex tangent equations for cosine and sine perturbations.
- Public parameters: `N=7`, `Omega/(2*pi)=7.7 MHz`, `T=6 us`, detuning endpoints
  `±10 Omega`.
- Explicit reconstruction parameters: `V_nn/Omega=20`, tangent shape `1.35`,
  sin-squared Rabi ramp and 2400 time steps.
- Verification: maximum norm error `6.35e-14`; half-grid response NRMSE
  `0.0310` (frequency) and `0.0455` (intensity); final total Z2 probability
  `0.9999853`.

## Efficiency And Reuse

The response solvers replace an explicit `O(N_f*N_t^2*d^3)` double integral
with one trajectory and Fourier-transformed/tangent operators. The two-atom
route scales as `O(N_t*d^3 + N_f*N_t*d^2)`; the seven-site route reuses diagonal
and global-X split operators to avoid dense exponentiation at every time step.
All formulas and physical parameters remain in dedicated domain modules; plot
layout never changes the computed arrays.
