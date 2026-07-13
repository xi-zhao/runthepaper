# Case Intro: Sensitivity To Perturbations In The 3D Anderson Model

## One-Sentence Result

这个 case 跟随 arXiv:2605.25594，复现了三维 Anderson 模型里 fidelity susceptibility 的本地特征版本：弱无序区的敏感性增强、从 chaos window 到局域化的谱统计变化、强无序下 IPR 增大，以及局域相里 average 和 typical susceptibility 的分离。

## Similarity Level

- Current level: `numerical_feature_reproduction`
- Similarity score: `67.49/100`
- Meaning: 已经跑通公式到数值再到图的链条，也看到了几个关键物理特征；但原文主图依赖 `L=20-38` 和多样本平均，本地 `L<=7` 还不能达到完整复现。
- Important note: 我们验收的是物理特征和数值对象，不把颜色、线宽、排版差异当成科学误差。

## Paper And Goal

- Paper: *Sensitivity to perturbations in the three-dimensional Anderson model*
- PaperID: `2605.25594`
- Case type: 理论/数值凝聚态物理论文复现
- Reproduction scope: Anderson Hamiltonian、fidelity susceptibility、gap ratio、IPR、spectral function、average/typical separation、strong-disorder perturbative trend
- Out of scope: sublattice 示意图；没有在本机跑论文级 `L=38` 全尺寸拟合

## Intuitive Derivation

论文的主线很清楚：给 Hamiltonian 加一个很小的扰动 `lambda O`，然后看本征态会变得多快。

如果两个能级很近，或者扰动矩阵元很大，那么本征态对扰动就非常敏感。这个敏感性写成：

```text
chi_n = sum_{m != n} |<n|O|m>|^2 / (E_n - E_m)^2
```

为了避免极小能级间隔把平均值完全支配，论文引入了 cutoff：

```text
chi_n^r = sum_m omega_nm^2 / (omega_nm^2 + mu^2)^2 * |O_nm|^2
```

然后比较两种统计量：

```text
chi_av^r  = average over states
chi_typ^r = geometric average over states
```

在 extended/chaotic 区域，average 和 typical 比较接近；进入局域相后，少数 resonance 会把 average 拉高，typical 则更能代表多数本征态。

## Numerical Method

本地代码构造开边界三维 Anderson 模型：

```text
H_A = - sum_<i,j> c_i^\dag c_j + sum_i epsilon_i c_i^\dag c_i
epsilon_i in [-W/2, W/2]
```

运行方式：

1. 对 `L=4,5,6,7` 做精确对角化。
2. 取谱中心 `20%` 的本征态。
3. 用 `T_s` 作为扰动算符计算 fidelity susceptibility。
4. 先输出 CSV，再画图。
5. 用 JSON 检查记录哪些物理特征出现了，哪些还没到论文级精度。

## Original vs Reproduced

### T001: Fig. 1 Fidelity Susceptibility

![Generated](../outputs/figures/fig1_fidelity_vs_disorder_reproduction.png)

**Consistency:** `partial_feature_match`

**Similarity level:** `feature_not_reproduced` for the full paper-level Fig. 1 claim

**Similarity score:** `59/100`

Explanation:

- Feature being checked: fidelity susceptibility should show sensitivity structures as disorder changes.
- What matches: local data shows weak-disorder enhancement, a moderate-disorder chaos window, and strong-disorder localization through gap ratio/IPR.
- What remains different: the two clean paper peaks, especially the Anderson-transition fidelity peak near `W=16.5`, are not quantitatively resolved at `L<=7`.
- Evidence: `../outputs/data/fidelity_vs_disorder_summary.csv`, `../outputs/checks/anderson_feature_checks.json`

### T002: Fig. 2 Weak-Disorder Crossover

![Generated](../outputs/figures/fig2_weak_crossover_scaling_reproduction.png)

**Consistency:** `numerical_feature_reproduction`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `61/100`

Explanation:

