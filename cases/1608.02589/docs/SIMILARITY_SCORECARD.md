# 相似度评分卡：1608.02589

## 总分

- Overall score: `73.56/100`
- Similarity level: `numerical_feature_reproduction`
- 解释：离散时间晶体的核心数值特征已经出现；主要短板是 Fig. 3b-d 的 scaling collapse 和 critical exponents 还没有达到原论文的大规模统计精度。

## 单图评分

| 数值图/表/面板 | Weight | 数值特征吻合度 | 关键数值接近度 | 原文目标覆盖度 | Score |
| --- | ---: | --- | --- | --- | ---: |
| Fig. 1 subharmonic rigidity | 1.0 | 50/50 - 相互作用系统半频峰锁定，自由自旋峰随 pulse error 漂移，核心现象清楚出现。 | 28/35 - 峰位置锁定误差为 0，但没有原文 disorder-averaged 曲线逐点比较。 | 9/15 - Fig. 1 主要目标已覆盖，统计规模仍不是完整论文级。 | 87 |
| Fig. 2 level statistics / variance peak | 1.0 | 43/50 - level statistics 和 variance peak 的转变信号出现。 | 18/35 - 趋势可见，但小规模样本噪声较大。 | 9/15 - 覆盖了本地图，但没有达到原文大样本 campaign。 | 70 |
| Fig. 3 endpoint mutual information / scaling | 1.5 | 40/50 - endpoint mutual information 在 epsilon=0 精确命中 log 2，大 detuning 下降。 | 24/35 - `L=8,10,12` medium campaign 中 Fig. 3c/d 塌缩较紧，Fig. 3b 和临界指数仍未收敛。 | 13/15 - Fig. 3a、3c、3d 已覆盖，3b 为 partial；缺少 `L=14–18` 和最终统计。 | 70 |
| Fig. 4 long-range diagnostic | 1.0 | 42/50 - 长程相互作用版本也出现方差峰。 | 18/35 - 趋势出现，但数值稳定性和统计精度还不够。 | 9/15 - 本地复现覆盖核心诊断，没有完成大规模 disorder 平均。 | 69 |

## 结论

离散时间晶体的核心数值特征已经出现；主要短板是 Fig. 3b-d 的 scaling collapse 和 critical exponents 还没有达到原论文的大规模统计精度。

这张评分卡的目标是让读者看到每一张数值图为什么得分，而不是只看到一个总分。

## 论文评测字段

| 数值图/表/面板 | Critical | Role | Artifact pass | Data-backed | Manual interventions | Failure type |
| --- | --- | --- | --- | --- | ---: | --- |
| Fig. 1 subharmonic rigidity | true | main_claim | true | true | 0 | missing_reference_curve |
| Fig. 2 level statistics / variance peak | true | supporting | true | true | 0 | insufficient_compute |
| Fig. 3 endpoint mutual information / scaling | true | main_claim | true | true | 0 | insufficient_compute |
| Fig. 4 long-range diagnostic | false | supporting | true | true | 0 | insufficient_compute |
