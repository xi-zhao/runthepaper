# 1711.03528: Quantum many-body scars

Paper: [Quantum many-body scars](https://arxiv.org/abs/1711.03528)

Public status: **Reduced-scale feature reproduction** · Audit score: **72.50/100**

Reproduces constrained Hilbert-space structure, scar overlaps, revivals, participation ratios, and symmetry-resolved level statistics.

## Start Here / 从这里开始

- [中文复现 Note](note/reproduction-note.zh-CN.md)
- [English reproduction note](note/reproduction-note.en.md)
- [Code and run commands](code/README.md)
- [Machine-readable scorecard](outputs/checks/similarity_scorecard.json)
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
```

Generated files are kept under [data](outputs/data/), [figures](outputs/figures/), and [checks](outputs/checks/).

## Reproduction Boundary

This public case includes paper-derived code, generated data, generated figures, public validation checks, and explanatory notes. It does not redistribute the paper PDF, arXiv source archive, original figures, EPS paths, digitized source curves, source-derived point sets, or source-vs-generated composite panels.

Remaining limitation: The full L=32 symmetry sector and thermodynamic-limit iTEBD calculations are not rerun.

Final-parameter rule: final public figures use the paper parameters when feasible. Any reduced-scale, subset, proxy, or blocked target must be labeled explicitly and cannot be presented as a complete reproduction.

## Generated Figures

![fig1 hilbert graph reproduction](outputs/figures/fig1_hilbert_graph_reproduction.png)

![fig2 special states reproduction](outputs/figures/fig2_special_states_reproduction.png)

![fig4 level statistics reproduction](outputs/figures/fig4_level_statistics_reproduction.png)

![fig ent dynamics reproduction](outputs/figures/fig_ent_dynamics_reproduction.png)

![sector level statistics](outputs/figures/sector_level_statistics.png)

![sector scar tower](outputs/figures/sector_scar_tower.png)
