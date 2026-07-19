# Similarity Scorecard

## Case Score

- Overall: **88.56/100**.
- Level: `numerical_feature_reproduction`.
- All four figure targets are data-backed, artifact-passing, and have passed essential physics assertions.
- Fig. 3 reaches `complete_reproduction`: paper-exact parameters, verified target-local formulas, pointwise PDF-vector comparison, and a pixel-registered render.
- Fig. 4 and Fig. S1 remain exploratory because the paper omits nonlinear continuation or pump-sample metadata; visual agreement cannot override that parameter gate.

| Target | Weight | Raw components (feature/numeric/scope) | Applied score | Parameter stage |
| --- | ---: | --- | ---: | --- |
| T001 / Fig. 2 | 1.0 | 48/50 + 33/35 + 15/15 | 80 | paper_subset / exploratory |
| T002 / Fig. 3 | 1.2 | 49/50 + 34/35 + 15/15 | 95 | paper_exact / final |
| T003 / Fig. 4 | 1.2 | 49/50 + 33/35 + 15/15 | 89 | paper_subset / exploratory |
| T004 / Fig. S1 | 0.7 | 47/50 + 28/35 + 15/15 | 89 | paper_subset / exploratory |

## Pixel Evidence

| Target | Canvas match | Axis-box IoU | 1 px ink proximity | Full-image SSIM |
| --- | --- | ---: | ---: | ---: |
| T002 / Fig. 3 | exact `1378 x 1383` | 0.962 | 0.790 | 0.860 |
| T003 / Fig. 4 | exact `935 x 371` | 0.924 | 0.830 | 0.792 |
| T004 / Fig. S1 | exact `1722 x 730` | 0.984 | 0.803 | 0.786 |

The SSIM values are reported honestly rather than promoted to 1.0 by copying source pixels. All generated curves come from independent CSV data. The strongest pointwise checks use vector paths from the PDFs strictly as references.

## Why The Score Is Not Higher

- No author CSV/table data exist. PDF vector paths supply pointwise references, but not the original solver metadata.
- The published and arXiv/source-curve detuning-shift conventions differ.
- Nonlinear iteration details and S1 pump values are not printed.
- Fig. 2's IPR inset now matches all 377 source-vector points (`r=0.99999999997`), but the excited-state threshold normalization is not printed and remains reconstructed.

Machine-readable records: `outputs/checks/similarity_scorecard.json`,
`outputs/checks/pixel_evidence.json`, and `outputs/checks/pixel_ssim.json`.
