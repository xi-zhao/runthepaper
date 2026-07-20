# Phase Transitions in Nonreciprocal Driven-Dissipative Condensates：公开复现讲义

## 结论

Uses an A100 grid calculation to reproduce the paper's gamma=0.3 lambda-2 branch and independently audits the frozen critical-exceptional-point claims. The paper curve passes its feature gate, while the frozen benchmark gold fails independent evaluation.

这个 case 的公开状态是 **A100 source-curve feature reproduction and benchmark audit**。评分代表当前公开证据的覆盖强度，不等于整篇论文已经逐图、逐表完整复现。PRL-Bench 的冻结答案如果与来源公式不一致，公开结果会保留独立计算和失败判定，而不会为了对齐 gold 修改物理模型。

## 核心方法

该复现从来源公式或算法出发，先通过解析恒等式、小规模数值或守恒/归一化检查，再生成结构化数据和图。公开包只包含独立实现、生成数据、生成图片及机器可读检查；原论文 PDF、原图、数字化曲线和内部纠错过程均未发布。

## 主要结果

- gamma=0.3 lambda-2 branch：A100 nonreciprocal-condensate source-curve reproduction（图：`../outputs/figures/idx63_cep_gamma03_reproduction.png`；检查：`../outputs/checks/idx63_figure_check.json`）

## 运行

从本 case 的 `code` 目录执行：

```bash
python scripts/render_idx63_figures.py
```

脚本会把结果写入 case 根目录下的 `outputs/data`、`outputs/figures` 和 `outputs/checks`。较大的 GPU 任务会在主 README 中单独标出，默认命令优先提供可在普通 Python 环境复查的路径。

## 复现边界

The paper-curve result is feature-level rather than author-data exact. Recomputing the full grid requires CUDA/PyTorch; the default public command regenerates figures from the included A100 summaries.

因此，本 case 应被理解为具有明确边界的可执行数值/特征复现，而不是对作者全部数据、图形风格或实验条件的替代。
