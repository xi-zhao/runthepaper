# Runnable code for 2605.25594

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2605.25594/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
python scripts/run_fig11_phenomenological_model.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The paper's L=32-38 targets were not forced through the current dense eigensolver: L=32 hit a 32-bit workspace failure and L=38 exceeds the practical single-A100 memory path. The T and randomized-site n operator panels remain outside the completed subset and are not replaced by proxy data.
