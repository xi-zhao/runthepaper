# Runnable code for 1804.04672

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/1804.04672/code
python scripts/run_first_target.py
python scripts/run_open_boundary_phase_diagram.py
python scripts/run_square_dynamics.py
python scripts/run_cylinder_phase_diagram.py
python scripts/run_gap_scaling.py
python scripts/run_disk_phase_diagram.py
```

Generated CSV files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Some phase-boundary and panel-level comparisons remain paper-subset or source-table validations rather than full independent finite-size reruns.
