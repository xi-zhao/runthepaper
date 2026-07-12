# Formula Verification

This case uses `EQUATION_CARDS.json` as the machine-readable formula map.

Machine-readable result:

```text
outputs/checks/formula_verification.json
```

Run:

```bash
cat cases/2512.23799/outputs/checks/formula_verification.json
```

## Gate Summary

| Formula | Role | Gate | Reason |
| --- | --- | --- | --- |
| MSC001 | Magic states as PSC eigenstates | verified | Defines PSC checks for magic-state structure. |
| MSC002 | Controlled-H Pauli propagation | verified | Checks simplest controlled-H Clifford-error propagation identity. |
| MSC003 | Pauli-rank fidelity expansion | verified | Defines Pauli expectation route for magic-state fidelity. |
| MSC004 | Toy benchmark acceptance model | reconstructed | Defines proxy acceptance model for local benchmark checks. |
| MSC005 | Toy benchmark infidelity model | reconstructed | Defines proxy conditional logical infidelity model. |
| MSC006 | Runtime and sampling proxy | reconstructed | Defines local proxy for average time per shot and sampling scaling. |

## Closed Or Unclear Formulas

None in the current local feature-level reproduction.
