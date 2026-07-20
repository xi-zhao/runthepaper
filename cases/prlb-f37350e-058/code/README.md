# Runnable code for prlb-f37350e-058

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-058/code
python scripts/run_idx58_audit.py
python scripts/render_idx58_figures.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The public result validates the source extrapolation rather than reproducing every supplemental curve. Frozen Tasks 2-4 disagree with the independently evaluated operator and are reported as benchmark-gold failures.
