# Runnable code for 10.1007-s11433-024-2478-8

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1007-s11433-024-2478-8/code
python scripts/run_fig3.py
python scripts/run_fig4.py
python scripts/run_fig5.py
python scripts/run_fig7.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The two-photon full three-level model gives gate error ~1e-3 vs the paper's <1e-4 (its waveforms were likely optimised in a reduced/effective model); Fig. 7 peak ~25% below the paper; Fig. 6 three-qubit Toffoli geometry is underspecified and not reproduced; Figs. a6-a8 have no published coefficients.
