# Similarity Scorecard

## Overall

- Overall score: `73.00/100`
- Level: `feature_not_accepted`
- Check status: `passed`

The result is not accepted as paper-figure reproduction under the original-parameter gate. Formula and method checks are useful, but the benchmark curves come from a proxy model rather than the paper's exact Steane circuit and benchmark parameters.

## Figure-Level Scores

| Target | Score | Level | Main reason |
| --- | ---: | --- | --- |
| T001 Infidelity benchmark | 55 | feature not reproduced | Proxy-model trend appears, but the exact Steane benchmark was not run. |
| T002 Acceptance benchmark | 35 | feature not reproduced | Only monotone decrease is retained. The original curve drops much faster, especially near `p=1e-2`. |
| T003 Runtime benchmark | 55 | feature not reproduced | Low-`p` speedup is only proxy timing, not author Stim/Cirq benchmark timing. |
| T004 Formula and sampling gate | 84 | numerical feature reproduction | Formula checks pass and sampling error scales correctly. |

## Why It Is Not Complete

Complete reproduction would require one of these:

- author benchmark CSV/code;
- faithful Steane flag-gadget implementation with the paper's Stim/Cirq settings;
- digitized curves plus a stated digitization tolerance.

None of those are present in the current arXiv source package.

## Machine-Readable Record

See `outputs/checks/similarity_scorecard.json`.
