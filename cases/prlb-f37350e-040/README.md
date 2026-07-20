# prlb-f37350e-040: Nonlinear Stage of Modulational Instability in Repulsive Two-Component Bose-Einstein Condensates

Preprint: [arXiv:2412.17083v2 — Nonlinear Stage of Modulational Instability in Repulsive Two-Component Bose-Einstein Condensates](https://arxiv.org/abs/2412.17083v2)

Published as: [Nonlinear Stage of Modulational Instability in Repulsive Two-Component Bose-Einstein Condensates](https://doi.org/10.1103/6jsr-f8q1)

Formal citation: Physical Review Letters 135, 113401 (2025) · DOI `10.1103/6jsr-f8q1` · Locator `113401`

Public status: **Equation-level numerical feature reproduction** · Audit score: **80.00/100**

Recomputes the benchmark selection rule and modulational-instability wedge directly from the source equations, with independent analytic and numerical checks.

## Start Here / 从这里开始

- [中文复现 Note](note/reproduction-note.zh-CN.md)
- [English reproduction note](note/reproduction-note.en.md)
- [Formula verification](docs/FORMULA_VERIFICATION.md)
- [Benchmark gold audit](docs/GOLD_AUDIT.md)
- [Source identity audit](docs/SOURCE_AUDIT.md)
- [Code and run commands](code/README.md)
- [Machine-readable scorecard](outputs/checks/similarity_scorecard.json)
- [Derivation (equations)](docs/DERIVATION.md)
- [Numerical methods](docs/NUMERICAL_METHODS.md)
- [Lessons learned](docs/LESSONS_LEARNED.md)

## Main Reproduced Results

| Paper item | Reproduced result | Figure | Check |
| --- | --- | --- | --- |
| Modulational-instability selection rule | Analytic wedge and frozen-answer consistency map | [PNG](outputs/figures/idx40_selection_rule_audit.png) | [JSON](outputs/checks/gold_audit_check.json) |

### Modulational-instability selection rule: Analytic wedge and frozen-answer consistency map

![Modulational-instability selection rule reproduction](outputs/figures/idx40_selection_rule_audit.png)

## Quick Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/prlb-f37350e-040/code
python scripts/run_gold_audit.py
python scripts/render_idx40_audit.py
```

Generated files are kept under [data](outputs/data/), [figures](outputs/figures/), and [checks](outputs/checks/).

## Reproduction Boundary

This public case includes paper-derived code, generated data, generated figures, public validation checks, and explanatory notes. It does not redistribute the paper PDF, arXiv source archive, original figures, EPS paths, digitized source curves, source-derived point sets, or source-vs-generated composite panels.

Remaining limitation: The source equations and benchmark observables are reproduced, but paper-panel curves are not claimed because the author simulation arrays and full evolution metadata are unavailable.

Final-parameter rule: final public figures use the paper parameters when feasible. Any reduced-scale, subset, proxy, or blocked target must be labeled explicitly and cannot be presented as a complete reproduction.
