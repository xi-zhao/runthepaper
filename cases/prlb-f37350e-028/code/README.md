# Runnable code for prlb-f37350e-028

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-028/code
python scripts/run_idx28_audit.py
python scripts/render_idx28_figures.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The package reproduces the benchmark-relevant macrospin object and audit, not the paper's full micromagnetic or experimental scope. The generated audit figure is independent and the original paper panel is not redistributed.
