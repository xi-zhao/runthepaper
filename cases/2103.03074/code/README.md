# Runnable code for 2103.03074

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2103.03074/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: do not launch the 53-qubit contraction as a normal case run. The paper table estimates 149 days on one A100, and the public case does not include the full circuit/path/slicing asset bundle. The checked-in scripts reproduce the 18-qubit statistical mechanism only.
