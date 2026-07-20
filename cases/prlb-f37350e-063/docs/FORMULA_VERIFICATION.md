# Formula verification

All six equation cards are open for numeric use.

- Source identity and definitions were read from the direct TeX bundle.
- Exact eigenpairs satisfy relative residual below `2e-14` for both `gamma=0.3` and `gamma=1.7` test regimes.
- Frozen Task 1 pairings have minimum residual `0.0575` and `0.299`, respectively, despite matching the eigenvalue set up to relabeling.
- The finite-size threshold agrees with direct eigenvalue stability.
- Both PH-compatible static branches satisfy the substituted equations.
- The full frozen CEP grid and its robustness variants were executed on A100.

Machine-readable status is generated at `outputs/checks/formula_verification.json`.
