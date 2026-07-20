# Frozen-gold audit

| Task | Verdict | Decisive result |
| --- | --- | --- |
| 1 | valid | Kernel, subtraction, scale, and quadratic phase match direct source lines 136-156. |
| 2 | invalid | `RKR=-I-K`; source bounds imply `1.128092 <= ||K|| <= 1.192466`, excluding 2. |
| 3 | invalid | Stationarity is valid and the branch decreases, but calibrated `Lambda(1/2)` is near 0.11 rather than 0.06405. Simplicity alone also does not prove strictness without a coupling condition. |
| 4 | invalid / ill-posed | `V(u,v)=-(u-v)sin(u^2-v^2)/pi`; the top-state form converges in grid at fixed `L` but grows approximately linearly with `L`. |

## Task 2: triangle bound is not a sharp norm

The projection form establishes bounded self-adjointness. It only gives the
coarse triangle inequality `||K||<=2`. Parity yields the stronger exact spectral
relation. Since the paper cites `sup sigma(K)<=0.192466`, the norm is at most
`1.192466`; the frozen Weyl-sequence assertion cannot be correct.

## Task 3: constrained value

The dual residual is below `4e-14` in every saved run. Even the smallest scan
value, `0.09511495` at `L=5,N=100`, exceeds the frozen scalar by more than 0.03.
Refined windows reach `0.11092468`. These discrepancies are far larger than any
reasonable truncation error and invalidate the requested six-digit answer.

## Task 4: missing full-line domain gate

Gaussian convolution gives the unique family printed in `DERIVATION.md` on a
Schwartz core. Standard simple-eigenvalue perturbation theory does not by itself
put the long-tailed top state in the quadratic-form domain of `V`. Numerically,
grid refinement at `L=10` stabilizes near 1.707, while window growth gives 3.503
at `L=20` and 5.303 at `L=30`. The frozen convergence certificate does not
exist. The direct paper itself describes smoothing as future work.

Terminal class: `benchmark_gold_invalid`; valid tasks `[1]`, failed tasks
`[2,3,4]`.
