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

Boundary: The exact 53-qubit contraction is not launched: the paper reports 4.51e18 head-contraction operations and 149 days on one A100, while a direct complex128 statevector would require 128 PiB. The public case also lacks the original circuit, contraction path, slicing configuration, and validation-amplitude bundle.
