# Runnable code for prlb-f37350e-000

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-000/code
python scripts/run_gold_audit.py
python scripts/render_prl_fig1.py
python scripts/render_idx0_audit.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Only PRL Fig. 1 is independently reconstructed. The benchmark record is outside the declared 2025-2026 PRL window, and source Figs. 3-4 require atmosphere-model arrays and implementation details that are not public.
