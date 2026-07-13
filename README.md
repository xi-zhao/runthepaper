# RunThePaper

RunThePaper is an open research reproduction project.

We turn papers into readable reproduction notes, runnable code, checkable data,
reproduced figures, and honest reproduction boundaries.

[Paper catalog](#paper-reproduction-catalog--论文复现目录) ·
[How to participate](#how-to-participate) ·
[Project roadmap](ROADMAP.md) ·
[Contributing guide](CONTRIBUTING.md)

## Paper Reproduction Catalog / 论文复现目录

<!-- case-catalog:start -->
**10 published cases.** Choose a paper below to open its case overview or go
directly to the bilingual notes, runnable code, and generated figures.

| Paper | Research topic | Reproduction status | Open resources |
| --- | --- | --- | --- |
| [Edge states and topological invariants of non-Hermitian systems](cases/1803.01876/README.md)<br>[Physical Review Letters 121, 086803 (2018)](https://doi.org/10.1103/PhysRevLett.121.086803) | Non-Hermitian SSH model and non-Bloch bulk-boundary correspondence | Paper-parameter complete reproduction | [中文 Note](cases/1803.01876/note/reproduction-note.zh-CN.md) · [English Note](cases/1803.01876/note/reproduction-note.en.md)<br>[Code](cases/1803.01876/code/README.md) · [Figures](cases/1803.01876/outputs/figures/) |
| [Non-Hermitian Chern bands](cases/1804.04672/README.md)<br>[arXiv:1804.04672](https://arxiv.org/abs/1804.04672) | Non-Hermitian Chern bands and non-Bloch Chern physics | Feature-level reproduction | [中文 Note](cases/1804.04672/note/reproduction-note.zh-CN.md) · [English Note](cases/1804.04672/note/reproduction-note.en.md)<br>[Code](cases/1804.04672/code/README.md) · [Figures](cases/1804.04672/outputs/figures/) |
| [Tackling the Qubit Mapping Problem for NISQ-Era Quantum Devices](cases/10.1145-3297858.3304023/README.md)<br>[DOI:10.1145-3297858.3304023](https://doi.org/10.1145/3297858.3304023) | SABRE qubit mapping and routing | Feature-level reproduction with partial benchmark coverage | [中文 Note](cases/10.1145-3297858.3304023/note/reproduction-note.zh-CN.md) · [English Note](cases/10.1145-3297858.3304023/note/reproduction-note.en.md)<br>[Code](cases/10.1145-3297858.3304023/code/README.md) · [Figures](cases/10.1145-3297858.3304023/outputs/figures/) |
| [Discrete time crystals: rigidity, criticality, and realizations](cases/1608.02589/README.md)<br>[arXiv:1608.02589](https://arxiv.org/abs/1608.02589) | Floquet many-body dynamics and discrete time crystals | Reduced-scale feature reproduction | [中文 Note](cases/1608.02589/note/reproduction-note.zh-CN.md) · [English Note](cases/1608.02589/note/reproduction-note.en.md)<br>[Code](cases/1608.02589/code/README.md) · [Figures](cases/1608.02589/outputs/figures/) |
| [Quantum many-body scars](cases/1711.03528/README.md)<br>[arXiv:1711.03528](https://arxiv.org/abs/1711.03528) | PXP dynamics and quantum many-body scars | Reduced-scale feature reproduction | [中文 Note](cases/1711.03528/note/reproduction-note.zh-CN.md) · [English Note](cases/1711.03528/note/reproduction-note.en.md)<br>[Code](cases/1711.03528/code/README.md) · [Figures](cases/1711.03528/outputs/figures/) |
| [Simulating the Sycamore quantum supremacy circuits](cases/2103.03074/README.md)<br>[arXiv:2103.03074](https://arxiv.org/abs/2103.03074) | Sycamore random-circuit simulation | Reduced-scale feature reproduction | [中文 Note](cases/2103.03074/note/reproduction-note.zh-CN.md) · [English Note](cases/2103.03074/note/reproduction-note.en.md)<br>[Code](cases/2103.03074/code/README.md) · [Figures](cases/2103.03074/outputs/figures/) |
| [Efficient simulation of logical magic state preparation protocols](cases/2512.23799/README.md)<br>[arXiv:2512.23799](https://arxiv.org/abs/2512.23799) | Logical magic-state preparation simulation | Partial feature reproduction | [中文 Note](cases/2512.23799/note/reproduction-note.zh-CN.md) · [English Note](cases/2512.23799/note/reproduction-note.en.md)<br>[Code](cases/2512.23799/code/README.md) · [Figures](cases/2512.23799/outputs/figures/) |
| [An Algorithm for Fast Assembling Large-Scale Defect-Free Atom Arrays](cases/2604.08669/README.md)<br>[arXiv:2604.08669](https://arxiv.org/abs/2604.08669) | Defect-free atom-array assembly | Reduced-scale feature reproduction | [中文 Note](cases/2604.08669/note/reproduction-note.zh-CN.md) · [English Note](cases/2604.08669/note/reproduction-note.en.md)<br>[Code](cases/2604.08669/code/README.md) · [Figures](cases/2604.08669/outputs/figures/) |
| [Boson Sampling as a Probe of Chaotic and Integrable Quantum Dynamics](cases/2605.25398/README.md)<br>[arXiv:2605.25398](https://arxiv.org/abs/2605.25398) | Boson sampling and quantum-chaos probes | Feature-level reproduction | [中文 Note](cases/2605.25398/note/reproduction-note.zh-CN.md) · [English Note](cases/2605.25398/note/reproduction-note.en.md)<br>[Code](cases/2605.25398/code/README.md) · [Figures](cases/2605.25398/outputs/figures/) |
| [Sensitivity to perturbations in the three-dimensional Anderson model](cases/2605.25594/README.md)<br>[arXiv:2605.25594](https://arxiv.org/abs/2605.25594) | Three-dimensional Anderson localization | Reduced-scale feature reproduction | [中文 Note](cases/2605.25594/note/reproduction-note.zh-CN.md) · [English Note](cases/2605.25594/note/reproduction-note.en.md)<br>[Code](cases/2605.25594/code/README.md) · [Figures](cases/2605.25594/outputs/figures/) |

For audit scores and reproduction boundaries, see the [detailed case index](CASES.md).
<!-- case-catalog:end -->

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
