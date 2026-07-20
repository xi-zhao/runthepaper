# Runnable code for 2607.02157

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2607.02157/code
python scripts/run_scan.py
python scripts/run_nmse.py
python scripts/run_figS1.py
python scripts/plot_figures.py
python scripts/adjudicate_pooling.py
python scripts/verify_formulas.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Comparison is a feature contract against the paper's raster panels (no author data or tables); score is bound at 80 because the paper releases no numerical data and we decline to digitize its curves. The disorder-ensemble aggregation convention (per-realization vs pooled) was adjudicated to resolve a TFIM peak ambiguity; three unspecified conventions (Mackey-Glass normalization, cluster boundary condition, F(omega) normalization) are documented as questions for the authors.
