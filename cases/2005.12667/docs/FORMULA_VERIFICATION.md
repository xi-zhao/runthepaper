# Formula Verification

机器记录：`outputs/checks/formula_verification.json`。

## Gate Summary

- Formula families: **30**
- Numeric open: **30**
- Numeric closed: **0**
- Main text coverage: Eq. (1)-(164)
- Appendix coverage: A1-A10, B1-B32, C1-C20
- Gate status: **passed**

| Formula family | Physical role | Gate evidence |
| --- | --- | --- |
| EQ001_006 | LC circuit canonical quantization | dimensions, commutator, oscillator spectrum |
| EQ007_019 | continuum line and CPW modes | wave equation, boundary modes, harmonic peaks |
| EQ020_028 | Cooper-pair box to transmon | charge-basis solve, phase transform, charge dispersion |
| EQ029_034 | capacitive coupling to Duffing-JC | source correction, coupling identity, RWA |
| EQ035_039 | exact JC blocks | analytic characteristic polynomial and eigensolver |
| EQ040_044 | dispersive Schrieffer-Wolff | second-order denominators and exact solve |
| EQ045_051 | normal modes and Kerr | matrix spectrum and quartic coefficients |
| EQ052_058 | black-box quantization | zero-point phase and participation identity |
| EQ059_062 | arbitrary multilevel shifts | finite virtual-transition denominators |
| EQ063 | longitudinal coupling | displacement and completed-square spectrum |
| EQ064_075 | thermal bath and input-output | Hermiticity, CPTP dynamics, commutator, passivity |
| EQ076_086 | noise, Purcell and drive | spectral density, susceptibility and limits |
| EQ087_099 | amplification | symplectic commutator and half-quantum noise |
| EQ100_106 | homodyne observables | quadrature normalization and Wigner moments |
| EQ107_120 | dispersive measurement | pointer ODE, dephasing and SNR optimum |
| EQ121_128 | coupling regimes and spectroscopy | vacuum-Rabi splitting, Bloch linewidth and saturation |
| EQ129_153 | control and gates | rotating frame, Gaussian/DRAG dynamics, norms |
| EQ154_157 | bosonic codes | Knill-Laflamme amplitude-damping conditions |
| EQ158_164 | displaced Kerr and squeezing | displacement order, DPA stability, covariance checks |
| APPA-C | circuit, transformation and port appendices | consistency with main-text conventions |

## Source Corrections

| Formula | Detection | Resolution |
| --- | --- | --- |
| arXiv Eq. (29) | decoupled resonator energy is negative | use positive-energy formal Eq. (31) |
| arXiv Eq. (51) | self-Kerr is larger by factor two | use quartic-derived formal Eq. (53) |
| arXiv Eq. (67) | literal real-coupling term is anti-Hermitian | use Hermitian formal Eq. (69) |
| arXiv Eq. (72)/(75) | literal relative signs violate one-port passivity | reconstruct an equivalent port phase convention with $|r|=1$ |

EQ075 remains labelled `reconstructed` for provenance transparency, but its numeric gate is open because the relative phase convention is fixed by the observable passivity invariant. No formula ambiguity remains that blocks an executed target.
