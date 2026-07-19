# Formula Verification

Machine-readable gate: `outputs/checks/formula_verification.json`.

## Gate Summary

All eight cards are numerically open; no target ran before this gate passed.

| Formula | Role | Derivation status | Numeric gate | Main check |
| --- | --- | --- | --- | --- |
| EQ001 | finite AA Hamiltonian | verified | open | Hermiticity and clean-chain spectrum |
| EQ002 | GAA corrections | verified | open | source parameters and Hermiticity |
| EQ003 | steady cavity amplitude | verified | open | zero-pump and positivity limits |
| EQ004 | susceptibility channels | verified | open | positivity and completeness sum rule |
| EQ005 | critical pump | reconstructed | open | clean source-curve intercept `0.2768J` |
| EQ006 | localized self-channel | verified | open | IPR classifier and deep-localized limit |
| EQ007 | momentum/channel indices | verified | open | Parseval scale and indices `151,137,27` |
| EQ008 | nonlinear mean field | reconstructed | open | zero-field limit and normalization |

## Disclosed Formula Ambiguities

- EQ005: arXiv v1/source Fig. 3 uses a two-factor detuning shift; the literal published expression suggests one factor. The source curve selects two for linear targets.
- EQ008/EQ003: the literal published one-factor cavity denominator reproduces nonlinear Fig. 4(a), so nonlinear and linear conventions remain target-local.
- S1: the equations are explicit, but pump samples and solver initialization are missing.

These uncertainties cap the similarity score at feature level; they are not hidden as implementation defaults.
