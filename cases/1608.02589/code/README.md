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

Boundary: The published medium campaign aggregates 168 jobs into 55 paper-parameter points at L=8,10,12. The final L=8,10,12,14 high-statistics campaign was not launched; optional L=16,18 also require a memory-aware eigensolver.
