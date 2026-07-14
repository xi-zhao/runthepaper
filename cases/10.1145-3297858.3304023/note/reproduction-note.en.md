# Reproduction Report

## What Was Reproduced

This pass reconstructs the core SABRE algorithm from the paper text. The
existing GitHub implementation was not used.

Current public label: `full_corpus_mechanism_reproduction`.

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
- all 26 Table II rows, with row-exact optimized values marked partial after a
  strict paper-parameter rerun with the imported original benchmark corpus.

## Main Checks

| Target | Status | Numeric feature checked |
| --- | --- | --- |
| T001 paper SWAP example | passed | 6 original CNOTs route with 1 SWAP, 3 additional CNOT-equivalent gates, depth 8 |
| T002 reverse traversal | passed | QFT-6/8/10 all improve or match first traversal on gate count and depth |
| T003 decay trade-off | passed first pass | Decay creates a shallower circuit at the cost of extra CNOT-equivalent gates |
| T004 Table II | full corpus / row-exact partial | All 26 rows run and are hardware compliant; the 2026-06-18 A100 1000-attempt rerun kept `g_op` exact matches at 7/26, so exact SABRE/BKA values still need missing metadata and baseline details |

## Comparison-figure difference reasons

- Fig. 3 trace: no residual difference; gate count, SWAP count, and depth match.
- Reverse traversal: the plot checks the same mechanism on QFT-6/8/10 rather
  than the paper's full benchmark mixture.
- Decay trade-off: the paper does not publish the complete Fig. 9 circuit mix
  and execution details, so the plot is a local sweep of the same mechanism.
- Table II: row-exact values require unpublished random seeds, tie-breaking
  order, and BKA post-processing inputs. The residual did not disappear after
  1000 attempts per row, so more compute alone cannot deterministically close it.

## Evidence Files

- `../outputs/checks/paper_swap_example.json`
- `../outputs/checks/core_benchmarks.json`
- `../outputs/checks/decay_tradeoff.json`
- `../outputs/data/paper_swap_example_ops.csv`
- `../outputs/data/core_benchmarks.csv`
- `../outputs/data/decay_tradeoff.csv`
- `../outputs/checks/table2_reproduction.json`
- `../outputs/checks/table2_seed_sensitivity.json`
- `../outputs/checks/completion_assessment.json`
- `../outputs/data/table2_reproduction.csv`
- `../outputs/figures/paper_swap_example_trace.png`
- `../outputs/figures/core_benchmarks_qft.png`
- `../outputs/figures/decay_tradeoff.png`
- `../outputs/figures/table2_gop_comparison.png`

## Important Limitation

The implementation is a faithful full-corpus reconstruction from the paper
text, but it is not yet a row-exact Table II reproduction. The 26 benchmark
inputs are present and `g_ori` matches 26/26 paper rows. The remaining mismatch is in the
optimized output columns, which depend on the paper's randomization policy,
tie-breaking choices, baseline implementation, transpilation choices, and
runtime environment. Those are not fully specified in the paper artifact we are
allowed to use.

The two-hour timing-bar rerun increased Table II search to `100` attempts per
row and improved `g_op` exact matches from 6/26 to 7/26. The 2026-06-18 A100
paper-parameter corpus rerun increased this again to `1000` attempts per row
with `16` workers, but `g_op` stayed at
7/26 exact matches and `g_la` exact matches dropped to 0/26 because the
best-of-1000 search often found values lower than the table value. This points
to missing randomization, tie-breaking, best-of-N policy, and BKA baseline
details rather than a simple local compute shortage. Under the paper's
best-of-5 protocol, 20/26 rows are exact or inside the seed-marginalized band;
the remaining six are ours-better, with zero paper-better rows.
