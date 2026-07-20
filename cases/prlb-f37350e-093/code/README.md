# Runnable code for prlb-f37350e-093

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-093/code
python scripts/render_prl_fig2b.py
python scripts/render_idx93_audit.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The source is a 2024 PRL outside the benchmark's declared window. Author trajectories, event counts, and optimized-coordinate rerun rates are unavailable, so the efficiency and speedup claims remain underdetermined.
