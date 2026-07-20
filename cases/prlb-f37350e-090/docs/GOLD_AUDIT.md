# Frozen-gold audit

| Task | Verdict | Reason |
|---|---|---|
| 1 | invalid | pole decomposition has the opposite sign |
| 2 | invalid | delta weight inherits the wrong sign |
| 3 | invalid | radial prefactor is low by four |
| 4 | valid | ordinary simple-pole integral diverges logarithmically |
| 5 | invalid | subtraction fails to cancel the pole; edge rate is not uniquely determined |
| 6 | valid | finite orthogonal residue is killed by the inverse Puiseux slope |
| 7 | invalid | literal decay is zero; excitation is `0.172290279130...`, not `0.02153628...` |

Terminal verdict: `benchmark_gold_invalid`. This is a benchmark transcription/method failure, not a rejection of the source paper's convention-consistent qualitative claim.
