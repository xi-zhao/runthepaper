# 2103.03074: Simulating the Sycamore quantum supremacy circuits

Preprint: [arXiv:2103.03074 — Simulating the Sycamore quantum supremacy circuits](https://arxiv.org/abs/2103.03074)

Published as: [Simulation of Quantum Circuits Using the Big-Batch Tensor Network Method](https://doi.org/10.1103/PhysRevLett.128.030501)

Formal citation: Physical Review Letters 128, 030501 (2022) · DOI `10.1103/PhysRevLett.128.030501` · Locator `030501`

Public status: **Compute-bounded feature reproduction** · Audit score: **70.00/100**

Reproduces batch-probability, post-selection XEB, conditional-probability, and complexity-table features.

## Start Here / 从这里开始

- [中文复现 Note](note/reproduction-note.zh-CN.md)
- [English reproduction note](note/reproduction-note.en.md)
- [Code and run commands](code/README.md)
- [Machine-readable scorecard](outputs/checks/similarity_scorecard.json)
- [Machine-readable completion boundary](outputs/checks/completion_assessment.json)
- [Numerical methods](docs/NUMERICAL_METHODS.md)
- [Lessons learned](docs/LESSONS_LEARNED.md)

## Quick Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2103.03074/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
```

Generated files are kept under [data](outputs/data/), [figures](outputs/figures/), and [checks](outputs/checks/).

## Reproduction Boundary

This public case includes paper-derived code, generated data, generated figures, public validation checks, and explanatory notes. It does not redistribute the paper PDF, arXiv source archive, original figures, EPS paths, digitized source curves, source-derived point sets, or source-vs-generated composite panels.

Remaining limitation: The exact 53-qubit contraction is not launched: the paper reports 4.51e18 head-contraction operations and 149 days on one A100, while a direct complex128 statevector would require 128 PiB. The public case also lacks the original circuit, contraction path, slicing configuration, and validation-amplitude bundle.

Final-parameter rule: final public figures use the paper parameters when feasible. Any reduced-scale, subset, proxy, or blocked target must be labeled explicitly and cannot be presented as a complete reproduction.

## Generated Figures

![fig2 depth20 reproduction](outputs/figures/fig2_depth20_reproduction.png)

![fig5 depth14 reproduction](outputs/figures/fig5_depth14_reproduction.png)

![fig6 conditional probability reproduction](outputs/figures/fig6_conditional_probability_reproduction.png)

![table2 method comparison reproduction](outputs/figures/table2_method_comparison_reproduction.png)
