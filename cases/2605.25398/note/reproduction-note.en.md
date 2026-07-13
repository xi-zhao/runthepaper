# Reproduction Report: 2605.25398

## Status

- Case status: `feature_reproduced`
- Similarity level: `numerical_feature_reproduction`
- Similarity score: `79.36/100`
- Main check status: `passed`

## What Was Reproduced

The case reproduced the theoretical/numerical part of the paper:

- random-matrix Hamiltonian interpolation between integrable and chaotic regimes;
- two-photon collision-free boson-sampling probability distribution;
- distance to Porter-Thomas statistics;
- Shannon entropy and Haar entropy reference;
- 4-point SFF feature timing;
- OTOC-equivalent output probabilities;
- participation ratio;
- conditional probability sanity check;
- short-time OTOC power laws;
- late-time FFT participation ratio;
- scaling trend with optical mode number.

## Main Feature Evidence

| Feature | Paper expectation | Local result | Status |
| --- | --- | --- | --- |
| PT distance | chaotic curve dips near `t*=1.79` | observed minimum `t=1.788` | passed |
| Entropy | chaotic curve peaks near `t*=1.79` | observed maximum `t=1.841` | passed |
| SFF | chaotic SFF minimum near `t*=1.79` | observed minimum `t=1.841` | passed |
| PR separation | chaotic PR much larger than integrable PR | `12.51` vs `1.05` at `t=1.79` | passed |
| Entropy separation | chaotic entropy much larger | `2.787` vs `0.144` at `t=1.79` | passed |
| Short-time OTOC | overlap-one `t^2`, overlap-zero `t^4` | slopes `1.999`, `3.999` | passed |
| FFT PR | chaotic frequency content broader | `146.13` vs `9.07` | passed |

Machine-readable check:

```text
outputs/checks/reproduction_feature_checks.json
```

## What Was Not Reproduced

- The physical photonic chip, optical setup, MZI mesh, and source characterization are not reproduced.
- The experimental red points in the paper figures are not reproduced because raw photon-count data are not included in the arXiv source.
- Author random seeds and exact matrix instances are not available, so exact curve identity is not claimed.

## Interpretation

The reproduction is scientifically meaningful because the paper's main theoretical claim is visible in independently generated data: chaotic boson-sampling statistics approach Porter-Thomas behavior, develop higher entropy, and spread over more collision-free output configurations than the integrable case.

The case should be described publicly as a strong feature-level reproduction, not as a complete reproduction of the full experiment.

## Files To Inspect

- Human introduction: `CASE_INTRO.md`
- Formula chain: `DERIVATION_TRACE.md`
- Numerical method: `NUMERICAL_METHODS.md`
- Scorecard: `SIMILARITY_SCORECARD.md`
- Code: `src/boson_sampling_chaos.py`
- Main generated figures: `../outputs/figures/`
