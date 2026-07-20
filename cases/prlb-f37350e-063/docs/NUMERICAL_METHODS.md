# Numerical methods

## Exact and analytic checks

NumPy constructs the complex tridiagonal matrix, source eigenpairs, frozen pairs, and relative residuals. Vacuum thresholds and bulk static branches are evaluated from closed forms and checked against direct matrix/substitution tests.

## Frozen Task 4

- `N=40`, `J=Gamma=1`, `theta=pi`, `gamma=0.3`
- `kappa=2.36...2.41` in steps of `1e-5` (5,001 trajectories)
- `dt=0.02`, `T=4000`, 200,000 time steps
- MT19937 seed 1, tested with NumPy Generator and legacy streams
- RK4 primary integrator, full Heun rerun
- static residual gate `<1e-8`
- centered finite-difference Jacobian with `epsilon=1e-7` and `epsilon/2`
- SVD nullity tolerance `5e-7`
- CEP criterion `|Re lambda_2|<1e-5`, nullities `(1,2)`

Trajectories were vectorized over the kappa grid on an A100. Jacobians are computed only for states passing the residual gate, preserving the frozen rule order.

## Source-figure comparison

The direct PDF was rasterized losslessly at 300 dpi. The `gamma=0.3` blue curve was extracted in calibrated axes and linearly compared with the independent A100 curve. Source pixels never replace generated physics data.
