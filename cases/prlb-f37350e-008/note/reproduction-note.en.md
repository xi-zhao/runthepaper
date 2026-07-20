# Extreme Resonant Eccentricity Excitation of Stars around Merging Black-Hole Binary: public reproduction note

## Result

Recomputes all seven frozen numerical tasks and independently renders the source phase portrait from the secular Hamiltonian. The numerical gold is consistent, while the frozen record does not satisfy the benchmark's declared publication-window contract.

The public status of this case is **Paper-figure feature reproduction and PRL-Bench source audit**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- Source phase portrait: Secular-resonance contours and separatrix structure (figure: `../outputs/figures/prl_figC_reproduced.png`; check: `../outputs/checks/figc_pixel_qa.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/run_gold_audit.py
python scripts/render_prl_figc.py
python scripts/render_idx8_audit.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

The reproduced source is a 2024 PRL rather than a paper in the benchmark's declared 2025-2026 window. The public package excludes the original figure and publishes only independently generated data and images.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
