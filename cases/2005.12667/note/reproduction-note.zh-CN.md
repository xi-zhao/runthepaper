# 《Circuit Quantum Electrodynamics》整篇公式与数值复现

本 case 复现 Blais、Grimsmo、Girvin 与 Wallraff 的综述 *Circuit Quantum Electrodynamics*（arXiv:2005.12667；RMP 93, 025005）。目标不是临摹论文图片，而是把正文 Eq. (1)–(164)、附录 A–C 与可由公开信息重建的数值结果连接成一条可运行、可审计的证据链。

最终结果：30/30 个公式族通过公式门禁，18/18 个独立数值或表格目标通过机器检查，24 个开发期单元测试通过；公开评分为 **90.28/100，numerical feature reproduction**。完整中文推导与数值报告同时提供为 [PDF](reproduction-note.zh-CN.pdf)。

## 核心物理模型

整篇综述可以由同一个状态链组织：

\[
\text{电路量子化}
\rightarrow \text{Duffing--Rabi}
\rightarrow \text{Jaynes--Cummings / 色散模型}
\rightarrow \text{多模与任意多能级}
\rightarrow \text{Born--Markov / 输入输出模型}.
\]

代码和检查始终维护四个不变量：哈密顿量厄米、封闭系统能谱为实数、主方程保迹并保持正性、无内部损耗的单端口散射满足 \(|r|=1\)。这些不变量也用于判断预印本中的符号或系数是否物理自洽。

## 公式覆盖

| 章节 | 公式范围 | 数值证据 |
| --- | --- | --- |
| Sec. II | Eq. (1)–(28) | CPW 谐振、transmon 波函数与电荷色散 |
| Sec. III | Eq. (29)–(63) | JC 的 \(2g\sqrt n\) 劈裂、色散能级、Kerr 与多能级检查 |
| Sec. IV | Eq. (64)–(86) | thermal Lindblad、厄米性、输入输出被动性 |
| Sec. V | Eq. (87)–(120) | 放大器量子极限、测量指针态、SNR 与腔拉移 |
| Sec. VI | Eq. (121)–(128) | 强耦合、真空 Rabi、避免交叉与光子数分裂 |
| Sec. VII | Eq. (129)–(157) | Gaussian/DRAG 控制、幅度阻尼码、cat code |
| Sec. VIII | Eq. (158)–(164) | Fock/Wigner 与压缩态 |
| Appendices | A1–A10、B1–B32、C1–C20 | 与正文符号、变换及端口约定的闭环检查 |

完整逐步推导见 [DERIVATION_TRACE](../docs/DERIVATION_TRACE.md)，30 个公式卡及其代码入口见 [DERIVATION](../docs/DERIVATION.md)，机器门禁摘要见 [FORMULA_VERIFICATION](../docs/FORMULA_VERIFICATION.md)。

## 关键数值结果

- JC 守恒激发子空间的解析本征值与独立矩阵对角化一致；\(2g\sqrt n\) 劈裂最大误差为 \(5.8\times10^{-15}\)。
- 四能级、40 维 Duffing–JC 精确对角化与二阶色散式最大差为 \(2.96\times10^{-6}\)，最小裸态重叠为 0.99298。
- transmon 从 \(E_J/E_C=2\) 到 50 的电荷色散抑制比为 \(3.30\times10^{-6}\)，\(n_g\) 周期性误差为 \(4.44\times10^{-15}\) GHz。
- thermal Lindblad 积分与解析平均光子数的最大误差为 \(4.98\times10^{-11}\)；迹、厄米性和正性同时通过。
- 强耦合真空 Rabi 谱的共振劈裂为 \(2g\)；DRAG 在短门区间将中位误差改善 3.83 倍。
- binomial code 的一阶损失条件达到 \(10^{-15}\) 量级；cat、Fock 叠加与 squeezed-state Wigner 函数通过归一化和非经典性检查。

数据、图和机器检查分别位于 [outputs/data](../outputs/data/)、[outputs/figures](../outputs/figures/) 与 [outputs/checks](../outputs/checks/)。评分口径见 [SIMILARITY_SCORECARD](../docs/SIMILARITY_SCORECARD.md)。

## 重要版本校勘

| arXiv v1 | 正式 RMP / 物理约束 | 本复现处理 |
| --- | --- | --- |
| Eq. (29) 谐振器能量为负 | 正式 Eq. (31) 改为正 | 采用谱下有界的正式版 |
| Eq. (51) 的 \(K_a\) 多出 \(1/2\) | 正式 Eq. (53) 删除该因子 | 由四次项组合因子独立验证 |
| Eq. (67) 对实耦合非厄米 | 正式 Eq. (69) 恢复厄米形式 | 采用正式版并做有限维厄米性审计 |
| Eq. (72)、(75) 直接组合破坏单端口被动性 | 端口相位约定未充分说明 | 固定满足 \(|r|=1\) 的等价约定，并保留 reconstructed 标签 |

## 运行方法

从 RunThePaper 仓库根目录执行：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2005.12667/code
python scripts/run_reproduction.py
python scripts/run_full_rmp_reproduction.py
```

第一个脚本重算 Sec. III 与 Sec. IV 指定内容，包含 Eq. (66)–(68)、(70)–(75)；第二个脚本重算全篇其余独立数值目标。脚本只依赖公开代码和参数，不依赖论文原图。详细离散化、截断与误差阈值见 [NUMERICAL_METHODS](../docs/NUMERICAL_METHODS.md)。

## 复现边界

这里的“整篇复现”指公开公式和参数允许独立重建的理论内容，不把缺失的实验数据或仿真工程冒充为自主结果。Fig. 4(b–e) 仍需要原始 COMSOL 几何、材料与边界条件；Fig. 21、28、32 的实验 panel 需要作者级原始数据和校准链。相应理论或 simulation panel 已重算，但这些外部证据被明确标为阻塞项。
