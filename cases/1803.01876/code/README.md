# Code

This folder contains the runnable numerical code for case `1803.01876`.

The scripts assume the current working directory is this `code/` directory.

```bash
python scripts/run_fig2_open_spectrum.py
python scripts/run_fig2_boundary_perturbation.py
python scripts/run_fig3_beta_skin.py
python scripts/run_fig4_winding.py
python scripts/run_fig5_t3.py
python scripts/run_supplemental_fig1_complex_spectra.py
python scripts/run_supplemental_fig2_gamma24.py
python scripts/check_core_derivations.py
```

Outputs are written one level up, under:

```text
../outputs/data/
../outputs/figures/
../outputs/checks/
```

The scripts use only generated numerical data. Original paper figures and
digitized source curves are not required for these public reproduction runs.
