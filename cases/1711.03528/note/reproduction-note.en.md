# Reproduction Report

## Scope

This case reproduces the numerical features of arXiv:1711.03528, "Quantum many-body scars", including a symmetry-resolved `L=28` partial reproduction.

Completed:

- arXiv PDF and source ingested.
- Paper figures rendered from source.
- Numerical figures classified.
- PXP Hamiltonian and constrained Hilbert space implemented.
- Formula checks passed before numerical plotting.
- Four reproduction figures generated from structured CSV data.
- The paper's `k=0, I=+1` sector reproduced at `L=28` (dimension 13201), including the 15-state scar tower and unfolded level statistics.

Not completed:

- Full `L=32` symmetry-resolved exact diagonalization.
- Thermodynamic-limit iTEBD with bond dimension 400.

## Commands

From the project root:

```bash
python3 cases/1711.03528/code/scripts/run_reproduction.py
python3 cases/1711.03528/code/scripts/plot_reproduction.py
python3 cases/1711.03528/code/scripts/run_symmetry_resolved_sector.py
python3 cases/1711.03528/code/scripts/plot_symmetry_resolved_sector.py
```

## Main Numerical Results

| Quantity | Local result | Meaning |
| --- | ---: | --- |
| Fig. 1 PBC `L=6` constrained states | `18` | matches Fibonacci-chain counting |
| `Z2` local-correlation period | `2.375` | close to paper value `~2.35` |
| `Z2` max return after `t>1` | `0.787` | much stronger than generic density waves |
| FSA basis dimension at `L=16` | `17` | closes as `L+1` |
| Max `Z2` overlap | `0.137` | scar tower visibly separated |
| Level-statistics `r` at `L=16` | `0.396` | small-size/full-sector proxy, still below paper-scale WD trend |
| Symmetry sector | `L=28`, dimension `13201` | same `k=0, I=+1` sector as the paper |
| Symmetry-resolved `r` | `0.497` | closer to GOE `0.531` than Poisson `0.386` |

## Interpretation

The reproduction captures the core physical story: the constrained PXP Hamiltonian creates a special trajectory from `|Z2>`, the spectrum contains a high-overlap tower of atypical states, and the same tower produces long-lived oscillations in local dynamics.

The symmetry-resolution method gap is closed at `L=28`. The remaining sector difference is scale: one dense float64 matrix for the paper's approximately 77k-dimensional `L=32` sector is about 47 GB before eigensolver workspace, beyond the current 40 GB A100 path. The thermodynamic-limit iTEBD runner at bond dimension around 400 also remains unimplemented. The `L=16` exact-dynamics comparator remains labeled as reduced scale and is not counted as iTEBD completion.
