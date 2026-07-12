# 2604.08669: An Algorithm for Fast Assembling Large-Scale Defect-Free Atom Arrays

Paper: [An Algorithm for Fast Assembling Large-Scale Defect-Free Atom Arrays](https://arxiv.org/abs/2604.08669)

Public status: **Reduced-scale feature reproduction**

Audit score at export: **61.60/100**

Similarity level: `numerical_feature_reproduction`

Reproduces reduced path-planning, P2WGS continuity, and pipelined timing objects for atom-array assembly.

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

Remaining limitation: The paper-scale GNN training and GPU-parallel decoder are not included; the public code is a reduced reconstruction.

Final-parameter rule: final public figures use the paper parameters when feasible. Any reduced-scale, subset, proxy, or blocked target must be labeled explicitly and cannot be presented as a complete reproduction.

## Quick Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install torch
cd cases/2604.08669/code
python scripts/run_reduced_pilot.py
python scripts/run_reduced_p2wgs_pilot.py
python scripts/plot_reduced_outputs.py
```

## Generated Figures

![fig3 reduced gnn metrics](outputs/figures/fig3_reduced_gnn_metrics.png)

![fig4 reduced p2wgs continuity](outputs/figures/fig4_reduced_p2wgs_continuity.png)

![fig5 reduced timing model](outputs/figures/fig5_reduced_timing_model.png)
