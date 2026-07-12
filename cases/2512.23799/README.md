# 2512.23799: Efficient simulation of logical magic state preparation protocols

Paper: [Efficient simulation of logical magic state preparation protocols](https://arxiv.org/abs/2512.23799)

Public status: **Partial feature reproduction**

Audit score at export: **73.00/100**

Similarity level: `numerical_feature_reproduction`

Implements local fidelity, acceptance, runtime, and sampling-precision models for logical magic-state preparation.

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

Remaining limitation: The public package excludes digitized paper curves; several visible benchmark trends remain proxy or subset validations.

Final-parameter rule: final public figures use the paper parameters when feasible. Any reduced-scale, subset, proxy, or blocked target must be labeled explicitly and cannot be presented as a complete reproduction.

## Quick Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2512.23799/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
```

## Generated Figures

![fig1 infidelity reproduction](outputs/figures/fig1_infidelity_reproduction.png)

![fig2 acceptance reproduction](outputs/figures/fig2_acceptance_reproduction.png)

![fig3 runtime reproduction](outputs/figures/fig3_runtime_reproduction.png)

![fig4 sampling precision reproduction](outputs/figures/fig4_sampling_precision_reproduction.png)
