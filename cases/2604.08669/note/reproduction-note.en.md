# Reproduction report

## Current reproduction state

This case now includes a paper-geometry partial reproduction rather than only a reduced single-figure proxy.

- Fig. 3 path-planning object: reduced pilot completed.
- Fig. 3 model object: a reduced reloadable checkpoint plus an A100-SXM4-80GB paper-geometry campaign summary and 64-instance validation probe.
- Fig. 4 P2WGS continuity object: paper-scale `N=10201`, `1024×1024` reconstruction completed.
- Fig. 5 pipelined timing object: analytic model encoded and plotted.
- Software assembly object: one joined path-planning -> P2WGS -> timing run completed.
- Software assembly sweep: four joined-chain configurations completed for iterative quality tracking.
- Decoder baseline: the same sweep grid can be forced to Hungarian labels for zero-gap reference.
- Modified auction decoder: a CPU bidding version is implemented and connected to the same sweep grid.

## Generated outputs

- `../outputs/checks/retrained_gnn_model/model_state.pt`
- `../outputs/checks/retrained_gnn_model/training_history.json`
- `../outputs/checks/retrained_gnn_model/metrics.json`
- `../outputs/checks/a100_paper_geometry_campaign.json`
- `../outputs/checks/completion_assessment.json`
- `../outputs/checks/p2wgs_paper_scale.json`
- `../outputs/checks/software_assembly_pipeline/metrics.json`
- `../outputs/checks/software_assembly_sweep/metrics.json`
- `../outputs/checks/software_assembly_sweep_hungarian/metrics.json`
- `../outputs/checks/software_assembly_sweep_modified_auction/metrics.json`
- `../outputs/figures/fig3_reduced_gnn_metrics.png`
- `../outputs/figures/fig3_a100_paper_geometry_gap.png`
- `../outputs/figures/fig4_reduced_p2wgs_continuity.png`
- `../outputs/figures/fig4_paper_scale_p2wgs_summary.png`
- `../outputs/figures/fig5_reduced_timing_model.png`

## Main limitations

1. The A100 short probe uses paper geometry but not the paper's million-sample training and 1024-instance final evaluation. On val64 it misses the strict paper references by `0.006` in mean distance and `0.013` in maximum distance.
2. The modified auction decoder is a CPU reduced reconstruction, not the paper's GPU-parallel decoder implementation.
3. P2WGS reaches paper parameter scale and reproduces the phase claim, but the exact Zhuifeng frame-trajectory protocol is unavailable, so the 3-to-5 intensity improvement is not reproduced.
4. The joined software assembly run is reduced scale and local-machine timed; it does not replace a measured RTX 5090 or A100 benchmark.

## Next loop step

Do not start long training until a new metric-contract probe improves the average-distance gate without worsening the maximum-distance tail. The GPU decoder remains a separate implementation and hardware-performance project.
