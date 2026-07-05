# RunThePaper Roadmap

RunThePaper is a public case library for reproduced papers. The roadmap is
organized around one question: what helps a human reader trust, run, and improve
a reproduction case?

## Phase 1: Make The First Case Trustworthy

Current focus:

- keep `1803.01876` easy to read from the case README;
- keep the reproduction note, code, generated data, generated figures, and
  checks aligned;
- make the public boundary explicit: no original paper PDFs, arXiv source
  archives, original figures, or source-derived comparison assets are
  redistributed;
- document known limitations instead of hiding them.

Exit criteria:

- a new reader can understand what was reproduced without reading the internal
  harness repository;
- a technical reader can rerun the scripts and regenerate the public outputs;
- the case states whether it is feature-level, author-data-level, or partial
  reproduction.

## Phase 2: Make Contributions Safe

Next collaboration surface:

- add a reusable case template;
- add issue templates for reproduction requests, note review, and bug reports;
- define the minimum public artifacts for a new case;
- define what must stay out of the public repository.

The rule is simple: contributors should improve public cases, not import
private harness internals or copyrighted source assets.

## Phase 3: Make Reproducibility Automatic

Automation should protect the case contract:

- run public scripts in CI;
- check that generated outputs are present;
- scan for raw source artifacts and obvious secrets before merge;
- keep failures tied to a specific case and script.

CI should stay small. The goal is not to rebuild PRAgent/RRAgent inside this
repository, but to verify that public cases remain runnable.

## Phase 4: Publish And Invite Review

Public writing should point readers to inspectable artifacts:

- introduce the project positioning;
- publish one article per reproduced paper;
- link each article to the corresponding case directory;
- invite readers to request papers, review notes, and report unclear
  reproduction boundaries.

The audience is human first. If model companies later want training packs, they
can build those from the public materials.
