# Enhanced Sampling of Configuration and Path Space in a Generalized Ensemble by Shooting Point Exchange：公开复现讲义

## 结论

Independently reconstructs Fig. 2B from the source potential and audits the frozen efficiency and speedup claims. The free-energy profile is reproduced, while several claimed statistics lack the event counts and rerun data needed for verification.

这个 case 的公开状态是 **Paper-figure feature reproduction and benchmark statistics audit**。评分代表当前公开证据的覆盖强度，不等于整篇论文已经逐图、逐表完整复现。PRL-Bench 的冻结答案如果与来源公式不一致，公开结果会保留独立计算和失败判定，而不会为了对齐 gold 修改物理模型。

## 核心方法

该复现从来源公式或算法出发，先通过解析恒等式、小规模数值或守恒/归一化检查，再生成结构化数据和图。公开包只包含独立实现、生成数据、生成图片及机器可读检查；原论文 PDF、原图、数字化曲线和内部纠错过程均未发布。

## 主要结果

- PRL Fig. 2B：Free-energy profile from deterministic marginalization（图：`../outputs/figures/prl_fig2b_reproduced.png`；检查：`../outputs/checks/gold_audit_check.json`）

## 运行

从本 case 的 `code` 目录执行：

```bash
python scripts/render_prl_fig2b.py
python scripts/render_idx93_audit.py
```

脚本会把结果写入 case 根目录下的 `outputs/data`、`outputs/figures` 和 `outputs/checks`。较大的 GPU 任务会在主 README 中单独标出，默认命令优先提供可在普通 Python 环境复查的路径。

## 复现边界

The source is a 2024 PRL outside the benchmark's declared window. Author trajectories, event counts, and optimized-coordinate rerun rates are unavailable, so the efficiency and speedup claims remain underdetermined.

因此，本 case 应被理解为具有明确边界的可执行数值/特征复现，而不是对作者全部数据、图形风格或实验条件的替代。
