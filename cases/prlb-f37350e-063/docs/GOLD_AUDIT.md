# Frozen gold audit

Terminal verdict: `benchmark_gold_invalid`.

| Task | Verdict | Decisive evidence |
|---|---|---|
| 1. OBC eigensystem | invalid | The printed positive-real vectors are not paired eigenvectors. Exact source pairs have residual `<2e-14`; frozen minimum residuals are `0.0575` (`gamma=0.3`) and `0.299` (`gamma=1.7`). |
| 2. Vacuum threshold | valid | `kappa_c=2 gamma` below `gamma=J`; the finite-size cosine correction above it matches direct stability. |
| 3. Bulk PH selection | invalid | Both `q=+pi/2` and `q=-pi/2` have site-independent PH ratio; the second branch exists at positive density for `kappa>4 gamma`. |
| 4. Deterministic CEP | invalid | Frozen `kappa=2.38930` has residual `0.07712817>1e-8`; no grid point passes the full CEP criterion in any of four robustness runs. |

## Task 4 robustness

All four runs contain 2,064 accepted static points, begin accepting at `kappa=2.38937`, and produce zero CEP candidates for both finite-difference epsilons. The first accepted point has `lambda_2=-0.00377748` and nullities `(1,1)`. Generator/legacy MT19937 and RK4/Heun change only insignificant residual digits at the rejected frozen point.

## Scope of failure

The paper source remains valid. Task 4 is a benchmark-added finite-time protocol, while the paper evaluates Jacobians on continued steady-state solutions. The benchmark should correct Tasks 1 and 3 and either implement the source continuation method for Task 4 or expect no accepted CEP under its current rule.
