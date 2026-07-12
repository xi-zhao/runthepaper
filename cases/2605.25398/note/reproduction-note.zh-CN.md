# Case Intro: Boson Sampling as a Probe of Quantum Chaos

## One-Sentence Result

这个案例跟随 arXiv:2605.25398，复现了论文中最核心的数值结论：用两光子 boson sampling 的输出概率，可以清楚地区分 chaotic random-matrix dynamics 和 integrable dynamics。

## Similarity Level

- Current level: `numerical_feature_reproduction`
- Similarity score: `79.36/100`
- Meaning: 主要物理特征已经复现，但还不是作者实验数据和随机种子级别的完整复现。
- Important note: 我们看重的是数值特征是否对上，不把颜色、线宽、排版差异当成科学误差。

## Paper And Goal

- Paper: "Boson Sampling as a Probe of Chaotic and Integrable Quantum Dynamics"
- PaperID: `2605.25398`
- Case type: 理论/数值物理论文复现，带实验背景
- Reproduction scope: 随机矩阵 Hamiltonian、两光子 boson sampling、PT 距离、Shannon entropy、SFF、OTOC-equivalent observables、participation ratio
- Out of scope: 光子芯片硬件图、实验装置图、原始 photon-count 实验数据

## Intuitive Derivation

论文的想法可以用一句话说清楚：先让一个量子系统按 `U(t)=exp(-iHt)` 演化，再把这个 `U(t)` 放进一个 boson sampling 装置里，看两光子输出概率的统计形状。

如果 `H` 是 chaotic 的，`U(t)` 在某个中间时间会接近 Haar-random。这个时候输出概率会接近 Porter-Thomas 分布，Shannon entropy 会变大，概率也会 spread 到更多输出构型上。

如果 `H` 是 integrable 的，输出概率会更局域。它不会在同一个时间点表现出同样强的 Porter-Thomas、entropy 和 PR 特征。

本 case 先把这条公式链写成代码，再做数值检查。核心计算对象是两光子 collision-free 输出概率：

```text
p(r,s) = |U[r,i] U[s,j] + U[r,j] U[s,i]|^2
```

然后把它归一化成条件概率分布，用来生成所有数值图。

## Numerical Method

本地复现使用论文的随机矩阵模型：

```text
H = (H0 + lambda V) / sqrt(1 + lambda^2)
Lambda = lambda^2 d / (2 pi)
```

其中：

- `Lambda=0.01` 代表 integrable / Poisson-like dynamics；
- `Lambda=1000` 代表 chaotic / GOE-like dynamics；
- `M=8` modes，`N=2` photons；
- collision-free output 数量是 `D=C(8,2)=28`；
- 论文重点时间是 `[1, 1.79, 29.29, 100, 1000]`。

生成顺序是：

1. 采样 Hamiltonian。
2. 对角化并生成 `U(t)`。
3. 计算两光子输出概率。
4. 生成 CSV 数据。
5. 计算 PT 距离、entropy、SFF、OTOC、PR。
6. 画复现图。
7. 用数值特征检查决定是否验收。

## Original vs Reproduced

### T001: Fig. 2g-h Output Probability Distributions

![Generated](../outputs/figures/fig2_output_distribution_reproduction.png)

**Consistency:** `scope_limited_partial`

**Similarity level:** `partial_feature_check`

**Similarity score:** `42/100`

Explanation:

- Feature being checked: chaotic 输出概率比 integrable 更分散。
- What matches: 只能说 chaotic 分布比 integrable 更分散这一弱特征出现。
- What remains different: 原图 g-h 是理论蓝柱和实验红柱的正负柱对比，并且使用作者随机实例；我们的图是本地理论概率柱状图，没有实验红柱，也没有复现原图的视觉形态。原先把这一项打到 `76/100` 偏高，现降为 `42/100`。
- Evidence: `../outputs/data/sparse_*_output_distributions.csv`

### T002: Fig. 3 PT Distance, Shannon Entropy, SFF

![Generated](../outputs/figures/fig3_main_probes_reproduction.png)

**Consistency:** `reproduced_at_feature_level`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `89/100`

Explanation:

- Feature being checked: chaotic 曲线在 `t*=1.79` 附近出现 PT 距离下探、entropy 上升、SFF 下探。
- What matches: PT 最小点 `t=1.788`，entropy 最大点约 `t=1.841`，SFF proxy 最小点约 `t=1.841`，与论文 `t*=1.79` 对齐。
- What remains different: 没有作者逐点曲线和实验红点，所以不做 pixel-level 或 pointwise overlay。
- Evidence: `../outputs/checks/reproduction_feature_checks.json`

