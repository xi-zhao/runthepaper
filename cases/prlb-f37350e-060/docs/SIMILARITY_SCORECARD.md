# Similarity scorecard

| Target | Weight | Components | Cap | Score |
| --- | ---: | --- | ---: | ---: |
| `T_SOURCE_IDENTITIES` | 0.4 | 50/50 feature, 35/35 numeric, 13/15 scope | 90 (`analytic_reference`) | 90 |
| `T_BENCH_AUDIT` | 0.6 | 50/50 feature, 35/35 numeric, 7/15 scope | 80 (one reconstructed well-posedness formula) | 80 |

Weighted score: **84.0/100**, `numerical_feature_reproduction`. The source target is capped at 90 because it compares against analytic source identities rather than author arrays, and Fig. 4(c) remains blocked. The benchmark target is capped because Task 5 is under-specified and its nonuniqueness proof is reconstructed rather than a paper claim.
