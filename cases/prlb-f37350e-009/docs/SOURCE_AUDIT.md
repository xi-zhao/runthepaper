# Source audit

## Verdict

`source_contract_mismatch`. The frozen record cannot be mapped to one PRL. It
combines three older, non-PRL sources and then adds formulas not supported by any
one of them.

## Direct lineage

| Frozen scope | Primary source | Direct evidence | Contract result |
| --- | --- | --- | --- |
| Task 1: `n_t` and `epsilon` | Wang, Zhang & Chen, arXiv:1512.03134v2 / Phys. Rev. D 94, 044033 (2016) | Source Eqs. `index`, `beta`, `index3` give `n_t=2 beta+4`, `epsilon=(beta+2)/(beta+1)`, and `n_t=-2 epsilon/(1-epsilon)`. | Wrong venue and year. |
| Task 2: graviton production | Same 2016 PRD | Source Eqs. `e1`, `betak` and surrounding text give `beta_k~k^-2`, `|beta_k|^2~k^-4`, and trace / `a''/a` jumps. | Wrong venue and year. |
| Task 3.1: massive scalar `rho_k,p_k` | Zhang, Ye & Wang, arXiv:1903.10115v4 | Source Eqs. `energykxi0`, `pk` give the minimally coupled massive scalar spectra. | de Sitter only; not a general power-law paper. |
| General power-law scalar regularization | Zhang, Wang & Ye, arXiv:1909.13010v2 / Chin. Phys. C 44, 095104 (2020) | Title, abstract, and Sec. 2 explicitly say **massless** scalar in general RW spacetime. | Does not support the frozen massive-power-law synthesis. |
| RGW comparison in Task 3.4 | 2016 PRD | Source Eqs. `reenergy`, `rp` give `p_re/rho_re=(beta-2)/(3(beta+4))`. | Formula supported, frozen downstream arithmetic is not. |

The 2019 massive-scalar source also warns that conventional fourth-order
subtraction can over-subtract and produce a negative spectrum; it does not
present the frozen arbitrary-power-law massive counterterms as a validated
result.

## Figure source

The numerical target is Fig. 2 of the 2016 PRD, stored in its original e-print
as `paper-source_rgw/Fig2.eps`. The reference PNG is a 200-dpi crop of PDF page 6;
it is evidence extraction, not a generated reference. The figure uses the exact
`beta=-2` Hankel-function specialization.

## Terminal interpretation

Source invalidity alone would justify `benchmark_source_invalid`. The frozen
gold also contains independently demonstrable formula errors, so the campaign's
more informative terminal state is `benchmark_gold_invalid` while retaining
this source-contract finding.
