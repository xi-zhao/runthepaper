# Runnable code for 2503.20566

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install cupy-cuda12x
cd cases/2503.20566/code
python scripts/render_idx47_benchmark_comparison.py
```

## Full paper-scale rerun

The full benchmark rerun requires an NVIDIA CUDA GPU and a compatible CuPy installation. The four numerical scripts checkpoint their JSON outputs before the summary render.

```bash
cd cases/2503.20566/code
python scripts/run_odd_z2_vbs_a100.py
python scripts/run_z2_vison_a100.py
python scripts/run_z2_matter_bulk_a100.py
python scripts/run_z3_derivatives_a100.py
python scripts/render_idx47_benchmark_comparison.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The four benchmark targets are complete, but the source paper's wider tensor-network figure set is not fully reproduced. Full numerical reruns require CUDA and CuPy; the default public command regenerates the summary figure from included data.
