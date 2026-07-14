# Numerical Methods

## Implemented Observables

- Stroboscopic autocorrelation `R(n)`.
- Fourier spectra of `R(n)`.
- Peak location near half the drive frequency.
- Half-frequency peak magnitude `h`.
- Variance `Var(h)` over disorder samples.
- Floquet quasienergy adjacent-gap ratio `<r>`.
- Endpoint mutual information from Floquet eigenstates.
- GHZ limiting-state check for endpoint mutual information.

## Generated Data

- `outputs/data/fig1_peak_locking.csv`
- `outputs/data/fig1_fourier_spectra.csv`
- `outputs/data/fig2_level_statistics.csv`
- `outputs/data/fig2_variance_h.csv`
- `outputs/data/fig3_mutual_information_small_ed.csv`
- `outputs/data/fig4_long_range_variance_h.csv`
- `outputs/data/iteration2_fig1_peak_locking_L14.csv`
- `outputs/data/iteration2_fig1_fourier_spectra_L14.csv`
- `outputs/data/iteration2_fig1_phase_boundary_proxy.csv`
- `outputs/data/iteration2_fig2_level_statistics_L6_L8_L10.csv`
- `outputs/data/iteration2_fig2_variance_L10.csv`
- `outputs/data/iteration2_fig3_mutual_information_corrected.csv`
- `outputs/data/iteration2_fig4_long_range_variance_L10.csv`
- `outputs/data/fig3_large_ed_campaign.csv` (medium campaign, 55 aggregated paper points)

## Generated Figures

- `outputs/figures/fig1_subharmonic_rigidity_reproduction.png`
- `outputs/figures/fig2_level_statistics_variance_reproduction.png`
- `outputs/figures/fig3_mutual_information_proxy_reproduction.png`
- `outputs/figures/fig4_long_range_variance_reproduction.png`
- `outputs/figures/iteration2_fig1_L14_subharmonic_rigidity.png`
- `outputs/figures/iteration2_fig1_phase_boundary_proxy.png`
- `outputs/figures/iteration2_fig2_level_statistics_variance_L10.png`
- `outputs/figures/iteration2_fig3_mutual_information_corrected.png`
- `outputs/figures/iteration2_fig4_long_range_variance_L10.png`
- `outputs/figures/fig3_scaling_collapse.png`

## Checks

- `outputs/checks/source_figure_render_check.json`
- `outputs/checks/formula_verification.json`
- `outputs/checks/dtc_feature_checks.json`
- `outputs/checks/iteration2_dtc_feature_checks.json`
- `outputs/checks/reproduction_scope_check.json`
- `outputs/checks/harness_case_audit.json`
- `outputs/checks/fig3_scaling_collapse.json`
- `outputs/checks/completion_assessment.json`

## Limitations

The medium Fig. 3 campaign covers `L=8,10,12`, 168 completed CuPy/NumPy jobs, and 55 aggregated paper-parameter points. The paper-scale final profile adds `L=14` and per-point disorder targets of `10000/10000/3000/1000` for `L=8/10/12/14`; optional `L=16,18` require a memory-aware eigensolver. These runs were not launched because they exceed the current compute and memory boundary.
