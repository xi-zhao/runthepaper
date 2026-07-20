# Lessons learned

## Model first

Treating geometry as an explicit site set keeps the hopping law unchanged while
square, rhombic, and aspect-ratio cuts vary. This single model explains both the
geometry-dependent skin accumulation and the boundary-dependent critical
spectra without panel-specific Hamiltonians.

## Numerical evidence before image similarity

Non-normal spectra can contain unstable outliers even when two Hamiltonians are
related by an exact reflection. Robust cloud statistics, matrix-level symmetry
tests, eigenpair residuals, and physical feature contracts are therefore more
reliable than a maximum pointwise distance alone.

The same separation is essential for figures. Data generation, scientific
acceptance, layout registration, and pixel comparison are four different
layers. A passed physical result can still have modest SSIM because of sampling,
interpolation, three-dimensional projection, fonts, and antialiasing.

## Expensive runs

Large eigensystems and disordered spectral-potential scans should save numerical
arrays before rendering. The case keeps CSV/NPZ data and machine-readable JSON
checks so visual fixes do not trigger unnecessary diagonalization and so each
figure can be audited independently.

## Remaining uncertainty

Several publication details are not specified: the Fig. 4(b) state sequence and
fit window, exact integer vertices in Fig. 4(d), the Fig. 4(e) disorder seed,
and the Fig. 4(f) probe grid. These are explicit reconstruction choices, not
hidden tuning parameters.
