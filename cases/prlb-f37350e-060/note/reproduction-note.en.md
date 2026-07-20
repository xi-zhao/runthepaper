# Error-Corrected Fermionic Quantum Processors with Neutral Atoms: public reproduction note

## Result

Reconstructs the paper's fermionic reference-state formulas and independently evaluates all frozen tasks. Source identities are exact; one task passes, three fail, and one is underdetermined by the published information.

The public status of this case is **Formula-level numerical feature reproduction and benchmark audit**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- Fermionic reference benchmark: Independent five-task formula and identifiability audit (figure: `../outputs/figures/idx60_gold_audit.png`; check: `../outputs/checks/idx60_figure_check.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/run_idx60_audit.py
python scripts/render_idx60_figures.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

This case reproduces the benchmark-relevant analytic and small numerical objects, not the full hardware protocol or experimental error-correction campaign.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
