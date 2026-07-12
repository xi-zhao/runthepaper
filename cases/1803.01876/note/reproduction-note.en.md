# Reproduction Report

## Scope

This case reproduces the main numerical physics of arXiv:1803.01876 with digitized original-figure references for all scored targets. It does not claim author-plotting-data equivalence. Acceptance separates independent physics generation from EPS/PNG digitized reference checks.

Similarity score: `94.0/100` (`complete_reproduction` under the digitized-curve scoring model).

## Reproduced Results

| Paper item | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Fig. 2 open-chain spectrum and boundary perturbation | digitized_curve_match | `../outputs/checks/fig2_open_spectrum.json`, `../outputs/checks/fig2_boundary_perturbation.json`, `../outputs/checks/all_digitized_curves.json` | All four Fig. 2 panels have EPS/PNG digitized reference CSVs with target-level mismatch count `0`. |
| Fig. 3 generalized Brillouin zone / skin effect | digitized_curve_match | `../outputs/checks/fig3_beta_skin.json`, `../outputs/checks/all_digitized_curves.json` | Beta-root, `C_beta`, and profile panels have digitized reference checks with mismatch count `0`. |
| Fig. 4 non-Bloch winding | digitized_curve_match | `../outputs/checks/fig4_winding.json`, `../outputs/checks/fig4_digitized_curve.json`, `../outputs/checks/all_digitized_curves.json` | Original EPS marker/step curve is digitized and matched against generated CSV. |
| Fig. 5 nonzero `t3` | paper-parameter high-precision digitized match | `../outputs/checks/fig5_t3.json`, `../outputs/checks/all_digitized_curves.json` | Spectrum, winding, and noncircular `C_beta` use the paper parameters. The `L=100` OBC spectrum and `C_beta` energy input are independently evaluated at 35 decimal digits; source EPS paths are reference-only. |
| Supplemental numerical figures | digitized_curve_match | `../outputs/checks/supplemental_fig1_complex_spectra.json`, `../outputs/checks/supplemental_fig2_gamma24.json`, `../outputs/checks/all_digitized_curves.json` | Complex spectra and large-`gamma` spectrum/winding panels have digitized reference checks. |

## Compute Refresh

The refreshed run includes a compute-budget profile:

- `COMPUTE_BUDGET.md`
- `../outputs/checks/compute_budget_profile.json`

All implemented numerical targets are local-ok on the current machine. Every scored target includes digitized EPS/PNG reference comparison. Fig. 5 uses a 35-digit eigenspectrum because the `L=100`, nonzero-`t3` open-chain matrix is too non-normal for double precision. The regression suite now rejects the former dense zigzag artifact and non-physical `C_beta` chords. The remaining gap is author plotting data, not paper parameters.

## How To Run

```bash
python3 cases/1803.01876/code/scripts/verify_formula_gate.py
python3 cases/1803.01876/code/scripts/check_core_derivations.py
python3 cases/1803.01876/code/scripts/run_fig2_open_spectrum.py
python3 cases/1803.01876/code/scripts/run_fig2_boundary_perturbation.py
python3 cases/1803.01876/code/scripts/run_fig3_beta_skin.py
python3 cases/1803.01876/code/scripts/run_fig4_winding.py
python3 cases/1803.01876/code/scripts/digitize_fig4_winding_reference.py
python3 cases/1803.01876/code/scripts/digitize_all_figure_references.py
python3 cases/1803.01876/code/scripts/run_fig5_t3.py
python3 cases/1803.01876/code/scripts/run_supplemental_fig1_complex_spectra.py
python3 cases/1803.01876/code/scripts/run_supplemental_fig2_gamma24.py
```

## Remaining Work

- Optional: obtain author plotting data for author-data-level comparison.
- Optional: obtain pixel-level layout targets for final visual alignment after author-data availability is resolved.
