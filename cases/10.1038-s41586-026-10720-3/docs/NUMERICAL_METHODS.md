# Numerical methods

## Public executable scope

The public package regenerates the numerical content of main-text Figs. 2, 4,
and 5. Fig. 1 is a conceptual schematic. Fig. 3 is an experimental acquisition
whose raw counts were not published.

## Fig. 2

- Piecewise Chebyshev evaluation in float64.
- Golden-section stationary-point search with 80 iterations.
- Bracketed bisection with 80 iterations.
- Generated curve and landmark data are written before plotting.

## Fig. 4

- Six frozen red-only fits, one for each disclosed probe wavelength.
- Peak-profile quadrature table: 50,001 points.
- Sideband orders: `m=-10,...,10`.
- Public output contains equation-generated theory curves only.
- Internal blind validation: mean NRMSE `0.0653`, correlation `0.9810`.

## Fig. 5

- Ordinary least-squares coefficients frozen after the independent regression.
- Public output contains fitted lines only, not the source-derived point set.
- Recomputed slope ratio: `1.0211`; paper: `1.02`.

## Runtime

This main-figure path is analytic and fit-evaluation work and completes in
seconds on a CPU. An A100 is unnecessary for these three figures. The separate
UPPE propagation study is retained as auxiliary internal validation and is not
part of this public main-figure package.
