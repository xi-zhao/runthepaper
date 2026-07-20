# Spontaneous Emission Decay and Excitation in Photonic Time Crystals: public reproduction note

## Result

Independently evaluates all seven frozen decay and excitation tasks using the source equations and controlled toy limits. Five frozen answers fail literal source or algebra consistency.

The public status of this case is **Complete benchmark-task reproduction and source-consistency audit**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- PRL-Bench idx 90 Tasks 1-7: Decay, excitation, and algebra consistency audit (figure: `../outputs/figures/idx90_gold_audit.png`; check: `../outputs/checks/idx90_figure_check.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/run_idx90_audit.py
python scripts/render_idx90_figures.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

The seven-task audit is complete, but the package does not reproduce the paper's full electromagnetic simulation or experimental apparatus. Results are formula- and benchmark-level numerical features.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
