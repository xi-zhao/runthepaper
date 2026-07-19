# Runnable code for 10.1103-PhysRevLett.124.113601

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1103-PhysRevLett.124.113601/code
python scripts/run_linear_targets.py
python scripts/run_nonlinear_targets.py
python scripts/render_pixel_registered.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Only Fig. 3 is final-reproduction eligible. Fig. 2 omits the excited-state threshold normalization, Fig. 4 has a published/arXiv detuning-convention split, and Fig. S1 omits pump samples and iterative-solver metadata.
