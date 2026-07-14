# Runnable code for 2507.09447

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2507.09447/code
python scripts/plot_paper_exact.py
python scripts/qa_paper_exact.py
```

## Full paper-scale rerun

The full L=1000, 3200-realization rerun is resumable but computationally expensive; the quick commands regenerate figures and scientific checks from the published generated data.

```bash
cd cases/2507.09447/code
python scripts/run_paper_exact.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: Author seeds, state-selection windows, transfer/grid details, and final artwork are unavailable; all scientific gates pass, but source-pixel identity is not claimed.
