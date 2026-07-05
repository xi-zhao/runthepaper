# RunThePaper

RunThePaper is an open research reproduction project.

We turn papers into readable reproduction notes, runnable code, checkable data,
reproduced figures, and honest reproduction boundaries.

## What This Repository Is

This repository publishes the human-facing outputs of our paper reproduction
work:

- reproduction notes;
- paper-derived numerical code;
- generated data and figures;
- validation checks and scorecards;
- lessons learned from failed and successful reproduction attempts.

The work is produced with a separate harness project, currently called
PRAgent/RRAgent. That harness is the production system. RunThePaper is the
public case library.

## What This Repository Is Not

RunThePaper is not a paper PDF mirror, an arXiv source mirror, or a model
training pack.

Original papers, publisher PDFs, arXiv source archives, and original figure
assets are not redistributed here. When a case uses those materials for
internal comparison, the public case records the evidence boundary and points
readers back to the official paper source.

## Current Cases

| Paper ID | Topic | Status |
| --- | --- | --- |
| `1803.01876` | Non-Hermitian SSH model and non-Bloch bulk-boundary correspondence | First public reproduction case |

Start here:

- [Case README](cases/1803.01876/README.md)
- [Reproduction Note](cases/1803.01876/note/reproduction-note.md)
- [Code README](cases/1803.01876/code/README.md)

## Repository Structure

```text
cases/
  <paper-id>/
    README.md              # public case overview
    note/                  # human-readable reproduction note
    code/                  # runnable reproduction code
    docs/                  # derivation, methods, scorecards, lessons
    outputs/
      data/                # generated CSV data
      figures/             # generated figures
      checks/              # validation JSON
```

## Reproduction Boundary

Each case separates:

- paper claims from our reproduction claims;
- generated numerical data from reference data;
- feature-level reproduction from author-data-level reproduction;
- scientific agreement from visual styling similarity;
- successful reproduction from remaining gaps.

This is the core rule of RunThePaper: do not hide uncertainty.

## License

Code is licensed under the MIT License. Notes, generated figures, and generated
data are licensed under CC BY 4.0 unless a case states otherwise.

Third-party papers, source files, and original figures remain under their
original rights holders' terms and are not covered by this repository's license.
