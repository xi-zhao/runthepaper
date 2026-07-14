# arXiv:2507.09447 中文复现讲义

## 论文身份

- 预印本：[*Lyapunov formulation of band theory for disordered non-Hermitian systems*](https://arxiv.org/abs/2507.09447)，arXiv:2507.09447。
- 正式发表：[*Universal Thouless relations for disordered non–Hermitian systems in one dimension*](https://doi.org/10.1016/j.scib.2026.05.055)，*Science Bulletin*，2026 年 online ahead of print。
- DOI：`10.1016/j.scib.2026.05.055`；PII：`S2095-9273(26)00583-9`。

本 case 的逐图目标仍然是 arXiv v1 的 Fig. 3–5；正式版补充材料只用于核对数值方法。

## 核心问题

无序破坏平移对称性后，通常的 Bloch 能带不再适用。论文用实空间转移矩阵的四个
Lyapunov 指数替代动量空间能带。两个中心指数 `gamma_2` 和 `gamma_3` 的符号决定
态是 Anderson 局域态、单向临界态还是趋肤态；正 Lyapunov 指数的数量还给出谱绕数。

我们的复现对象不是作者图片，而是这套可执行数值关系：有限尺寸 OBC/PBC 谱、
热力学极限 Lyapunov 密度、态分类、绕数，以及随无序增强发生的趋肤–Anderson 相变。

## 做到了什么

- Fig. 3/4 使用 `L=1000` 和 3200 个确定性无序实现，完成 OBC/PBC 谱直方图。
- 用周期 QR 稳定化计算高分辨率 Lyapunov 网格。
- 独立计算十个 ALM、一个近临界态和一个趋肤态的右本征矢轮廓。
- 扫描 `W=0.4,0.8,1.2,1.6,2.0` 的 mobility contour，并在 `W∈[0,3]` 上恢复
  Anderson 局域比例 `alpha`。
- 九项科学验收全部通过，并恢复论文相变点 `W_c=2.1`。

![Fig. 3 independent reproduction](../outputs/figures/fig3_paper_exact.png)

![Fig. 4 independent reproduction](../outputs/figures/fig4_paper_exact.png)

![Fig. 5 independent reproduction](../outputs/figures/fig5_paper_exact.png)

## 如何运行

从仓库根目录运行：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2507.09447/code
python scripts/plot_paper_exact.py
python scripts/qa_paper_exact.py
```

这两个快速命令使用仓库中公开的独立生成数据重画图片并重算科学验收。完整的
`L=1000 × 3200` 计算可运行 `python scripts/run_paper_exact.py`，但耗时显著，且会在
本地生成不纳入 Git 的 checkpoint。

## 复现边界

作者没有公开随机种子、态筛选窗口、转移长度、QR 间隔、Fig. 5 积分细节和最终
Illustrator 工程。因此我们能够复现论文尺度、物理结构、画布几何和相变点，但不声称
逐像素同一。导出审计的 full-image SSIM 为 Fig. 3 `0.7721`、Fig. 4 `0.7735`、
Fig. 5 `0.8521`。这些数值说明视觉差距，不替代科学验收。
