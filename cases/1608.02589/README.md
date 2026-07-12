# 1608.02589: Discrete time crystals: rigidity, criticality, and realizations

Paper: [Discrete time crystals: rigidity, criticality, and realizations](https://arxiv.org/abs/1608.02589)

Public status: **Reduced-scale feature reproduction**

Audit score at export: **73.56/100**

Similarity level: `numerical_feature_reproduction`

Reproduces subharmonic rigidity, level statistics, variance, long-range variance, and mutual-information features with exact local evolution.

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

Remaining limitation: Paper-scale disorder statistics and the largest exact-diagonalization targets remain compute-limited.

Final-parameter rule: final public figures use the paper parameters when feasible. Any reduced-scale, subset, proxy, or blocked target must be labeled explicitly and cannot be presented as a complete reproduction.

## Quick Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/1608.02589/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
python scripts/run_reproduction_iteration2.py
python scripts/plot_reproduction_iteration2.py
```

## Generated Figures

![fig1 subharmonic rigidity reproduction](outputs/figures/fig1_subharmonic_rigidity_reproduction.png)

![fig2 level statistics variance reproduction](outputs/figures/fig2_level_statistics_variance_reproduction.png)

![fig3 mutual information proxy reproduction](outputs/figures/fig3_mutual_information_proxy_reproduction.png)

![fig3 scaling collapse](outputs/figures/fig3_scaling_collapse.png)

![fig4 long range variance reproduction](outputs/figures/fig4_long_range_variance_reproduction.png)

![iteration2 fig1 L14 subharmonic rigidity](outputs/figures/iteration2_fig1_L14_subharmonic_rigidity.png)

![iteration2 fig1 phase boundary proxy](outputs/figures/iteration2_fig1_phase_boundary_proxy.png)

![iteration2 fig2 level statistics variance L10](outputs/figures/iteration2_fig2_level_statistics_variance_L10.png)

![iteration2 fig3 mutual information corrected](outputs/figures/iteration2_fig3_mutual_information_corrected.png)

![iteration2 fig4 long range variance L10](outputs/figures/iteration2_fig4_long_range_variance_L10.png)
