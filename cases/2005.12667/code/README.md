# Runnable code for 2005.12667

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2005.12667/code
python scripts/run_reproduction.py
python scripts/run_full_rmp_reproduction.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Full review means all theory recoverable from public equations and parameters, not unavailable author evidence. Fig. 4(b-e) remains blocked by the missing COMSOL project; the experimental panels of Figs. 21, 28, and 32 require author-level raw data and calibration. Targets with incomplete absolute parameters are explicitly labeled paper-subset or analytic-reference rather than exact.
