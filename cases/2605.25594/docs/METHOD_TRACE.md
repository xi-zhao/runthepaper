# Method Trace

## Local Reproduction Method

1. Build the open-boundary 3D Anderson Hamiltonian for `L=4,5,6,7`.
2. Add uniform onsite disorder `epsilon_i in [-W/2, W/2]`.
3. Diagonalize the full single-particle Hamiltonian exactly.
4. Select the central `20%` eigenstates, matching the paper's energy-window rule.
5. Transform the perturbation operator `T_s` into the eigenbasis.
6. Compute `chi_n`, `chi_n^r`, `chi_typ^r`, `chi_av^r`, gap ratio, and IPR.
7. Generate CSV data before plotting.
8. Run JSON feature checks before writing the case summary.

## Why This Is Only Feature-Level

The paper uses systems up to `L=38`, i.e. `V=54872` single-particle sites, and averages over multiple disorder realizations. A full dense diagonalization of such matrices is not realistic on the current local machine.

The local case therefore uses exact diagonalization at small `L`. This is good enough to test the formula chain and several physical features, but not enough to claim exact paper-scale peak positions or fitted exponents.

## Implemented Checks

- Formula gate: `outputs/checks/formula_verification.json`
- Feature gate: `outputs/checks/anderson_feature_checks.json`
- Similarity scoring: `outputs/checks/similarity_scorecard.json`
- Performance profile: `outputs/checks/performance_profile.json`
