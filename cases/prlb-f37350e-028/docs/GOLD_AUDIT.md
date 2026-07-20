# Frozen-gold audit

| Task | Verdict | Decisive result |
|---|---|---|
| 1 | invalid | The frozen Morse indices are reversed: off-axis points are minima and `+y` is a saddle for `lambda<1`. |
| 2 | invalid | The exact barrier has breakpoints at `lambda=1/2` and `1`, not only at `1`. |
| 3 | invalid / ill-posed | For `lambda>1` the alleged saddle is a local minimum and the MEP maximum is an endpoint. |
| 4 | invalid | Exact algebra constructs an interior precession family; the source paper explicitly describes it. |

All four frozen answers fail. The terminal campaign class is `benchmark_gold_invalid`, not a failed implementation.
