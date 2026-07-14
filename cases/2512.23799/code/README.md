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

## Full paper-scale rerun

The paper profile evaluates all 12 physical-error points with the larger Monte Carlo shot budget used by the published case output.

```bash
cd cases/2512.23799/code
python scripts/run_steane_exact_benchmark.py --profile paper
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Exact-circuit acceptance matches all 12 validated points, while mid-range logical infidelity remains 0.42-0.68x of the paper curve because the panel-(c) gate/idle schedule is reconstructed and the author implementation is unavailable. Runtime remains proxy timing; digitized source point sets are not redistributed.
