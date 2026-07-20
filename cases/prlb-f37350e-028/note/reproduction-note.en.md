# Deterministic Switching of the Neel Vector by Asymmetric Spin Torque: public reproduction note

## Result

Implements the paper's macrospin equations, recomputes switching observables, and audits all four frozen tasks against independent algebra and source constraints. The reproducible result shows that the four frozen answers do not satisfy the verified source model.

The public status of this case is **Source-grounded macrospin reproduction and benchmark audit**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- Macrospin switching audit: Independent switching trajectory and four-task consistency audit (figure: `../outputs/figures/idx28_gold_audit.png`; check: `../outputs/checks/idx28_figure_check.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/run_idx28_audit.py
python scripts/render_idx28_figures.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

The package reproduces the benchmark-relevant macrospin object and audit, not the paper's full micromagnetic or experimental scope. The generated audit figure is independent and the original paper panel is not redistributed.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
