# Source audit

The frozen record maps to Robert Ott, Daniel González-Cuadra, Torsten V. Zache, Peter Zoller, Adam M. Kaufman, and Hannes Pichler, *Error-Corrected Fermionic Quantum Processors with Neutral Atoms*, PRL 135, 090601 (2025), DOI `10.1103/zkpl-hh28`, arXiv:2412.16081v1. The complete TeX and all four vector figures are present.

The paper's main derivation assumes the strict regime `M_r > N > M_s`. It states `P[R,R†]P=0` and the exact referenced CAR. The supplement notes that `N=M_r=M_s` is the minimum-resource realization, but does not promote its two boundary defects to identities throughout the weak-inequality domain.

The logical operator, vacuum, stabilizers, physical parity errors, error-free exchange cycle, and calibration `<Y>=-cos Theta` are direct source content. The coherent `V(lambda)=exp(i lambda Xi)` modification and the Task-5 overlap are benchmark additions. The paper does not specify the action of the error-free logical cycle on the benchmark's uncorrected syndrome sector.

Fig. 4(c) reports 100,000 random-error realizations with 99% Clopper-Pearson intervals. The archive supplies only the rendered panel, not its arrays, RNG seed, simulation code, or complete gate-level error schedule; exact pixel registration is therefore not auditable.
