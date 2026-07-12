# Similarity Scorecard: 2605.25398

## 总分

- Overall score: `79.36/100`
- Similarity level: `numerical_feature_reproduction`
- 解释：这篇论文的核心数值特征已经复现。chaotic dynamics 在 `t*=1.79` 附近接近 Porter-Thomas 分布，Shannon entropy 和 participation ratio 明显高于 integrable dynamics；OTOC 的短时幂律和频域 delocalization 也对上了。还不能说完整复现，因为没有作者原始实验数据、随机种子和逐点曲线真值。

## 单图评分

| 数值图/表/面板 | Weight | 数值特征吻合度 | 关键数值接近度 | 原文目标覆盖度 | Score |
| --- | ---: | --- | --- | --- | ---: |
| Fig. 2g-h theoretical output distributions | 0.6 | 25/50 - 只保留 chaotic 比 integrable 更分散这一弱特征。 | 10/35 - 没有复现原图正负柱、实验红柱和作者随机实例。 | 7/15 - 只覆盖 g-h 的局部理论分布，不覆盖整张 Fig.2。 | 42 |
| Fig. 3 PT distance, Shannon entropy, and SFF | 1.5 | 49/50 - chaotic PT 距离在 `t*=1.79` 附近下探，entropy 同时升高。 | 30/35 - PT 最小点 `1.788`，entropy/SFF 特征点约 `1.841`，与论文 `1.79` 非常接近。 | 12/15 - 主理论曲线覆盖；缺少实验红点和作者曲线。 | 89 |
| Fig. 4 OTOC-equivalent observables and PR | 1.3 | 48/50 - chaotic 更快、更广地 spread，PR 明显更高。 | 29/35 - `t=1.79` 时 chaotic PR `12.51`，integrable PR `1.05`。 | 11/15 - 理论 OTOC/PR 覆盖；没有实验测量点。 | 80 |
| Fig. S1 conditional probability proof | 0.6 | 50/50 - `D=28` 的 post-selected 分布贴近 PT。 | 32/35 - 只剩 Monte Carlo histogram 噪声。 | 13/15 - 覆盖论文的 `N0=36, D=28` 场景。 | 90 |
| Fig. S4 scaling behavior | 0.8 | 42/50 - 模数增大时 finite-size effect 变弱，趋势出现。 | 22/35 - 趋势一致，但缺少作者 sample count 和原始曲线。 | 9/15 - 本地覆盖 `M=4` 到 `M=14`，不是作者数据级复现。 | 70 |
| Fig. S5 ideal OTOCs for all configurations | 0.8 | 46/50 - 所有 collision-free 输出构型显示 overlap-sector 结构。 | 27/35 - sector hierarchy 和 saturation 行为一致；缺作者曲线。 | 11/15 - 覆盖全部非初态输出构型。 | 80 |
| Fig. S6 short-time OTOC and FFT PR | 0.8 | 49/50 - `t^2/t^4` 幂律和 chaotic 频域 delocalization 都出现。 | 31/35 - slope 为 `1.999` 和 `3.999`；FFT PR 为 chaotic `146.13` vs integrable `9.07`。 | 12/15 - 数据和检查完整；缺作者随机种子级重合。 | 89 |

## 结论

这个 case 仍然达到“数值特征复现”，但 T001 不能再被表述成视觉相似复现。它只能说明 Agent 从论文公式出发实现了两光子概率对象，并观察到 chaotic 分布更分散这一局部特征；真正支撑高可信度的是后续 Fig. 3、Fig. 4 和附录 OTOC/PR 检查。

它还没有达到“完整复现”。主要原因不是公式或程序失败，而是论文没有公开逐点实验数据、作者随机矩阵样本和可直接 overlay 的原始曲线。

## 论文评测字段

| 数值图/表/面板 | Critical | Role | Parameter match | Artifact pass | Data-backed | Failure type |
| --- | --- | --- | --- | --- | --- | --- |
| Fig. 2g-h theoretical output distributions | false | method_validation | paper_subset | true | true | missing_reference_curve |
| Fig. 3 PT distance, Shannon entropy, and SFF | true | main_claim | paper_subset | true | true | missing_reference_curve |
| Fig. 4 OTOC-equivalent observables and PR | true | main_claim | paper_subset | true | true | missing_reference_curve |
| Fig. S1 conditional probability proof | false | sanity_check | paper_exact | true | true | none |
| Fig. S4 scaling behavior | false | supporting | reduced_scale | true | true | partial_target_coverage |
| Fig. S5 ideal OTOCs for all configurations | false | supporting | paper_subset | true | true | missing_reference_curve |
| Fig. S6 short-time OTOC and FFT PR | false | supporting | paper_subset | true | true | missing_reference_curve |

## What Prevents A Higher Score

- No raw experimental photon-count data are included in the arXiv source.
- No author random seeds or ensemble files are available.
- No digitized original curves are used for pointwise overlay.
- Fig. S4 is a local feature-level scaling run, not an author-data reproduction.

Machine-readable record:

```text
outputs/checks/similarity_scorecard.json
```
