# Reproduction Report

## Summary

The 1804 case now has six evidence-compared targets following the paper story
line, the cylinder block, and the first supplemental method check. `T003`
reproduces the Fig. 1 phase-diagram
structure with the Bloch fan, non-Bloch theory curve, source-table red
boundary reference, and Fig. 2 marker points. `T004` reproduces the Fig. 2
square spectra and wave-packet dynamics at those two marker points. `T002` and
`T001` reproduce the Fig. 3 cylinder phase diagram and complex spectrum at the
star point. `T005` reproduces the Supplemental Fig. S2 finite-size gap-square
extrapolation examples that explain how the red boundary is obtained. `T006`
reproduces the Supplemental Fig. S3 disk phase diagram for geometry
independence.

## Similarity Level

- Current level: numerical_feature_reproduction
- Similarity score: `80.18`
- Reason: Fig. 1 and Fig. 2 now anchor the paper story line, while Fig. 3(a)
  and Fig. 3(b) keep the cylinder evidence. Supplemental Fig. S2 adds the
  finite-size fitting method behind Fig. 1, and S3 checks geometry
  independence. Fig. 2/S2/S3 are capped because source comparison is visual
  only. Fig. 1 is capped because the full red open-boundary numerical curve is
  currently a source-table reference, not a fresh phase-boundary-wide
  finite-size extrapolation run.

## Reproduced Results

| Paper item | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Fig. 1, `T003` | evidence_compared | `../outputs/data/fig1_open_boundary_phase.csv`, `../outputs/checks/fig1_open_boundary_phase.json`, `../outputs/figures/fig1_open_boundary_phase.png` | Bloch fan, non-Bloch theory boundary `m=2+gamma^2`, the tabulated numerical boundary, shaded phase regions, and Fig. 2 marker points are rendered. A fresh phase-boundary-wide finite-size scan remains pending. |
| Fig. 2, `T004` | evidence_compared | `../outputs/data/fig2_square_spectrum.csv`, `../outputs/data/fig2_wavepacket.csv`, `../outputs/checks/fig2_square_dynamics.json`, `../outputs/figures/fig2_square_dynamics.png` | Square open-boundary spectra and normalized wave-packet intensity maps are generated at `m=2.2121` and `m=1.7879`, `gamma=0.15`, `L=30`, and times `0,5,20`. |
| Fig. 3(a), `T002` | evidence_compared | `../outputs/data/fig3a_cylinder_phase.csv`, `../outputs/checks/fig3a_cylinder_phase.json`, `../outputs/figures/fig3a_cylinder_phase.png` | Non-Bloch cylinder phase regions are generated from the analytic band-touching boundaries of the open-y non-Bloch continuum. The star point `(m,gamma)=(1.717,0.2)` is classified as `chern_one`. Internal digitized validation gives RMSE `0.0148`; those source-derived points are not redistributed. |
| Fig. 3(b), `T001` | evidence_compared | `../outputs/data/first_target.csv`, `../outputs/figures/first_target.png`, `../outputs/checks/similarity_scorecard.json` | `14400` eigenvalues are generated with the paper parameters. Internal source-curve validation is recorded in the check summary, while source-derived points are not redistributed. |
| Suppl. Fig. S2, `T005` | evidence_compared | `../outputs/data/figs2_gap_scaling.csv`, `../outputs/data/figs2_gap_scaling_fit.csv`, `../outputs/checks/figs2_gap_scaling.json`, `../outputs/figures/figs2_gap_scaling.png` | Disk open-boundary spectra are solved for radii `20,24,28,32`; `min|E|^2` is fit against `1/L^2` at `m=2.2000`, `2.0800`, and `2.0400`. The first two intercepts are nonzero, while the `m=2.0400` intercept is near zero. |
| Suppl. Fig. S3, `T006` | evidence_compared | `../outputs/data/figs3_disk_phase.csv`, `../outputs/checks/figs3_disk_phase.json`, `../outputs/figures/figs3_disk_phase.png` | Disk-geometry phase diagram is rendered with the supplement disk numerical boundary, the non-Bloch theory curve, and the Bloch dotted fan. |

## Out-of-Scope Items

| Paper item | Reason |
| --- | --- |

## How to Run

Regenerate the first target data and checks:

```bash
python cases/1804.04672/code/scripts/run_first_target.py
python cases/1804.04672/code/scripts/run_open_boundary_phase_diagram.py
python cases/1804.04672/code/scripts/run_square_dynamics.py
python cases/1804.04672/code/scripts/run_cylinder_phase_diagram.py
python cases/1804.04672/code/scripts/run_gap_scaling.py
python cases/1804.04672/code/scripts/run_disk_phase_diagram.py
```

## Remaining Work

- Replace or verify Fig. 1's red open-boundary boundary with an independent
  phase-boundary-wide finite-size extrapolation run.
- Add larger-radius and digitized-curve validation for Supplemental Fig. S2.
- Add quantitative source matching for Fig. 2 spectra and intensity maps.
- Add blue point-cloud distance as a quantitative comparison gate.
- Add pixel/layout targets for axis placement, marker density, and exact source
  path ordering.
- Keep the old boundary-localization label as diagnostic only.

## Planned Large-Scale Runs

For any target that is blocked by local compute, missing hardware, long runtime,
or unavailable benchmark scale, record the concrete next-run specification:

| Paper item | Plan document | Machine-readable config | What would count as success |
| --- | --- | --- | --- |
