# Reproduction Report

Similarity score: `73.56/100` (`numerical_feature_reproduction`).

## Completed

- Ingested arXiv PDF and TeX source.
- Rendered original main-text figures from source.
- Derived the Floquet model and observables before numerical work.
- Implemented exact Floquet evolution and explicit Floquet diagonalization.
- Generated structured CSV data before plotting.
- Reproduced the main DTC rigidity feature at `L=14`.
- Generated level-statistics, variance, long-range variance, and corrected mutual-information outputs.
- Added an observable sanity check for endpoint mutual information.
- Wrote machine-readable checks and passed the harness audit.

## Commands

```bash
python3 cases/1608.02589/code/scripts/run_reproduction.py
python3 cases/1608.02589/code/scripts/plot_reproduction.py
python3 cases/1608.02589/code/scripts/run_reproduction_iteration2.py
python3 cases/1608.02589/code/scripts/plot_reproduction_iteration2.py
```

## Second Iteration Results

| Target | Result |
| --- | --- |
| Fig. 1b-d | Feature reproduced at `L=14`; interacting peak locking error is `0.0`. |
| Fig. 1a | Local phase-boundary proxy generated from `Var(h)` peak; not a full phase diagram. |
| Fig. 2a | Same level-statistics observable generated through `L=10`; crossing remains sample-limited. |
| Fig. 2b | Feature reproduced: variance peak appears and moves with interaction strength. |
| Fig. 3a | Feature reproduced after correcting endpoint mutual information; `epsilon=0` gives `log 2`, large detuning drops near zero. |
| Fig. 3b-d | Not fully reproduced locally; concrete large-ED rerun parameters are recorded in `FIG3_LARGE_ED_PLAN.md`. |
| Fig. 4 | Feature reproduced at `L=10` for the long-range `alpha=1.5` model. |

## Evidence

- `../outputs/checks/iteration2_dtc_feature_checks.json`
- `../outputs/figures/iteration2_fig1_L14_subharmonic_rigidity.png`
- `../outputs/figures/iteration2_fig1_phase_boundary_proxy.png`
- `../outputs/figures/iteration2_fig2_level_statistics_variance_L10.png`
- `../outputs/figures/iteration2_fig3_mutual_information_corrected.png`
- `../outputs/figures/iteration2_fig4_long_range_variance_L10.png`
- `FIG3_LARGE_ED_PLAN.md`
- `PLANNED_LARGE_SCALE_RUNS.md`
- `config/fig3_large_ed_recommended.yaml`

## Scope

This is now a strong feature-level reproduction of the main numerical physics. It is still not a full PRL-scale rerun, because the paper uses much larger disorder averaging and larger exact-diagonalization sizes for the phase diagram and critical scaling.
