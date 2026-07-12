# Method Trace

## Reproduction Strategy

The paper combines theory, simulation, and experiment. This case reproduces the theoretical/numerical part:

1. sample integrable and chaotic Hamiltonians from the paper's random-matrix family;
2. evolve them with `U(t)=exp(-iHt)`;
3. compute collision-free two-photon boson-sampling probabilities;
4. derive all plotted diagnostics from those probability vectors;
5. compare physical features, not visual styling.

## Local Run Scale

The paper's experimental setting is small enough to reproduce locally at feature level:

- modes: `M=8`;
- photons: `N=2`;
- collision-free states: `D=28`;
- paper times: `[1, 1.79, 29.29, 100, 1000]`;
- sparse paper-style samples: `16` realizations per time, except chaotic `t=1.79` uses `75`, matching the paper's special treatment of the SFF dip time;
- ideal curves: locally averaged over hundreds of Hamiltonian instances on a denser time grid.

## Main Algorithms

| Step | Implementation | Evidence |
| --- | --- | --- |
| Hamiltonian sampling | `sample_hamiltonian` in `src/boson_sampling_chaos.py` | `outputs/data/*metrics.csv` |
| Unitary evolution | eigendecomposition of each real symmetric Hamiltonian | `outputs/data/ideal_*_metrics.csv` |
| Boson-sampling probabilities | two-photon permanent formula and collision-free normalization | `outputs/checks/reproduction_feature_checks.json` |
| PT distance | Wasserstein-1 distance to `D exp(-Dp)` | `fig3_main_probes_reproduction.png` |
| Shannon entropy | `-sum p log p` with Haar reference | `fig3_main_probes_reproduction.png` |
| OTOC equivalent | target and sector probability curves | `fig4_otoc_pr_reproduction.png`, `figS5_ideal_otocs_reproduction.png` |
| Frequency analysis | FFT participation ratio of late-time OTOC fluctuations | `figS6_extra_otoc_reproduction.png` |

## Acceptance Checks

The numerical feature checks require:

- chaotic PT distance minimum near `t*=1.79`;
- chaotic entropy maximum near `t*=1.79`;
- chaotic SFF proxy minimum near `t*=1.79`;
- chaotic PR much larger than integrable PR at `t*=1.79`;
- chaotic entropy much larger than integrable entropy at `t*=1.79`;
- short-time OTOC slopes close to `2` and `4`;
- chaotic FFT participation ratio larger than integrable FFT participation ratio.

All checks pass in:

```text
outputs/checks/reproduction_feature_checks.json
```

## Known Method Boundaries

- The code does not reproduce measured red experimental points because raw photon-count data are not included in the arXiv source.
- The code does not claim seed-level identity with the authors' random ensembles.
- The SFF plotted here is a normalized 4-point proxy built from the sampled eigenvalues; it is used as a feature-level check for the dip-ramp-plateau relation, not as a claim of exact author-curve equality.
