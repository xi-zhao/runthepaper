# Contributing

RunThePaper accepts contributions that make a reproduction case more accurate,
clear, runnable, or honest.

Good contributions include:

- fixing a derivation mistake;
- improving a numerical method;
- adding a missing validation check;
- reducing ambiguity in a reproduction note;
- reporting a mismatch between generated results and the paper;
- adding a new case with clear evidence boundaries.

Please do not add original paper PDFs, publisher source archives, or original
figure assets unless the license explicitly allows redistribution and the case
documents that permission.

Limited source-versus-reproduction comparison panels are allowed only when they
are necessary for validation. Use the minimum source excerpt, label both sides,
cite the official paper, keep the standalone source panel out of the repository,
and state that visual agreement is not author-data-level equivalence.

For each case, keep the public boundary clear:

- generated data belongs in `outputs/data/`;
- generated figures belong in `outputs/figures/`;
- limited validation comparison panels belong in `docs/comparisons/`;
- validation results belong in `outputs/checks/`;
- paper/source references should be links or citations, not copied raw assets.

## Before Opening a Pull Request

Regenerate navigation after adding or changing a catalog entry:

```bash
python scripts/render_case_catalog.py
```

Then verify the public package:

```bash
python scripts/render_case_catalog.py --check
python scripts/validate_public_cases.py
python -m compileall -q scripts cases
```
