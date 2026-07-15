# 《Benchmarking and Fidelity Response Theory of High-Fidelity Rydberg Entangling Gates》复现说明

本文复现对应 PRX Quantum 6, 010331 (2025)，DOI：
`10.1103/PRXQuantum.6.010331`。公开 case 的目标不是临摹论文图片，
而是把论文中的响应理论、哈密顿量和公开参数变成可运行的数值程序。

## 复现范围

我们追踪并计算了九个可独立数值化的理论目标：Fig. 15 的 Appendix-L
通用响应包络、Fig. 6(a) 的 Rabi 频率缩放、Fig. 1(f)/Fig. 7 的误差缩放、
Fig. 8 的公开锚点标度、Fig. 9(a,b) 的三种 CZ 协议响应、Fig. 10 的
spin-lock 滤波函数、Fig. 12 的 140 kHz 腔传递、Fig. 17 的相位翻转/SSB
解析模型，以及 Fig. 11 的七站点 128 维多体响应。每个目标都有 CSV、
生成图和机器检查。

T001-T002 是按论文打印公式和系数直接数值化的正式解析复现；T003-T008
是公式数值化或带公开锚点的重构；T005 和 T009 分别包含独立的两原子
8 维哈密顿量传播和七体 128 维传播。`79.89/100` 只评价具有 paper-exact
解析参照的 T001-T002，不把缺少作者数组的目标强行做像素相似度评分。

## 如何运行

在本 case 的 `code` 目录执行：

```bash
python scripts/run_reproduction.py
python scripts/run_formula_theory_targets.py
pytest -q tests
```

程序从 `code/config` 读取参数，将数值表、图和检查结果写入 case 根目录的
`outputs`。核心模块分别负责通用 fidelity response、门协议、多体响应和
其他解析理论目标，绘图只消费已经生成的数值数组。

## 无像素计算承诺

任何论文图片像素、描点曲线或栅格拟合都没有进入物理计算。计算链严格为
“公式/哈密顿量与参数 → 数值数据 → 生成图”。论文图片只在计算完成后进入
两张预先生成的并排对照拼图；公开代码不读取它们，自动 provenance 审计也
确认整个计算路径没有图像读取。

## 不能 paper-exact 的边界

论文没有公开全部测量 PSD、硬件校准数组、精确原子几何和 ramp、Fig. 15
专用优化相位轨迹以及部分离散电路信息。因此相关绝对曲线保留为 partial、
reconstructed 或 blocked；本复现没有用原图像素“补齐”这些缺失物理输入。
