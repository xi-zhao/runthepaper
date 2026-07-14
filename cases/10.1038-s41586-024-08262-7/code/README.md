# Runnable code for 10.1038-s41586-024-08262-7

Run commands from the repository root unless a command below changes directory.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1038-s41586-024-08262-7/code
python scripts/gen_fig2.py
python scripts/run_ed_validation.py
```

Generated data files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.

Boundary: The Nature figure is raster-only and no author plotting-data table is available, so the comparison tier is analytic-reference rather than author-data pointwise. The two-dimensional KDH model, eight-body plaquette terms, and braiding demonstration are outside this case's scope.
