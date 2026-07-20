# Runnable code for 2407.01296

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2407.01296/code
python scripts/run_reproduction_smoke.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Supplementary Figs. S2 and S4-S7 are not independently complete. Fig. 2(d) uses author-released ED tables, and unreported state selection, integer boundary vertices, random seeds, probe grids, three-dimensional projection, and renderer details limit pixel identity in Fig. 3 and several Fig. 4 panels.
