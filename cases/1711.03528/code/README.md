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
python scripts/plot_symmetry_resolved_sector.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The paper's k=0, I=+1 sector is reproduced at L=28 (dimension 13201), including the 15-state scar tower. L=32 is not launched because one float64 dense matrix is already about 47 GB before eigensolver workspace on the current 40 GB A100 path; thermodynamic-limit iTEBD also remains unimplemented.
