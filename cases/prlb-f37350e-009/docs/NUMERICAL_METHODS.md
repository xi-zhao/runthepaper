# Numerical methods

This is a T1 analytic case.

- Floating-point type: IEEE-754 binary64.
- Source Fig. 2 sampling: 3001 points, uniform in `x=|k tau|` on `[0,3]`.
- Pixel comparison: source and generated plot spines define normalized plot
  coordinates; colored annotation boxes are excluded; visible blue and red
  curve pixels are compared by bidirectional nearest-neighbor distance.
- Counterterm audit point: `(beta,m,t,k)=(-2.2,0.3,0.8,7)`, chosen away from
  rational singularities and large enough that all terms remain well-scaled.
- No optimizer or convergence tolerance is required for the closed forms.

The reference PNG comes from `pdftoppm` at 200 dpi followed by a fixed crop of
page 6. The original EPS and PDF are retained as source evidence.
