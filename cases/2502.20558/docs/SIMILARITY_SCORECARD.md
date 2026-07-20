# Similarity Scorecard

## Case Score

- Overall score: **74.22 / 100**.
- Similarity level: **numerical feature reproduction**.
- Interpretation: six independently generated targets pass their own physics
  checks, including three final paper-exact analytic artifacts. The central
  surface-code Monte Carlo claim remains a proxy because author code/data are
  unavailable.

## Figure Scores

| Target | Paper item | Score | Stage | Parameter match | Main limitation |
| --- | --- | ---: | --- | --- | --- |
| T001 | Fig. 2(b) | 47.5 | exploratory | proxy_model | absolute surface-code MLE curve not reproduced |
| T002 | Fig. 4(b) | 83.5 | final_reproduction | paper_exact | finite-size markers unavailable |
| T003 | Fig. 6(b) | 89.0 | final_reproduction | paper_exact | source-only formula cap |
| T004 | Fig. 14(c) | 80.0 | exploratory | paper_subset | boundary-round convention reconstructed |
| T005 | Fig. 16(a) | 72.5 | exploratory | paper_subset | SWAP role-resolved subcurves open |
| T006 | Table I analytic rows | 80.0 | final_reproduction | paper_exact | simulation rows deferred |

The score evaluates scientific features and numeric evidence. It does not award
credit for copying source panels or digitizing curves. Machine-readable scoring,
component reasons, caps, and physics assertions live in
`outputs/checks/similarity_scorecard.json`.

## What Prevents A Higher Score

- 19 of 24 numeric panel/table groups remain `deferred_blocked`.
- The arXiv source supplies vector plot assets but no raw samples or code.
- The paper does not disclose shots, seeds, fit windows, complete physical-error
  grids, or the exact circuit/decoder revision.
- The only local Monte Carlo is a clearly labeled repetition-code mechanism
  proxy and cannot establish the paper's absolute surface-code performance.
