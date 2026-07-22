# 超快原子—离子纠缠门复现讲义

本文复现 Mu Qiao 的预印本《Deterministic atom-shuttle interconnects via
ultrafast atom-ion entangling gate》（[arXiv:2607.15597](https://arxiv.org/abs/2607.15597)）。
公开案例关注三个层次：几何 CZ 门的可执行物理模型、多离子与架构层的定量特征、以及与论文版式对齐但不冒充作者原始数据的展示图。

## 核心结果

原子处于 Rydberg 态时，电荷诱导偶极力对原子和离子产生分支依赖位移；离子上的光学 Magnus 力补偿这些分支，使运动轨迹在一个阱周期后同时闭合。四个逻辑分支的几何相位组合为

\[
\Phi_{CZ}=-8\pi(\omega_g/\omega)^2.
\]

取 \(\omega_g/\omega=1/(2\sqrt2)\) 得到 CZ 相位。独立计算在 `t=T`
给出约 `1.7e-16` 的最大位移残差和接近 1 的 concurrence；在 `2T`
回到无纠缠状态。

十离子部分从库仑晶体的平衡位置与 Hessian 计算轴向模，再以 25 段确定性切换序列同时闭合十个模。最高归一化模频率约为 `6.576`，最大闭合残差达到机器精度量级。这证明了论文所需的多模闭合机制，但不宣称恢复作者未公开的具体脉冲。

架构层计算得到混合互连与 250 Hz 光子链路约在 `2 mm` 相交。存储误差按图注公式 `2 pT / Nops` 随操作数下降；论文 Fig. 4(b) 的栅格方向与该公式相反，因此公开科学图遵循公式，并单独保留一致性检查。

## 如何运行

从 RunThePaper 仓库根目录执行：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2607.15597/code
python scripts/run_reproduction.py
```

脚本会重新生成 17 份 CSV、8 张科学复现图和核心 JSON 检查。代码入口在
[`../code/scripts/run_reproduction.py`](../code/scripts/run_reproduction.py)，
完整方程见 [`../docs/DERIVATION.md`](../docs/DERIVATION.md)。

## 怎样理解“像素配准”

公开包还提供 8 张按论文原画布尺寸重绘的 PNG。它们全部通过尺寸一致性检查，最佳全图 SSIM 为 `0.8297`，均值为 `0.7524`；严格阈值 `0.95` 为 `0/8` 通过。因此准确说法是 pixel-registered，而不是 pixel-exact。未公开曲线点、字体和编辑器后处理不能靠复制原图来伪造。

## 复现边界

综合科学证据得分为 `75.21/100`，属于数值特征复现。精确公式与公开表格可以独立重建；Fig. 3 中间时序、热态 QuTiP 扫描、MQDT/Stark map 和 qLDPC Monte Carlo 仍缺少作者输入或运行元数据。所有代理模型和 source-only 投影都在计分卡中单独标记。
