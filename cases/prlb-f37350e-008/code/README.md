# Runnable code for prlb-f37350e-008

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-008/code
python scripts/run_gold_audit.py
python scripts/render_prl_figc.py
python scripts/render_idx8_audit.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The reproduced source is a 2024 PRL rather than a paper in the benchmark's declared 2025-2026 window. The public package excludes the original figure and publishes only independently generated data and images.
