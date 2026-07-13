<h1 align="center">RunThePaper</h1>

<p align="center"><strong>From papers to runnable, checkable research.</strong></p>

<p align="center">
  <a href="#reproduction-catalog--论文复现目录">Explore cases</a> ·
  <a href="https://github.com/xi-zhao/runthepaper/issues/new">Request a paper</a> ·
  <a href="ROADMAP.md">Roadmap</a> ·
  <a href="CONTRIBUTING.md">Contribute</a>
</p>

RunThePaper is an open library of paper reproductions. Each case combines
bilingual notes, runnable code, generated results, validation checks, and an
explicit reproduction boundary.

## Reproduction Catalog / 论文复现目录

<!-- case-catalog:start -->
**10 public cases.** Open a paper below, then choose the reading or
reproduction resource you need.

| Paper | Publication / source | Reproduction status | Open package |
| --- | --- | --- | --- |
| [Edge states and topological invariants of non-Hermitian systems](cases/1803.01876/README.md) | [Physical Review Letters 121, 086803 (2018)](https://doi.org/10.1103/PhysRevLett.121.086803) | Paper-parameter complete reproduction | [中文 Note](cases/1803.01876/note/reproduction-note.zh-CN.md) · [English Note](cases/1803.01876/note/reproduction-note.en.md)<br>[Code](cases/1803.01876/code/README.md) · [Figures](cases/1803.01876/outputs/figures/) · [Checks](cases/1803.01876/outputs/checks/) |
| [Non-Hermitian Chern bands](cases/1804.04672/README.md) | [arXiv:1804.04672](https://arxiv.org/abs/1804.04672) | Feature-level reproduction | [中文 Note](cases/1804.04672/note/reproduction-note.zh-CN.md) · [English Note](cases/1804.04672/note/reproduction-note.en.md)<br>[Code](cases/1804.04672/code/README.md) · [Figures](cases/1804.04672/outputs/figures/) · [Checks](cases/1804.04672/outputs/checks/) |
| [Tackling the Qubit Mapping Problem for NISQ-Era Quantum Devices](cases/10.1145-3297858.3304023/README.md) | [DOI:10.1145-3297858.3304023](https://doi.org/10.1145/3297858.3304023) | Feature-level reproduction with partial benchmark coverage | [中文 Note](cases/10.1145-3297858.3304023/note/reproduction-note.zh-CN.md) · [English Note](cases/10.1145-3297858.3304023/note/reproduction-note.en.md)<br>[Code](cases/10.1145-3297858.3304023/code/README.md) · [Figures](cases/10.1145-3297858.3304023/outputs/figures/) · [Checks](cases/10.1145-3297858.3304023/outputs/checks/) |
| [Discrete time crystals: rigidity, criticality, and realizations](cases/1608.02589/README.md) | [arXiv:1608.02589](https://arxiv.org/abs/1608.02589) | Reduced-scale feature reproduction | [中文 Note](cases/1608.02589/note/reproduction-note.zh-CN.md) · [English Note](cases/1608.02589/note/reproduction-note.en.md)<br>[Code](cases/1608.02589/code/README.md) · [Figures](cases/1608.02589/outputs/figures/) · [Checks](cases/1608.02589/outputs/checks/) |
| [Quantum many-body scars](cases/1711.03528/README.md) | [arXiv:1711.03528](https://arxiv.org/abs/1711.03528) | Reduced-scale feature reproduction | [中文 Note](cases/1711.03528/note/reproduction-note.zh-CN.md) · [English Note](cases/1711.03528/note/reproduction-note.en.md)<br>[Code](cases/1711.03528/code/README.md) · [Figures](cases/1711.03528/outputs/figures/) · [Checks](cases/1711.03528/outputs/checks/) |
| [Simulating the Sycamore quantum supremacy circuits](cases/2103.03074/README.md) | [arXiv:2103.03074](https://arxiv.org/abs/2103.03074) | Reduced-scale feature reproduction | [中文 Note](cases/2103.03074/note/reproduction-note.zh-CN.md) · [English Note](cases/2103.03074/note/reproduction-note.en.md)<br>[Code](cases/2103.03074/code/README.md) · [Figures](cases/2103.03074/outputs/figures/) · [Checks](cases/2103.03074/outputs/checks/) |
| [Efficient simulation of logical magic state preparation protocols](cases/2512.23799/README.md) | [arXiv:2512.23799](https://arxiv.org/abs/2512.23799) | Partial feature reproduction | [中文 Note](cases/2512.23799/note/reproduction-note.zh-CN.md) · [English Note](cases/2512.23799/note/reproduction-note.en.md)<br>[Code](cases/2512.23799/code/README.md) · [Figures](cases/2512.23799/outputs/figures/) · [Checks](cases/2512.23799/outputs/checks/) |
| [An Algorithm for Fast Assembling Large-Scale Defect-Free Atom Arrays](cases/2604.08669/README.md) | [arXiv:2604.08669](https://arxiv.org/abs/2604.08669) | Reduced-scale feature reproduction | [中文 Note](cases/2604.08669/note/reproduction-note.zh-CN.md) · [English Note](cases/2604.08669/note/reproduction-note.en.md)<br>[Code](cases/2604.08669/code/README.md) · [Figures](cases/2604.08669/outputs/figures/) · [Checks](cases/2604.08669/outputs/checks/) |
| [Boson Sampling as a Probe of Chaotic and Integrable Quantum Dynamics](cases/2605.25398/README.md) | [arXiv:2605.25398](https://arxiv.org/abs/2605.25398) | Feature-level reproduction | [中文 Note](cases/2605.25398/note/reproduction-note.zh-CN.md) · [English Note](cases/2605.25398/note/reproduction-note.en.md)<br>[Code](cases/2605.25398/code/README.md) · [Figures](cases/2605.25398/outputs/figures/) · [Checks](cases/2605.25398/outputs/checks/) |
| [Sensitivity to perturbations in the three-dimensional Anderson model](cases/2605.25594/README.md) | [arXiv:2605.25594](https://arxiv.org/abs/2605.25594) | Reduced-scale feature reproduction | [中文 Note](cases/2605.25594/note/reproduction-note.zh-CN.md) · [English Note](cases/2605.25594/note/reproduction-note.en.md)<br>[Code](cases/2605.25594/code/README.md) · [Figures](cases/2605.25594/outputs/figures/) · [Checks](cases/2605.25594/outputs/checks/) |

Status describes reproduction scope, not rank. See [how to read reproduction quality](#how-to-read-reproduction-quality) and the [detailed case index](CASES.md) for audit scores and explicit boundaries.
<!-- case-catalog:end -->

## Run One Reproduction

Start with the paper-parameter complete reproduction of PRL 121, 086803 (2018):

```bash
git clone https://github.com/xi-zhao/runthepaper.git
cd runthepaper
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python cases/1803.01876/code/scripts/run_fig4_winding.py
```

The command regenerates the non-Bloch winding figure, CSV data, and JSON checks
under [`cases/1803.01876/outputs/`](cases/1803.01876/outputs/). See the [full
case instructions](cases/1803.01876/code/README.md) for the other figures.

## Why RunThePaper

- **Understand the method.** Trace the formulas, parameters, numerical choices,
  and limitations behind the headline result.
- **Run and verify it.** Recompute figures from code, inspect generated data,
  and check machine-readable evidence.
- **Build on it.** Use a working case as a research baseline, or contribute a
  correction, extension, or new target.

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

## Request or Contribute

Have a paper you want reproduced? [Open an
issue](https://github.com/xi-zhao/runthepaper/issues/new) with its title, DOI or
arXiv ID, and the figure or claim you care about most.

You can also rerun an existing case, report a problem, review its formulas or
checks, or extend it with new results. See the [contributing
guide](CONTRIBUTING.md) for the public-case rules.

## The Agent4Science Direction

The public reproduction case is the core product. Our self-developed
paper-reproduction agent is the system used to trace methods, implement
calculations, run paper parameters, and assemble the evidence behind each case.

Across many papers, these execution traces can become richer evaluation and
improvement data for scientific agents than papers alone.

## License

Code is licensed under the MIT License. Notes, generated figures, and generated
data are licensed under CC BY 4.0 unless a case states otherwise.

Third-party papers, source files, and original figures remain under their
original rights holders' terms and are not covered by this repository's license.
