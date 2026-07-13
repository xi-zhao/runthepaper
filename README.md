# RunThePaper

RunThePaper is an open research reproduction project.

We turn papers into readable reproduction notes, runnable code, checkable data,
reproduced figures, and honest reproduction boundaries.

## What This Repository Is

This repository publishes the human-facing outputs of our paper reproduction
work:

- Chinese and English getting-started reproduction notes;
- paper-derived numerical code;
- generated data and figures;
- validation checks and scorecards;
- lessons learned from failed and successful reproduction attempts.

RunThePaper is the public collaboration surface: readers can inspect, run,
question, extend, and improve each case.

## The Reproduction Agent Behind the Project

RunThePaper is supported by a separate reproduction system, currently called
PRAgent/RRAgent. The public project and the reproduction agent serve different
roles: RunThePaper is the open case library; the agent is the execution engine
used to produce and validate those cases.

The longer-term Agent4Science goal is to move beyond AI systems that only read
or summarize papers. A reproduction agent should be able to turn a paper into
an executable and checkable workflow:

1. identify the paper's claims, target figures, and required evidence;
2. trace formulas, parameters, boundary conditions, and numerical methods;
3. implement and run the calculation with the paper's final parameters;
4. compare generated results against physical and numerical acceptance checks;
5. record failures, uncertainty, and the remaining reproduction boundary.

The reproduction notes in this repository are the human-readable entry points
created from that execution process. Code, generated data, figures, and checks
preserve the evidence behind each note. Across many papers, these real
execution traces can also become useful evaluation and improvement data for
scientific agents.

## How To Participate

You can participate without working on the agent itself:

- request a paper by providing its title, DOI or arXiv ID, and the figure or
  claim you most want reproduced;
- run an existing case and report any environment, numerical, or documentation
  problem;
- review formulas, parameters, code, checks, or reproduction boundaries;
- extend a case and share what you learn from using it as a research baseline.

Open a GitHub issue with enough context for another researcher to understand
the target. Every concrete request, correction, and extension helps improve the
public case library.

## What This Repository Is Not

RunThePaper is not a paper PDF mirror, an arXiv source mirror, or a model
training pack.

Original papers, publisher PDFs, arXiv source archives, and original figure
assets are not redistributed here. When a case uses those materials for
internal comparison, the public case records the evidence boundary and points
readers back to the official paper source.

## Start Here

RunThePaper currently publishes 10 inspectable reproduction cases across
non-Hermitian physics, many-body dynamics, quantum circuits, atom-array
assembly, boson sampling, and localization.

### Featured case: PRL 121, 086803 (2018)

The `1803.01876` case reproduces the open-boundary spectrum, generalized
Brillouin zone, skin profiles, non-Bloch winding, and the nonzero-`t3`
extension with the paper's final parameters.

- [Case overview and four main reproduced figures](cases/1803.01876/README.md)
- [中文复现 Note](cases/1803.01876/note/reproduction-note.zh-CN.md)
- [English reproduction note](cases/1803.01876/note/reproduction-note.en.md)
- [Runnable code](cases/1803.01876/code/README.md)

Browse the project:

- [All published cases](CASES.md)
- [Project roadmap](ROADMAP.md)
- [How to contribute](CONTRIBUTING.md)

## Repository Structure

```text
cases/
  <paper-id>/
    README.md              # public case overview
    note/                  # Chinese and English getting-started notes
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

## Publication Contract

A case is ready to publish when it has both Chinese and English notes, runnable
public scripts, generated outputs, machine-readable checks, and an explicit
limitation statement. The audit score is supporting evidence, not a publishing
threshold.

Final figures use the paper's parameters whenever local resources and public
inputs make that possible. If a paper-scale run is not feasible, the case must
be labeled as reduced-scale, subset, proxy, or blocked; a test-scale result must
not be presented as a complete reproduction.

Maintainers can verify the public package with:

```bash
python scripts/render_case_catalog.py --check
python scripts/validate_public_cases.py
python -m compileall -q scripts cases
```

## License

Code is licensed under the MIT License. Notes, generated figures, and generated
data are licensed under CC BY 4.0 unless a case states otherwise.

Third-party papers, source files, and original figures remain under their
original rights holders' terms and are not covered by this repository's license.
