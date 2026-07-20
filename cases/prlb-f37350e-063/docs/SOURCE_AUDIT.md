# Source audit

## Identity gate

- arXiv: `2502.05267v3`
- publication: *Physical Review Letters* **135**, 123401 (2025)
- DOI: `10.1103/gphr-d1bc`
- direct source bundle: `paper-source/main_wrefs.tex`, `paper-source/supp_wrefs.tex`, and rendered PDF figures

Status: `verified_direct_prl`.

## Formula gate

The source explicitly provides:

- the Hatano-Nelson matrix and `J_+`, `J_-`, and `Delta` definitions;
- the open-boundary eigenvector with site-dependent factor `r^j exp(i delta j/2)`;
- the two finite-size vacuum thresholds on the two sides of `gamma=J`;
- periodic plane-wave solutions and the particle-hole transformation;
- the CEP diagnostic as a Jacobian evaluated on a steady-state solution approached from the static phase.

## Important protocol boundary

Frozen Task 4 is not a transcription of the source method. It defines independent finite-time trajectories, a residual gate, finite-difference Jacobians, and fixed tolerances. That extension can be audited, but failure of that extension does not contradict the paper's steady-state-continuation CEP evidence.
