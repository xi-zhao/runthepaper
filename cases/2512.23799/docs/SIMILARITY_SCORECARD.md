# Similarity Scorecard

## Overall

- Overall score: `73.00/100`
- Level: `numerical_feature_reproduction`
- Public status: `exact_circuit_partial_reproduction`
- Check status: `passed`

T001/T002 are now backed by the reconstructed exact Steane circuit rather than the earlier proxy model. The score remains limited by the declared mid-range infidelity residual and by proxy-only runtime evidence.

## Figure-Level Scores

| Target | Score | Level | Main reason |
| --- | ---: | --- | --- |
| T001 Infidelity benchmark | 75 | numerical feature reproduction | Exact protocol matches the trend and edge regimes; the mid-range remains `0.42-0.68x` of the paper curve. |
| T002 Acceptance benchmark | 80 | numerical feature reproduction | All 12 internally digitized validation points pass. |
| T003 Runtime benchmark | 55 | feature not accepted | Local proxy timing cannot reproduce author wall-clock values. |
| T004 Formula and sampling gate | 84 | numerical feature reproduction | Formula, stabilizer, decoding, and sampling checks pass. |

## Remaining Boundary

- The paper does not publish the exact panel-(c) gate/idle schedule or simulation code needed to resolve the second-order infidelity coefficient.
- Author wall-clock timing depends on unavailable hardware and software metadata.
- Digitized source point sets are not redistributed.

See `outputs/checks/similarity_scorecard.json` and `outputs/checks/completion_assessment.json`.
