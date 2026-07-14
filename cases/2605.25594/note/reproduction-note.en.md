# Reproduction Report

## Result

This case completed a local exact-diagonalization baseline and a paper-scale subset campaign for arXiv:2605.25594. The A100 campaign covers `L=24/28/31` and 605 disorder realizations.

Status: `paper_scale_subset_reproduction`.

The gap-ratio midpoint is `W=16.588/16.599/16.564` for `L=24/28/31`, independently pinning the transition near the paper's `W_c=16.5`. The data also reproduce the GOE-to-Poisson crossover, fidelity-peak sharpening, IPR growth, the typical/average separation, and a transition spectral exponent near `0.48` versus the paper's `0.52` at `L=38`.

## What Was Reproduced

| Target | Result | Reason for the remaining difference |
| --- | --- | --- |
| Fig. 1 fidelity susceptibility and transition | Reproduced at the paper-size subset `L=24/28/31` | The complete `L=32-38` scaling ladder exceeds the available single-A100 dense-eigensolver path. |
| Fig. 2 weak-disorder crossover | Feature and paper-size subset reproduced | The `L=31` peak touches the lower edge of the current disorder grid, and the `L=38` endpoint is absent. |
| Fig. 3 spectral mechanism | Both mechanisms reproduced; fitted critical exponent `a≈0.48` | The paper's `a≈0.52` uses the larger `L=38` low-frequency window. |
| Fig. 8/9 localized-regime behavior | Typical/average separation and the finite-size drift of the crossover are reproduced | The current disorder grid and missing `L=32-38` data do not support a paper-precision estimate of `W_3^*`. |
| Fig. 10 perturbative trend | Mechanism reproduced | The full large-size operator panel was not computed. |

Every comparison in this note states the reason for the remaining difference. A missing paper-size result is not replaced with proxy data.

![A100 paper-size subset with the remaining difference labeled](../outputs/figures/fig1_a100_subset_reproduction.png)

## Numerical Evidence

- Local correctness baseline: `L=4,5,6,7`.
- A100 paper-scale subset: `L=24,28,31`, 605 disorder realizations, double-precision diagonalization.
- Aggregated evidence: `../outputs/data/remote_campaign_summary.csv`.
- Machine-readable gates: `../outputs/checks/remote_campaign_summary.json` and `../outputs/checks/similarity_scorecard.json`.
- Completion decision: `../outputs/checks/completion_assessment.json`.
- Remote spectral evidence: `../outputs/data/remote/results_spectral.jsonl` and `../outputs/data/remote/results_weakW.jsonl`.

## Stop Decision And Compute Boundary

We assessed the missing largest sizes and stopped rather than forcing an invalid approximation:

- at `L=32`, the double-precision GPU eigensolver hit its underlying 32-bit workspace limitation;
- a CPU fallback is approximately an hour or more per disorder realization on the available path;
- at `L=38`, the dense Hamiltonian and eigenvector matrices alone total roughly 48 GB before eigensolver workspace, beyond the practical memory path of the available single A100;
- the missing `L=32-38` targets are therefore recorded as `compute_limited_current_resource`.

They should only be reopened with a 256 GB+ memory node, a distributed eigensolver, or suitable multi-GPU large-memory resources.

## Files

- Code: `src/anderson_sensitivity.py`
- Local run script: `scripts/run_reproduction.py`
- Plot script: `scripts/plot_reproduction.py`
- Data: `../outputs/data/`
- Figures: `../outputs/figures/`
- Checks: `../outputs/checks/`
