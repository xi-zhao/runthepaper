# Runnable code for prlb-f37350e-063

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install torch
cd cases/prlb-f37350e-063/code
python scripts/render_idx63_figures.py
```

## Full paper-scale rerun

The full grid rerun requires an NVIDIA CUDA GPU and PyTorch with CUDA support. The included JSON summaries allow the figure to be regenerated without a GPU.

```bash
cd cases/prlb-f37350e-063/code
python scripts/run_idx63_a100_grid.py
python scripts/render_idx63_figures.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The paper-curve result is feature-level rather than author-data exact. Recomputing the full grid requires CUDA/PyTorch; the default public command regenerates figures from the included A100 summaries.
