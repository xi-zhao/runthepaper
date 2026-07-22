# Numerical methods

## Core boundary

`code/src/` owns the physical objects and invariants. The executable in
`code/scripts/` orchestrates targets, writes CSV data first, then renders PNG
figures and writes JSON checks. Paper reference pixels never enter a numerical
model or a generated curve.

## Targets

- **Single-ion gate:** closed-form branch displacements and Magnus phases on
  801 time points; the density matrix is checked for trace, positivity, exact
  motion closure, CZ phase, and concurrence checkpoints.
- **Chain scaling:** integer `N=1..100`; the disclosed duration contract and
  decay law are evaluated explicitly. Intermediate optimized durations remain
  reconstructed because the author vector is unavailable.
- **Architecture scaling:** 241 logarithmic distances and operation counts.
  The hybrid link and photon rate use reported values; the QCCD affine model is
  reconstructed. The memory curve follows `2 pT / Nops`.
- **Ten-ion closure:** equilibrium positions minimize the dimensionless
  Coulomb-plus-harmonic potential. The analytic Hessian gives normal modes.
  Twenty-five positive segment durations are optimized against ten complex
  closure residuals using deterministic multistarts.
- **Thermal and circular targets:** 301 logarithmic occupation values use the
  disclosed decay expression plus a clearly labelled analytic feature model.
  These curves are not QuTiP/Lindblad-equivalent simulations.
- **qLDPC projection:** code distances `d=6..30` use the disclosed Fowler power
  law. Monte Carlo markers are not regenerated.

## Reproducibility

- Fixed optimizer seed: `260715597`.
- Dependencies: NumPy, SciPy, and Matplotlib from the repository requirements.
- Typical local runtime: below one minute on a laptop CPU.
- Generated data: `outputs/data/`.
- Generated figures: `outputs/figures/`.
- Machine checks: `outputs/checks/`.

The pixel-registered PNGs use the measured source canvas and axes geometry, but
remain presentation artifacts. The independent scientific data and formula
gates determine the reproduction claim.
