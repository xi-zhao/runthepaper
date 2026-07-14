# 推导讲义：从"能不能有第三种交换统计"到 Fig. 2

> 目标读者：物理研一水平。默认你学过量子力学和一点二次量子化（知道费米/玻色的
> $a,a^\dagger$），不需要任何范畴论、量子群、张量网络背景。全篇自足。
>
> 这份讲义把论文（Wang & Hazzard, *Nature* **637**, 314, 2025）里 Fig. 2 背后的
> 数学从头推一遍，并指出每一步对应本 case 的哪段代码。机读版见 `DERIVATION.md`
> / `EQUATION_CARDS.json`，英文提纲见 `DERIVATION_TRACE.md`。

---

## 0. 一分钟回顾：费米/玻色的二次量子化

一个模态（比如某个动量/格点）上，玻色子有 $[a,a^\dagger]=1$，可以塞任意多个：
态 $|n\rangle=\frac{(a^\dagger)^n}{\sqrt{n!}}|0\rangle$，$n=0,1,2,\dots$。费米子有
$\{a,a^\dagger\}=1$、$(a^\dagger)^2=0$，一个模态最多一个：$n=0,1$。

**关键观察**：费米/玻色的全部区别，浓缩在"交换两个产生算符"这一步的符号上：

$$a^\dagger_i a^\dagger_j = \pm\, a^\dagger_j a^\dagger_i \qquad (+\text{玻色},\ -\text{费米}).$$

论文的出发点就是问：如果把这个 $\pm1$ 换成一个**矩阵** $R$，会怎样？能不能得到
既不是费米也不是玻色、但仍然自洽（局域、幺正、可解）的"第三种粒子"？答案是能，
这种粒子叫 **仲统计粒子（paraparticle）**。

---

## 1. 定义：R 矩阵与基本对易关系

给每个粒子一个额外的**内部指标** $a=1,\dots,m$（像"颜色"）。产生/湮灭算符写成
$\hat\psi^\pm_{i,a}$，$i$ 是模态（位置/动量），$a$ 是颜色。核心定义是一组对易关系
（论文 Eq. `fundamental_Rcommu`）：

$$
\hat\psi^-_{i,a}\hat\psi^+_{j,b}=\sum_{cd}R^{ac}_{bd}\,\hat\psi^+_{j,c}\hat\psi^-_{i,d}+\delta_{ab}\delta_{ij},
\qquad
\hat\psi^+_{i,a}\hat\psi^+_{j,b}=\sum_{cd}R^{cd}_{ab}\,\hat\psi^+_{j,c}\hat\psi^+_{i,d}.
$$

这里 $R^{ab}_{cd}$ 是一个 $m^2\times m^2$ 的数表（四个颜色指标）。它就是"交换两个粒子时
颜色如何混合"的规则，替代了费米/玻色的那个 $\pm1$。

**验证它确实包含费米/玻色**：取 $R^{ab}_{cd}=\pm\,\delta_{ad}\delta_{bc}$（即 $\pm$ 乘一个
"交换颜色"的操作）。代入第二式：
$\hat\psi^+_{i,a}\hat\psi^+_{j,b}=\pm\,\hat\psi^+_{j,a}\hat\psi^+_{i,b}$——正是玻色/费米的
交换规则（内部指标随位置一起换）。所以 $R=\pm\text{swap}$ 就退回老结果，$R$ 是它的推广。

---

## 2. 自洽性：为什么 R 必须解 Yang–Baxter 方程

三个粒子可以按两种顺序两两交换到同一末态（先换 12 再换 23……对比先换 23 再换 12）。
要求两条路径给出同一个结果，就得到 $R$ 必须满足的**常数 Yang–Baxter 方程（YBE）**
（论文 Eq. `YBE`），示意地写作

$$
R_{12}R_{13}R_{23}=R_{23}R_{13}R_{12}.
$$

这不是额外假设，而是"交换操作无歧义"的必要条件。论文 Table 1 给的四个 $R$ 都满足 YBE
（可直接代入验证）。这份 case 用到的四个例子（$m$ 为颜色数）：

| Ex. | $R^{ab}_{cd}$ | 直观 |
|---|---|---|
| 1 (decoupled) | $-\delta_{ad}\delta_{bc}$ | $-$swap，等价于 $m$ 种费米子 |
| 2 (Green) | $\delta_{ad}\delta_{bc}(-1)^{\delta_{ab}}$ | 同色费米、异色玻色 |
| 3 | $-\delta_{ac}\delta_{bd}$ | 关键的非平凡例子 |
| 4 | $\lambda_{ab}\xi_{cd}-\delta_{ac}\delta_{bd}$ | $\lambda\xi\lambda^T\xi^T=\mathbb 1,\ \mathrm{Tr}(\lambda\xi^T)=2$ |

