# General Quantum Backflow in Realistic Wave Packets: public reproduction note

## Result

Independently solves the backflow eigenproblem, validates the source extrapolation, and audits four frozen tasks. The paper-level extrapolation is reproduced at feature level; only the first frozen task survives the independent calculation.

The public status of this case is **Source-extrapolation feature reproduction and benchmark audit**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- Backflow extrapolation: Finite-bandwidth eigenvalue sequence and asymptotic extrapolation (figure: `../outputs/figures/idx58_source_extrapolation.png`; check: `../outputs/checks/idx58_figure_check.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/run_idx58_audit.py
python scripts/render_idx58_figures.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

The public result validates the source extrapolation rather than reproducing every supplemental curve. Frozen Tasks 2-4 disagree with the independently evaluated operator and are reported as benchmark-gold failures.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
