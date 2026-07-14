# Runnable code for 2512.23799

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2512.23799/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
python scripts/run_steane_exact_benchmark.py --profile smoke
python scripts/plot_steane_exact_comparison.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

The smoke profile exercises the exact circuit without overwriting the published full-run artifacts. To regenerate the 790,000-shot paper grid, use:

```bash
python scripts/run_steane_exact_benchmark.py --profile paper
```

Boundary: T001/T002 now use the reconstructed exact Steane circuit. Acceptance is reproduced; logical infidelity has a declared mid-range residual caused by unpublished schedule details. T003 remains proxy timing. Digitized paper curves and source-derived point sets are not distributed.
