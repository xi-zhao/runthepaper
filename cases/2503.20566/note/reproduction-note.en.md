# Accurate Gauge-Invariant Tensor Network Simulations for Abelian Lattice Gauge Theory in (2+1)D: ground state and real-time dynamics: public reproduction note

## Result

Independently reproduces all four frozen benchmark targets using exact gauge-invariant bases for odd Z2, pure Z2, Z2 matter, and Z3 dynamics. The generated comparison consolidates the A100 numerical evidence and analytic checks.

The public status of this case is **Complete PRL-Bench target reproduction; partial paper coverage**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- PRL-Bench idx 47 Tasks 1-4: Odd-Z2, pure-Z2, Z2-matter, and Z3 benchmark comparison (figure: `../outputs/figures/idx47_benchmark_comparison.png`; check: `../outputs/checks/similarity_scorecard.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/render_idx47_benchmark_comparison.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

The four benchmark targets are complete, but the source paper's wider tensor-network figure set is not fully reproduced. Full numerical reruns require CUDA and CuPy; the default public command regenerates the summary figure from included data.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
