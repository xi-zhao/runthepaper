# Frozen gold audit

| Task | Frozen answer | Independent result | Verdict |
| --- | --- | --- | --- |
| 1 | both boundary defects always present | top defect iff `N=M_s`; bottom defect iff `M_r=N`; neither exists in the paper's strict regime | invalid |
| 2 | projected mixed CAR is exact | exact; maximum physical-matrix residual 0 | valid |
| 3 | `<Q†Q>=1/4` | exactly 0 because `Q` annihilates every 0/2-particle component | invalid |
| 4 | `<Y>(lambda)=-cos(lambda)` | `Xi|psi>=0`, hence the kick is trivial and `<Y>=+1`, `Theta=pi` | invalid |
| 5 | `A(lambda)=0` | underdetermined: two unitary extensions satisfying the stated `U|psi>=i|psi>` give `+/- exp(-i lambda)` | invalid as a uniquely graded task |

The record is `benchmark_gold_invalid`. The repaired Task 1 must include equality indicators; Task 3 should be zero; Task 4 should be constant; Task 5 must specify the physical cycle or its action on all relevant error-syndrome sectors.
