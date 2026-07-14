# Runnable code for 10.1103-PhysRevB.91.085420

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1103-PhysRevB.91.085420/code
python scripts/run_fig1.py
python scripts/run_fig2.py
python scripts/run_fig3.py
python scripts/run_fig4.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Comparison is a source-vs-reproduction feature contract against the paper's raster figures (no author data or tables); Fig. 2 is feature-level due to the intrinsic ~10^2-rad phase sensitivity of Eq. (8) at T=1024, and the Fig. 4 actual peak sits below the paper value in the narrow band-touching window where the dynamics is genuinely T-sensitive.
