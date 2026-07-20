# Frozen-gold audit

| Task | Verdict | Decisive evidence |
|---|---|---|
| 1 | valid | matrix eigenvalues equal `-lambda ± sqrt(g²-delta²)` |
| 2 | valid | instability iff `g² > lambda²+delta²`; detuning cut `|delta|=g` |
| 3 | invalid | physical phase optimum disagrees with frozen formula and matches dense phase search |
| 4 | invalid | frozen assumptions do not guarantee a peak; frozen time is not stationary when a peak exists |
| 5 | invalid | exact vacuum Lyapunov occupation is `r²/[2(1-r²)]` |
| 6 | valid | 80-digit result differs from frozen decimal by only `1.2835580e-16` |

Terminal verdict: `benchmark_gold_invalid`.

This verdict does not invalidate the paper. Tasks 3-5 are benchmark-added claims that exceed or alter the paper's explicitly semiclassical scope.
