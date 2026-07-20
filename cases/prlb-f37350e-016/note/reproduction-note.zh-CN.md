# D-wave single-impurity resonance benchmark source/gold audit：公开复现讲义

## 结论

Recomputes the frozen impurity-resonance arithmetic, pole equation, and diagnostic curves. The numerical audit is reproducible, but no single PRL source matching the frozen record has been identified.

这个 case 的公开状态是 **Formula-level reproduction with unresolved source identity**。评分代表当前公开证据的覆盖强度，不等于整篇论文已经逐图、逐表完整复现。PRL-Bench 的冻结答案如果与来源公式不一致，公开结果会保留独立计算和失败判定，而不会为了对齐 gold 修改物理模型。

## 核心方法

该复现从来源公式或算法出发，先通过解析恒等式、小规模数值或守恒/归一化检查，再生成结构化数据和图。公开包只包含独立实现、生成数据、生成图片及机器可读检查；原论文 PDF、原图、数字化曲线和内部纠错过程均未发布。

## 主要结果

- Benchmark impurity-resonance audit：Pole equation, resonance energies, and source-identity diagnostics（图：`../outputs/figures/idx16_gold_audit.png`；检查：`../outputs/checks/idx16_audit_figure_check.json`）

## 运行

从本 case 的 `code` 目录执行：

```bash
python scripts/run_gold_audit.py
python scripts/render_idx16_audit.py
```

脚本会把结果写入 case 根目录下的 `outputs/data`、`outputs/figures` 和 `outputs/checks`。较大的 GPU 任务会在主 README 中单独标出，默认命令优先提供可在普通 Python 环境复查的路径。

## 复现边界

This is a benchmark-task case rather than a verified one-paper reproduction. The formulas trace to older review literature and a possible newer candidate, while the frozen third task fails its own pole contract.

因此，本 case 应被理解为具有明确边界的可执行数值/特征复现，而不是对作者全部数据、图形风格或实验条件的替代。
