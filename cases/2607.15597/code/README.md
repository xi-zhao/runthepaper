# Runnable code for 2607.15597

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2607.15597/code
python scripts/run_reproduction.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Author curve points and optimized Fig. 3 schedules are unavailable; the thermal and circular figures use labelled analytic feature models rather than the full QuTiP/Lindblad workflow; MQDT and qLDPC Monte Carlo require unpublished scientific inputs and run metadata. Pixel registration reaches best SSIM 0.8297 and 0 of 8 images meet the strict 0.95 threshold.
