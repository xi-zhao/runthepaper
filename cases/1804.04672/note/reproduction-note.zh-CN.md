# Non-Hermitian Chern Bands 复现笔记

论文：Shunyu Yao, Fei Song, Zhong Wang, *Non-Hermitian Chern bands*, arXiv:1804.04672

本 note 的目标是把这篇文章的主线讲清楚：模型怎么写，为什么普通 Bloch Chern number 会失效，非 Bloch 描述怎么修正，数值图分别在验证什么，以及当前独立代码复现到了什么程度。

## 1. 物理问题

Hermitian Chern insulator 里，bulk-boundary correspondence 的意思很直接：周期边界下的 Bloch Hamiltonian 给出 Chern number，开边界下就应该看到相应数目的 chiral edge modes。

这篇文章研究的是非厄米二维 Chern 模型。非厄米性带来一个关键变化：开边界本征态不再是普通 Bloch 波，而会出现 non-Hermitian skin effect。也就是说，bulk 态本身会在开边界下向边界堆积。这样一来，用周期边界的 Bloch Hamiltonian 去判断开边界边缘态，会得到错误的相图。

论文的主张可以概括成一句话：

> chiral edge modes 不由普通 Bloch Chern number 控制，而由复波矢空间里的 non-Bloch Chern number 控制。

## 2. 模型

论文主模型是二维两能带非厄米 Chern/Qi-Wu-Zhang 型 Hamiltonian：

$$
H(\mathbf{k})=
\sum_{j=x,y} (v_j \sin k_j+i\gamma_j)\sigma_j+
\left(m-\sum_{j=x,y}t_j\cos k_j+i\gamma_z\right)\sigma_z .
$$

主图中主要使用

$$
t_x=t_y=v_x=v_y=1,\quad \gamma_x=\gamma_y=\gamma,\quad \gamma_z=0.
$$

如果只看普通 Bloch Hamiltonian，能带在复能量平面中分离的边界是

$$
m_\pm=2\pm \sqrt{2}\gamma .
$$

这两条线就是 Fig. 1 和 Fig. 3(a) 里的灰色 dotted Bloch boundaries。它们不是开边界真实相变线，只是用来展示 Bloch 判断会偏离开边界物理。

## 3. 开边界为什么要用 non-Bloch 描述

开边界下，本征态不再满足普通 Bloch ansatz

$$
\psi_n \sim e^{ikn}.
$$

更合适的形式是

$$
\psi_n \sim \beta^n,\quad \beta=re^{i\tilde{k}},
$$

其中 $r$ 可以不等于 1。这个 $r\neq 1$ 就对应 skin effect：bulk 态也会向边界指数局域。

在低能连续近似里，论文得到开边界相变线

$$
m_c=2+\gamma^2 .
$$

这就是 Fig. 1 中蓝色 dashed curve。红色数值边界来自有限尺寸开边界谱的 gap closing；蓝色理论曲线和红色数值曲线接近，说明 non-Bloch 理论抓住了开边界相变。

## 4. Fig. 1：开边界相图

Fig. 1 画的是 square/open-boundary 体系的拓扑相图。横轴是 $m$，纵轴是 $\gamma$。

图里有三类曲线，物理身份不同，不能混在一起：

- 灰色 dotted lines：普通 Bloch gap closing，$m_\pm=2\pm\sqrt{2}\gamma$。
- 蓝色 dashed line：低能 non-Bloch 理论相变线，$m=2+\gamma^2$。
- 红色 solid line：开边界数值谱在热力学极限的 gap closing 点。

当前复现中，Fig. 1 的整体相图结构已经生成；红线仍使用补充材料表格里的数值边界作为 reference，因此 Fig. 1 还不是完整的独立 red-boundary scan。

![Fig. 1 独立生成的开边界相图](../outputs/figures/fig1_open_boundary_phase.png)

Fig. 1 的验收重点不是线条美观，而是三类边界的物理身份是否分清：

- Bloch fan 是对照组；
- non-Bloch curve 是解析近似；
- red curve 是开边界谱的 numerical transition；
- Fig. 2 的两个 marker 落在 Bloch boundary 附近，但开边界物理不同。

## 5. Fig. 2：两个 Bloch 边界点的谱和波包动力学

Fig. 2 选取 Fig. 1 上两个参数点：

$$
\gamma=0.15,\quad m=2.2121,
$$

和

$$
\gamma=0.15,\quad m=1.7879.
$$

这两个点都在普通 Bloch phase boundary 上。按 Bloch 观点，它们都很特殊；但按开边界 non-Bloch 观点，它们处在不同物理区域。

