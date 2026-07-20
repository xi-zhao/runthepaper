# Similarity scorecard

Overall: **83.6 / 100**, `numerical_feature_reproduction`.

| Target | Weight | Raw components | Evidence cap | Final score |
| --- | ---: | --- | --- | ---: |
| `T_SOURCE_EXTRAPOLATION` | 0.4 | 48/50 feature, 34/35 numeric, 13/15 scope | 89: `paper_subset` and mixed source/independent provenance | 89 |
| `T_BENCH_AUDIT` | 0.6 | 50/50 feature, 35/35 numeric, 7/15 paper scope | 80: benchmark-added dual/Gaussian formulas are `reconstructed` | 80 |

Both artifacts pass, both are data-backed, and there were zero manual numeric
interventions. Both remain `exploratory`; neither is eligible for the
`final_reproduction` label. The complete machine record is
`outputs/checks/similarity_scorecard.json`.
