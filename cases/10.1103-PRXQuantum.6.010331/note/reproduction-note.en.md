# Reproduction note: Benchmarking and Fidelity Response Theory of High-Fidelity Rydberg Entangling Gates

This case reproduces PRX Quantum 6, 010331 (2025), DOI
`10.1103/PRXQuantum.6.010331`. Its purpose is to turn the paper's response
theory, Hamiltonians and public parameters into executable numerical models,
not to imitate the published raster figures.

## Scope

Nine independently computable theory targets are tracked: the Appendix-L
universal envelopes in Fig. 15; the Rabi-frequency scaling in Fig. 6(a); the
error scalings in Fig. 1(f)/Fig. 7; the public-anchor scaling in Fig. 8; three CZ
protocol responses for Fig. 9(a,b); the spin-lock filter in Fig. 10; the 140 kHz
cavity transfer in Fig. 12; the phase-flip/SSB formulas in Fig. 17; and a
seven-site, 128-dimensional many-body response for Fig. 11. Each target has a
generated table, figure and machine-readable check.

T001-T002 directly sample formulas and coefficients printed by the paper.
T003-T008 evaluate formulas or public-anchor reconstructions. T005 and T009
include independent propagation of an eight-dimensional two-atom Hamiltonian
and a 128-dimensional seven-site model. The `79.89/100` similarity score applies
only to T001-T002, which have paper-exact analytic references; targets lacking
author arrays are not assigned a misleading pixel-similarity score.

## Run

From this case's `code` directory:

```bash
python scripts/run_reproduction.py
python scripts/run_formula_theory_targets.py
pytest -q tests
```

Configuration lives in `code/config`. The scripts write numerical tables,
figures and checks to the case-level `outputs` directory.

## No-pixel computation rule

No paper-figure pixel, digitized curve or raster fit enters the physical
calculation. The pipeline is strictly equations/Hamiltonians plus parameters,
then numerical data, then generated plots. Paper imagery appears only in two
already-rendered post-computation comparison composites. The public code does
not read them, and an automated provenance audit confirms that image reads are
absent from the computational path.

## Exact-reproduction boundary

The paper does not release all measured PSDs, hardware-calibration arrays,
exact geometry/ramp data, the target-specific Fig. 15 optimized phase trajectory,
or all discrete circuit metadata. Corresponding absolute curves remain labelled
partial, reconstructed or blocked. Missing physical inputs are never filled by
tracing the source figures.