Fig. 2 左侧是 square geometry 的低能实本征值。右侧是波包演化，初态为

$$
\psi(0)=\mathcal{N}
\exp\left[-\frac{(x-15)^2}{40}-\frac{(y-1)^2}{10}\right](1,1)^T .
$$

时间演化满足

$$
i\partial_t|\psi(t)\rangle=H|\psi(t)\rangle .
$$

展示的是每个时刻归一化后的强度

$$
I(x,y,t)=\sum_{\alpha=A,B}|\psi_{x,y,\alpha}(t)|^2,\quad \sum_{x,y}I(x,y,t)=1.
$$

物理解释：

- Fig. 2(a), $m=2.2121$：低能谱有明显 gap，没有 chiral edge mode，初始边界波包很快进入 bulk。
- Fig. 2(b), $m=1.7879$：存在 in-gap edge energies，波包沿边界单向传播。

![Fig. 2 独立生成的方形样品谱与波包动力学](../outputs/figures/fig2_square_dynamics.png)

当前复现使用同一个 square open-boundary Hamiltonian 独立生成谱和波包。视觉上已经复现了“上排入体、下排沿边”的物理特征。还没有做 source intensity map 的像素级匹配。

## 6. Fig. 3：cylinder 几何和方向依赖的 non-Bloch 拓扑

Fig. 3 换成 cylinder：$x$ 方向周期，$y$ 方向开边界。

这个几何下 $k_x$ 仍然是好量子数，$y$ 方向要用 non-Bloch ansatz：

$$
\psi_n=\beta^n\phi .
$$

补充材料给出 open-$y$ bulk continuum 的等模条件。对应半径为

$$
r(k_x)=
\sqrt{\left|
\frac{m-t_x\cos k_x+\gamma_y}
{m-t_x\cos k_x-\gamma_y}
\right|}.
$$

于是

$$
\beta=r(k_x)e^{i\tilde{k}_y}.
$$

Fig. 3(a) 是 cylinder phase diagram。这里的拓扑数是 $C_y$，不一定等于 square/open-boundary 下更物理的 $C$。这也是论文想强调的地方：non-Bloch Chern number 会依赖开边界方向，但真正预测有限样品边缘波包运动的是与实际边界物理相匹配的 non-Bloch 描述。

![Fig. 3(a) 独立生成的 cylinder 相图](../outputs/figures/fig3a_cylinder_phase.png)

当前 Fig. 3(a) 的红色 gapless 边界来自 open-y non-Bloch cylinder bulk continuum 的 band-touching 条件。在论文主参数 $t_x=t_y=v_x=v_y=1,\gamma_x=\gamma_y=\gamma$ 下，边界为

$$
m_-(\gamma)=1+\sqrt{1-2\gamma+2\gamma^2},\quad
m_+(\gamma)=1+\sqrt{1+2\gamma+2\gamma^2}.
$$

我们把论文源图中的红色边界数字化后做验收，当前 RMSE 为 `0.0148`，低于 `0.025` 的门限。源图数字化只作为验收，不作为生成曲线的数据来源。

Fig. 3(b) 固定参数

$$
(m,\gamma)=(1.717,0.2),\quad L_y=40,
$$

取 180 个 $k_x$ 点，把所有复能量画在复平面上。红色分支是 chiral edge states。

当前复现中，红色 edge branch 不是用“边界权重大”直接判定。原因是 skin effect 会让 bulk 态也有边界局域权重。我们采用解析 chiral edge trace

$$
E_+(k_x)=\sin k_x+i\gamma,\quad
E_-(k_x)=-\sin k_x-i\gamma
$$

来匹配有限 strip 谱中的红色分支。EPS 红点提取后，source 有 102 个红点，生成图也有 102 个红点；排序匹配的 mean distance 为 0.0098，max distance 为 0.0263。

![Fig. 3(b) 独立生成的 cylinder 复能谱](../outputs/figures/first_target.png)

## 7. Supplemental Fig. S2：红色相变边界怎么数值确定

Fig. 1 的红线来自开边界谱 gap closing。补充材料说明了具体方法：

1. 对不同系统尺寸 $L$ 求开边界谱；
2. 取最小谱 gap 的平方；
3. 画

$$
|\Delta(L)|^2
$$

对

$$
1/L^2
$$

的图；
4. 做线性拟合：

$$
|\Delta(L)|^2=a/L^2+b;
$$

5. 截距

$$
b=|\Delta(L\to\infty)|^2
$$

判断热力学极限是否 gapless。

Supplemental Fig. S2 取 disk geometry，参数为

$$
\gamma_x=\gamma_y=0.2,
$$

