# 2604.08669 reduced-scale reproduction pilot

Paper: "An Algorithm for Fast Assembling Large-Scale Defect-Free Atom Arrays".

This case targets the paper's two-stage algorithm: the GNN path planner and the
P2WGS potential generator. The private Zhuifeng package is not included in the
arXiv source, so the current implementation is an independent public
reconstruction.

The current reduced-scale path-planning chain is:

1. Randomly generate occupied atom sites and target sites.
2. Use the Hungarian algorithm to create optimal assignment labels.
3. Build a candidate graph with atom-target, atom-atom, and target-target edges.
4. Train a lightweight message-passing edge scorer.
5. Decode edge scores with either score-Hungarian or CPU modified-auction assignment.
6. Compare predicted and optimal max/average movement distances.

The current reduced-scale P2WGS chain is:

1. Use the assignment to generate straight-line atom trajectories.
2. Represent each moving tweezer as a Gaussian target profile.
3. Iterate between SLM and tweezer planes with FFT/iFFT.
4. Enforce target amplitude and phase on the tweezer support.
5. Measure intensity and phase continuity between consecutive frames.

The software-only assembly chain now joins those pieces:

1. Generate one stochastic loading instance.
2. Decode an atom-to-target assignment from the local GNN checkpoint when it is
   available, otherwise fall back to Hungarian labels.
3. Reuse that assignment as the moving-tweezer trajectory input for P2WGS.
4. Feed the measured P2WGS frame-generation time into the pipelined assembly
   timing model.

Current status: reduced-scale pilots completed for Fig. 3, Fig. 4, and the
Fig. 5 timing model; one joined software-only path-planning -> P2WGS -> timing
run is available at
`../outputs/checks/software_assembly_pipeline/metrics.json`.

The first reproducibility sweep is available at
`../outputs/checks/software_assembly_sweep/metrics.json`. It runs the
same joined chain across two target counts and two P2WGS iteration counts, so
future loop steps can track whether assignment gaps, continuity metrics, and
assembly timing improve or degrade as scale changes.

A matching Hungarian-label baseline is available at
`../outputs/checks/software_assembly_sweep_hungarian/metrics.json`. It
uses the same sweep grid with zero assignment-distance gap by construction, so
decoder changes can be compared against a fixed reference.

A CPU modified-auction decoder sweep is available at
`../outputs/checks/software_assembly_sweep_modified_auction/metrics.json`.
It uses the same GNN checkpoint and sweep grid as the score-Hungarian decoder.
