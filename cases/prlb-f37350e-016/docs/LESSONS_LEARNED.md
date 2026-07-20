# Lessons learned

1. Topic similarity is not source identity. The 2025 PRB explains the narrative; the 2006 RMP supplies the equations.
2. A local Green function can change units after density-of-states normalization. The symbol should change or the normalization must be explicit.
3. Reproducing a closed-form number is only the first gate. Substitution into the parent equation is the decisive check.
4. A resonance energy without its imaginary part can be misleading. Here the omitted width is as large as the energy.
5. "Strong scattering" is not established by `c < 1` alone; the actual logarithmic control parameter must be checked.
6. Parameter-free source schematics should not receive pixel-reproduction credit.

## New Failure Modes

- `normalized_object_unit_collision`: one symbol is reused for dimensional momentum-space and normalized local propagators.
- `fixed_log_real_part_as_exact_pole`: a complex iterative approximation is rationalized, stripped of its width, and mislabeled exact.
- `topic_candidate_promoted_to_formula_source`: a close modern paper is credited for equations that actually come from an older review.

## Reusable Checks Or Tools

- Always substitute a reported pole into the complete complex denominator.
- Record `|Im Omega / Re Omega|` beside any resonance energy.
- Compare cutoff constants and normalization conventions at the equation-card level.
- `src/dwave_impurity_audit.py` provides deterministic residual, width, and cutoff-sensitivity helpers.
