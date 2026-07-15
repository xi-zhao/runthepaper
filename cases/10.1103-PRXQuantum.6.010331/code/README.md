# Runnable code for 10.1103-PRXQuantum.6.010331

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1103-PRXQuantum.6.010331/code
python scripts/run_reproduction.py
python scripts/run_formula_theory_targets.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The 79.89 score covers only T001-T002, which have paper-exact analytic references. Exact absolute curves that require unreleased PSD or calibration arrays, target-specific pulse/ramp identity, atomic geometry, or discrete circuit metadata remain explicitly partial or reconstructed and were not filled by tracing paper figures.
