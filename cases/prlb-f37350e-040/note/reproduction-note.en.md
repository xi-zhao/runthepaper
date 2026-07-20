# Nonlinear Stage of Modulational Instability in Repulsive Two-Component Bose-Einstein Condensates: public reproduction note

## Result

Recomputes the benchmark selection rule and modulational-instability wedge directly from the source equations, with independent analytic and numerical checks.

The public status of this case is **Equation-level numerical feature reproduction**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- Modulational-instability selection rule: Analytic wedge and frozen-answer consistency map (figure: `../outputs/figures/idx40_selection_rule_audit.png`; check: `../outputs/checks/gold_audit_check.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/run_gold_audit.py
python scripts/render_idx40_audit.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

The source equations and benchmark observables are reproduced, but paper-panel curves are not claimed because the author simulation arrays and full evolution metadata are unavailable.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
