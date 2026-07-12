# Reproduction report

## Current reproduction state

This case has started the full paper-story reproduction rather than only a single-figure proxy.

- Fig. 3 path-planning object: reduced pilot completed.
- Fig. 3 model object: reduced-scale 6-pass GNN retrained and saved as a reloadable checkpoint.
- Fig. 4 P2WGS continuity object: reduced pilot completed.
- Fig. 5 pipelined timing object: analytic model encoded and plotted.
- Software assembly object: one joined path-planning -> P2WGS -> timing run completed.
- Software assembly sweep: four joined-chain configurations completed for iterative quality tracking.
- Decoder baseline: the same sweep grid can be forced to Hungarian labels for zero-gap reference.
- Modified auction decoder: a CPU bidding version is implemented and connected to the same sweep grid.

## Generated outputs

- `../outputs/checks/retrained_gnn_model/model_state.pt`
- `../outputs/checks/retrained_gnn_model/training_history.json`
- `../outputs/checks/retrained_gnn_model/metrics.json`
- `../outputs/checks/software_assembly_pipeline/metrics.json`
- `../outputs/checks/software_assembly_sweep/metrics.json`
- `../outputs/checks/software_assembly_sweep_hungarian/metrics.json`
- `../outputs/checks/software_assembly_sweep_modified_auction/metrics.json`
- `../outputs/figures/fig3_reduced_gnn_metrics.png`
- `../outputs/figures/fig4_reduced_p2wgs_continuity.png`
- `../outputs/figures/fig5_reduced_timing_model.png`

## Main limitations

1. The retrained GNN checkpoint is not yet paper-scale. The paper uses `127 x 127` initial sites, `101 x 101` target sites, 1024 test instances, and million-scale training.
2. The modified auction decoder is a CPU reduced reconstruction, not the paper's GPU-parallel decoder implementation.
3. The P2WGS pilot is a public reduced reconstruction. The arXiv source does not include Zhuifeng.
4. The joined software assembly run is reduced scale and local-machine timed; it does not replace a measured RTX 5090 or A100 benchmark.

## Next loop step

The repair loop should next use the sweep table as the quality surface: the CPU modified-auction sweep now matches the score-Hungarian distance gaps, so the next improvement target is GNN score quality and scale rather than decoder wiring.
