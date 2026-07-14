# Runnable code for 2605.25594

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2605.25594/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
python scripts/run_fig11_phenomenological_model.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Several exponent-level and paper-size targets remain compute-limited or only partially reproduced.
