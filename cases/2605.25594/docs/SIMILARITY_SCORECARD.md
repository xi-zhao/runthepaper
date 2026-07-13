# Similarity Scorecard

## Overall

- Overall score: `67.49/100`
- Level: `numerical_feature_reproduction`
- Check status: `partial`

The case barely enters the feature-level band. That is intentional: several local physical features are visible, but the paper's central peak positions and exponents need much larger systems.

## Figure-Level Scores

| Target | Score | Level | Main reason |
| --- | ---: | --- | --- |
| T001 Fig. 1 susceptibility vs disorder | 59 | feature not reproduced | Local trends appear, but the two paper-level peaks are not cleanly separated. |
| T002 Fig. 2 weak crossover | 61 | numerical feature reproduction | Low-W enhancement appears, but strict `41/sqrt(V)` scaling is not stable locally. |
| T003 Fig. 3 spectral function | 55 | feature not reproduced | Correct object is computed, but exponent/width fits require large systems. |
| T004 Fig. 8-11 localized regime | 66 | numerical feature reproduction | Average/typical separation and strong-disorder localization appear. |

## Why The Score Is Low

This paper is scale-sensitive. The formulas are straightforward to implement, but the main scientific claims depend on finite-size scaling:

- `W_1^*` needs large `V` to show clean `1/sqrt(V)` behavior.
- `W_2^*≈16.5` needs enough states and samples to produce a sharp susceptibility peak.
- `W_3^*≈27.92` needs dense `mu` sweeps and large `L`.

The current machine ran only `L<=7`, so the result is useful as a formula-and-feature proof, not as a full paper-level reproduction.

## Machine-Readable Record

See `outputs/checks/similarity_scorecard.json`.
