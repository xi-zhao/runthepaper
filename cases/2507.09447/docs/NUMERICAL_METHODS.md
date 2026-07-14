# Numerical methods

## Model and numerical object

The case studies a one-dimensional non-Hermitian chain with hopping range
`M=2`, onsite disorder sampled uniformly from `[-W, W]`, and hoppings
`t_-2=1`, `t_-1=1`, `t_1=1.5`, and `t_2=0.5`.

The core numerical object is the ordered four-component Lyapunov spectrum of
the site transfer matrix. Its two central exponents determine whether a state
is Anderson localized, critical, or a skin state. OBC and PBC spectral
potentials are calculated from different sums of the positive Lyapunov
exponents.

## Paper-scale stages

1. **Finite spectra:** diagonalize OBC and PBC chains at `L=1000` for 3200
   deterministic disorder realizations and accumulate two-dimensional spectral
   histograms.
2. **Lyapunov grids:** propagate the four-dimensional transfer matrix with
   periodic QR stabilization on the Fig. 3/4 energy grid.
3. **Profiles:** diagonalize selected OBC realizations and classify ten
   Anderson-localized profiles, one near-critical profile, and one skin
   profile using independently evaluated Lyapunov exponents.
4. **Transition scan:** evaluate mobility contours at
   `W=0.4,0.8,1.2,1.6,2.0` and the Anderson-localized fraction on
   `W=0,0.1,...,3.0`.
5. **Scientific gates:** compare finite and thermodynamic density support,
   scaling exponents, state classifications, contour shrinkage, and the
   transition point.

The full run contract is stored in
[`code/config/paper_exact_run.json`](../code/config/paper_exact_run.json).
The expensive ensemble is resumable, but checkpoints are runtime state and are
not published. The included generated arrays allow the figures and scientific
checks to be rerun without repeating the complete ensemble.

## Stabilization and reproducibility

- Lyapunov exponents use batched QR factorization to prevent overflow and loss
  of subleading directions.
- OBC eigenvalues use a similarity gauge to improve conditioning without
  changing the exact OBC spectrum.
- Sparse-LU log determinants are used for finite-size potential convergence.
- The top-level seed is `250709447`; ED batches are applied exactly once.
- BLAS thread counts should be set to one when using multiple worker processes.

## Generated evidence

- `outputs/data/paper_ed_histograms.npz`: OBC/PBC spectral densities.
- `outputs/data/paper_fig34_theory.npz`: Fig. 3/4 Lyapunov grids.
- `outputs/data/paper_profiles.npz`: independently computed state profiles.
- `outputs/data/paper_fig5_contours.npz`: disorder-dependent mobility grids.
- `outputs/data/paper_alpha.csv`: Anderson-localized fraction and transition.
- `outputs/checks/paper_scientific_similarity.json`: nine scientific gates.

The authors did not publish their random seeds, state-selection windows,
transfer length, QR interval, or final plotting project. These quantities are
therefore explicit implementation choices rather than claimed author settings.
