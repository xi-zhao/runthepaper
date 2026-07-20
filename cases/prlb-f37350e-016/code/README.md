# Runnable code for prlb-f37350e-016

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-016/code
python scripts/run_gold_audit.py
python scripts/render_idx16_audit.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: This is a benchmark-task case rather than a verified one-paper reproduction. The formulas trace to older review literature and a possible newer candidate, while the frozen third task fails its own pole contract.
