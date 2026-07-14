# arXiv:2507.09447 reproduction note

## Paper identity

- Preprint: [*Lyapunov formulation of band theory for disordered non-Hermitian systems*](https://arxiv.org/abs/2507.09447), arXiv:2507.09447.
- Formal publication: [*Universal Thouless relations for disordered non–Hermitian systems in one dimension*](https://doi.org/10.1016/j.scib.2026.05.055), *Science Bulletin* (2026), online ahead of print.
- DOI: `10.1016/j.scib.2026.05.055`; PII: `S2095-9273(26)00583-9`.

The figure-level target remains Figs. 3–5 of arXiv v1. The formal supplement is
used only to cross-check the numerical method.

## Scientific object

When disorder removes translation symmetry, ordinary Bloch bands no longer
provide the right real-space description. The paper replaces them with four
Lyapunov exponents of a site transfer matrix. The signs of the two central
exponents distinguish Anderson-localized, unidirectional-critical, and skin
states; the number of positive exponents also fixes the spectral winding.

This case reproduces the executable relationships rather than copying the
authors' artwork: finite OBC/PBC spectra, thermodynamic Lyapunov densities,
state classifications, winding sectors, and the disorder-driven skin–Anderson
transition.

## Reproduced results

- Figs. 3 and 4 use an `L=1000`, 3200-realization deterministic disorder
  ensemble.
- High-resolution Lyapunov grids use periodic QR stabilization.
- Ten ALM profiles, one near-critical profile, and one skin profile are computed
  from independent right eigenvectors.
- Mobility contours are evaluated at `W=0.4,0.8,1.2,1.6,2.0`, and the localized
  fraction is scanned on `W∈[0,3]`.
- All nine scientific gates pass, including recovery of `W_c=2.1`.

![Fig. 3 independent reproduction](../outputs/figures/fig3_paper_exact.png)

**Difference reason:** the authors did not publish disorder seeds or eigenstate
selection windows. The reproduction uses an independent deterministic ensemble,
so spectral microstructure and profile pixels are not uniquely recoverable.

![Fig. 4 independent reproduction](../outputs/figures/fig4_paper_exact.png)

**Difference reason:** transfer length, QR interval, and final artwork are
unpublished. Winding sectors and spectral support agree, while local density
texture and layout differ.

![Fig. 5 independent reproduction](../outputs/figures/fig5_paper_exact.png)

**Difference reason:** the Fig. 5 quadrature grid details and Illustrator source
are unpublished. The transition `W_c=2.1` agrees; remaining differences come
from grid interpolation and plotting post-processing.

## Run the public package

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2507.09447/code
python scripts/plot_paper_exact.py
python scripts/qa_paper_exact.py
```

These quick commands regenerate the figures and scientific checks from the
published independently generated arrays. The complete `L=1000 × 3200` run is
available through `python scripts/run_paper_exact.py`, but it is computationally
expensive and creates local checkpoints that are intentionally not committed.

## Reproduction boundary

The authors did not publish random seeds, state-selection windows, transfer
length, QR interval, Fig. 5 quadrature details, or the final Illustrator project.
We therefore claim paper-scale scientific and geometric reproduction, not pixel
identity. Export-time full-image SSIM values are `0.7721`, `0.7735`, and `0.8521`
for Figs. 3, 4, and 5. These values document the visual gap; they are not the
scientific acceptance criterion. The paper-scale data are complete; the residual
is an author-protocol and artwork boundary rather than a compute shortage, so no
additional large campaign is scheduled.
