# Numerical Methods

## Model

We implement the single-particle 3D Anderson model on an `L x L x L` cubic lattice:

```text
H_A = - nearest-neighbor hopping + random onsite disorder
```

- Boundary condition: open boundary.
- Disorder: iid uniform `[-W/2, W/2]`.
- Local sizes: `L=4,5,6,7`.
- Paper sizes: up to `L=38`.

## Observable

The local run focuses on the sublattice kinetic-energy perturbation `T_s`. This is the operator that most clearly shows the weak-disorder crossover in the paper.

The code also keeps the model structure explicit enough to add `T` and randomized site occupation `n` in a larger rerun.

## Frequency Cutoff

For the main disorder scan, we follow the paper's default cutoff:

```text
mu_star = 2 log(V) omega_av
```

For the localized-regime check, we run a small `mu` sweep:

```text
mu = 0.02, 0.05, 0.1, 0.2, 0.5
```

## Generated Data

- `outputs/data/fidelity_vs_disorder_raw.csv`
- `outputs/data/fidelity_vs_disorder_summary.csv`
- `outputs/data/spectral_function_summary.csv`
- `outputs/data/mu_sweep_summary.csv`
- `outputs/data/perturbation_theory_summary.csv`

## Acceptance Features

The case checks whether:

- weak-disorder sensitivity is visible in the largest local size;
- gap ratio is higher in the chaotic/moderate-disorder window than at strong disorder;
- IPR is much larger at high disorder;
- `chi_av^r / chi_typ^r` grows in the localized regime.

Strict extraction of `W_1^*`, `W_2^*`, `W_3^*`, and fitted exponents is left for the planned large-scale run.