---

## 3. 一个救命的代数结构：$\hat e_{ij}$ 与 $\mathfrak{gl}_N$

单独看 $\hat\psi^\pm$ 很难驾驭。论文的关键技巧是定义**双线性算符**（对颜色求和）：

$$
\hat e_{ij}\equiv\sum_{a=1}^m \hat\psi^+_{i,a}\hat\psi^-_{j,a}.
$$

用基本对易关系可以算出（论文 Eq. `commu_Eab_Ecd`）：

$$
[\hat e_{ij},\hat e_{kl}]=\delta_{jk}\hat e_{il}-\delta_{il}\hat e_{kj}.
$$

**这正是 $\mathfrak{gl}_N$ 李代数**（$N\times N$ 矩阵单位元的对易关系）。$R$ 的复杂性
被"洗掉"了：不管 $R$ 多奇怪，$\hat e_{ij}$ 永远闭合成同一个 $\mathfrak{gl}_N$。三件好事随之而来：

1. **粒子数**：$\hat n_i\equiv\hat e_{ii}$ 两两对易，$\hat n=\sum_i\hat n_i$ 是好量子数；
   且 $[\hat n_i,\hat\psi^\pm_{j,b}]=\pm\delta_{ij}\hat\psi^\pm_{j,b}$，确认 $\psi^+$ 加一个粒子。
2. **局域性**：不相交区域上的可观测量（$\hat e_{ij}$ 的多项式）互相对易 →
   微观因果、幺正演化都成立。仲统计粒子是"物理上合法"的。
3. **可解性**：自由哈密顿量 $H=\sum_{ij}h_{ij}\hat e_{ij}$ 是 $\mathfrak{gl}_N$ 的元素，
   可以像费米/玻色一样被对角化（见 §7）。

> 代码对应：`src/spin_model_1d.py` 里的在位数算符、以及 §7 的自由粒子谱都建立在这条之上。

---

## 4. 广义排斥统计 $d_n$ —— Fig. 2 左图

问：**一个模态里能塞几个仲统计粒子？** 费米=1，玻色=∞，仲统计粒子介于其间，而且
"填第 $n$ 个"时还可能有多个独立态。定义

$$
d_n=\dim\{\,n\text{ 个粒子占据同一个模态的独立态空间}\,\}.
$$

$n$ 个粒子在同一模态的态由波函数 $\Psi_{a_1\dots a_n}$（每个颜色指标 $1..m$）描述，但不是所有
$\Psi$ 都独立——第二条对易关系强加了线性约束。论文（SI Eq. `V_n_basis`）把约束写成：
$\Psi$ 必须是 **"R-对称"** 的，即对每对相邻指标 $j,j{+}1$，

$$
\boxed{\ \sum_{a'_j,a'_{j+1}}R^{a_ja_{j+1}}_{a'_ja'_{j+1}}\ \Psi_{a_1\dots a'_j a'_{j+1}\dots a_n}=\Psi_{a_1\dots a_j a_{j+1}\dots a_n}\ }
$$

$d_n$ = 这个线性方程组的独立解个数。费米/玻色（$R=\pm$swap）时它就是"全反对称/全对称"。
现在逐个例子算（这就是 Fig. 2 左图每一列）：

- **$n=0,1$（对所有 $R$）**：方程为空，无约束 → $d_0=1$（真空），$d_1=m$（$m$ 种颜色的单粒子态）。
- **费米（$m{=}1$）**：反对称，单指标 $\Rightarrow d_0=d_1=1,\ d_{n\ge2}=0$。
- **玻色（$m{=}1$）**：全对称，任意 $n$ 都恰有一个态 $\Rightarrow d_n=1\ \forall n$。
- **Ex.1 / Ex.2**：约束把 $\Psi$ 变成相邻反对称 $\Rightarrow d_n=\binom{m}{n}$，即 $z=(1+x)^m$。
- **Ex.3（$R=-\delta_{ac}\delta_{bd}$）**：取 $n=2$，方程给 $-\Psi_{ab}=\Psi_{ab}\Rightarrow\Psi=0$。
  于是 $d_{n\ge2}=0$：**一个模态最多一个仲统计粒子，但这一个可以有 $m$ 种颜色**（$d_1=m$）。
