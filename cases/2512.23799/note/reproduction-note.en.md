# Reproduction Report

## Summary

This case is not accepted as paper-figure reproduction under the original-parameter gate. The formula gate passed and the proxy checks are useful, but the benchmark curves were not generated from the paper's exact Steane circuit and benchmark parameters.

## Reproduced Parts

| Target | Result | Evidence |
| --- | --- | --- |
| PSC formula gate | passed | `../outputs/checks/formula_verification.json` |
| Infidelity benchmark | proxy trend only | `../outputs/figures/fig1_infidelity_reproduction.png` |
| Acceptance benchmark | weak trend only | `../outputs/figures/fig2_acceptance_reproduction.png` |
| Runtime benchmark | proxy timing only | `../outputs/figures/fig3_runtime_reproduction.png` |
| Sampling precision | method validation passed | `../outputs/figures/fig4_sampling_precision_reproduction.png` |

## Main Numerical Results

- Max acceptance mismatch between the local reference curve and local Monte Carlo feature model: `0.00106`. This does not measure closeness to the paper curve.
- Max infidelity mismatch between reference curve and Monte Carlo feature model: `0.000859`.
- Low-`p` runtime speedup at `p=1e-3`: about `22x` in the conservative local proxy.
- Sampling error slope: `-0.498`, matching the expected `1/sqrt(N)` behavior.

## Visual Feature Checks

The harness visual validator was also run on the source PNGs:

- T001 infidelity: `partial_match`, digitized visual feature.
- T002 acceptance: downgraded to `weak_trend_only` after manual review; the generated curve drops too slowly compared with the paper.
- T003 runtime: `mismatch`, which is expected because this case uses local proxy timing rather than the authors' timing data.

These checks support the case conclusion but do not replace author CSV or exact benchmark reruns.

## What Is Missing

The case does not include a full Steane flag-gadget implementation and does not reproduce the authors' original benchmark arrays. The source package contains PNG figures but no CSV data or implementation code. This prevents complete pointwise reproduction.

## Verdict

The case is suitable as a demonstration of formula-to-code proxy checks. It should not be advertised as reproduction of the authors' exact numerical benchmark until the paper parameters and exact Steane circuit are run.
