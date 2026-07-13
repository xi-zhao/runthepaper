# Reproduction Report

## What Was Reproduced

This pass reconstructs the core SABRE algorithm from the paper text. The
existing GitHub implementation was not used.

Current local label: `feature_reproduced_large_scale_blocked`.

Similarity score: `68.29/100` (`numerical_feature_reproduction`).

The reproduced object is not a physics formula plot. It is an algorithmic
pipeline:

```text
input circuit + hardware coupling graph
-> logical-to-physical mapping
-> inserted SWAPs
-> hardware-compliant routed circuit
-> gate count, depth, and trade-off data
```

## Figure and Result Scope

Most figures in the paper are explanatory diagrams. The numeric targets are:

- the Fig. 3 SWAP example, used as a small correctness trace;
- Algorithm 1, implemented as the main router;
- Fig. 5 reverse traversal, checked through QFT-style benchmark circuits;
- Fig. 7 and Fig. 9 decay trade-off behavior, checked through a seeded local
  circuit sweep;
- Table II, marked partial after a strict paper-parameter rerun with the
  imported original benchmark corpus.

## Main Checks

| Target | Status | Numeric feature checked |
| --- | --- | --- |
| T001 paper SWAP example | passed | 6 original CNOTs route with 1 SWAP, 3 additional CNOT-equivalent gates, depth 8 |
| T002 reverse traversal | passed | QFT-6/8/10 all improve or match first traversal on gate count and depth |
| T003 decay trade-off | passed first pass | Decay creates a shallower circuit at the cost of extra CNOT-equivalent gates |
| T004 Table II | strict rerun / partial | Imported corpus validates inputs; the 2026-06-18 A100 1000-attempt rerun kept `g_op` exact matches at 7/26, so exact SABRE/BKA values still need missing metadata and baseline details |

## Evidence Files

- `../outputs/checks/paper_swap_example.json`
- `../outputs/checks/core_benchmarks.json`
- `../outputs/checks/decay_tradeoff.json`
- `../outputs/data/paper_swap_example_ops.csv`
- `../outputs/data/core_benchmarks.csv`
- `../outputs/data/decay_tradeoff.csv`
- `../outputs/figures/paper_swap_example_trace.png`
- `../outputs/figures/core_benchmarks_qft.png`
- `../outputs/figures/decay_tradeoff.png`
- `PLANNED_LARGE_SCALE_RUNS.md`
- `config/table2_exact_reproduction_recommended.yaml`

## Important Limitation

The implementation is a faithful reconstruction from the paper text, but this
is not yet an exact Table II reproduction. The 26 benchmark inputs are now
present and `g_ori` matches 26/26 paper rows. The remaining mismatch is in the
optimized output columns, which depend on the paper's randomization policy,
tie-breaking choices, baseline implementation, transpilation choices, and
runtime environment. Those are not fully specified in the paper artifact we are
allowed to use.

The refreshed harness flow records this as a planned large-scale/exactness
target rather than a vague blocker. The two-hour timing-bar rerun increased
Table II search to `100` attempts per row and improved `g_op` exact matches
from 6/26 to 7/26. The 2026-06-18 A100 paper-parameter corpus rerun increased
this again to `1000` attempts per row with `16` workers, but `g_op` stayed at
7/26 exact matches and `g_la` exact matches dropped to 0/26 because the
best-of-1000 search often found values lower than the table value. This points
to missing randomization, tie-breaking, best-of-N policy, and BKA baseline
details rather than a simple local compute shortage.
