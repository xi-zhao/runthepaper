# Source audit

## Identity

- arXiv:2503.20566v2; title and authors match the frozen topic.
- Physical Review Letters 135, 130401 (2025), DOI `10.1103/3m3j-ds18`.
- The Hamiltonian, Gauss law, open-boundary convention, odd-Z2 sector, matter
  coupling, and 6x6 vison protocol all match the frozen record.

## Contract differences

- The source Z3 plots use sizes 8–24; frozen Task 1 asks for an exact-feasible
  5x5 extension at the same Hamiltonian and transition coupling.
- The source odd-Z2 maps are 32x32 and show a finite-size curve; frozen Task 2
  selects the 6x6 value.
- The source matter examples are 3x3/two-boson and 16x16/half-filled; frozen
  Task 3 asks for a 4x4 half-filled benchmark extension.
- Source Fig. 4(a) explicitly compares 6x6 GI-PEPS with exact diagonalization,
  matching frozen Task 4's Hamiltonian and preparation. The PDF legend names
  its third shown curve `P(2,2)`, whereas the independently verified frozen
  scalar belongs to `P(1,1)`.

No author code or raw arrays are packaged. The paper mentions TenPy only for a
separate one-dimensional benchmark. Frozen scalars were therefore audited with
independent exact solvers, not reverse engineered from rendered pixels.
