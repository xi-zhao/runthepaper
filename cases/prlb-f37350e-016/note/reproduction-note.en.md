# D-wave single-impurity resonance benchmark source/gold audit: public reproduction note

## Result

Recomputes the frozen impurity-resonance arithmetic, pole equation, and diagnostic curves. The numerical audit is reproducible, but no single PRL source matching the frozen record has been identified.

The public status of this case is **Formula-level reproduction with unresolved source identity**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- Benchmark impurity-resonance audit: Pole equation, resonance energies, and source-identity diagnostics (figure: `../outputs/figures/idx16_gold_audit.png`; check: `../outputs/checks/idx16_audit_figure_check.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/run_gold_audit.py
python scripts/render_idx16_audit.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

This is a benchmark-task case rather than a verified one-paper reproduction. The formulas trace to older review literature and a possible newer candidate, while the frozen third task fails its own pole contract.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