- **Ex.4**：取 $n=2$，代入 $R=\lambda\xi-\text{swap}$ 得
  $\lambda_{ab}\!\sum_{cd}\xi_{cd}\Psi_{cd}=2\Psi_{ab}$。因为 $\mathrm{Tr}(\lambda\xi^T)=2$，唯一解是
  $\Psi_{ab}\propto\lambda_{ab}$，故 $d_2=1$；$n\ge3$ 无非零解 $\Rightarrow d_{n\ge3}=0$。
  即 $d=(1,m,1,0,\dots)$。

> 这些整数就是 Fig. 2 左图里每一列的能级：横线的**高度**是 $n$，横线的**宽度**编码 $d_n$
> （$d_1$ 越大越宽）。代码：`src/paraparticles.py::Species.degeneracies`，机读校验
> `outputs/checks/fig2.json`（与上面手算逐一对上）。

---

## 5. 单模配分函数 $z_R$ 与热占据 —— Fig. 2 右图

把这些 $d_n$ 打包进一个母函数。设单模能量 $\epsilon$（$H=\epsilon\hat n$），配分函数
（论文 Eq. `single_mode_Z`，数学上叫 $R$ 的 **Hilbert 级数**）：

$$
z_R(x)=\mathrm{Tr}\,e^{-\beta\epsilon\hat n}=\sum_{n\ge0}d_n\,x^n,\qquad x=e^{-\beta\epsilon}.
$$

于是 $d_n$ 就是 $z_R$ 的泰勒系数。Table 1：Ex.1/2 $\to(1+x)^m$，Ex.3 $\to 1+mx$，
Ex.4 $\to 1+mx+x^2$；费米 $\to1+x$，玻色 $\to\sum x^n=1/(1-x)$。

**热占据数**（论文 Eq. `n_k_expectation`）。直接算平均：

