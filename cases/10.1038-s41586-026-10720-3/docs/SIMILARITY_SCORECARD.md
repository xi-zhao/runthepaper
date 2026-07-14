# Similarity scorecard

Public status: **numerical feature reproduction**.

The complete internal case audit score is **78.47/100**. For the requested
main-text numerical scope alone, Figs. 2, 4, and 5 have a weighted view of
**80.05/100**.

| Target | Numerical result | Presentation diagnostic | Boundary |
| --- | --- | ---: | --- |
| Fig. 2 | seven landmarks reproduced; maximum `omega` error `8.06e-4 rad/fs` | SSIM `0.8238` | dispersion is reconstructed from the printed vector curve |
| Fig. 4 | mean blind NRMSE `0.0653`; correlation `0.9810` | SSIM `0.7348` | red fit inputs and black validation paths are not redistributed |
| Fig. 5 | slope ratio `1.0211` versus `1.02` | SSIM `0.8201` | normalized points are source-derived and are not redistributed |

The result is not author-data-level exact reproduction. The fibre coefficients,
raw spectra, fitted parameter tables, raw NRR fluxes, and measured pulse shapes
are unavailable. No author code was used.
