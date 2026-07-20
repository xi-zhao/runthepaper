# Similarity scorecard

## Source target: 89/100 before evidence caps

- feature match: 48/50
- numeric closeness: 34/35
- paper scope coverage: 7/15

The target is capped by `parameter_match=paper_subset`. It covers one branch of one supplemental panel, so it must not be presented as a full-paper reproduction.

## Benchmark audit: 90/100 audit completeness

- feature match: 50/50
- numeric closeness: 35/35
- paper scope coverage: 5/15

This high audit-completeness score does not rescue the benchmark: the target status is `failed` because the expected answers are false under their own rules.

Overall machine status: `failed`, reflecting benchmark-gold validity rather than source-paper validity. The authoritative structured scorecard is `outputs/checks/similarity_scorecard.json`.
