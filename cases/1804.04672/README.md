# 1804.04672: Non-Hermitian Chern bands

Paper: [Non-Hermitian Chern bands](https://arxiv.org/abs/1804.04672)

Public status: **Feature-level reproduction**

Audit score at export: **80.18/100**

Similarity level: `numerical_feature_reproduction`

Reproduces open-boundary and cylinder phase structure, square dynamics, complex spectra, and finite-size checks.

## Start Here / 上手讲义

- [中文上手讲义](note/reproduction-note.zh-CN.md)
- [English getting-started note](note/reproduction-note.en.md)
- [Bilingual note index](note/reproduction-note.md)
- [Code and run commands](code/README.md)
- [Machine-readable scorecard](outputs/checks/similarity_scorecard.json)
- [Numerical methods](docs/NUMERICAL_METHODS.md)
- [Lessons learned](docs/LESSONS_LEARNED.md)

## Public Boundary

This public case includes paper-derived code, generated data, generated figures, public validation checks, and explanatory notes. It does not redistribute the paper PDF, arXiv source archive, original figures, EPS paths, digitized source curves, source-derived point sets, or source-vs-generated composite panels.

Remaining limitation: Some phase-boundary and panel-level comparisons remain paper-subset or source-table validations rather than full independent finite-size reruns.

Final-parameter rule: final public figures use the paper parameters when feasible. Any reduced-scale, subset, proxy, or blocked target must be labeled explicitly and cannot be presented as a complete reproduction.

## Quick Run

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

## Generated Figures

![edge branch diagnostic](outputs/figures/edge_branch_diagnostic.png)

![fig1 open boundary phase](outputs/figures/fig1_open_boundary_phase.png)

![fig2 square dynamics](outputs/figures/fig2_square_dynamics.png)

![fig3a cylinder phase](outputs/figures/fig3a_cylinder_phase.png)

![figs2 gap scaling](outputs/figures/figs2_gap_scaling.png)

![figs3 disk phase](outputs/figures/figs3_disk_phase.png)

![first target](outputs/figures/first_target.png)
