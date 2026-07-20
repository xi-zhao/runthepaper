# Source audit — idx8

Status: `source_contract_mismatch`; numeric gold is independently valid.

## Direct formula source

The frozen rotating Hamiltonian, coefficients `B`, `C`, and `gamma`, linearized Hamiltonian, separatrix peak, Poincaré action, and adiabatic eccentricity trend match Liu & Lai, “Extreme Resonant Eccentricity Excitation of Stars around Merging Black-Hole Binary,” arXiv:2403.03250v2 / *Phys. Rev. Lett.* **132**, 231403 (2024).

Source locations in `paper-source_prl/ms.tex`:

- Eqs. `ROT potential` and `dimensionless Hamiltonian`, lines 248–270.
- Poincaré action and eccentricity increase, lines 277–301.
- Small-eccentricity Hamiltonian and separatrix peak, lines 822–889.

This PRL predates the frozen benchmark window.

## Closest in-window source

Hu, Liu & Zhu, arXiv:2509.20806v2 / *ApJL* (2025), uses the same physical mechanism for Gaia BH3 and cites the 2024 PRL. It is not a PRL. Moreover, it defines

$$
\gamma_{\rm ApJL}=\frac{\dot\varpi_{\rm out}}{\dot\varpi_{\rm in}},
$$

which crosses unity from above to below, whereas the frozen record and 2024 PRL use the reciprocal convention and an increasing gamma.

## Gate decision

No single PRL in the claimed window supports the frozen record. The recovered 2024 package was sufficient to audit every displayed formula and number and independently reproduce Supplemental Fig. C.
