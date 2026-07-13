# Reproducing PRL 121, 086803: a getting-started guide

Paper: Shunyu Yao and Zhong Wang, *Edge States and Topological Invariants of Non-Hermitian Systems*, [Physical Review Letters 121, 086803 (2018)](https://doi.org/10.1103/PhysRevLett.121.086803); [arXiv:1803.01876](https://arxiv.org/abs/1803.01876).

Public reproduction status: **Paper-parameter complete reproduction**

Audit score at export: **94/100**

This note is the English entry point for the public case. It explains the physics first, then connects each paper figure to runnable code, generated data, and machine-readable checks.

Quick links:

- [Case overview](../README.md)
- [中文复现 Note](reproduction-note.zh-CN.md)
- [Run commands](../code/README.md)
- [Numerical methods](../docs/NUMERICAL_METHODS.md)
- [Machine-readable scorecard](../outputs/checks/similarity_scorecard.json)

## 1. What problem does the paper solve?

In a Hermitian SSH chain, a Bloch topological invariant computed with periodic boundary conditions predicts boundary states in an open chain. This assumes that periodic and open systems share the same bulk states.

The non-Hermitian skin effect breaks that assumption. Asymmetric hopping makes many states accumulate near one boundary, so the open-chain bulk is not described by plane waves on the unit circle.

The paper replaces the Bloch factor `exp(ik)` with a complex number `beta`. Its phase describes oscillation and its modulus describes exponential growth or decay. The allowed open-boundary bulk values form the generalized Brillouin zone, usually written as `C_beta`.

The central claim is therefore operational: compute topology along `C_beta`, not along the ordinary Bloch unit circle, and the bulk-boundary correspondence is restored.

## 2. Core formulas

For `t3 = 0`, the off-diagonal Bloch Hamiltonian is

```text
H(k) = [[0, t1 + gamma/2 + t2 exp(-ik)],
        [t1 - gamma/2 + t2 exp(+ik), 0]].
```

The open-boundary transition is

```text
t1 = +/- sqrt(t2^2 + (gamma/2)^2).
```

With the ansatz `psi_n = beta^n psi`, the long-chain bulk condition gives

```text
|beta| = sqrt(|(t1 - gamma/2) / (t1 + gamma/2)|).
```

The non-Bloch winding is evaluated along this generalized Brillouin zone. The implementation uses the branch-stable off-diagonal form

```text
W = (wind[a(beta)] - wind[b(beta)]) / 2.
```

When `t3` is nonzero, both off-diagonal elements contain `beta` and `beta^-1`. The energy equation becomes quartic in `beta`, and the generalized Brillouin zone is reconstructed from the middle-root condition `|beta_2| = |beta_3|`.

The detailed derivation trace is available in [DERIVATION_TRACE.md](../docs/DERIVATION_TRACE.md), and the public formula gate is summarized in [FORMULA_VERIFICATION.md](../docs/FORMULA_VERIFICATION.md).

## 3. What was reproduced?

| Paper item | Independent result | Public figure | Public check |
| --- | --- | --- | --- |
| Fig. 2 | Open-boundary spectrum and zero-mode interval | [PNG](../outputs/figures/fig2_open_spectrum.png) | [JSON](../outputs/checks/fig2_open_spectrum.json) |
| Fig. 3 | Beta roots, generalized Brillouin zone, and skin profiles | [PNG](../outputs/figures/fig3_beta_skin.png) | [JSON](../outputs/checks/fig3_beta_skin.json) |
| Fig. 4 | Integer non-Bloch winding plateau | [PNG](../outputs/figures/fig4_winding.png) | [JSON](../outputs/checks/fig4_winding.json) |
| Fig. 5 | Nonzero-`t3` spectrum, winding, and noncircular GBZ | [PNG](../outputs/figures/fig5_t3.png) | [JSON](../outputs/checks/fig5_t3.json) |

### Fig. 2: open-boundary spectrum

For `t2 = 1` and `gamma = 4/3`, the reproduced open-boundary transition is

```text
|t1| = 1.201850425...
```

The zero-mode interval and the overall `|E|`, `Re(E)`, and `Im(E)` structures agree with the paper-level target. The solver uses the chiral block structure rather than relying on an unstable direct dense eigenspectrum near strongly non-normal parameter values.

### Fig. 3: generalized Brillouin zone and skin effect

At `t1 = 1`, the reproduced generalized Brillouin-zone radius is

```text
|beta| = sqrt(1/5) = 0.4472135955...
```

The equal-modulus beta-root condition and the left-localized open-chain profiles are produced from the same model parameters. This connects the complex-plane generalized Brillouin zone directly to the real-space skin effect.

### Fig. 4: non-Bloch winding

The reproduced invariant is an integer step: `W = 1` inside the open-boundary topological interval and `W = 0` outside. The public plot keeps the step structure instead of smoothing a discrete topological quantity.

### Fig. 5: nonzero `t3`

This is the most numerically delicate target. The final public run uses the paper parameters `L = 100`, `t2 = 1`, `gamma = 4/3`, and `t3 = 0.2`.

The `L = 100` open-chain spectrum is evaluated at 35 decimal digits because ordinary double precision produces visible pseudospectral drift for this non-normal matrix. The reproduced transitions are near `t1 = +/-1.562`, consistent with the paper caption value `+/-1.56`, and the reconstructed generalized Brillouin zone is noncircular.

## 4. How to run the public case

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install mpmath
cd cases/1803.01876/code
python scripts/run_fig2_open_spectrum.py
python scripts/run_fig3_beta_skin.py
python scripts/run_fig4_winding.py
python scripts/run_fig5_t3.py
```

The scripts write generated artifacts to:

- [outputs/data](../outputs/data/) for CSV data;
- [outputs/figures](../outputs/figures/) for generated plots;
- [outputs/checks](../outputs/checks/) for JSON validation records.

See [code/README.md](../code/README.md) for the maintained command list.

## 5. What does 94/100 mean?

The score summarizes the evidence available at export time. It is not a statement that “94% of the physics is correct,” and it is not a cross-paper ranking.

This case has:

- verified formula-to-code dependencies;
- independently generated numerical data and figures;
- paper-parameter final runs for the scored targets;
- feature-level and numerical acceptance checks;
- internal digitized-figure comparisons used for audit.

The remaining gap is author-data-level equivalence. The authors' original plotting data are not public, so the case can establish agreement in physical structure, key numerical values, and digitized-figure tolerances, but it cannot claim point-for-point identity with the authors' plotting arrays.

## 6. Public boundary

The repository publishes the reproduction notes, paper-derived numerical code, generated CSV data, generated figures, and public checks.

It does not redistribute the publisher PDF, arXiv source archive, original figures, EPS paths, digitized source curves, or source-versus-generated comparison panels. Those materials are either linked at their official source or retained only as non-redistributed internal validation evidence.

That distinction is intentional: the public case should be runnable and inspectable without becoming a mirror of copyrighted paper assets.
