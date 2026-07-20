# Numerical methods

Direct complex arithmetic independently checks the closed kDOS component. Unit tests require the frozen formula to equal its negative.

The toy root lies only `2.5e-19` below the edge, below binary64 resolution near one. `Decimal` with 80 digits is therefore used for the root, Jacobian-cancelled rate, limiting magnitude, and frozen-formula comparisons.

Ten focused tests cover the sign, delta weight, angular factor, residual subtraction, residue-sign partition, edge scaling, high-precision root, toy rate, and orthogonal-mode limit.
