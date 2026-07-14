# Similarity scorecard

This scorecard is intentionally conservative. The case now has an A100 paper-geometry GNN short probe and paper-scale P2WGS, but it has not completed million-sample training or the GPU decoder.

| Target | Current level | Main cap |
| --- | --- | --- |
| T001 / Fig. 3 | Paper-geometry short-probe reproduction | val64 only, failed metric-contract gate, no GPU decoder |
| T002 / Fig. 4 | Paper-scale parameter reproduction | three stochastic samples, no exact Zhuifeng trajectory protocol |
| T003 / Fig. 5 | Timing model reproduction | analytic model only, no GPU timing campaign |
| T004 / Fig. 3-5 interface | Software assembly reproduction plus sweep | reduced scale, local timing only |

The normalized scorecard lives at `../outputs/checks/similarity_scorecard.json`.
