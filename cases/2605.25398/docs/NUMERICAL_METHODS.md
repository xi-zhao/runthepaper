# Numerical Methods

## Numerical Object

The numerical object is a time-dependent probability vector over collision-free two-photon output configurations:

```text
p(t) = {p_cond(r,s;t) | 1 <= r < s <= M}
```

For the main paper setting, `M=8`, `N=2`, so there are `D=C(8,2)=28` entries.

## Parameters

| Parameter | Value | Source |
| --- | --- | --- |
| Modes | `M=8` | paper experiment |
| Photons | `N=2` | paper experiment |
| Input pair | modes `(3,4)` in one-based notation | OTOC discussion in main text |
| Integrable regime | `Lambda=0.01` | paper random-matrix section |
| Chaotic regime | `Lambda=1000` | paper random-matrix section |
| Paper times | `[1, 1.79, 29.29, 100, 1000]` | appendix construction of unitaries |
| Collision-free dimension | `D=28` | appendix conditional probabilities |

## Data Products

| Data file | Purpose |
| --- | --- |
| `outputs/data/sparse_*_metrics.csv` | Paper-time PT distance, entropy, PR, target OTOC, SFF proxy. |
| `outputs/data/sparse_*_output_distributions.csv` | Output probability bars for Fig. 2g-h style reproduction. |
| `outputs/data/ideal_*_metrics.csv` | Dense-time ideal diagnostic curves for Fig. 3 and Fig. 4. |
| `outputs/data/ideal_*_otoc_sectors.csv` | Overlap-sector averaged OTOC probabilities. |
| `outputs/data/appendix_conditional_probability_demo.csv` | Conditional probability validation for Fig. S1. |
| `outputs/data/appendix_scaling_summary.csv` | Mode-scaling diagnostics for Fig. S4. |
| `outputs/data/appendix_ideal_otocs_full.csv` | All-configuration OTOC curves for Fig. S5. |
| `outputs/data/appendix_otoc_short_time.csv` | Short-time OTOC curves for Fig. S6a. |
| `outputs/data/appendix_otoc_fft_spectrum.csv` | Late-time FFT spectrum for Fig. S6b. |
| `outputs/data/appendix_otoc_fft_pr.csv` | Frequency-space participation ratio for Fig. S6c. |

## Generated Figures

| Generated figure | Paper target |
| --- | --- |
| `outputs/figures/fig2_output_distribution_reproduction.png` | Fig. 2g-h theoretical probability distributions |
| `outputs/figures/fig3_main_probes_reproduction.png` | Fig. 3 |
| `outputs/figures/fig4_otoc_pr_reproduction.png` | Fig. 4 |
| `outputs/figures/figS1_conditional_probability_reproduction.png` | Fig. S1 |
| `outputs/figures/figS4_scaling_reproduction.png` | Fig. S4 |
| `outputs/figures/figS5_ideal_otocs_reproduction.png` | Fig. S5 |
| `outputs/figures/figS6_extra_otoc_reproduction.png` | Fig. S6 |

## Numerical Checks

The central check values are:

- PT distance minimum for chaotic ideal curve: `t=1.788`, close to paper `t*=1.79`;
- entropy maximum for chaotic ideal curve: `t=1.8407`, close to paper `t*=1.79`;
- SFF proxy minimum for chaotic ideal curve: `t=1.8407`, close to paper `t*=1.79`;
- chaotic PR at `t=1.79`: `12.51`;
- integrable PR at `t=1.79`: `1.05`;
- chaotic entropy at `t=1.79`: `2.787`;
- integrable entropy at `t=1.79`: `0.144`;
- short-time slopes: overlap-one `1.999`, overlap-zero `3.999`;
- mean FFT PR: chaotic `146.13`, integrable `9.07`.

These are recorded in:

```text
outputs/checks/reproduction_feature_checks.json
```
