# Method Trace

## Pipeline

1. Read paper source and figure captions.
2. Classify figures into numerical, schematic, experimental, and out-of-scope targets.
3. Extract the model equations: PXP Hamiltonian, `Z2` states, FSA basis.
4. Verify formulas with small exact checks.
5. Generate structured data for each numerical target.
6. Plot generated figures from data.
7. Score each figure separately.

## Why This Order Matters

For this paper, running numerical plots before checking the Hamiltonian would be risky. A wrong blockade convention or boundary condition can still produce oscillatory-looking curves. The formula gate catches the core assumptions first:

- allowed states contain no adjacent excitations;
- dimensions match Fibonacci counting;
- the Hamiltonian flips only legally flippable sites;
- the particle-hole symmetry anticommutes with `H`;
- the FSA split reconstructs the Hamiltonian.

Only after these checks pass do the plotted results become meaningful.
