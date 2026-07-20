# Lessons learned

1. An eigenvalue set match is weaker than an eigenpair check. Residuals must preserve the source's mode labeling and site-dependent phase.
2. Symmetry compatibility is not the same as uniqueness. Both static momenta must be substituted before declaring PH selection.
3. A protocol's gates are ordered business rules. A state that fails the residual gate cannot be promoted to a CEP by later Jacobian calculations.
4. Paper methods and benchmark extensions need separate provenance objects. Otherwise an invalid benchmark extension can be mistaken for a paper failure.
5. Digitized source comparisons are valuable when paired with independent generated data and a narrow, explicit panel scope.

## New Failure Modes

- `eigenvalue_set_without_pairing`: a spectrum can match while every displayed vector is paired to the wrong eigenvalue or misses a site-dependent phase.
- `symmetry_compatibility_as_uniqueness`: satisfying a symmetry relation does not establish that no other branch satisfies it.
- `downstream_metric_before_acceptance_gate`: computing a Jacobian metric on a trajectory that failed the static-state gate changes the protocol.

## Reusable Checks Or Tools

- `eigenpair_residuals` compares `(A v_m-lambda_m v_m)` mode by mode instead of comparing unordered spectra only.
- `run_frozen_cep_grid` vectorizes a long independent-trajectory sweep while preserving residual-before-Jacobian ordering.
- The source-curve digitizer stores calibrated pixel axes and source-reference provenance separately from generated numerical data.
