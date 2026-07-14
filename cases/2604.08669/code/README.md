# Runnable code for 2604.08669

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install torch
cd cases/2604.08669/code
python scripts/run_reduced_pilot.py
python scripts/run_reduced_p2wgs_pilot.py
python scripts/plot_reduced_outputs.py
python scripts/plot_completion_summary.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

`run_paper_scale_gnn_training.py --profile paper_target --dry-run` records the full configuration without launching the million-sample job. `plot_completion_summary.py` redraws the checked-in A100 paper-geometry and paper-scale P2WGS summaries without starting training.

Boundary: the A100 paper-geometry short probe is complete, but long training is blocked by the failed metric-contract gate and large compute budget. The public source has no GPU-parallel auction kernel; the CPU decoder validates assignment logic but is not a hardware-performance reproduction.
