# 相似度评分卡：10.1145-3297858.3304023

## 总分

- Overall score: `68.29/100`
- Similarity level: `numerical_feature_reproduction`
- 解释：SABRE 的核心算法和 Table II 26 行全语料流程已经复现；逐行最优值仍受作者未公开运行元数据限制。

## 单图/单表评分

| 数值图/表/面板 | Weight | 数值特征吻合度 | 关键数值接近度 | 原文目标覆盖度 | Score |
| --- | ---: | --- | --- | --- | ---: |
| Fig. 3 swap example | 1.0 | 50/50 - 论文小例子的 SWAP 决策和路由结构完全复现。 | 35/35 - CNOT 数、SWAP 数和深度都和论文例子一致。 | 13/15 - 这个解释性目标完整复现，但它不是全 benchmark corpus。 | 98 |
| Reverse traversal feature | 1.0 | 45/50 - 反向遍历改善初始映射的机制出现。 | 22/35 - 门数和深度趋势吻合，但不是论文全表的逐行数值。 | 8/15 - 该目标覆盖代表性 QFT benchmark；完整 Table II 由独立的 T004 全语料目标验收。 | 55 |
| Decay trade-off | 1.0 | 44/50 - decay 带来的门数/深度 trade-off 出现。 | 20/35 - 趋势吻合，但缺作者实现细节导致逐行数值无法确认。 | 7/15 - 本地 sweep 能展示机制，但不是原文完整实验设置。 | 55 |
| Table II benchmark corpus | 4.0 | 40/50 - 26/26 输入门数匹配，26/26 输出满足硬件约束，全语料流程跑通。 | 20/35 - 按论文 best-of-5 协议，20/26 行精确或落在种子分布区间，其余 6 行均为本实现结果更优。 | 7.5/15 - 26 行全部覆盖，但逐行相等需要未公开的 seed、tie-breaking 和 BKA 输入。 | 67.5 |

## 结论

SABRE 的核心算法和 Table II 26 行全语料流程已经复现；逐行最优值仍受作者未公开运行元数据限制。

这张评分卡的目标是让读者看到每一张数值图或表为什么得分，而不是只看到一个总分。

## 论文评测字段

| 数值图/表/面板 | Critical | Role | Parameter match | Artifact pass | Data-backed | Failure type |
| --- | --- | --- | --- | --- | --- | --- |
| Fig. 3 swap example | false | sanity_check | paper_exact | true | true | none |
| Reverse traversal feature | true | method_validation | proxy_model | true | true | partial_target_coverage |
| Decay trade-off | false | supporting | proxy_model | true | true | partial_target_coverage |
| Table II benchmark corpus | true | main_claim | paper_subset | true | true | missing_benchmark_metadata |

说明：Table II 已经使用原文 26 个 benchmark 行和表格参数重跑；这里仍标为 `paper_subset`，是因为两个 benchmark 的 QASM qubit 元数据与论文表格不一致，并且作者的 seed/tie-breaking/BKA 细节没有公开。这个字段不是说我们只跑了 toy case，而是说严格完整复现所需的元信息仍不完整。
