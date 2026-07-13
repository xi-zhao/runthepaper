# Reproduction Report

## Result

The case completed a reduced local reproduction of arXiv:2605.25594.

Status: `partial_feature_reproduction`.

The formula chain and local numerical implementation are working. The output reproduces several key physical signs:

- weak-disorder sensitivity enhancement;
- chaos-window gap-ratio behavior;
- high-disorder IPR growth;
- average/typical susceptibility separation in the localized regime;
- strong-disorder perturbative trend.

## What Was Reproduced

| Target | Result |
| --- | --- |
| Fig. 1 local analog | Partial. The local plot shows useful trends but not the clean two-peak paper curve. |
| Fig. 2 local analog | Feature-level. Low-W sensitivity enhancement is visible; asymptotic scaling is not. |
| Fig. 3 spectral object | Pipeline implemented; exponent-level reproduction not accepted. |
| Fig. 8 local analog | Feature-level. Average/typical ratio grows in localized regime. |
| Fig. 10 local analog | Feature-level. Perturbative strong-disorder trend appears. |

## Files

- Code: `src/anderson_sensitivity.py`
- Run script: `scripts/run_reproduction.py`
- Plot script: `scripts/plot_reproduction.py`
- Data: `../outputs/data/`
- Figures: `../outputs/figures/`
- Checks: `../outputs/checks/`

## Important Limitation

The original paper used large system sizes up to `L=38`. This local run uses exact diagonalization only up to `L=7`. That is the dominant reason for the remaining mismatch.
