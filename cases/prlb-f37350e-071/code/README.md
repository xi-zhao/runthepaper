# Runnable code for prlb-f37350e-071

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-071/code
python scripts/run_idx71_audit.py
python scripts/render_idx71_figures.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The benchmark-task scope is complete, but this is not a reproduction of every paper figure or experimental implementation. The package publishes only independently generated audit data and graphics.
