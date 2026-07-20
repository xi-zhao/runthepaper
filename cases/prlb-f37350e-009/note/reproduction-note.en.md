# Vacuum and Gravitons of Relic Gravitational Waves, and Regularization of Spectrum and Energy-Momentum Tensor: public reproduction note

## Result

Independently reconstructs a source running-spectrum figure and audits the composite frozen task against its three older source lineages. The figure-level target is paper-exact, while several benchmark counterterms and equation-of-state values are internally inconsistent.

The public status of this case is **Paper-exact figure reproduction and composite benchmark audit**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- Relic-wave running-spectrum figure: Paper-exact tensor-spectrum running curves (figure: `../outputs/figures/rgw_fig2_reproduced.png`; check: `../outputs/checks/rgw_fig2_pixel_qa.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/run_gold_audit.py
python scripts/render_rgw_fig2.py
python scripts/render_idx9_audit.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

The frozen record combines multiple older non-PRL sources and therefore is not a one-paper PRL reproduction. The public case exposes the independent calculation and audit but does not redistribute source artwork or digitized curves.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
