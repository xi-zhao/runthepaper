# Runnable code for prlb-f37350e-009

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-009/code
python scripts/run_gold_audit.py
python scripts/render_rgw_fig2.py
python scripts/render_idx9_audit.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The frozen record combines multiple older non-PRL sources and therefore is not a one-paper PRL reproduction. The public case exposes the independent calculation and audit but does not redistribute source artwork or digitized curves.
