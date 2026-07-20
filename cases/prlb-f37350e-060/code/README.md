# Runnable code for prlb-f37350e-060

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-060/code
python scripts/run_idx60_audit.py
python scripts/render_idx60_figures.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: This case reproduces the benchmark-relevant analytic and small numerical objects, not the full hardware protocol or experimental error-correction campaign.
