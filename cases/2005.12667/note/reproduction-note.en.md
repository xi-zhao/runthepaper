# Full-formula and numerical reproduction of *Circuit Quantum Electrodynamics*

This case reproduces Blais, Grimsmo, Girvin, and Wallraff, *Circuit Quantum Electrodynamics* (arXiv:2005.12667; RMP 93, 025005). Its goal is not pixel imitation. It connects main-text Eqs. (1)–(164), Appendices A–C, and every numerical result recoverable from public information into an executable and auditable evidence chain.

The final result has 30/30 formula families open, 18/18 independent numerical or tabular targets passing, and 24 development-time unit tests passing. The public audit score is **90.28/100, numerical feature reproduction**. A complete Chinese derivation and numerical report is also available as a [PDF](reproduction-note.zh-CN.pdf).

## Core physical model

The review is organized as one sequence of controlled model reductions:

\[
\text{circuit quantization}
\rightarrow \text{Duffing--Rabi}
\rightarrow \text{Jaynes--Cummings / dispersive models}
\rightarrow \text{multimode and multilevel systems}
\rightarrow \text{Born--Markov / input--output theory}.
\]

Four invariants remain explicit throughout the code and checks: Hamiltonians are Hermitian; closed-system spectra are real; master-equation evolution preserves trace and positivity; and a lossless one-port response satisfies \(|r|=1\). These invariants are also used to adjudicate sign and coefficient differences between the preprint and formal publication.

## Formula coverage

| Section | Equation scope | Numerical evidence |
| --- | --- | --- |
| Sec. II | Eqs. (1)–(28) | CPW modes, transmon wavefunctions, charge dispersion |
| Sec. III | Eqs. (29)–(63) | JC \(2g\sqrt n\) splitting, dispersive ladders, Kerr and multilevel checks |
| Sec. IV | Eqs. (64)–(86) | thermal Lindblad dynamics, Hermiticity, passive input–output response |
| Sec. V | Eqs. (87)–(120) | amplifier quantum limit, pointer states, SNR and cavity pull |
| Sec. VI | Eqs. (121)–(128) | strong coupling, vacuum Rabi splitting, avoided crossing and number splitting |
| Sec. VII | Eqs. (129)–(157) | Gaussian/DRAG control, amplitude-damping codes and cat codes |
| Sec. VIII | Eqs. (158)–(164) | Fock/Wigner and squeezed states |
| Appendices | A1–A10, B1–B32, C1–C20 | closure checks against main-text conventions |

Read the full step-by-step derivation in [DERIVATION_TRACE](../docs/DERIVATION_TRACE.md), the 30 equation cards and code bindings in [DERIVATION](../docs/DERIVATION.md), and the machine-gate summary in [FORMULA_VERIFICATION](../docs/FORMULA_VERIFICATION.md).

## Key numerical findings

- Independent diagonalization of every conserved JC excitation block agrees with the analytic spectrum; the largest \(2g\sqrt n\) splitting error is \(5.8\times10^{-15}\).
- A four-level, 40-dimensional Duffing–JC diagonalization differs from the second-order dispersive expression by at most \(2.96\times10^{-6}\), with minimum bare-state overlap 0.99298.
- From \(E_J/E_C=2\) to 50, transmon charge dispersion is suppressed by a factor \(3.30\times10^{-6}\); the \(n_g\)-periodicity error is \(4.44\times10^{-15}\) GHz.
- Thermal Lindblad integration matches the analytic mean photon number within \(4.98\times10^{-11}\), while trace, Hermiticity, and positivity pass simultaneously.
- The resonant vacuum-Rabi spectrum splits by \(2g\); DRAG improves the median short-gate error by a factor of 3.83.
- First-order binomial-code loss conditions hold at the \(10^{-15}\) scale, and the cat, Fock-superposition, and squeezed-state Wigner functions pass normalization and nonclassicality checks.

Structured data, figures, and machine checks are in [outputs/data](../outputs/data/), [outputs/figures](../outputs/figures/), and [outputs/checks](../outputs/checks/). The scoring contract is documented in [SIMILARITY_SCORECARD](../docs/SIMILARITY_SCORECARD.md).

## Source-version adjudication

| arXiv v1 issue | Formal RMP / invariant | Resolution |
| --- | --- | --- |
| Eq. (29) gives the resonator a negative energy | Formal Eq. (31) restores the positive sign | Use the lower-bounded formal expression |
| Eq. (51) contains an extra \(1/2\) in \(K_a\) | Formal Eq. (53) removes it | Verify the quartic combinatorial factor independently |
| Eq. (67) is non-Hermitian for real coupling | Formal Eq. (69) restores Hermiticity | Use the formal expression and test finite matrices |
| Eqs. (72) and (75), combined literally, violate one-port passivity | The port phase convention is underspecified | Fix an equivalent convention satisfying \(|r|=1\), retaining a reconstructed provenance label |

## Running the case

From the RunThePaper repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2005.12667/code
python scripts/run_reproduction.py
python scripts/run_full_rmp_reproduction.py
```

The first command reruns the selected Sec. III and Sec. IV material, including Eqs. (66)–(68) and (70)–(75). The second reruns all remaining independent full-review numerical targets. Both runners use only public code and parameters, with no dependency on paper-owned images. Discretization, truncation, and acceptance thresholds are described in [NUMERICAL_METHODS](../docs/NUMERICAL_METHODS.md).

## Reproduction boundary

“Full review” means the theoretical content that can be independently reconstructed from public equations and parameters. It does not relabel unavailable experimental data or simulation projects as independent results. Fig. 4(b–e) requires the original COMSOL geometry, materials, and boundary conditions; the experimental panels of Figs. 21, 28, and 32 require author-level data and calibration chains. Their corresponding theory or simulation panels are reproduced, while these external-evidence gaps remain explicitly blocked.
