# Runnable code for 10.1126-science.aaw1611

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1126-science.aaw1611/code
python scripts/run_reproduction.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Author theory tables, experimental shots, and tomography arrays are unavailable. Publisher rasters are used only for internal validation and are not redistributed; the S20 correlator audit remains visibly weaker than the density panels.
