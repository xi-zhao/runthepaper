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

`run_symmetry_resolved_sector.py` performs the `L=28`, `k=0`, `I=+1` ED and then renders its figures. To redraw the checked-in sector figures without repeating the approximately five-minute ED, run `plot_symmetry_resolved_sector.py` alone.

Boundary: `L=32` is not launched on the current 40 GB A100 dense path because one float64 matrix is already about 47 GB before eigensolver workspace. The thermodynamic-limit iTEBD path at bond dimension around 400 still needs a validated runner and separate compute budget.
