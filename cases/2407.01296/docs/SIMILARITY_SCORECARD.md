# Similarity scorecard

Public status: **main-text scientific reproduction; pixel-registered, not identical**.

The export audit score is **88.39/100**. This score records evidence strength,
not a claim that 88.39% of pixels match.

| Target | Scientific status | Provenance | Pixel diagnostic |
| --- | --- | --- | ---: |
| Fig. 1 | analytic schematic redraw | independent construction | SSIM `0.8443` |
| Fig. 2(a–d) | passed | a–c independent; d author-data-assisted | SSIM `0.7948` |
| Fig. 3(a–b) | passed | independent GBZ numerics | SSIM `0.6969` |
| Fig. 4(a–f) | all six panels passed | independent numerics | SSIM `0.5823` |
| Fig. 5 | analytic schematic redraw | independent construction | SSIM `0.8625` |

Fig. 4 panel SSIM values are `0.9107`, `0.5717`, `0.7042`, `0.4353`, `0.4181`,
and `0.4946` for panels a–f. Every panel has the exact target canvas dimensions
and passes its scientific acceptance checks, but none reaches the strict
pixel-exact threshold of `0.95`.

The main-text evidence chain is complete. The remaining scientific boundary is
the supplementary scope: Figs. S2 and S4–S7 have not been independently rerun.
The only source-assisted main-text numerical panel is Fig. 2(d). Unreported
state-selection, boundary-discretization, random-seed, probe-grid, and rendering
choices limit pixel identity in Fig. 3 and several Fig. 4 panels.
