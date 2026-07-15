# Lessons Learned

## Core lesson

A gate protocol name is not a parameter identity. Multiple control trajectories
can all close to an excellent CZ gate while producing substantially different
frequency-domain noise responses. A scalar fidelity check is therefore necessary
but not sufficient for a response-theory reproduction.

## What worked

- Building equation and parameter provenance before the solver kept all nine
  targets tied to a physical model.
- Treating `equations + parameters + solver` as the core target object produced
  data first and figures second, making pixel-derived computation structurally
  unnecessary.
- Separating paper-exact analytic targets from reconstructed Hamiltonian
  diagnostics prevented a valid but unidentified pulse from being overclaimed.
- Fourier factorization and tangent propagation made the response calculations
  tractable without changing the underlying equations.

## Reusable checks

- Require target-specific waveform evidence before calling an optimized-control
  trajectory `paper_exact`.
- Test gate closure, unitarity and leakage together with response-curve features.
- Run grid-convergence checks before interpreting a disagreement as a physical
  model failure.
- Carry provenance in every generated table and keep missing experimental arrays
  as explicit missing inputs.

## Remaining boundary

The paper does not release every PSD, calibration array, geometry/ramp detail or
target-specific waveform required to regenerate every exact raster feature. The
public package reproduces everything closed by printed formulas and public
parameters, and labels the remaining reconstructions and blockers directly.