- Feature being checked: weak-disorder sensitivity should be tied to finite-size scale.
- What matches: the largest local system has a clear low-W enhancement; the code extracts peak positions and compares them with the paper's `41/sqrt(V)` law.
- What remains different: strict monotonic finite-size scaling is not stable for `L<=7`; the paper fit uses much larger `V>=18^3`.
- Evidence: `../outputs/figures/fig2_weak_crossover_scaling_reproduction.png`

### T003: Fig. 3 Spectral-Function Mechanism

![Generated](../outputs/figures/fig3_spectral_function_reproduction.png)

**Consistency:** `proxy_only`

**Similarity level:** `feature_not_reproduced`

**Similarity score:** `55/100`

Explanation:

- Feature being checked: the spectral function `|f(omega)|^2` is the mechanism behind the susceptibility peaks.
- What matches: the same binned spectral-function object is implemented and plotted.
- What remains different: the fitted Lorentzian width and exponent `a≈0.52` need `L=28-38` and many realizations. The local result is too small and noisy for that claim.
- Evidence: `../outputs/data/spectral_function_summary.csv`

### T004: Fig. 8-11 Localized-Regime Behavior

![Generated](../outputs/figures/fig8_typical_average_reproduction.png)

**Consistency:** `numerical_feature_reproduction`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `66/100`

Explanation:

- Feature being checked: in the localized regime, typical and average fidelity susceptibility separate.
- What matches: `chi_av^r / chi_typ^r` grows at large `W`; IPR also grows strongly, showing real-space localization.
- What remains different: `W_3^*≈27.92` is not extracted quantitatively because that needs large `L` and dense `mu` grids.
- Evidence: `../outputs/data/mu_sweep_summary.csv`

### T005: Fig. 10 Perturbative Strong-Disorder Trend

![Generated](../outputs/figures/fig10_perturbation_reproduction.png)

**Consistency:** `numerical_feature_reproduction`

Explanation:

- Feature being checked: deep in the localized regime, perturbation theory predicts a strong-disorder decay trend.
- What matches: the numerical and perturbative curves move toward the same trend at large `W`.
- What remains different: small `L` gives noisy unregularized values, so this is a mechanism check rather than a full Fig. 10 reproduction.
- Evidence: `../outputs/data/perturbation_theory_summary.csv`

## What Still Differs From The Paper

- The paper's clean `W_1^* ~ 41/sqrt(V)` fit is not recovered at `L<=7`.
- The Anderson-transition fidelity peak near `W_2^*=16.5` is not sharply resolved in the local susceptibility curve.
- Spectral-function exponent `a≈0.52` is not fitted reliably.
- `W_3^*≈27.92` is not quantitatively extracted.
- Operators `T` and `n` are not fully rerun in this local version.

## Recommended Compute For Complete Reproduction

To move from feature-level to complete reproduction:

- Use `L=18,20,24,28,32,38`.
- Use 20 disorder realizations for `L<=28`, 5 for `L>28`, and 40 for gap-ratio appendices.
- Use sparse shift-invert or block eigensolvers around the spectrum center.
- Recommended machine: 32+ CPU cores, 128GB+ RAM for `L<=28`, and 256GB+ or cluster queue for `L=38`.
- Expected runtime: multi-day batch workflow for the full figure set.

Machine-readable plan: `config/paper_scale_run_plan.json`.

## Code Structure

- `src/anderson_sensitivity.py`: Anderson Hamiltonian, observables, susceptibility, checks.
- `scripts/run_reproduction.py`: generates CSV and JSON checks.
- `scripts/plot_reproduction.py`: generates the five local reproduction figures.
- `../outputs/data/`: all numerical data behind plots.
- `../outputs/checks/`: formula gate, feature checks, scorecard, performance profile.
- `../outputs/figures/`: generated figures.

## Final Takeaway

这个 case 说明 Agent 已经能把一篇新的理论物理论文转成公式、代码、数据和图，并能诚实地区分“本地特征复现”和“完整论文级复现”。这篇文章最有价值的结果需要大规模数值计算；当前版本把公式链和本地物理特征跑通了，也给出了下一轮完整复现的具体算力和参数方案。
