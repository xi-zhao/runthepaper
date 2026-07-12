# 相似度评分卡：1711.03528

## 总分

- Overall score: `72.50/100`
- Similarity level: `numerical_feature_reproduction`
- 解释：量子多体 scar 的核心数值特征已经出现；主要差距是论文的 `L=32` 对称性 sector 和 iTEBD 热力学极限没有在本地重跑。

## 单图评分

| 数值图/表/面板 | Weight | 数值特征吻合度 | 关键数值接近度 | 原文目标覆盖度 | Score |
| --- | ---: | --- | --- | --- | ---: |
| Fig. 1 Hamiltonian graph | 0.5 | 50/50 - `L=6` Fibonacci basis 和 PXP 连接结构复现。 | 32/35 - 节点数和边规则一致，布局不要求完全相同。 | 9/15 - 覆盖模型结构图，不是主数值结论。 | 90 |
| Entanglement dynamics | 1.2 | 46/50 - `Z2` 慢纠缠增长、局域振荡、revival 都出现。 | 26/35 - 振荡周期 `2.375` 接近论文 `~2.35`。 | 7/15 - 本地 finite-size ED，不是 iTEBD thermodynamic limit。 | 70 |
| Fig. 2 scar tower / FSA | 1.5 | 43/50 - 高 `Z2` overlap tower、FSA ground profile 和 PR2 enhancement 出现。 | 24/35 - ground FSA 对得很好，near-zero scar 幅度仍有差距。 | 7/15 - 本地 `L=16` full sector，不是论文 `L=32` symmetry sector。 | 70 |
| Fig. 4 level statistics | 0.8 | 34/50 - density of states 和小尺寸 `r` 值上升趋势出现。 | 17/35 - spacing distribution 受未分解对称性影响，和论文图差距明显。 | 7/15 - 没有完成 `k=0, I=+` sector 和 unfolding。 | 58 |

## 结论

这个 case 已经能展示论文的主要物理机制：PXP 约束、`Z2` scar trajectory、长时间振荡和高重叠 scar tower。Fig. 4 是当前最弱项，它需要更严格的对称性 sector 和更大系统尺寸。

## 论文评测字段

| 数值图/表/面板 | Critical | Role | Parameter match | Artifact pass | Data-backed | Failure type |
| --- | --- | --- | --- | --- | --- | --- |
| Fig. 1 Hamiltonian graph | false | method_validation | paper_exact | true | true | none |
| Entanglement dynamics | true | main_claim | reduced_scale | true | true | insufficient_compute |
| Fig. 2 scar tower / FSA | true | main_claim | reduced_scale | true | true | insufficient_compute |
| Fig. 4 level statistics | false | supporting | reduced_scale | true | true | partial_target_coverage |
