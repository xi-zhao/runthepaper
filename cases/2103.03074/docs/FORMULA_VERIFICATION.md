# Formula Verification

This case uses `EQUATION_CARDS.json` as the machine-readable formula map.

Machine-readable result:

```text
outputs/checks/formula_verification.json
```

Run:

```bash
cat cases/2103.03074/outputs/checks/formula_verification.json
```

## Gate Summary

| Formula | Role | Gate | Reason |
| --- | --- | --- | --- |
| BBTN001 | Output probability | verified | Defines circuit output probability. |
| BBTN002 | Bitstring split | verified | Defines closed/open bitstring partition for batching. |
| BBTN003 | Head-tail amplitude factorization | verified | Defines reusable big-batch tensor-network contraction object. |
| BBTN004 | XEB fidelity | verified | Defines XEB fidelity estimator used by benchmark curves. |
| BBTN005 | Porter-Thomas distribution | verified | Defines scaled output-probability reference distribution. |
| BBTN006 | Conditional probability | verified | Defines normalized conditional batch distribution. |

## Closed Or Unclear Formulas

None in the current local feature-level reproduction.
