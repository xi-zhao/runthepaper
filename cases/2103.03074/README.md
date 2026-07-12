# 2103.03074: Simulating the Sycamore quantum supremacy circuits

Paper: [Simulating the Sycamore quantum supremacy circuits](https://arxiv.org/abs/2103.03074)

Public status: **Reduced-scale feature reproduction**

Audit score at export: **70.00/100**

Similarity level: `numerical_feature_reproduction`

Reproduces batch-probability, post-selection XEB, conditional-probability, and complexity-table features.

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

Remaining limitation: Exact 53-qubit tensor contractions and paper-scale amplitude recomputation require external compute.

Final-parameter rule: final public figures use the paper parameters when feasible. Any reduced-scale, subset, proxy, or blocked target must be labeled explicitly and cannot be presented as a complete reproduction.

## Quick Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2103.03074/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
```

## Generated Figures

![fig2 depth20 reproduction](outputs/figures/fig2_depth20_reproduction.png)

![fig5 depth14 reproduction](outputs/figures/fig5_depth14_reproduction.png)

![fig6 conditional probability reproduction](outputs/figures/fig6_conditional_probability_reproduction.png)

![table2 method comparison reproduction](outputs/figures/table2_method_comparison_reproduction.png)
