# Lessons learned

## New Failure Modes

1. Copying a spectral line shape without its projection prefactor can flip every signed observable.
2. A subtraction written for `rho` cannot cancel a residue defined for `k^2 rho` unless the radial Jacobian is carried explicitly.
3. A supposedly universal nonnegative rate is underdetermined when the sign of its renormalized residue is unspecified.
4. A printed numerical answer can disagree simultaneously with the prompt and its own displayed closed formula.

## Reusable Checks Or Tools

1. Multiply one complex pole by hand and compare with direct complex arithmetic.
2. Recompute all Fourier/angular prefactors from the supplied measure.
3. Expand the proposed regularized integrand locally and verify the pole residue is exactly zero.
4. Preserve sub-float64 edge distances with decimal arithmetic.
5. Evaluate a closed formula and reported decimal independently before treating either as gold.
