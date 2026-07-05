# Code

This folder contains the runnable numerical code for case `1804.04672`.

The scripts assume the current working directory is this `code/` directory.

```bash
python scripts/run_first_target.py
python scripts/run_open_boundary_phase_diagram.py
python scripts/run_square_dynamics.py
python scripts/run_cylinder_phase_diagram.py
python scripts/run_gap_scaling.py
python scripts/run_disk_phase_diagram.py
python scripts/analyze_edge_branch_candidates.py
```

Outputs are written one level up, under:

```text
../outputs/data/
../outputs/figures/
../outputs/checks/
```

The scripts use only generated numerical data. Original paper figures,
source-extracted point sets, and side-by-side source-panel comparisons are not
required for these public reproduction runs.
