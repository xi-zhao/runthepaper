# Runnable code for prlb-f37350e-040

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-040/code
python scripts/run_gold_audit.py
python scripts/render_idx40_audit.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The source equations and benchmark observables are reproduced, but paper-panel curves are not claimed because the author simulation arrays and full evolution metadata are unavailable.
