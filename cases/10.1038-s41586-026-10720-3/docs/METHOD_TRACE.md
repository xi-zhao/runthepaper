# Method trace

## Fig. 2

The printed vector dispersion is represented by piecewise Chebyshev segments.
Stationary points are found by a bracketed golden-section search, and the three
ultraviolet phase-matching roots by bisection. The Raman-shifted pump state is
kept separate from the incident 800 nm pulse state.

Validation against the withheld vector landmarks gives a maximum frequency
error of `8.06e-4 rad/fs` and a maximum co-moving-frequency error of
`2.96e-7 rad/fs`.

## Fig. 4

Only the red experimental markers entered the bounded multistart fit. The
paper's black paths were excluded until every Eq. (D.1) parameter was frozen.
The public script contains the frozen fit parameters and regenerates the six
theory curves without redistributing either marker set.

## Fig. 5

The two straight lines were independently recomputed from the visible
normalized points. The public script regenerates the lines from the frozen
coefficients but deliberately omits the source-derived points.

## Presentation

The internal validation renderer used the exact PDF crop and axes rectangles.
At 144 dpi its structural similarities were `0.8238`, `0.7348`, and `0.8201`
for Figs. 2, 4, and 5. These are presentation diagnostics; the numerical and
provenance checks remain primary.
