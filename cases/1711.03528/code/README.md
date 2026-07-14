# Runnable code for 1711.03528

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/1711.03528/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
python scripts/run_symmetry_resolved_sector.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The full L=32 symmetry sector and thermodynamic-limit iTEBD calculations are not rerun.
