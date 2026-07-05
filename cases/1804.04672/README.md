# 1804.04672: Non-Hermitian Chern Bands Reproduction

Paper: *Non-Hermitian Chern bands*

This case reproduces the main numerical structure behind the paper's
non-Hermitian Chern model: open-boundary phase diagrams, square-geometry spectra
and wave-packet dynamics, cylinder non-Bloch phase structure, cylinder complex
spectrum, and supplemental finite-size checks.

## Public Boundary

This public case includes:

- a reproduction note;
- paper-derived numerical code;
- generated CSV data;
- generated figures;
- JSON validation checks;
- derivation, method, scorecard, and lessons notes.

It does not include the original paper PDF, arXiv source archive, original EPS
figures, digitized source curves, source-extracted point sets, or side-by-side
source-panel comparison assets. Those were used internally as reference
material, but they are not redistributed here.

## Result

The case reaches feature-level reproduction for the main numerical targets. The
generated results reproduce the key physical claims:

- ordinary Bloch phase boundaries can disagree with open-boundary physics;
- non-Bloch theory gives the relevant open-boundary transition curve;
- square geometry separates gapped and edge-propagating wave-packet behavior;
- cylinder geometry shows a direction-dependent non-Bloch phase diagram;
- the cylinder complex spectrum contains the analytic chiral edge branch;
- supplemental gap-square scaling and disk geometry checks support the phase
  boundary story.

The public scorecard is in [docs/SIMILARITY_SCORECARD.md](docs/SIMILARITY_SCORECARD.md).
The main limitation is that source-derived point and pixel validation assets are
not part of this public package, and Fig. 1's red boundary still uses a
source-table reference rather than a fresh full finite-size scan.

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
cd cases/1804.04672/code
python scripts/run_first_target.py
python scripts/run_open_boundary_phase_diagram.py
python scripts/run_square_dynamics.py
python scripts/run_cylinder_phase_diagram.py
python scripts/run_gap_scaling.py
python scripts/run_disk_phase_diagram.py
```

The scripts write generated data to `cases/1804.04672/outputs/data/`, figures to
`cases/1804.04672/outputs/figures/`, and checks to
`cases/1804.04672/outputs/checks/`.

## Generated Figures

![Fig. 1 open-boundary phase diagram](outputs/figures/fig1_open_boundary_phase.png)

![Fig. 2 square dynamics](outputs/figures/fig2_square_dynamics.png)

![Fig. 3(a) cylinder phase diagram](outputs/figures/fig3a_cylinder_phase.png)

![Fig. 3(b) cylinder complex spectrum](outputs/figures/first_target.png)

![Supplemental Fig. S2 gap-square scaling](outputs/figures/figs2_gap_scaling.png)

![Supplemental Fig. S3 disk phase diagram](outputs/figures/figs3_disk_phase.png)
