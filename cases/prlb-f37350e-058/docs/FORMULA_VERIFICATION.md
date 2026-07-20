# Formula verification

All five numerical gates are open; see
`outputs/checks/formula_verification.json`.

| Formula | Status | Basis |
| --- | --- | --- |
| `EQ_KERNEL` | verified | direct source plus removable-diagonal check |
| `EQ_PARITY_NORM` | verified | exact operator conjugation and discrete spectral symmetry |
| `EQ_DUAL` | reconstructed | Lagrange/Hellmann-Feynman derivation; absent from paper |
| `EQ_GAUSSIAN` | reconstructed | Gaussian Fourier multiplier; paper labels topic future work |
| `EQ_NYSTROM` | verified | direct source and machine-precision published-row calibration |

`reconstructed` formulas may feed this audit but cap the benchmark target score;
they do not become source-paper claims.
