# Numerical methods

## Exact evaluator

The code branches on the sign of `g²-delta²` and evaluates `c(T),s(T)` using real hyperbolic, critical, or trigonometric functions. This avoids unstable complex-to-real cancellation.

## Independent phase search

`brute_phase_gain` evaluates 200,000 equally spaced phases on `[0,pi)`. The interval is sufficient because energy is pi-periodic. Tests cover real and imaginary splitting and require absolute agreement below `2e-10`.

## Peak checks

One test supplies a stable no-peak counterexample. A second checks that the exact point exceeds neighboring values and that the frozen point is not stationary.

## Quantum check

The analytic Lyapunov solution is evaluated at `r=0.2,0.5,0.9`; the frozen result must equal exactly twice the corrected value.

## Precision

Task 6 uses Python `Decimal` with 80 significant digits and compares against both a 64-digit reference and the frozen decimal tolerance.
