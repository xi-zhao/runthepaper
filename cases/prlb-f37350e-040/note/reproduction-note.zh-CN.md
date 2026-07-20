# Nonlinear Stage of Modulational Instability in Repulsive Two-Component Bose-Einstein Condensates：公开复现讲义

## 结论

Recomputes the benchmark selection rule and modulational-instability wedge directly from the source equations, with independent analytic and numerical checks.

这个 case 的公开状态是 **Equation-level numerical feature reproduction**。评分代表当前公开证据的覆盖强度，不等于整篇论文已经逐图、逐表完整复现。PRL-Bench 的冻结答案如果与来源公式不一致，公开结果会保留独立计算和失败判定，而不会为了对齐 gold 修改物理模型。

## 核心方法

该复现从来源公式或算法出发，先通过解析恒等式、小规模数值或守恒/归一化检查，再生成结构化数据和图。公开包只包含独立实现、生成数据、生成图片及机器可读检查；原论文 PDF、原图、数字化曲线和内部纠错过程均未发布。

## 主要结果

- Modulational-instability selection rule：Analytic wedge and frozen-answer consistency map（图：`../outputs/figures/idx40_selection_rule_audit.png`；检查：`../outputs/checks/gold_audit_check.json`）

## 运行

从本 case 的 `code` 目录执行：

```bash
python scripts/run_gold_audit.py
python scripts/render_idx40_audit.py
```

脚本会把结果写入 case 根目录下的 `outputs/data`、`outputs/figures` 和 `outputs/checks`。较大的 GPU 任务会在主 README 中单独标出，默认命令优先提供可在普通 Python 环境复查的路径。

## 复现边界

The source equations and benchmark observables are reproduced, but paper-panel curves are not claimed because the author simulation arrays and full evolution metadata are unavailable.

因此，本 case 应被理解为具有明确边界的可执行数值/特征复现，而不是对作者全部数据、图形风格或实验条件的替代。
