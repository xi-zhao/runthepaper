# Lessons learned

## New Failure Modes

1. A real-linear physical state may occupy only a conjugacy-constrained subspace. Optimizing an arbitrary doubled vector, or using a convenient coefficient in place of the constrained phase optimum, changes the observable.
2. “Stable near threshold” does not by itself guarantee transient amplification. The initial logarithmic slope supplies an additional existence condition.
3. A benchmark can import quantum-noise claims into a source that explicitly says the quantum treatment is future work.
4. Vacuum diffusion conventions expose factor-of-two errors that semiclassical rate intuition can miss.

## Reusable Checks Or Tools

1. Reduce periodic conjugate dynamics to a constant 2 by 2 matrix before attempting numerical integration.
2. Verify phase-optimized expressions with a dense direct phase search on the physical input manifold.
3. Test the existence assumptions of every requested extremum before deriving its location.
4. Solve the steady second moments directly and preserve the commutator-generated `+1` term.
5. Recompute printed high-precision values independently and score them against the requested tolerance, not against cosmetic final digits.
