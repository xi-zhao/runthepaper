# Runnable code for 1608.02589

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/1608.02589/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
python scripts/run_reproduction_iteration2.py
python scripts/plot_reproduction_iteration2.py
python scripts/extract_fig3_scaling_collapse.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

The checked-in Fig. 3 CSV is the completed `medium` campaign: 168 CuPy/NumPy jobs aggregated into 55 points at `L=8,10,12`. `extract_fig3_scaling_collapse.py` regenerates the comparison figure from that data; exit code `1` is expected while its quality status remains `partial`.

Boundary: do not run the `final` profile by default. It adds `L=14` and raises the disorder targets to `10000/10000/3000/1000` samples per point for `L=8/10/12/14`. Optional `L=16,18` also require a memory-aware eigensolver rather than the current naive dense path.
