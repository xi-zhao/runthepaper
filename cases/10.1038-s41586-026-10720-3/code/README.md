# Runnable code for 10.1038-s41586-026-10720-3

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install torch
cd cases/10.1038-s41586-026-10720-3/code
python scripts/run_main_figures.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The measured fibre coefficients, raw spectra, fitted parameter tables, raw NRR fluxes, and measured pulse shapes are unavailable; visible PDF vector content is used internally as a source-derived fit or validation input, so this is not author-data-level exact reproduction.
