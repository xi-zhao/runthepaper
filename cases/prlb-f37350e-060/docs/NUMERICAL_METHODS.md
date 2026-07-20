# Numerical methods

All calculations use complex128 dense matrices in the occupation-number basis. Jordan-Wigner signs are generated from the parity of lower-index occupied modes. The largest physical model uses 8 modes (`M_s=3,N=4,M_r=5`), hence dimension 256; the referenced subspace has dimension 8.

No referenced CAR or projected reference identity is assumed. The code constructs physical operators first, generates the eight states by applying `c_i†=s_i†R` to `Omega`, verifies their Gram matrix, and only then compresses operators. Four parameter regimes isolate the strict interior, both boundaries, the top boundary alone, and the bottom boundary alone.

The audit is deterministic and seed-free. Seven focused tests complete locally in roughly 0.25 seconds, so A100 execution would add transport overhead without increasing fidelity.
