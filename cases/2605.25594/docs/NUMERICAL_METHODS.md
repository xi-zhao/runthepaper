# Numerical Methods

## Model

We implement the single-particle 3D Anderson model on an `L x L x L` cubic lattice:

```text
H_A = - nearest-neighbor hopping + random onsite disorder
```

- Boundary condition: open boundary.
- Disorder: iid uniform `[-W/2, W/2]`.
- Local correctness sizes: `L=4,5,6,7`.
- A100 campaign sizes: `L=24,28,31`, totaling 605 disorder realizations.
- Paper sizes: up to `L=38`.

## Observable

The completed local and A100 runs focus on the sublattice kinetic-energy perturbation `T_s`. This is the operator that most clearly shows the weak-disorder crossover in the paper.

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
- `outputs/data/remote/results_L24.jsonl`
- `outputs/data/remote/results_L28.jsonl`
- `outputs/data/remote/results_L31.jsonl`
- `outputs/data/remote_campaign_summary.csv`

## Acceptance Features

The case checks whether:

- weak-disorder sensitivity is visible in the largest local size;
- gap ratio is higher in the chaotic/moderate-disorder window than at strong disorder;
- IPR is much larger at high disorder;
- `chi_av^r / chi_typ^r` grows in the localized regime.

The A100 subset pins the gap-ratio crossing to `W=16.56-16.60`, resolves the GOE-to-Poisson crossover, and gives a transition spectral exponent near `0.48` versus the paper's `0.52`. The full `L=32-38` scaling ladder remains compute-limited on the available single-A100 dense-eigensolver path.
