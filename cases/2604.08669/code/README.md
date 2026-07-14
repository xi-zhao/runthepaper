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

Boundary: The case includes an A100-SXM4-80GB 127x127 to 101x101 geometry probe and paper-scale P2WGS at N=10201. Full million-sample GNN training was stopped after the strict metric-contract gate failed; the unavailable GPU-parallel auction kernel is not replaced by CPU timing claims.
