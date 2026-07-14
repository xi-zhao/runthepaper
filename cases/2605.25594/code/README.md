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

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`. The quick run regenerates the local correctness baseline. Precomputed independent A100 results for `L=24/28/31` are published under `../outputs/data/remote/` together with their aggregate checks.

Boundary: the current public evidence covers a paper-scale size subset, not the full `L<=38` campaign. The missing `L=32-38` runs are compute-limited on the available single-A100 dense-eigensolver path and are not replaced by proxy data.
