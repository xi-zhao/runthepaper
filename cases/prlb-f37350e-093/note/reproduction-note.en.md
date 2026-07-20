# Enhanced Sampling of Configuration and Path Space in a Generalized Ensemble by Shooting Point Exchange: public reproduction note

## Result

Independently reconstructs Fig. 2B from the source potential and audits the frozen efficiency and speedup claims. The free-energy profile is reproduced, while several claimed statistics lack the event counts and rerun data needed for verification.

The public status of this case is **Paper-figure feature reproduction and benchmark statistics audit**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- PRL Fig. 2B: Free-energy profile from deterministic marginalization (figure: `../outputs/figures/prl_fig2b_reproduced.png`; check: `../outputs/checks/gold_audit_check.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/render_prl_fig2b.py
python scripts/render_idx93_audit.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

The source is a 2024 PRL outside the benchmark's declared window. Author trajectories, event counts, and optimized-coordinate rerun rates are unavailable, so the efficiency and speedup claims remain underdetermined.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