### T003: Fig. 4 OTOC-Equivalent Observables And PR

![Generated](../outputs/figures/fig4_otoc_pr_reproduction.png)

**Consistency:** `reproduced_at_feature_level`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `80/100`

Explanation:

- Feature being checked: chaotic dynamics 在 Hilbert space 中更强 delocalization。
- What matches: `t=1.79` 时 chaotic PR 为 `12.51`，integrable PR 为 `1.05`；chaotic OTOC 更早 spread。
- What remains different: 原文实验点需要 chip data；本 case 复现理论/ideal 数值对象。
- Evidence: `../outputs/data/ideal_*_metrics.csv`

### T004: Fig. S1 Conditional Probability Proof

![Generated](../outputs/figures/figS1_conditional_probability_reproduction.png)

**Consistency:** `reproduced`

**Similarity level:** `complete_reproduction`

**Similarity score:** `90/100`

Explanation:

- Feature being checked: `N0=36, D=28` 时，collision-free post-selection 后的概率分布仍接近 PT 分布。
- What matches: `D=28` 的 conditional probability 曲线贴近 PT reference。
- What remains different: 只剩 histogram 采样噪声。
- Evidence: `../outputs/data/appendix_conditional_probability_demo.csv`

### T005: Fig. S4 Scaling Behavior

![Generated](../outputs/figures/figS4_scaling_reproduction.png)

**Consistency:** `partial_feature_match`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `70/100`

Explanation:

- Feature being checked: 系统规模增大后，chaos probe 的有限尺寸偏差减小。
- What matches: scaling 趋势出现，chaotic 的诊断时间聚在预期区域，PT/entropy 指标随规模改善。
- What remains different: 本地运行没有作者原始 sample count 和原始曲线。
- Evidence: `../outputs/data/appendix_scaling_summary.csv`

### T006: Fig. S5 Ideal OTOCs

![Generated](../outputs/figures/figS5_ideal_otocs_reproduction.png)

**Consistency:** `physically_consistent`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `80/100`

Explanation:

- Feature being checked: 所有 collision-free 输出构型按 overlap sector 组织，并且 chaotic 更早 spread。
- What matches: overlap `0` 和 overlap `1` 的 sector structure 出现；chaotic 左移并更快饱和。
- What remains different: 没有作者随机 ensemble 曲线，不能逐点比较。
- Evidence: `../outputs/data/appendix_ideal_otocs_full.csv`

### T007: Fig. S6 Short-Time OTOC And FFT PR

![Generated](../outputs/figures/figS6_extra_otoc_reproduction.png)

**Consistency:** `reproduced`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `89/100`

Explanation:

- Feature being checked: overlap-one 构型短时按 `t^2` 增长，overlap-zero 构型按 `t^4` 增长；chaotic 的频域 PR 更大。
- What matches: fitted slopes 是 `1.999` 和 `3.999`；mean FFT PR 是 chaotic `146.13` vs integrable `9.07`。
- What remains different: 作者随机 seed 不可用。
- Evidence: `../outputs/checks/reproduction_feature_checks.json`

## What Still Differs From The Paper

- 没有原始实验 photon-count 数据，所以不能复现实验红点。
- 没有作者 random-matrix seeds，所以不能要求每条曲线逐点重合。
- Fig. S4 scaling 是本机 feature-level run，不是作者完整曲线重跑。
- 原图排版包含多面板组合，本 case 生成的是更适合检查和展示的独立复现图。

## Recommended Compute For Complete Reproduction

当前 M3 Pro / 18GB 内存已经足够完成本 case 的 feature-level reproduction。

若要推进到更接近完整复现，建议：

- 获取作者原始实验 photon-count 数据和随机矩阵 ensembles；
- 使用 32GB+ 内存机器重跑更大 sample count；
- 对 Fig. S4 使用更密集的 mode grid 和更多 Hamiltonian instances；
- 做原始曲线 digitization 或作者数据 overlay。

## Code Structure

- `src/boson_sampling_chaos.py`: Hamiltonian sampling、two-photon probability、diagnostics、checks。
- `scripts/run_reproduction.py`: 生成 CSV 和 JSON 检查。
- `scripts/plot_reproduction.py`: 从 CSV 生成全部复现图。
- `../outputs/data/`: 所有图背后的数值数据。
- `../outputs/checks/`: 算力、原图渲染、特征检查和相似度评分。

## Final Takeaway

这个 case 展示了 Agent/Harness 的一条完整科研 follow 路径：从论文公式出发，先核验推导，再把公式数值化，最后用数据特征验收图像。它没有复现实验硬件本身，但已经复现了论文最重要的理论数值特征。
