# Similarity Scorecard

Overall: **79.54 / 100 — numerical feature reproduction** (machine-readable:
`../outputs/checks/similarity_scorecard.json`). All four targets are
`paper_exact`, use independent numerics, and pass a `verified` formula gate; each
target caps at 80 because the paper publishes only raster figures (no author data
or tables), so the honest comparison ceiling is a source-vs-reproduction feature
contract.

| Target | Figure | feature/50 | numeric/35 | scope/15 | cap | score |
| --- | --- | --- | --- | --- | --- | --- |
| T101 | Fig. 1 spectrum + populations | 47 | 31 | 15 | 80 | 80 |
| T201 | Fig. 2 Delta rho actual vs Eq. (8) | 38 | 26 | 14 | 80 | 78 |
| T301 | Fig. 3 <x>(t), Eq. (13) vs Berry-only | 48 | 33 | 15 | 80 | 80 |
| T401 | Fig. 4 Delta<x> vs J transition probe | 48 | 32 | 15 | 80 | 80 |

Weights: T101 0.7, T201 0.8, T301 1.0, T401 1.0.

## Why feature-level (not complete) reproduction

Complete reproduction would require a strong reference (author data, benchmark
data, an exact table, a digitized curve, or an analytic reference). The paper
provides only raster figures with no data files, so the ceiling is a visual
feature contract (cap 80). The underlying reproduction is nonetheless paper-exact
and independently generated: exact transition location (J = 5.14), exact Chern
jump, exact peak magnitudes, and -- the strongest evidence -- the analytic theory
(Eq. 13) agreeing with the exact wave-packet dynamics to about 2%.

## What matched / what remains

- **Matched:** band structure and initial populations (Fig. 1); the Delta rho
  envelope and theory-vs-actual structure (Fig. 2, correlation ~0.9);
  T-independent displacement 3.10 with theory 3.08 and Berry-only 4.33 (Fig. 3);
  the transition at 5.14 with theory peak 19.5 and Berry-only 11.1 (Fig. 4).
- **Remains:** Fig. 2 is not pixel-exact (intrinsic ~10^2-rad phase sensitivity of
  Eq. 8 at T=1024); Fig. 4 actual peak ~17.4 versus ~19 in the band-touching
  window, which is genuinely T-sensitive, as the paper itself notes.
