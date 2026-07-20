# Numerical methods

- Root: `scipy.optimize.brentq` on `x in [0.4,0.6]`, tolerance `1e-15`.
- Curves: deterministic NumPy evaluation of analytic expressions.
- Verification: seven pytest cases, including source eigenvalues, limiting behavior, unique optimum, and series coefficients.
- No stochastic seeds, fitting, digitization, or GPU kernels are used.
