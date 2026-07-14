# Numerical methods

## Core solver

The public reproduction uses dense Hermitian eigendecomposition in conserved
particle-number sectors. The largest matrix is only `78 x 78`; stochastic
sampling and GPU hardware are unnecessary. NumPy is the reference backend, and
the same domain implementation was separately checked against a CuPy/A100 run.
The worst absolute backend difference across five structured signatures was
`1.08e-14`.

## One-photon targets

- Open chain with the first ten calibrated nearest-neighbour couplings.
- Initial launches at Q6, Q1, and Q11.
- Time grid from 0 to 250 ns in 0.5 ns steps.
- Outputs: density, one-site entropy, connected correlation, concurrence, and
  root-mean-square displacement.
- Checks: norm and density conservation, exact initial states, observable
  bounds, and the reported propagation-velocity scale.

## Two-photon targets

- Twelve calibrated couplings and on-site anharmonicities.
- Initial launches Q1+Q12 and Q6+Q7.
- Calibrated, `U=0`, and hard-core models.
- Full time grid plus snapshots at 10.5, 19.5, 28.5, 37.5, 46.5, and 55.5 ns.
- Checks: norm, total density 2, `sum_ij G_ij=2`, suppressed double occupancy,
  and proximity of the strong-interaction pattern to the hard-core limit.

## Reproducibility contract

Run `python scripts/run_reproduction.py` from the case's `code` directory. The
script writes CSV arrays, machine-readable JSON checks, and four overview PNG
figures to the sibling `outputs` directory. All acceptance rules are evaluated
from numerical arrays before plotting.