并展示三组 $m$：

$$
m=2.2000,\quad m=2.0800,\quad m=2.0400.
$$

前两者截距非零，说明 gap 不闭合；第三个截距接近零。注意

$$
2+\gamma^2=2+0.2^2=2.04,
$$

所以 $m=2.0400$ 正是 non-Bloch 理论给出的边界点。

当前复现使用 disk sites

$$
x^2+y^2\leq L^2
$$

构造开边界 Hamiltonian，对半径

$$
L=20,24,28,32
$$

求近零谱，并计算

$$
|\Delta|^2=\min_E |E|^2.
$$

拟合得到的截距为：

| panel | m | intercept |
| --- | ---: | ---: |
| S2(a) | 2.2000 | 0.02846 |
| S2(b) | 2.0800 | 0.00252 |
| S2(c) | 2.0400 | 0.000029 |

这个顺序复现了论文物理：非零、非零、接近零。

![Supplemental Fig. S2 独立生成的有限尺寸标度](../outputs/figures/figs2_gap_scaling.png)

## 8. Supplemental Fig. S3：disk geometry 相图

S3 的作用是检查 Fig. 1 的相图是否依赖样品形状。主文 Fig. 1 是 square geometry；S3 换成 disk geometry。

物理对象仍然是同一组边界：

- 红线：disk open-boundary numerical boundary；
- 蓝线：non-Bloch theory, $m=2+\gamma^2$；
- 灰色 dotted lines：普通 Bloch boundaries, $m_\pm=2\pm\sqrt{2}\gamma$。

如果相图是拓扑的，它不应该对 square 或 disk 这种几何细节敏感。S3 里红线和蓝线仍然贴合，说明 disk geometry 得到的 phase diagram 与 Fig. 1 的 square geometry 相图基本一致。

当前复现使用补充材料 Table I 的 disk numerical boundary 作为红线 reference，同时独立生成 Bloch fan 和 non-Bloch theory curve。

![Supplemental Fig. S3 独立生成的 disk 相图](../outputs/figures/figs3_disk_phase.png)

## 9. 当前复现状态

当前共有 6 个 evidence-compared targets：

| Target | 图 | 状态 | 主要剩余缺口 |
| --- | --- | --- | --- |
| T003 | Fig. 1 open-boundary phase diagram | feature-level | red boundary 仍需完整独立 finite-size scan |
| T004 | Fig. 2 square spectra and dynamics | feature-level | intensity map 尚未 digitized/pixel-gated |
| T002 | Fig. 3(a) cylinder phase diagram | digitized-curve-gated feature-level | 仍需 full $C_y$ grid integration gate |
| T001 | Fig. 3(b) cylinder spectrum | stronger feature-level | blue point cloud 和完整 layout 尚未 gate |
| T005 | Suppl. Fig. S2 finite-size fitting | method feature-level | 需要更大半径和 digitized source curve gate |
| T006 | Suppl. Fig. S3 disk phase diagram | method feature-level | red boundary 仍来自 supplement table |

机器评分记录为：

$$
\text{overall score}=80.18,\quad
\text{level}=\text{numerical\_feature\_reproduction}.
$$

这个分数的含义不是“只做对了 80.18% 的物理”，而是对当前证据层级、覆盖范围和剩余缺口的保守评分。它必须和每个目标的证据类型及边界说明一起阅读。

## 10. 代码入口

主要代码和输出如下：

```text
cases/1804.04672/code/src/nonhermitian_chern.py
cases/1804.04672/code/scripts/run_open_boundary_phase_diagram.py
cases/1804.04672/code/scripts/run_square_dynamics.py
cases/1804.04672/code/scripts/run_cylinder_phase_diagram.py
cases/1804.04672/code/scripts/run_first_target.py
cases/1804.04672/code/scripts/run_gap_scaling.py
cases/1804.04672/code/scripts/run_disk_phase_diagram.py
```

主要验收文件：

```text
cases/1804.04672/outputs/checks/similarity_scorecard.json
cases/1804.04672/outputs/checks/harness_case_audit.json
cases/1804.04672/outputs/checks/target_contracts.json
```

## 11. 下一步

按照论文故事线，下一步应做 Supplemental Fig. S4 parameter-variation phase diagrams。它检查非 Bloch 相图在不同非厄米参数和速度参数下是否仍然成立。

接下来优先级是：

1. S4 参数变化相图；
2. S5/S6 skin-effect profile；
3. S8/S9 exactly solvable model。

真正达到像素级复现，需要在每个 target 后再加一层 source digitization 或 pixel-layout gate。当前 note 先把公式、物理对象和独立数值链路跑通。
