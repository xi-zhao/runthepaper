# Reproduction Report

Similarity score: `73.56/100` (`numerical_feature_reproduction`). Public status: `medium_scale_partial_reproduction`.

## Completed

- Ingested arXiv PDF and TeX source.
- Rendered original main-text figures from source.
- Derived the Floquet model and observables before numerical work.
- Implemented exact Floquet evolution and explicit Floquet diagonalization.
- Generated structured CSV data before plotting.
- Reproduced the main DTC rigidity feature at `L=14`.
- Generated level-statistics, variance, long-range variance, and corrected mutual-information outputs.
- Added an observable sanity check for endpoint mutual information.
- Completed a mixed CuPy/NumPy medium campaign for Fig. 3b-d: 168 jobs, 55 paper-parameter points, and `L=8,10,12`.
- Wrote machine-readable checks and passed the harness audit.

## Commands

```bash
python3 cases/1608.02589/code/scripts/run_reproduction.py
python3 cases/1608.02589/code/scripts/plot_reproduction.py
python3 cases/1608.02589/code/scripts/run_reproduction_iteration2.py
python3 cases/1608.02589/code/scripts/plot_reproduction_iteration2.py
python3 cases/1608.02589/code/scripts/extract_fig3_scaling_collapse.py
```

## Second Iteration Results

| Target | Result |
| --- | --- |
| Fig. 1b-d | Feature reproduced at `L=14`; interacting peak locking error is `0.0`. |
| Fig. 1a | Local phase-boundary proxy generated from `Var(h)` peak; not a full phase diagram. |
| Fig. 2a | Same level-statistics observable generated through `L=10`; crossing remains sample-limited. |
| Fig. 2b | Feature reproduced: variance peak appears and moves with interaction strength. |
| Fig. 3a | Feature reproduced after correcting endpoint mutual information; `epsilon=0` gives `log 2`, large detuning drops near zero. |
| Fig. 3b-d | Medium campaign completed at `L=8,10,12`; strong-coupling collapses are tight, but the weak-coupling panel and fitted critical exponents have not converged. |
| Fig. 4 | Feature reproduced at `L=10` for the long-range `alpha=1.5` model. |

## Evidence

- `../outputs/checks/iteration2_dtc_feature_checks.json`
- `../outputs/figures/iteration2_fig1_L14_subharmonic_rigidity.png`
- `../outputs/figures/iteration2_fig1_phase_boundary_proxy.png`
- `../outputs/figures/iteration2_fig2_level_statistics_variance_L10.png`
- `../outputs/figures/iteration2_fig3_mutual_information_corrected.png`
- `../outputs/figures/fig3_scaling_collapse.png`
- `../outputs/checks/completion_assessment.json`
- `../outputs/figures/iteration2_fig4_long_range_variance_L10.png`
## Scope

This is a medium-scale partial reproduction of the main numerical physics. It is still not a full PRL-scale rerun because the paper-scale exponent fit requires `L=14`, optional `L=16,18` checks, and much larger disorder averaging. The final campaign was not launched under the stop-at-resource-boundary policy.

Difference reason shown on the Fig. 3 comparison: the medium campaign stops at `L=12` and uses reduced disorder sampling; missing sizes and statistics prevent paper-level critical-exponent agreement.