$$
\langle\hat n\rangle_\beta=\frac{\sum_n n\,d_n x^n}{\sum_n d_n x^n}
=\frac{x\,\frac{d}{dx}\sum_n d_n x^n}{\sum_n d_n x^n}
=\frac{x\,z_R'(x)}{z_R(x)}=x\frac{d}{dx}\ln z_R(x).
$$

中间用了恒等式 $\sum_n n\,d_n x^n=x\,z_R'(x)$。**这是一步就能独立复现论文公式的推导。**
逐条曲线（$x=e^{-\beta\epsilon}$，横轴 $\beta\epsilon$）：

| 物种 | $z_R$ | $\langle n\rangle$ | $\beta\epsilon{=}0$（$x{=}1$） | $\beta\epsilon\to-\infty$（$x\to\infty$） |
|---|---|---|---|---|
| 费米 | $1+x$ | $\dfrac{x}{1+x}=\dfrac1{e^{\beta\epsilon}+1}$ | $1/2$ | $1$ |
| 玻色 | $\dfrac1{1-x}$ | $\dfrac{x}{1-x}=\dfrac1{e^{\beta\epsilon}-1}$ | 发散 | — |
| Ex.2 ($m{=}2$) | $(1+x)^2$ | $\dfrac{2x}{1+x}$ | $1$ | $2$ |
| Ex.3 ($m{=}2$) | $1+mx$ | $\dfrac{mx}{1+mx}$ | $\dfrac{m}{1+m}{=}\tfrac23$ | $1$ |
| Ex.4 ($m{=}3$) | $1+mx+x^2$ | $\dfrac{mx+2x^2}{1+mx+x^2}$ | $1$ | $2$ |

**一个容易搞错、值得记住的直觉**：$x\to\infty$（$\beta\epsilon\to-\infty$，强烈想填充）时
$\langle n\rangle$ 趋于"最大的、$d_n\neq0$ 的那个 $n$"。所以 **Ex.3 饱和到 1，不是 $m$**——
因为 $d_2=0$，每个模态上限就是 1 个粒子。$m$ 重颜色简并只是让"这 1 个粒子有 $m$ 种选择"，
从而**抬高中温的占据/熵**（右图里 Ex.3 的橙线在 $\beta\epsilon=0$ 处是 $2/3$，比费米的 $1/2$ 高），
**但不改变上限**。这正是"广义排斥统计"区别于费米玻色的地方。

> 代码：`src/paraparticles.py::Species.occupation`，`scripts/gen_fig2.py`；极限值在
> `outputs/checks/fig2.json` 里逐一断言通过。左右两图合成即 Fig. 2，与原图逐特征吻合
> （对照 `docs/comparisons/…_fig2_source_vs_reproduction.png`）。

---

## 6. 自由仲统计粒子的精确解

一般自由（双线性）哈密顿量 $H=\sum_{ij}h_{ij}\hat e_{ij}$，$h$ 是 $N\times N$ 厄米矩阵。
因为 $\{\hat e_{ij}\}$ 构成 $\mathfrak{gl}_N$（§3），存在一个**正则变换**（把模态线性重组成
本征模 $k$），使

$$
H=\sum_{k=1}^N \epsilon_k\,\tilde n_k,\qquad \epsilon_k=\text{eig}(h),
$$

其中 $\tilde n_k$ 是互相对易的本征模占据数。于是总配分函数**因子化**：

$$
Z=\mathrm{Tr}\,e^{-\beta H}=\prod_{k=1}^N z_R\!\big(e^{-\beta\epsilon_k}\big),
$$

每个本征模就是一个独立的"单模问题"，占据数照抄 §5 的 $\langle\tilde n_k\rangle=xz'/z$。
**这就是"自由仲统计粒子气体"**：热力学完全由单模 $z_R$ 和单粒子谱 $\{\epsilon_k\}$ 决定。

---

## 7. 落到实处：1D 可解自旋模型 = 自由仲统计粒子（本 case 的 ED 验证）

前面都是算符代数。它对应真实系统吗？论文给了一个**局域、厄米的自旋链**
（Ex.3，论文 Eq. `Hamil1Dspin`），每个格点是 $(m{+}1)$ 维，基 $|0\rangle,\{|1,a\rangle\}$，
在位阶梯算符 $\hat y^+_a|0\rangle=|1,a\rangle$、$\hat x^\pm=\hat y^\pm$：

$$
H=\sum_{i,a}J_i\big(\hat x^+_{i,a}\hat y^-_{i+1,a}+\hat x^-_{i,a}\hat y^+_{i+1,a}\big)-\sum_{i,a}\mu_i\,\hat y^+_{i,a}\hat y^-_{i,a}.
$$

**广义 Jordan–Wigner 变换（gJWT）** 把在位算符映成仲统计粒子算符 $\hat\psi$ 的 MPO 串
（费米的 JW 符号串，在这里换成了 $R$ 的串）。映完之后

$$
H=\sum_{ij}h_{ij}\hat e_{ij},\qquad h\ \text{三对角}:\ h_{i,i+1}=h_{i+1,i}=J_i,\ h_{ii}=-\mu_i.
$$

因为 gJWT 是代数同构，它**保谱**。结合 §6：多体谱就是"挑一个占据模子集 $S$，能量
$\sum_{k\in S}\epsilon_k$"，而每个被占据的模有 $m$ 重颜色简并、每模最多占 1 个（Ex.3 的 $d_1=m,d_2=0$）：

$$
\boxed{\ \text{谱}=\Big\{\textstyle\sum_{k\in S}\epsilon_k:\ S\subseteq\{1,\dots,N\}\Big\},\quad \text{每个 }S\text{ 的重数}=m^{|S|}.\ }
$$

自洽性检查：总维数 $\sum_{S}m^{|S|}=\sum_{j}\binom{N}{j}m^{j}=(1+m)^N=(m{+}1)^N$，正好等于
自旋链的希尔伯特空间维数，检查通过。

**这正是本 case 独立验证的对象**：`src/spin_model_1d.py` 暴力搭出 $(m{+}1)^N$ 维的 $H$、
严格对角化，`scripts/run_ed_validation.py` 把它的整条谱和上面盒子里的自由粒子预言逐一对比：

- 谱吻合到 $\sim10^{-14}$（机器精度），$N=4,5\,(m{=}2)$ 与 $N=4\,(m{=}3)$；
- $[H,\hat n]=0$ 精确成立（守恒的仲统计粒子数）。

也就是说，$z_R=1+mx$ 不是凑出来的母函数——它是一个**真实局域自旋模型**的精确解，从第一性
原理被数值证实。这是把 Fig. 2 的公式"钉死"的一步。机读结果：`outputs/checks/ed_validation.json`。

---

## 8. 一句话串起来

$R$ 矩阵（解 YBE）定义交换规则 → 双线性算符给出 $\mathfrak{gl}_N$，保证局域可解 →
R-对称条件数出每模能容纳的态数 $d_n$（Fig. 2 左）→ 母函数 $z_R=\sum d_n x^n$ 与
$\langle n\rangle=xz'/z$ 给出热力学（Fig. 2 右）→ 自由哈密顿量因子化成单模问题 →
一个真实的 1D 可解自旋链在严格对角化下正好实现这套自由仲统计粒子谱。
