# RunThePaper

**An open, inspectable library of paper reproductions.**

Built with our self-developed paper reproduction Agent, RunThePaper turns
papers into readable notes, runnable code, generated figures, and checkable
evidence. The Agent4Science goal is to move from paper summarization to research
that readers can run, audit, and extend.

[Paper catalog](#paper-reproduction-catalog--论文复现目录) ·
[What each case includes](#what-each-case-includes) ·
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

## What Each Case Includes

- Chinese and English reproduction notes;
- runnable code and run commands;
- generated data and figures;
- machine-readable checks, an audit score, and an explicit limitation statement;
- derivation, numerical-method, and lessons-learned documents where relevant.

## How To Participate

- request a paper by providing its title, DOI or arXiv ID, and the figure or
  claim you most want reproduced;
- run an existing case and report any environment, numerical, or documentation
  problem;
- review or extend a case and share corrections, checks, or new results.

Start by [opening an issue](https://github.com/xi-zhao/runthepaper/issues) with
the paper and target result. You do not need to work on the Agent itself.

## How To Read Reproduction Quality

Final public figures use the paper's parameters whenever public inputs and
available resources make that possible. Otherwise the case is labeled as
reduced-scale, subset, proxy, or blocked; a test-scale result is never presented
as a complete reproduction.

The audit score measures the coverage of available evidence. It is not a
percentage of physical correctness, a visual similarity rating, a cross-paper
ranking, or a publication threshold. Read the status and limitation statement
together with the score.

Original paper PDFs, source archives, figures, and extracted plotting data are
not redistributed here. Each case links to the official paper and states its
remaining reproduction boundary.

## License

Code is licensed under the MIT License. Notes, generated figures, and generated
data are licensed under CC BY 4.0 unless a case states otherwise.

Third-party papers, source files, and original figures remain under their
original rights holders' terms and are not covered by this repository's license.
