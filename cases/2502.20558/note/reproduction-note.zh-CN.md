# 2502.20558 复现 Note：利用量子比特丢失探测改进容错量子算法

## 一句话结论

这个公开 case 独立生成了 5 张图和 Table I 的解析行，综合审计分为
**74.22/100**。Fig. 4(b) 的印刷公式、Fig. 6(b) 的完整数值柱状面板以及
Table I 的生命周期/时空开销行达到 paper-exact；Fig. 2(b)、Fig. 14(c) 和
Fig. 16(a) 是明确标注的机制或子集复现。它不是整篇论文的完整数值复现。

论文来源：[Physical Review X 16, 011002 (2026)](https://doi.org/10.1103/ycwc-3myc)，
预印本为 [arXiv:2502.20558](https://arxiv.org/abs/2502.20558)。

## 论文解决什么问题

带 atom loss 或 qubit loss 的量子硬件可以在测量时知道某个量子比特已经
丢失，但通常不知道丢失发生在该生命周期中的哪个时刻。论文的 delayed-
erasure decoder 使用最终的 SSR 丢失标记，枚举可能的丢失位置，并把每种
位置对应的 detector-error hypergraph 按概率合并。这样既利用了丢失信息，
又不要求实时知道精确丢失时刻。

论文进一步把“量子比特生命周期长度”作为架构比较的核心变量：生命周期
越短，可能的丢失位置越少，解码问题越简单。SWAP、直接转换和 teleportation
等 syndrome-extraction 方案因此可以通过生命周期和时空开销统一比较。

## 公开复现结果

### Fig. 2(b)：delayed-erasure 信息优势

- 状态：`exploratory / proxy_model`
- 评分：47.5
- 做到的事情：在距离五 repetition-code analogue 中，保持论文的 1% 丢失
  率和展示 round 范围，验证“无 SSR 信息最差，delayed SSR 明显改善”的顺序。
- 没做到的事情：没有复现论文 surface-code correlated-MLE 的绝对逻辑错误率。

该结果只能证明信息机制合理，不能用来宣称论文主曲线已被逐点复现。

### Fig. 4(b)：生命周期—loss threshold 关系

- 状态：`final_reproduction / paper_exact analytic relation`
- 评分：83.5
- 独立计算论文印刷的 `7/lifecycle^(1/3)%` 关系，覆盖面板的生命周期区间。
- 原文有限尺寸模拟 marker 因没有原始样本和拟合信息而不在复现声明内。

### Fig. 6(b)：算法生命周期

- 状态：`final_reproduction / paper_exact`
- 评分：89.0
- GHZ、15-to-1 distillation、H/T synthesis 和 adder 的 average/maximum
  lifecycle 四组数值全部复现。这是当前完成度最高的一张图。

### Fig. 14(c)：SWAP all-qubit lifecycle invariant

- 状态：`exploratory / paper_subset`
- 评分：80.0
- 复现 period 1 与 period 2 的 all-qubit 平均生命周期重合，以及向有限距离
  极限收敛的趋势。
- 精确的 noiseless boundary convention 仍需作者 circuit builder 确认。

### Fig. 16(a)：conventional 与 SWAP 生命周期

- 状态：`exploratory / paper_subset`
- 评分：72.5
- 复现 conventional data lifecycle 随深度增长、measure lifecycle 保持常数，
  以及 all-qubit SWAP/conventional 平均值一致的性质。
- SWAP 的 data/measure role-resolved 子曲线需要作者的边界配对规则。

### Table I：解析行

七种方法的 data/measure lifecycle 和 space-time overhead 公式均已独立生成。
表中的 threshold 与 effective-distance 行属于模拟结果，未纳入该解析目标。

## 如何运行

从 RunThePaper 仓库根目录执行：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2502.20558/code
python scripts/run_reproduction.py
```

脚本会重新生成 6 份 CSV、5 张独立图和逐目标 JSON 检查，不读取论文图片、
数字化曲线或作者数据。

## 复现边界

论文和 arXiv 源文件包含 27 张 vector figure，但不包含 surface-code circuit
generator、相关 MLE decoder、raw samples、shots、seeds、完整物理错误率网格和
fit windows。因此 24 个数值 panel/table group 中有 19 个保留为
`missing_author_data`，没有用读图或复制曲线填补。

公开仓库中的对照板只保留验证所需的最小论文摘图片段，左侧明确标记为 paper
reference，右侧为独立生成结果。它们用于解释结构和特征，不代表取得作者原始
数据，也不建立 point-for-point equivalence。
