# Runnable code for 2605.25398

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2605.25398/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
```

Generated CSV files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Several figures use paper-parameter subsets or local random-matrix instances rather than the full experimental setting.
