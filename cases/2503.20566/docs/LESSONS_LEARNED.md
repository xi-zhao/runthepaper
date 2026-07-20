# Lessons learned

1. A T3 tensor-network description can hide a much smaller exact physical
   Hilbert space once Gauss constraints and OBC are modeled first.
2. The odd-Z2 frozen notation means the square of the directional expectation;
   `<D^2>` is a different number and must not be substituted.
3. Source-panel labels and benchmark coordinates can differ while the numerical
   benchmark remains valid; direct Hamiltonian evaluation settles the contract.
4. The A100 was scientifically useful here, but the core acceleration came from
   a clean domain model rather than brute-force link-basis enumeration.
5. A paper-derived benchmark can be exact inside its frozen contract while
   remaining exploratory relative to every source-paper panel. Benchmark
   equality must never be encoded as `parameter_match=paper_exact`.

## New Failure Modes

- A source panel may label a different site coordinate than the frozen
  benchmark. Treat the source label as evidence about paper scope, not as a
  reason to silently rewrite the benchmark contract.
- An observable written as a squared bracket can mean either
  $\langle D\rangle^2$ or $\langle D^2\rangle$. Computing both cheaply exposes
  the ambiguity before a long run is launched.
- A formally correct link-basis implementation can be computationally
  impossible because it ignores Gauss-law reduction; estimate the physical
  Hilbert-space dimension before choosing the representation.
- Reusing a source-panel label for a reduced or synthetic benchmark can make a
  partial scalar look like paper-figure coverage. Inventory benchmark targets
  and source-paper assets as separate objects before scoring.

## Reusable Checks Or Tools

- Enumerate a spanning-tree Gauss-law reference field, then verify every
  reference state against all vertex constraints before eigensolving.
- Validate dual-space matrix-free operators against a tiny explicit sparse
  Hamiltonian before scaling them to the A100.
- Persist residual norms, state dimensions, device identity, wall time, and
  printed-gold deltas in the same result JSON so each scalar is auditable.
- Gate the workflow terminal on both axes: declared-target completion and
  `paper_scope_complete`. The former may be true while the latter is false.
