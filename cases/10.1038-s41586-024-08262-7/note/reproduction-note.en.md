# Particle exchange statistics beyond fermions and bosons — reproduction note

## Paper identity

Zhiyuan Wang and Kaden R. A. Hazzard, *Particle exchange statistics beyond
fermions and bosons*, Nature **637**, 314–318 (2025), DOI
`10.1038/s41586-024-08262-7`; preprint arXiv:2308.05203.

The paper constructs nontrivial paraparticles that are physically inequivalent
to ordinary fermions and bosons. It develops their generalized exclusion
statistics, free-particle thermodynamics, second quantization, and local exactly
solvable spin-model realizations.

## Reproduction scope

This public case reproduces the paper's numerical main figure and adds an
independent validation of its underlying physics:

1. Generate the single-mode degeneracy sequences `d_n` for fermions, bosons,
   and the three paraparticle examples shown in the figure.
2. Evaluate the thermal occupation `<n>_beta` from the same closed-form
   single-mode partition functions.
3. Exact-diagonalize the paper's one-dimensional solvable spin model and compare
   its full many-body spectrum with the free-paraparticle prediction.

The final figure uses the published legend parameters: Ex.2 `m=2`, Ex.3 `m=2`,
and Ex.4 `m=3`. A separate main-text sentence states `m=5`; because the target is
the printed figure, the legend parameters define the reproduction contract.

## Core calculation

Let `d_n` be the dimension of the `n`-particle state space in one mode. The
single-mode partition function is

```text
z_R(x) = sum_n d_n x^n,    x = exp(-beta*epsilon),
```

and the thermal occupation follows without fitting:

```text
<n>_beta = x z'_R(x) / z_R(x).
```

The reproduced species use `z=1+x` (fermion), `z=1/(1-x)` (boson),
`z=(1+x)^2` (Ex.2), `z=1+2x` (Ex.3), and `z=1+3x+x^2` (Ex.4). The code checks
the exact integer degeneracies and the analytic limiting values to `1e-9`.

## Independent exact-diagonalization check

For the one-dimensional Ex.3 spin model, the predicted many-body spectrum is

```text
E = sum_{k in S} epsilon_k,    multiplicity = m^|S|.
```

Brute-force diagonalization for `N=4,5, m=2` and `N=4, m=3` matches this full
spectrum to approximately `1e-14`; the conserved-number commutator also vanishes
to machine precision. This independently connects the plotted Hilbert series
`z_R=1+mx` to a local exactly solvable model.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1038-s41586-024-08262-7/code
python scripts/gen_fig2.py
python scripts/run_ed_validation.py
```

Generated CSV data, the reproduction figure, and machine-readable checks are
written under `../outputs/`.

## Status and boundary

Public status: **Complete reproduction**. Audit score: **90/100**. The score
measures evidence coverage, not a percentage of physical correctness or a
cross-paper ranking.

The score is capped because the Nature figure is raster-only and no author data
table is available. The strongest public evidence is therefore analytic
agreement with the paper's closed-form expressions plus independent exact
diagonalization, rather than pointwise residuals against author plotting data.
The two-dimensional KDH model, eight-body plaquette terms, and braiding
demonstration remain outside this case's scope.

See [`../docs/DERIVATION_WALKTHROUGH.zh-CN.md`](../docs/DERIVATION_WALKTHROUGH.zh-CN.md)
for the full Chinese derivation and [`../docs/SIMILARITY_SCORECARD.md`](../docs/SIMILARITY_SCORECARD.md)
for the scoring evidence.
