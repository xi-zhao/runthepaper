# Formula verification

The audit formulas are verified; this does not endorse every frozen claim.

- `EQ_CLEAN`: standard matrix inversion and numerical substitution pass.
- `EQ_LOCAL`: cutoff-2/negative-imaginary frozen and cutoff-4/positive-imaginary RMP conventions both pass direct evaluation when kept separate.
- `EQ_FROZEN_POLE`: literal transcription reproduces 4.484506 meV, but fails the parent pole equation and cannot be labeled exact.
- `EQ_RMP_POLE`: transcription of RMP Eq. `impdwave1` passes, while the requested (c=0.3) violates its stated `log >> 1` control condition.

Executable evidence is in `tests/test_dwave_impurity_audit.py` and `outputs/data/idx16_gold_audit.json`.
