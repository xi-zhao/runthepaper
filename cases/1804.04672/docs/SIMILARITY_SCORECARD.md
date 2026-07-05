# Public Reproduction Scorecard

This scorecard describes the public reproduction package. It only treats files
inside this repository as inspectable evidence.

The internal harness also used original paper panels and source-derived
validation assets. Those assets are not redistributed here, so they are not
listed as public evidence.

## Case Level

- Public level: `feature_level_reproduction`
- Internal harness score at export time: `72.39/100`
- Public claim: the generated figures reproduce the paper's main numerical
  mechanisms and qualitative phase-structure claims, but this is not an
  author-data-level or pixel-level reproduction.

## Public Targets

| Target | Paper item | Public evidence | Public status |
| --- | --- | --- | --- |
| `T001` | Fig. 3(b) cylinder complex spectrum | `outputs/data/first_target.csv`, `outputs/checks/first_target.json`, `outputs/figures/first_target.png` | Generated with paper parameters; analytic chiral edge trace is visible. |
| `T002` | Fig. 3(a) cylinder phase diagram | `outputs/data/fig3a_cylinder_phase.csv`, `outputs/checks/fig3a_cylinder_phase.json`, `outputs/figures/fig3a_cylinder_phase.png` | Non-Bloch cylinder phase regions and star point classification are generated. |
| `T003` | Fig. 1 open-boundary phase diagram | `outputs/data/fig1_open_boundary_phase.csv`, `outputs/checks/fig1_open_boundary_phase.json`, `outputs/figures/fig1_open_boundary_phase.png` | Bloch fan, non-Bloch theory curve, red boundary reference, and Fig. 2 markers are rendered. |
| `T004` | Fig. 2 square spectra and dynamics | `outputs/data/fig2_square_spectrum.csv`, `outputs/data/fig2_wavepacket.csv`, `outputs/checks/fig2_square_dynamics.json`, `outputs/figures/fig2_square_dynamics.png` | Square spectra and normalized wave-packet motion are generated at the paper marker points. |
| `T005` | Supplemental Fig. S2 gap-square scaling | `outputs/data/figs2_gap_scaling.csv`, `outputs/data/figs2_gap_scaling_fit.csv`, `outputs/checks/figs2_gap_scaling.json`, `outputs/figures/figs2_gap_scaling.png` | Finite-size gap-square fitting examples are generated for the supplement parameters. |
| `T006` | Supplemental Fig. S3 disk phase diagram | `outputs/data/figs3_disk_phase.csv`, `outputs/checks/figs3_disk_phase.json`, `outputs/figures/figs3_disk_phase.png` | Disk-geometry phase diagram is generated as a geometry-independence check. |

## Main Limits

- Fig. 1's red boundary still uses a source-table reference, not a fresh
  phase-boundary-wide finite-size extrapolation.
- Source-derived point sets, original figure panels, and side-by-side comparison
  images are intentionally absent from this public repository.
- The public package supports feature-level reproduction, not complete
  pixel/layout reproduction.
- Larger-radius and larger-grid checks would be needed before upgrading the
  claim beyond feature-level reproduction.
