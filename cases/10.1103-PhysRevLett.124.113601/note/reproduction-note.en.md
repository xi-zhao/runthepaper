# Pixel-registered reproduction of localization-driven superradiance

## Paper and question

This public package reproduces the localization-driven superradiant
instability studied by Yin et al., *Physical Review Letters* **124**, 113601
(2020).  The central question is why quasiperiodic localization enhances the
cavity scattering response and can drive the superradiant threshold to zero.

## Independent calculation

The code independently implements finite Aubry–André and generalized
Aubry–André Hamiltonians, state-resolved IPR, cavity scattering susceptibility,
the linear critical pump, and the self-consistent atomic-orbital/cavity-field
iteration.  Public curves are rendered from the generated CSV files.  Paper
pixels appear only in limited attributed comparison boards and never enter the
calculation or generated images.

## Main results

- Fig. 2 places the mobility edge at `alpha=233` and `epsilon_c/J=0.4396`.
  All 377 visible IPR vector samples agree with correlation
  `0.99999999997`.  The excited-state threshold normalization is not published,
  so this target remains exploratory.
- All five panels of Fig. 3 are regenerated.  The clean threshold is
  `eta_c/J=0.27681`, and the Fig. 3(a) threshold curve has vector-path
  correlation `0.99999695`.  Fig. 3 reaches `complete_reproduction`.
- Fig. 4 reproduces the nonlinear photon onset and cavity-wave-vector
  threshold landscape.  A published/arXiv detuning-convention split keeps the
  target at paper-subset level.
- Fig. S1 regenerates five normal/superradiant density pairs.  All ten visible
  PDF vector paths pass their pointwise contract, but the pump samples and
  iteration metadata are omitted by the supplement.

Full-canvas SSIM is `0.8602` for Fig. 3, `0.7921` for Fig. 4, and `0.7856` for
Fig. S1.  These values compare independently generated data after registration
to the paper geometry; they are not obtained by copying the reference image.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1103-PhysRevLett.124.113601/code
python scripts/run_linear_targets.py
python scripts/run_nonlinear_targets.py
python scripts/render_pixel_registered.py
```

The two numerical scripts took about 22.65 seconds in the latest complete Apple
M4 rerun.  Data, figures, and JSON checks are written to `../outputs/data`,
`../outputs/figures`, and `../outputs/checks`.  Set
`LDSI_OUTPUT_ROOT=/tmp/ldsi-run` to isolate validation outputs.

## Boundary

The Harness score is `88.56/100`, with case-level status
`numerical_feature_reproduction`.  Missing Fig. 2 threshold normalization, the
Fig. 4 version-dependent convention, and missing S1 pump/solver metadata are
not overridden by visual agreement.  The public package excludes the paper
PDF, standalone source figures, vector samples, and internal process logs.
