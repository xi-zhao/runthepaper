# Method Trace

## METHOD001 - formula-first full-review pipeline

- Source: arXiv main text Eq. (1)-(164), Appendices A-C, formal RMP cross-version audit.
- Product rule: no numeric target runs before its formula family has source anchors, assumptions, numerical form, checks and code pointers.
- Inputs: frozen PDFs/TeX, `EQUATION_CARDS.json`, `paper_scope.json`, `full_rmp_scope.json`.
- Flow: paper map -> target ledger -> formula derivation -> formula gate -> structured data -> figures -> invariant checks -> similarity score -> PDF visual QA.
- Outputs: 30 equation cards, 27 total targets, 18 scored numerical targets, 20 generated datasets in the project manifest, 18 rendered evidence figures, 20 evidence comparisons.
- Code: `scripts/run_reproduction.py`, `scripts/run_full_rmp_reproduction.py`, `src/`, `tests/`.
- Checks: 30/30 formula families open; 18/18 scored targets pass; 24 tests pass; project and claim ledgers pass with zero findings.
- Status: completed for public formula/theory scope.
- External dependency: author COMSOL project and three author-level experimental datasets remain unavailable.
