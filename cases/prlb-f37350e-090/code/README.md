# Runnable code for prlb-f37350e-090

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-090/code
python scripts/run_idx90_audit.py
python scripts/render_idx90_figures.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The seven-task audit is complete, but the package does not reproduce the paper's full electromagnetic simulation or experimental apparatus. Results are formula- and benchmark-level numerical features.
