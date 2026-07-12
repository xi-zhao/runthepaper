# 2605.25398: Boson Sampling as a Probe of Chaotic and Integrable Quantum Dynamics

Paper: [Boson Sampling as a Probe of Chaotic and Integrable Quantum Dynamics](https://arxiv.org/abs/2605.25398)

Public status: **Feature-level reproduction**

Audit score at export: **79.36/100**

Similarity level: `numerical_feature_reproduction`

Reproduces Porter-Thomas distance, entropy, spectral-form-factor, OTOC, participation-ratio, and scaling features.

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

Remaining limitation: Several figures use paper-parameter subsets or local random-matrix instances rather than the full experimental setting.

Final-parameter rule: final public figures use the paper parameters when feasible. Any reduced-scale, subset, proxy, or blocked target must be labeled explicitly and cannot be presented as a complete reproduction.

## Quick Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2605.25398/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
```

## Generated Figures

![fig2 output distribution reproduction](outputs/figures/fig2_output_distribution_reproduction.png)

![fig3 main probes reproduction](outputs/figures/fig3_main_probes_reproduction.png)

![fig4 otoc pr reproduction](outputs/figures/fig4_otoc_pr_reproduction.png)

![figS1 conditional probability reproduction](outputs/figures/figS1_conditional_probability_reproduction.png)

![figS4 scaling reproduction](outputs/figures/figS4_scaling_reproduction.png)

![figS5 ideal otocs reproduction](outputs/figures/figS5_ideal_otocs_reproduction.png)

![figS6 extra otoc reproduction](outputs/figures/figS6_extra_otoc_reproduction.png)
