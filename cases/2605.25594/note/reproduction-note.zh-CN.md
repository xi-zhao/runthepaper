# Case Intro: Sensitivity To Perturbations In The 3D Anderson Model

## One-Sentence Result

这个 case 跟随 arXiv:2605.25594，完成了本地精确对角化基线，并在 A100 上对 `L=24/28/31` 共 605 个无序样本进行了论文尺寸子集复现。结果重现了弱无序敏感性增强、`W_c≈16.5` 附近的谱统计转变、强无序 IPR 增大，以及局域相里 average 和 typical susceptibility 的分离。

## Similarity Level

- Current level: `paper_scale_subset_reproduction`
- Similarity score: `67.49/100`
- Meaning: 已经跑通公式、数值和绘图链条，并覆盖三个论文尺度附近的系统尺寸。A100 子集把 gap-ratio 中点定位在 `W=16.56-16.60`，但没有覆盖论文最大的 `L=32-38` 完整 scaling ladder。
- Important note: 我们验收的是物理特征和数值对象，不把颜色、线宽、排版差异当成科学误差。

## Paper And Goal

- Paper: *Sensitivity to perturbations in the three-dimensional Anderson model*
- PaperID: `2605.25594`
- Case type: 理论/数值凝聚态物理论文复现
- Reproduction scope: Anderson Hamiltonian、fidelity susceptibility、gap ratio、IPR、spectral function、average/typical separation、strong-disorder perturbative trend
- Out of scope: sublattice 示意图；`L=32-38` 全尺寸拟合；`T` 和随机占据算符 `n` 的完整远程 panel

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

运行分为两层：

1. 本地 `L=4,5,6,7` 精确对角化用于公式和流程正确性检查。
2. A100 对 `L=24,28,31` 使用双精度完整对角化，共完成 605 个无序样本。
3. 两层计算都取谱中心 `20%` 的本征态，并以 `T_s` 作为主要扰动算符。
4. 原始数值写入 CSV/JSONL，再由独立聚合检查生成图和 scorecard。
5. `L=32` 的 GPU 求解触发底层 32-bit workspace 失败；`L=38` 超出当前单卡 A100 稠密求解路径的实用内存范围，因此没有用 proxy 冒充完成结果。

## Paper Targets vs Reproduced

下面每张对比图都单独给出“差异原因”。原因用于解释复现边界，不会被包装成已经完成的结果。

### T001: Fig. 1 Fidelity Susceptibility

![Generated](../outputs/figures/fig1_fidelity_vs_disorder_reproduction.png)

![A100 paper-size subset](../outputs/figures/fig1_a100_subset_reproduction.png)

**Consistency:** `numerical_feature_reproduction`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `79/100`

Explanation:

- Feature being checked: fidelity susceptibility should show sensitivity structures as disorder changes.
- What matches: A100 数据在 `L=24/28/31` 上给出从 GOE 到 Poisson 的完整转变，gap-ratio 中点为 `16.588/16.599/16.564`；fidelity peak 随尺寸向 `W_c=16.5` 移动并变尖。
- Difference reason / 差异原因: 图中本地曲线仍是 `L<=7` 的可重跑基线；完整论文拟合还缺 `L=32-38`。原因是当前单卡 A100 的双精度稠密对角化在 `L=32` 触发 workspace 限制，`L=38` 的矩阵和求解工作区超出实用显存，而不是公式或物理模型不一致。
- Evidence: `../outputs/data/remote_campaign_summary.csv`, `../outputs/checks/remote_campaign_summary.json`

### T002: Fig. 2 Weak-Disorder Crossover

![Generated](../outputs/figures/fig2_weak_crossover_scaling_reproduction.png)

**Consistency:** `numerical_feature_reproduction`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `62/100`

Explanation:

- Feature being checked: weak-disorder sensitivity should be tied to finite-size scale.
- What matches: 本地数据重现低无序增强；远程 `L=24/28/31` spectral campaign 的 `W_1^*sqrt(V)` 落在论文给出的 crossover band 内。
- Difference reason / 差异原因: `L=31` 的弱无序峰受到当前最小 `W` 网格边界影响，且没有 `L=38` 端点，因此不能重新声明论文的渐近系数 `41`。
- Evidence: `../outputs/figures/fig2_weak_crossover_scaling_reproduction.png`, `../outputs/data/remote/results_weakW.jsonl`

### T003: Fig. 3 Spectral-Function Mechanism

![Generated from A100 subset](../outputs/figures/fig3_spectral_remote_reproduction.png)

