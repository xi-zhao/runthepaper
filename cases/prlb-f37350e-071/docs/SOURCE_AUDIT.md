# Source audit

## Identity

- title: *Unwanted Couplings Can Induce Amplification in Quantum Memories despite Negligible Apparent Noise*;
- arXiv:2411.15362;
- Physical Review Letters 135, 070802 (2025);
- DOI: 10.1103/pz34-47pw.

The PDF and arXiv source archive are stored under `raw/`.

## Formula provenance

The source derives a semi-analytic four-level equation, defines `alpha`, and gives a simplified unwanted-coupling term whose solution has square-root detuning splitting (`main.tex:196-242`). This supports the physical motivation and the form audited in Tasks 1-2.

## Scope boundary

The source explicitly states that its treatment is semiclassical and that quantitative noise requires a full Heisenberg-Langevin analysis (`main.tex:288-290`). Therefore frozen Task 5 is not a source result. Tasks 3-4 are likewise benchmark extensions.

## Data availability finding

The source bundle includes TeX and rendered PDF/PNG figures. It does not include numerical arrays, model code, optimization histories, or solver configuration sufficient for pixel-level paper-figure reproduction.
