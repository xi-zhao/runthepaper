# Lessons learned

## New Failure Modes

1. A coherent topic title does not prove a coherent paper source. Here “massive”
   and “general power-law” come from different scalar papers.
2. A correct intermediate WKB formula can coexist with incorrect downstream
   counterterms. Substitution into the defining observable is the decisive gate.
3. Always check a claimed fixed point in the displayed rational formula. The
   frozen RGW claim fails by direct arithmetic at `beta=-2`.
4. Paper-exact curve reproduction remains valuable even when the benchmark gold
   fails, provided paper scope and audit scope are scored separately.
5. A100 usage should follow the verification signal, not the nominal difficulty
   label. Closed-form asymptotics and pixels are stronger here than more compute.

## Reusable Checks Or Tools

- Add a source-scope matrix that tests attributes such as massive/massless and
  de Sitter/general RW independently; topic overlap is not source equivalence.
- After accepting a WKB amplitude, automatically substitute it into every
  downstream stress-tensor definition and compare powers of `a`, `m`, and `tau`.
- Evaluate every claimed rational fixed point in the displayed formula before
  accepting its physical label.

These candidates are recorded in `PRAgent-workflow/HARNESS_BACKLOG.md` under this
case ID.