**Consistency:** `numerical_feature_reproduction`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `65/100`

Explanation:

- Feature being checked: the spectral function `|f(omega)|^2` is the mechanism behind the susceptibility peaks.
- What matches: A100 子集按论文协议重现了 Lorentzian spectral function；临界点幂指数约为 `a=0.48`，接近论文 `L=38` 的 `0.52`。
- Difference reason / 差异原因: 指数差异主要来自最大尺寸停在 `L=31`，没有论文的 `L=38` 低频窗口；弱无序 Lorentzian 宽度也仍有明显有限尺寸效应。
- Evidence: `../outputs/data/remote/results_spectral.jsonl`, `../outputs/figures/fig3_spectral_remote_reproduction.png`

### T004: Fig. 8-11 Localized-Regime Behavior

![Generated](../outputs/figures/fig8_typical_average_reproduction.png)

**Consistency:** `numerical_feature_reproduction`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `72/100`

Explanation:

- Feature being checked: in the localized regime, typical and average fidelity susceptibility separate.
- What matches: `chi_av^r / chi_typ^r` 和 IPR 都在局域区增长；A100 数据给出 `W_3^*` bracket 从 `L=24` 的约 `22.0` 漂移到 `L=28` 的约 `23.6`，方向与论文一致。
- Difference reason / 差异原因: 当前 `W` 网格步长较粗且缺 `L=32-38`，所以不能把论文的 `W_3^*` 数值重新拟合到相同精度。
- Evidence: `../outputs/data/fig9_chi_typ_curves.csv`, `../outputs/checks/remote_campaign_summary.json`

### T005: Fig. 10 Perturbative Strong-Disorder Trend

![Generated](../outputs/figures/fig10_perturbation_reproduction.png)

**Consistency:** `numerical_feature_reproduction`

Explanation:

- Feature being checked: deep in the localized regime, perturbation theory predicts a strong-disorder decay trend.
- What matches: the numerical and perturbative curves move toward the same trend at large `W`.
- Difference reason / 差异原因: 这张图仍以小尺寸数值和解析微扰趋势做机制核验；完整 panel 需要未完成的大尺寸算符数据，因此不声明逐点一致。
- Evidence: `../outputs/data/perturbation_theory_summary.csv`

## What Still Differs From The Paper

- `L=24/28/31` 已完成，但论文最大的 `L=32-38` scaling ladder 未完成。
- `W_2^*=16.5` 已由三个尺寸的 gap-ratio crossing 数值支持；最大尺寸 fidelity scaling 仍缺。
- spectral-function 指数得到 `a≈0.48`，尚未达到论文 `L=38` 的 `a≈0.52`。
- `W_3^*` 的有限尺寸漂移方向已重现，但没有用粗网格强行报告论文精度。
- 算符 `T` 和 `n` 尚未完成远程全 panel。

## Stop Decision And Compute Boundary

我们已经评估过继续扩算，而不是把“没跑”笼统归因于困难：

- 已完成：单卡 A100 上的 `L=24/28/31`，605 个无序样本。
- 实测停止点：`L=32` 的双精度 GPU 求解触发底层 workspace 限制；CPU 回退约为每样本小时级。
- 内存判断：`L=38` 的 Hamiltonian 和 eigenvector 两个双精度稠密矩阵本身合计约 48 GB，尚未计入 eigensolver workspace，当前单卡路径不具备完成条件。
- 结论：`L=32-38` 标记为 `compute_limited_current_resource`，本轮停止，不用 proxy 数据替代。
- 若未来有 256 GB+ 内存节点、分布式 eigensolver 或多卡大显存资源，再重新打开该目标。

Machine-readable plan: `config/paper_scale_run_plan.json`.

## Code Structure

- `src/anderson_sensitivity.py`: Anderson Hamiltonian, observables, susceptibility, checks.
- `scripts/run_reproduction.py`: generates CSV and JSON checks.
- `scripts/plot_reproduction.py`: generates the five local reproduction figures.
- `../outputs/data/`: all numerical data behind plots.
- `../outputs/checks/`: formula gate, feature checks, scorecard, performance profile.
- `../outputs/figures/`: generated figures.

## Final Takeaway

这个 case 已经超过本地 feature demo：A100 论文尺寸子集支持了主要物理结论，但完整 `L=32-38` scaling ladder 受当前资源限制。公开结论因此是“论文尺寸子集复现”，而不是完整论文级复现；每张图的剩余差异都明确标注了原因。
