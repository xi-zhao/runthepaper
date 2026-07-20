# Phase Transitions in Nonreciprocal Driven-Dissipative Condensates: public reproduction note

## Result

Uses an A100 grid calculation to reproduce the paper's gamma=0.3 lambda-2 branch and independently audits the frozen critical-exceptional-point claims. The paper curve passes its feature gate, while the frozen benchmark gold fails independent evaluation.

The public status of this case is **A100 source-curve feature reproduction and benchmark audit**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- gamma=0.3 lambda-2 branch: A100 nonreciprocal-condensate source-curve reproduction (figure: `../outputs/figures/idx63_cep_gamma03_reproduction.png`; check: `../outputs/checks/idx63_figure_check.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/render_idx63_figures.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

The paper-curve result is feature-level rather than author-data exact. Recomputing the full grid requires CUDA/PyTorch; the default public command regenerates figures from the included A100 summaries.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
