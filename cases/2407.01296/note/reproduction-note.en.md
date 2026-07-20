# Non-Hermitian skin effect in arbitrary dimensions — reproduction note

## Result

This case completes a scientific reproduction of the formal paper's main-text
Figs. 1–5. Figs. 2(a–c), 3, and 4(a–f) are recomputed from the published model
with Python/SciPy. Figs. 1 and 5 are analytic schematic redraws. Fig. 2(d) is the
only source-assisted numerical panel: it uses author-released finite-size ED
tables, while the displayed observable is recomputed by this case.

This is not a pixel copy of the paper. Every formal canvas is registered to the
published dimensions, but none passes the strict `SSIM >= 0.95` threshold. The
main-text scientific evidence chain is complete; Supplementary Figs. S2 and
S4–S7 have not yet been independently rerun panel by panel.

## How Fig. 3 is drawn

The current version addresses the line construction in Fig. 3(a) and the view
of Fig. 3(b):

- Fig. 3(a) projects regular `101 x 101` momentum grids onto the two beta planes
  instead of connecting irregular inverse-solver points;
- Fig. 3(b) uses periodic seam-free interpolation for the momentum surfaces;
- the 3D camera is fixed at `24°` elevation and `-41°` azimuth with equal axis
  proportions.

All scientific gates pass, while the full-figure SSIM remains `0.6969`. The
status is therefore `pixel_registered_not_identical`. Sampling, interpolation,
projection, font rasterization, and antialiasing remain visible sources of
pixel difference.

## How Fig. 4 is drawn

All six Fig. 4 panels pass their independent numerical checks. The full-figure
SSIM is `0.5823`; panel SSIM values are `0.9107`, `0.5717`, `0.7042`, `0.4353`,
`0.4181`, and `0.4946`. The lower-scoring panels depend on unreported choices
such as the state sequence, integer boundary vertices, random realization,
energy-probe grid, and exact typesetting. These uncertainties are disclosed in
the machine checks instead of being hidden by copying paper pixels.

## Public boundary

The public package contains clean-room numerical kernels, lightweight runners,
generated data, generated figures, machine checks, and limited attributed
comparison boards. It excludes the paper PDF, standalone original figures,
vector paths, digitized curves, and private process history. Comparison pixels
are used only for presentation audits and never enter the numerical model.

## Quick run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2407.01296/code
python scripts/run_reproduction_smoke.py
```

This runs reduced-scale Fig. 2 geometry and Fig. 4(d) boundary-ratio checks.
Paper-scale generated results are included in the case. See
[`../docs/NUMERICAL_METHODS.md`](../docs/NUMERICAL_METHODS.md) and
[`../docs/SIMILARITY_SCORECARD.md`](../docs/SIMILARITY_SCORECARD.md) for the
method and evidence boundary.
