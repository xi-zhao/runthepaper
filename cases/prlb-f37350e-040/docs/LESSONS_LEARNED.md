# Lessons learned

## New Failure Modes

- A benchmark can copy a dispersion correctly while switching from the stable real branch to an unstable imaginary branch in the next definition.
- “Minimum positive” on an open interval may denote only an unattained infimum.
- Correct optimizer coordinates do not validate a downstream observable when both are monotone functions of the same intermediate quantity.
- A displayed series coefficient and its worked derivation can differ by a factor of two.

## Reusable Checks Or Tools

- Branch-domain gate: record whether an observable uses `Re omega`, `Im omega`, the stable band, or the unstable band.
- Attainment gate: check compactness/boundaries before numerical minimization.
- Cross-evaluate every printed number against the formula immediately above it.
