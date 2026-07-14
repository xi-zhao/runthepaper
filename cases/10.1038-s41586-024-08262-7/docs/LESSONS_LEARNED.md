# Lessons Learned

## Case Summary

- Paper: Particle exchange statistics beyond fermions and bosons (Wang & Hazzard)
- PaperID: `10.1038-s41586-024-08262-7`
- Final status: complete_reproduction (90/100); Fig. 2 reproduced, 1D model validated by ED
- Main reproduced targets: T1 Fig. 2 (exclusion statistics + thermodynamics), T2 1D solvable-model ED
- Main blockers: none (in-scope targets are analytically closed-form and small)

## What Worked

- Rendering the reference figure PDF (`sips -s format png`) *before* coding
  surfaced that the published legend uses `m=2/3`, contradicting the `m=5` prose.
  Reproducing the wrong `m` would have produced curves that don't match the figure.
- Treating the single-mode partition function `z_R(x)` as the one core object made
  the whole figure fall out of `d_n` = Taylor coefficients and `<n>=x z'/z`.
- Using the paper's *own solvable model* (ED) as the formula verification, instead
  of only re-plotting the formula, turned a "replot" into a first-principles check
  and let the formula gate be honestly `verified`.

## What Was Difficult

- The `<n>_beta` asymptote is subtle: Ex.3 (`z=1+m x`) saturates to **1**, not
  `m` — the m-fold internal degeneracy raises mid-temperature occupation but the
  max occupancy per mode is still 1 because `d_2=0`. A first (wrong) sanity check
  asserted saturation to `m`; the figure and the algebra both say 1.

## Generalized Experience

| Lesson | Why it matters beyond this case | Future recommendation |
| --- | --- | --- |
| Trust the figure over the prose when they disagree on a parameter | Papers regenerate figures without updating captions/text | Always render the source figure and read its legend before fixing final parameters |
| For a "single-generating-function" theory figure, derive `d_n`/observables as coefficients, not fits | Avoids digitization and makes provenance `analytic_reference` | Encode the generating function; read observables off it |
| Validate an analytic formula via the paper's own solvable model | An ED that matches to 1e-14 is far stronger evidence than a visual overlay | When a theory paper provides an exactly-solvable realization, diagonalize it |

## Common Pitfalls And Pain Points

| Pitfall | How it appeared | How future runs should avoid it |
| --- | --- | --- |
| Wrong high-T asymptote for exclusion statistics | `<n>` for `z=1+m x` saturates to 1, not m | Derive the limit from `x z'/z` as `x->inf` = largest `n` with `d_n>0` |
| Text/figure parameter mismatch (m=5 vs m=2/3) | Main text vs legend disagree | Cross-check caption, legend, and axis extents before setting `parameter_match=paper_exact` |

## Recommended Practices

| Practice | When to use it | Evidence from this case |
| --- | --- | --- |
| Render reference figure first | Any figure with numeric labels/legend | Caught the m discrepancy up front |
| ED as formula gate | Theory paper with a solvable-model realization | `ed_validation.json`, max dev ~1e-14 |

## New Failure Modes

| Failure mode | Where it appeared | How future runs should detect it |
| --- | --- | --- |
| Caption/figure parameter drift | Fig. 2 legend vs prose | Compare stated params against features actually drawn (ladder heights, asymptotes) |

## Reusable Checks Or Tools

| Candidate | Why it is reusable | Suggested destination |
| --- | --- | --- |
| "generating-function → `{d_n}` / `<n>=x z'/z`" pattern | Recurs for any statistical-mechanics single-mode figure | Keep case-local for now; note in experience playbook |

## Harness Backlog Items

| Priority | Improvement | Evidence from this case | Status |
| --- | --- | --- | --- |
| low | A helper to render a source figure PDF→PNG within size limits (sips `-Z`), so the legend can be inspected before coding | Manual `sips` step here | proposed |

## Prompt Or Workflow Changes

- None. The 18-step workflow fit a pure-theory paper well; the only addition worth
  emphasizing is the "render-and-read-the-legend-before-fixing-parameters" habit.
