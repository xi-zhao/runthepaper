# Reproduction Report

## Scope

This case reproduces the numerical features of arXiv:1711.03528, "Quantum many-body scars", at feature level.

Completed:

- arXiv PDF and source ingested.
- Paper figures rendered from source.
- Numerical figures classified.
- PXP Hamiltonian and constrained Hilbert space implemented.
- Formula checks passed before numerical plotting.
- Four reproduction figures generated from structured CSV data.

Not completed:

- Full `L=32` symmetry-resolved exact diagonalization.
- Thermodynamic-limit iTEBD with bond dimension 400.
- Exact unfolded level-spacing distribution in the paper's `k=0, I=+` sector.

## Commands

From the project root:

```bash
python3 cases/1711.03528/code/scripts/run_reproduction.py
python3 cases/1711.03528/code/scripts/plot_reproduction.py
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

## Interpretation

The reproduction captures the core physical story: the constrained PXP Hamiltonian creates a special trajectory from `|Z2>`, the spectrum contains a high-overlap tower of atypical states, and the same tower produces long-lived oscillations in local dynamics.

The main limitation is scale and symmetry resolution. The original paper uses larger symmetry-resolved sectors and iTEBD. The local case verifies the mechanism, but does not claim complete paper-scale numerical reproduction.
