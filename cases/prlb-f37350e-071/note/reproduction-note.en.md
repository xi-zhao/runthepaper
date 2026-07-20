# Unwanted Couplings Can Induce Amplification in Quantum Memories despite Negligible Apparent Noise: public reproduction note

## Result

Independently evaluates all six frozen quantum-memory tasks, including gain, apparent noise, threshold behavior, and the high-precision scalar result. The complete audit shows that three central frozen answers are inconsistent with the verified source equations.

The public status of this case is **Complete benchmark-task reproduction and source audit**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- PRL-Bench idx 71 Tasks 1-6: Gain, noise, threshold, and precision audit (figure: `../outputs/figures/idx71_gold_audit.png`; check: `../outputs/checks/idx71_figure_check.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/run_idx71_audit.py
python scripts/render_idx71_figures.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

The benchmark-task scope is complete, but this is not a reproduction of every paper figure or experimental implementation. The package publishes only independently generated audit data and graphics.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
