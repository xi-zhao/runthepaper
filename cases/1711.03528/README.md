# 1711.03528: Quantum many-body scars

Preprint: [arXiv:1711.03528 — Quantum many-body scars](https://arxiv.org/abs/1711.03528)

Published as: [Weak ergodicity breaking from quantum many-body scars](https://doi.org/10.1038/s41567-018-0137-5)

Formal citation: Nature Physics 14, 745–749 (2018) · DOI `10.1038/s41567-018-0137-5` · Locator `745–749`

Public status: **Symmetry-resolved partial reproduction** · Audit score: **72.50/100**

Reproduces constrained Hilbert-space structure, scar overlaps, revivals, participation ratios, and symmetry-resolved level statistics.

## Start Here / 从这里开始

- [中文复现 Note](note/reproduction-note.zh-CN.md)
- [English reproduction note](note/reproduction-note.en.md)
- [Code and run commands](code/README.md)
- [Machine-readable scorecard](outputs/checks/similarity_scorecard.json)
- [Completion assessment](outputs/checks/completion_assessment.json)
- [Numerical methods](docs/NUMERICAL_METHODS.md)
- [Lessons learned](docs/LESSONS_LEARNED.md)

## Quick Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/1711.03528/code
python scripts/run_reproduction.py
python scripts/plot_reproduction.py
python scripts/run_symmetry_resolved_sector.py
python scripts/plot_symmetry_resolved_sector.py  # replot saved L=28 data without rerunning ED
```

Generated files are kept under [data](outputs/data/), [figures](outputs/figures/), and [checks](outputs/checks/).

## Reproduction Boundary

This public case includes paper-derived code, generated data, generated figures, public validation checks, and explanatory notes. It does not redistribute the paper PDF, arXiv source archive, original figures, EPS paths, digitized source curves, source-derived point sets, or source-vs-generated composite panels.

The paper's `k=0, I=+1` sector is reproduced at `L=28` (dimension 13201), including the 15-state scar tower and unfolded level statistics. The `L=32` dense path was not launched: one float64 matrix is already about 47 GB before eigensolver workspace, beyond the current single 40 GB A100 path. Thermodynamic-limit iTEBD at bond dimension around 400 also remains unimplemented; the `L=16` exact-dynamics comparator stays explicitly labeled and is not counted as iTEBD completion.

Final-parameter rule: final public figures use the paper parameters when feasible. Any reduced-scale, subset, proxy, or blocked target must be labeled explicitly and cannot be presented as a complete reproduction.

## Generated Figures

![fig1 hilbert graph reproduction](outputs/figures/fig1_hilbert_graph_reproduction.png)

![fig2 special states reproduction](outputs/figures/fig2_special_states_reproduction.png)

![fig4 level statistics reproduction](outputs/figures/fig4_level_statistics_reproduction.png)

![fig ent dynamics reproduction](outputs/figures/fig_ent_dynamics_reproduction.png)

![sector level statistics](outputs/figures/sector_level_statistics.png)

![sector scar tower](outputs/figures/sector_scar_tower.png)
