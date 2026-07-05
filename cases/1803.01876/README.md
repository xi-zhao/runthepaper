# 1803.01876: Non-Hermitian SSH Reproduction

Paper: *Edge states and topological invariants of non-Hermitian systems*

This case reproduces the main numerical structure behind the non-Hermitian SSH
model: open-boundary spectra, generalized Brillouin zone, skin-effect profiles,
non-Bloch winding number, and the nonzero-`t3` extension.

## Public Boundary

This public case includes:

- a reproduction note;
- paper-derived numerical code;
- generated CSV data;
- generated figures;
- JSON validation checks;
- derivation and method notes.

It does not include the original paper PDF, arXiv source archive, original EPS
figures, digitized source curves, or side-by-side source-panel comparison
assets. Those were used internally as reference material, but they are not
redistributed here.

## Result

The case reaches feature-level reproduction for the main numerical targets. The
generated results reproduce the key physical claims:

- open-boundary zero modes appear in the non-Bloch topological interval;
- the generalized Brillouin zone differs from the unit circle;
- right eigenstates show non-Hermitian skin localization;
- the non-Bloch winding number matches the open-boundary transition;
- the nonzero-`t3` model produces the expected shifted topological interval and
  non-circular beta curve.

The public scorecard is in [docs/SIMILARITY_SCORECARD.md](docs/SIMILARITY_SCORECARD.md).
The most important limitation is that author plotting data is not available in
this public package, so this is not an author-data-level reproduction claim.

## Read

- [Reproduction Note](note/reproduction-note.md)
- [Derivation Trace](docs/DERIVATION_TRACE.md)
- [Numerical Methods](docs/NUMERICAL_METHODS.md)
- [Lessons Learned](docs/LESSONS_LEARNED.md)

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/1803.01876/code
python scripts/run_fig2_open_spectrum.py
python scripts/run_fig3_beta_skin.py
python scripts/run_fig4_winding.py
python scripts/run_fig5_t3.py
```

The scripts write generated data to `cases/1803.01876/outputs/data/`, figures to
`cases/1803.01876/outputs/figures/`, and checks to
`cases/1803.01876/outputs/checks/`.

## Generated Figures

![Fig. 2 open spectrum](outputs/figures/fig2_open_spectrum.png)

![Fig. 3 beta skin](outputs/figures/fig3_beta_skin.png)

![Fig. 4 winding](outputs/figures/fig4_winding.png)

![Fig. 5 t3](outputs/figures/fig5_t3.png)
