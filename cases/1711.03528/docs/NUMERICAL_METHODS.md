# Numerical Methods

## Local Compute Decision

The base run was completed on an Apple M3 Pro with 18 GB memory. A later symmetry-resolved run reached `L=28`, `k=0`, `I=+1` (dimension 13201). The paper's `L=32` sector remains outside the current single 40 GB A100 dense path because one float64 matrix alone is about 47 GB before eigensolver workspace.

Default local scale:

- exact diagonalization for the main scar plot: `L=16`, PBC, full constrained Hilbert space;
- time evolution: `L=16`, PBC, finite-size exact evolution;
- level statistics: `L=12, 14, 16`, full constrained sector.
- symmetry-resolved scar tower and unfolded level statistics: `L=28`, `k=0`, `I=+1`.

## Model Implementation

The code builds the constrained Hilbert space explicitly. A basis state is a bitstring with no adjacent excitations. The Hamiltonian matrix has unit entries between two basis states if one allowed Rydberg flip connects them.

Implemented files:

- `src/pxp_scars.py`: basis, Hamiltonian, symmetry checks, FSA, dynamics, ED observables.
- `scripts/run_reproduction.py`: generates CSV data and JSON checks.
- `scripts/plot_reproduction.py`: renders all reproduction figures from CSV.
- `scripts/run_symmetry_resolved_sector.py`: runs the `L=28` sector calculation.
- `scripts/plot_symmetry_resolved_sector.py`: redraws saved sector data without rerunning ED.

## Data Generated Before Plotting

- `outputs/data/fig1_graph_nodes.csv`
- `outputs/data/fig1_graph_edges.csv`
- `outputs/data/fig_ent_dynamics.csv`
- `outputs/data/fig2a_scar_overlaps.csv`
- `outputs/data/fig2bc_fsa_basis_overlaps.csv`
- `outputs/data/fig2d_participation_ratio.csv`
- `outputs/data/fig4_level_spacing_distribution.csv`
- `outputs/data/fig4_density_of_states.csv`
- `outputs/data/sector_scar_tower.csv`
- `outputs/data/sector_level_spacings.csv`

## Feature Checks

The run checks:

- Fibonacci Hilbert-space dimension.
- Particle-hole anticommutation.
- `H = H+ + H-`.
- FSA closure to `L+1` basis vectors.
- `Z2` oscillation period.
- `Z2` return revival compared with the vacuum state.
- High-overlap scar tower.
- Participation-ratio enhancement of special states.
- Small-size level-spacing trend.
- Exact small-size containment of the symmetry-sector spectrum in the full spectrum.
- `L=28` scar-tower count and spacing uniformity.
- Symmetry-resolved GOE-vs-Poisson gap-ratio and unfolded-spacing gates.
