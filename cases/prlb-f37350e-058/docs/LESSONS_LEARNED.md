# Lessons learned

## Case summary

- Paper: *General Quantum Backflow in Realistic Wave Packets*
- Final status: `source_verified / benchmark_gold_invalid`
- Main result: source extrapolation validated; frozen Task 1 valid, Tasks 2-4 invalid.
- Blockers: missing plotted state arrays and under-specified two-Gaussian source panel.

## Reusable lessons

| Lesson | Why it matters | Future rule |
| --- | --- | --- |
| A triangle-inequality bound is not a sharp norm | Projection sums often have hidden symmetries that shrink the spectrum | Before accepting equality, search unitary/parity conjugations and source spectral bounds |
| The value of a step function at a grid boundary can be source-identifying | `Theta(0)=0,1/2,1` changed the finite eigenvalue visibly | Calibrate boundary conventions against one published row before extrapolating |
| A pointwise/core derivative does not guarantee eigenvalue perturbation theory | The second-variation kernel is unbounded on the full line and the top state has long tails | Require window growth and form-domain convergence before reporting a perturbative coefficient |
| Refinement and domain growth are different limits | `c2` stabilized in `N` while diverging in `L` | Encode and test the paper’s order of limits separately |
| Source-table validation is not full independent numerics | Exact refits can coexist with only a subset of recomputed matrix rows | Use mixed provenance and keep artifacts exploratory |

## What worked

- Exact parity reduced a difficult norm claim to a one-line spectral relation.
- One published matrix row fixed the otherwise ambiguous `Theta(0)` convention.
- Edge-only symmetric eigensolvers kept the full audit to about five seconds.
- Feature-level comparison avoided meaningless SSIM on an independent replot.

## Harness backlog

- Add a reusable “bound versus attained equality” operator audit checklist.
- Add a two-axis convergence contract that distinguishes discretization
  refinement from physical-domain growth.
- Add a perturbation-domain warning when a differentiated kernel grows in its
  coordinates or the source state has nondecaying/long oscillatory tails.

`copied_to_backlog`: these items are recorded under the idx58 section of
`PRAgent-workflow/HARNESS_BACKLOG.md`, and the abstract operator/domain lesson is
recorded in `PRAgent-workflow/REPRODUCTION_EXPERIENCE.md`.

## New Failure Modes

| Failure mode | Detection |
| --- | --- |
| Coarse projection bound asserted as an attained norm | Search exact conjugation identities and compare with published one-sided spectral bounds |
| Simple-eigenvalue perturbation used outside the derivative form domain | Refine the grid and grow the physical window as separate gates |
| Endpoint convention silently changes an extrapolation | Reproduce one published finite-grid row before fitting |

## Reusable Checks Or Tools

| Candidate | Suggested destination |
| --- | --- |
| Operator bound-attainment checklist | formula/method gate templates |
| Two-axis convergence report (`resolution`, `domain`) | generic numerical target contract |
| Boundary-convention calibration row | paper-table reproduction helper |
