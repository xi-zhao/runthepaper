# 2502.20558 reproduction note: leveraging qubit-loss detection

## One-sentence result

This public case independently generates five figures and the analytic rows of
Table I, with an audit score of **74.22/100**. The printed Fig. 4(b) relation,
the complete Fig. 6(b) numerical bar panel, and the analytic lifecycle/overhead
rows of Table I are paper-exact targets. Figs. 2(b), 14(c), and 16(a) remain
explicit mechanism or paper-subset reproductions. This is not a complete
numerical reproduction of the paper.

Paper: [Physical Review X 16, 011002 (2026)](https://doi.org/10.1103/ycwc-3myc).
Preprint: [arXiv:2502.20558](https://arxiv.org/abs/2502.20558).

## Scientific model

Loss detection reveals which qubit lifecycle ended, but usually not the exact
time of the loss. The delayed-erasure decoder enumerates compatible loss
locations, cancels subsequent gates, constructs a detector-error hypergraph for
each possibility, and combines the models with their conditional weights. The
paper then uses lifecycle length as a compact architectural variable: shorter
lifecycles reduce the number of compatible loss locations and simplify the
decoding problem.

## Public reproduction targets

- **Fig. 2(b), 47.5:** a distance-five repetition-code analogue reproduces the
  information ordering between no SSR information and delayed-erasure
  decoding. It is an exploratory proxy, not the paper's surface-code MLE curve.
- **Fig. 4(b), 83.5:** independently evaluates the printed
  `7/lifecycle^(1/3)%` relation over the panel domain. The unavailable
  finite-size markers are excluded from the claim.
- **Fig. 6(b), 89.0:** reproduces all four average/maximum lifecycle pairs for
  GHZ, 15-to-1 distillation, H/T synthesis, and the adder.
- **Fig. 14(c), 80.0:** reproduces the all-qubit SWAP period invariant and its
  finite-distance trend, with a reconstructed boundary-round convention.
- **Fig. 16(a), 72.5:** reproduces the conventional data/measure trends and the
  all-qubit SWAP/conventional invariant. SWAP role-resolved subcurves remain
  open.
- **Table I, 80.0:** reproduces the analytic lifecycle and space-time rows for
  all seven methods. Simulation-derived threshold rows are deferred.

## Run the public code

From the RunThePaper repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2502.20558/code
python scripts/run_reproduction.py
```

The runner regenerates six CSV files, five independent figures, and target-level
JSON checks. It does not read paper pixels, digitized curves, or author data.

## Reproduction boundary

The released manuscript materials include 27 vector figure assets but no
surface-code circuit generator, correlated MLE implementation, raw samples,
shot counts, seeds, complete error grids, or fit windows. Nineteen of the 24
numeric panel/table groups therefore remain blocked by missing author data. The
case does not fill those targets by copying or digitizing published curves.

The limited comparison boards retain only the paper excerpts needed to inspect
the feature-level agreement. They clearly separate the paper reference from the
independent result and do not establish author-data-level or point-for-point
equivalence.
