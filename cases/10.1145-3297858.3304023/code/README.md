# Runnable code for 10.1145-3297858.3304023

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install networkx qiskit
cd cases/10.1145-3297858.3304023/code
python scripts/run_paper_swap_example.py
python scripts/run_core_benchmarks.py
python scripts/run_decay_tradeoff.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: All 26 Table II rows run and produce hardware-compliant routes, but row-exact optimized values require the paper's unpublished random seeds, tie-breaking order, and BKA post-processing inputs. This is a metadata boundary, not a compute boundary.
