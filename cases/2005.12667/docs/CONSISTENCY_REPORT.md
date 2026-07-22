# Consistency Report

## Summary

| Class | Count | Meaning |
| --- | ---: | --- |
| paper-exact numeric targets | 9 | published parameters sufficient for the executed theory target |
| paper-subset targets | 5 | source omits some calibration/style/experimental inputs |
| analytic targets without absolute parameters | 4 | invariant and independent-solver comparison |
| scored targets passed | 18 | all structured artifacts and physics thresholds present |
| formula-only targets verified | 9 | T003, T004, T021-T027 |
| external blockers | 4 | one FEM set and three author-data experiment sets |

## Chapter-level consistency

| Section | Targets | Status | Strongest independent check |
| --- | --- | --- | --- |
| II | T005-T007, T021 | passed | transmon periodicity and $3.30\times10^{-6}$ dispersion suppression |
| III | T001-T003 | passed | JC machine precision; dispersive model versus 40D diagonalization |
| IV | T004, T022 | passed | Hermiticity, CPTP thermal evolution and $|r|=1$ |
| V | T008-T009, T023 | passed | SNR optimum converges to $2|\chi|/\kappa=1$ |
| VI | T010-T015, T024 | passed | exact $2g$ splitting, Bloch saturation and dressed-branch return |
| VII | T016-T018, T025 | passed/partial experiment | DRAG improvement, code loss conditions, Wigner negativity |
| VIII | T019-T020, T026 | passed/partial experiment | Wigner normalization and exact squeezing dB |
| Appendices | T027 | passed | main-text and appendix convention closure |

## Interpretation of the 90.28 score

The score is capped by evidence type, not by failed physics. Every scored item has independent numerical provenance, formula gate verified, artifact pass and data-backed status. Analytic source figures are capped at 90 because they do not supply an absolute plotting dataset; paper-subset targets are capped by missing calibration or experimental inputs. Table I is exact and scores 100.

The project therefore supports a full formula and numerical-feature reproduction claim. It does not support a claim that unavailable experimental acquisitions or COMSOL field solutions were reproduced.

## Cross-check highlights

| Invariant | Result |
| --- | ---: |
| JC eigenvalue residual | 0 |
| JC square-root splitting residual | $5.77\times10^{-15}$ |
| multilevel dispersive energy residual | $2.96\times10^{-6}$ |
| transmon periodicity error | $4.44\times10^{-15}$ GHz |
| thermal Lindblad mean-number error | $4.98\times10^{-11}$ |
| single-port passivity error | $3.33\times10^{-16}$ |
| avoided-crossing resonant split error | 0 |
| DRAG maximum norm error | $8.40\times10^{-10}$ |
| binomial equal-loss residual | $6.28\times10^{-16}$ |
| squeezed-state dB identity error | $1.78\times10^{-15}$ dB |

No accepted claim relies on visual similarity alone.
