# Public Reproduction Scorecard

This public scorecard reports what can be checked from files included in this
repository: generated code, generated data, generated figures, and validation
JSON.

Internal development also used original paper figures and digitized references,
but those source-derived assets are not redistributed here. Therefore this
public scorecard is a feature-level reproduction record, not an
author-data-level or pixel-level equivalence claim.

| Target | Included public evidence | Public status | Remaining boundary |
| --- | --- | --- | --- |
| Fig. 2 open-boundary spectrum | `outputs/data/fig2_open_spectrum.csv`, `outputs/checks/fig2_open_spectrum.json`, `outputs/figures/fig2_open_spectrum.png` | Key open-boundary zero-mode interval and chiral pairing reproduced | No author plotting data; original source panels not redistributed |
| Fig. 2 boundary perturbation | `outputs/data/fig2_boundary_perturbation.csv`, `outputs/checks/fig2_boundary_perturbation.json`, `outputs/figures/fig2_boundary_perturbation.png` | Boundary-perturbed spectrum generated from the same open-chain model | Styling/layout not treated as a public acceptance gate |
| Fig. 3 GBZ and skin localization | `outputs/data/fig3_beta_roots.csv`, `outputs/data/fig3_cbeta.csv`, `outputs/data/fig3_profiles.csv`, `outputs/checks/fig3_beta_skin.json`, `outputs/figures/fig3_beta_skin.png` | GBZ radius, beta-root structure, and left-localized profiles reproduced | Public package does not include digitized source curves |
| Fig. 4 non-Bloch winding number | `outputs/data/fig4_winding.csv`, `outputs/checks/fig4_winding.json`, `outputs/figures/fig4_winding.png` | Winding plateau and transition location reproduced | No author plotting data |
| Fig. 5 nonzero `t3` topology | `outputs/data/fig5_t3_spectrum.csv`, `outputs/data/fig5_t3_winding.csv`, `outputs/data/fig5_t3_cbeta.csv`, `outputs/checks/fig5_t3.json`, `outputs/figures/fig5_t3.png` | Shifted topological interval and non-circular beta curve reproduced | Original EPS/path references are not redistributed |
| Supplemental spectra | `outputs/data/supplemental_*`, `outputs/checks/supplemental_*`, `outputs/figures/supplemental_*` | Supplemental complex spectra and high-gamma winding features reproduced | Auxiliary target; not used as the headline claim |

## Public Claim

The public case supports this claim:

> The main non-Hermitian SSH numerical features in the paper can be reproduced
> from the derived model equations with the included code and generated data.

It does not support this stronger claim:

> The public package is identical to the authors' plotting data or original
> figure pixels.
