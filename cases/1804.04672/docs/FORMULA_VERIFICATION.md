# Formula Verification

This document explains which formulas are allowed to feed numerical reproduction.

Machine-readable result:

```text
outputs/checks/formula_verification.json
```

Run:

```bash
cd cases/1804.04672/code
python scripts/run_first_target.py
python scripts/run_cylinder_phase_diagram.py
python scripts/run_gap_scaling.py
```

## Gate Summary

| Formula | Role | Gate | Reason |
| --- | --- | --- | --- |
| `EQC001` | Main Bloch Hamiltonian | source_traced | Source-traced and used by `code/src/nonhermitian_chern.py`. |
| `EQC002` | Cylinder finite-strip Hamiltonian | reconstructed/source_only | Reconstructed from the source model and open-boundary hopping; used by the first runner. |
| `EQC003` | Non-Bloch Chern number | source_only | Interpretive context only; not used by the first runner. |
| `EQC004` | Cylinder non-Bloch bulk continuum | source_only | Supplement-derived equal-modulus condition used by the edge-branch diagnostic. |

## Closed Or Unclear Formulas

| Formula | Reason | Numerical consequence |
| --- | --- | --- |
| `EQC003` | Not needed for first spectrum data. | Do not claim full non-Bloch topological invariant reproduction from `T001` alone. |
| `EQC004` | Used as a diagnostic reference for skin-localized bulk candidates. | The rendered red branch is selected by the analytic chiral edge trace; `EQC004` explains why boundary weight alone is not a valid red-branch rule. |
