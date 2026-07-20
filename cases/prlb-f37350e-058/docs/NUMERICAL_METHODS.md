# Numerical methods

The case uses the paper’s symmetric uniform Nyström matrix, not a surrogate
kernel. `scipy.linalg.eigh(..., subset_by_index=...)` computes only the required
spectral edge. The dual constraint is solved by bracketed scalar root finding;
no optimizer is allowed to change the physical marginal.

The source protocol reaches matrices of dimension `2N+1=10801`. Repeating all
published rows is an expensive dense `O(N^3)` campaign and is not required to
disprove benchmark values that differ by `O(10^-2)`. The local audit therefore
uses:

- exact source-table refits for the paper’s published extrapolation;
- independent matrix calibration at `L=10`, `N=100,200,300,400`;
- constrained and Gaussian domain scans through `L=30,N=900`;
- float64 arithmetic and residual/symmetry checks.

The order of limits follows the paper: refine `N` at fixed `L`, then grow `L`.
For the Gaussian coefficient this order is part of the scientific question:
fixed-`L` convergence does not license a full-line coefficient if the value
then grows with `L`.
