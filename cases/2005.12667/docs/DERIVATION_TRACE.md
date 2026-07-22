# 公式推导与可执行追踪

本文档复现 arXiv:2005.12667 全篇可执行公式链：正文式 (1)--(164) 与附录 A--C。公式编号默认采用用户给出的 arXiv v1；正式发表的 RMP 版本编号不同。第三、四章保留逐式展开，第二、五至八章按共享假设和共同生成元组织成公式族；这比逐行抄公式更能显示每一步近似从哪里来。所有进入数值代码的公式均有 `EQUATION_CARDS.json` 卡片、代码入口和机器校验。

## 0. 约定、核心模型与版本校勘

统一取

\[
[a,a^\dagger]=[b,b^\dagger]=1,\qquad
\Delta=\omega_q-\omega_r,\qquad
\alpha_q=E_C/\hbar>0,
\]

其中 transmon 的非简谐性是负的：相邻跃迁频率为

\[
\omega_{j,j+1}=\omega_q-j\alpha_q.
\]

数值代码采用 \(\hbar=1\)，但推导保留 \(\hbar\)。本复现的核心对象不是单张图，而是同一个“电路自由度--有效哈密顿量--开放端口”模型在不同近似下的状态：

\[
\text{电路量子化}
\to \text{Duffing--Rabi}
\to \text{Jaynes--Cummings / 色散模型}
\to \text{多模与任意多能级}
\to \text{Born--Markov / 输入输出模型}.
\]

沿这条链必须始终满足四个不变量：哈密顿量厄米、封闭系统能谱实数、主方程保迹且保持正性、无内部损耗的单端口散射满足 \(|r|=1\)。这些不变量也用于校勘论文版本：

| arXiv v1 | 正式 RMP | 校勘结论 | 本复现采用 |
| --- | --- | --- | --- |
| 式 (29)：谐振器能量前为负号 | 式 (31)：改为正号 | 解耦极限必须是下有界的正能谐振子 | 正式版正号 |
| 式 (51)：\(K_a=-(E_C/2\hbar)(g/\Delta)^4\) | 式 (53)：去掉额外的 \(1/2\) | 由变换后的四次项直接比对系数可证 | 正式版系数 |
| 式 (67)：\(ab_\omega^\dagger-a^\dagger b_\omega\)，实 \(\lambda\) 时非厄米 | 式 (69)：改为 \(ab_\omega^\dagger+a^\dagger b_\omega\) | 有限维矩阵厄米性直接判别 | 正式版加号 |
| 式 (68)：写成 \(-i[H_S,\rho]\) | 式 (70) 同样简写 | 若 \(H_S\) 以能量计，量纲要求 \(-i[H_S,\rho]/\hbar\) | 代码取 \(\hbar=1\) |
| 式 (72)、(75)：边界项与驱动项同号 | 正式版式 (74)、(77) 未改 | 两式同时照抄会得到无损端口 \(|r|\ne1\) | 使用等价、被动且自洽的相位约定 |

前三项是可由正式发表版和物理不变量共同确认的源修订；最后一项属于约定重建，不能伪装成逐字照抄。

## A. 第二章：从电路变量到 transmon（式 1--28）

### A.1 LC 模的正则量子化（式 1--6）

选节点磁通 \(\Phi(t)=\int^tV(t')dt'\) 为广义坐标，拉氏量为

\[
L=\frac{C}{2}\dot\Phi^2-\frac{\Phi^2}{2L}.
\]

共轭动量就是电荷

\[
Q=\frac{\partial L}{\partial\dot\Phi}=C\dot\Phi,
\]

Legendre 变换给出

\[
H=Q\dot\Phi-L=\frac{Q^2}{2C}+\frac{\Phi^2}{2L}. \tag{1}
\]

正则量子化要求 \([\hat\Phi,\hat Q]=i\hbar\)。令

\[
\hat\Phi=\Phi_{\rm zpf}(a+a^\dagger),\qquad
\hat Q=-iQ_{\rm zpf}(a-a^\dagger),
\]

则交换关系要求 \(2\Phi_{\rm zpf}Q_{\rm zpf}=\hbar\)。另一方面，消去 \(a^2\) 与 \(a^{\dagger2}\) 要求

\[
\frac{Q_{\rm zpf}^2}{2C}=\frac{\Phi_{\rm zpf}^2}{2L}.
\]

两式联立得到

\[
\Phi_{\rm zpf}=\sqrt{\frac{\hbar Z_r}{2}},\qquad
Q_{\rm zpf}=\sqrt{\frac{\hbar}{2Z_r}},\qquad
Z_r=\sqrt{L/C},
\]

并得到

\[
H=\hbar\omega_r(a^\dagger a+1/2),\qquad \omega_r=1/\sqrt{LC}. \tag{5}
\]

这里有两个独立检查：Heisenberg 方程给出 \(\ddot\Phi+\Phi/(LC)=0\)；真空电压方差为 \(\Delta V_0^2=\hbar\omega_r/(2C)\)。

### A.2 传输线连续极限与模展开（式 7--16）

把长度 \(d\) 的传输线离散成 \(\delta x\) 小段，每段电容 \(c_0\delta x\)、电感 \(l_0\delta x\)。连续极限的 Hamiltonian 是

\[
H=\int_0^d dx\left[\frac{Q(x)^2}{2c_0}+\frac{(\partial_x\Phi)^2}{2l_0}\right]. \tag{7}
\]

由 \(\dot\Phi=Q/c_0\)、\(\dot Q=\partial_x^2\Phi/l_0\) 得

\[
\partial_t^2\Phi=v_0^2\partial_x^2\Phi,\qquad
v_0=\frac1{\sqrt{l_0c_0}}. \tag{8}
\]

开路端电流 \(I=-\partial_x\Phi/l_0\) 为零，所以 Neumann 边界条件选择

\[
u_m(x)=\sqrt2\cos(k_mx),\qquad k_m=(m+1)\pi/d.
\]

把 \(\Phi(x,t)=\sum_m\Phi_m(t)u_m(x)\) 代回并用正交关系

\[
\frac1d\int_0^d u_m(x)u_n(x)dx=\delta_{mn},
\]

交叉项全部消失，每个模都变成独立 LC 振子：

\[
H=\sum_m\left(\frac{Q_m^2}{2C_m}+\frac{\Phi_m^2}{2L_m}\right)
=\sum_m\hbar\omega_m(a_m^\dagger a_m+1/2),
\]

\[
\omega_m=v_0k_m=2\pi(m+1)\frac{v_0}{2d}. \tag{16}
\]

这直接给出图 2 的等间隔 \(f_m=(m+1)f_0\)。有限线宽只需令每模具有 \(\kappa_m=\omega_m/Q_m\)；它不是新的本征频率假设。

三维矩形腔则从 Maxwell 边界条件分离变量得到

\[
\omega_{mnl}=c\sqrt{(m\pi/a)^2+(n\pi/b)^2+(l\pi/d)^2}. \tag{17}
\]

这个解析式只能复现频率结构，不能复现图 4(b--e) 的 COMSOL 场图；后者还需要完整几何、材料、端口和网格。

### A.3 Josephson 非线性与精确 transmon Hamiltonian（式 18--20）

Josephson 关系

\[
I=I_c\sin\varphi,\qquad \varphi=2\pi\Phi/\Phi_0
\]

给出微分电感

\[
L_J(\Phi)=\left(\frac{\partial I}{\partial\Phi}\right)^{-1}
=\frac{\Phi_0}{2\pi I_c\cos(2\pi\Phi/\Phi_0)}. \tag{18}
\]

势能由 \(dU/d\Phi=I\) 积分：

\[
U_J(\Phi)=-E_J\cos\varphi,\qquad E_J=\Phi_0I_c/(2\pi). \tag{19}
\]

加入总电容 \(C_\Sigma\) 和偏置电荷 \(Q_g=2en_g\)，得到

\[
H_T=4E_C(\hat n-n_g)^2-E_J\cos\hat\varphi,qquad E_C=e^2/(2C_\Sigma). \tag{20}
\]

在电荷基中 \(e^{\pm i\varphi}|n\rangle=|n\pm1\rangle\)，因此

\[
\langle n|H_T|m\rangle=4E_C(n-n_g)^2\delta_{nm}
-\frac{E_J}{2}(\delta_{n,m+1}+\delta_{n,m-1}).
\]

这是图 5、6 的数值起点，而不是四阶近似。把 \(n_g\to n_g+1\) 同时把基标号 \(n\to n+1\)，谱不变，给出严格的 Cooper-pair 周期性检查。

### A.4 transmon 极限与 Duffing 模（式 21--25）

当 \(E_J/E_C\gg1\)，低能波函数局域在余弦势阱底部：

\[
-E_J\cos\varphi=-E_J+\frac{E_J}{2}\varphi^2-\frac{E_J}{24}\varphi^4+O(\varphi^6).
\]

二次部分由

\[
\varphi=\left(\frac{2E_C}{E_J}\right)^{1/4}(b+b^\dagger),\qquad
n=\frac{i}{2}\left(\frac{E_J}{2E_C}\right)^{1/4}(b^\dagger-b)
\]

对角化，裸 plasma 频率为 \(\omega_p=\sqrt{8E_CE_J}/\hbar\)。对四次项作正常序并在 RWA 下保留等数目的 \(b,b^\dagger\)：

\[
(b+b^\dagger)^4\ \longrightarrow\ 6b^{\dagger2}b^2+12b^\dagger b+3.
\]

于是除去常数后

\[
H_q\simeq\hbar\omega_qb^\dagger b-\frac{E_C}{2}b^{\dagger2}b^2,
\qquad \hbar\omega_q=\sqrt{8E_CE_J}-E_C. \tag{25}
\]

因此 \(\omega_{12}-\omega_{01}=-E_C/\hbar\)。该结论只对低能级成立；四次截断 Hamiltonian 在无限 Hilbert 空间下不下有界，数值高激发态必须回退到完整余弦模型。

### A.5 SQUID 可调性（式 26--28）

两结的总 Josephson 势为

\[
-E_{J1}\cos\varphi_1-E_{J2}\cos\varphi_2,
\]

磁通量子化给 \(\varphi_1-\varphi_2=2\pi\Phi_x/\Phi_0\)。取平均相位并合并两项，可写成一个有相移的余弦：

\[
H_T=4E_Cn^2-E_J(\Phi_x)\cos(\varphi-\varphi_0),
\]

\[
E_J(\Phi_x)=E_{J\Sigma}\cos(\pi\Phi_x/\Phi_0)
\sqrt{1+d^2\tan^2(\pi\Phi_x/\Phi_0)},\quad
d=\frac{E_{J2}-E_{J1}}{E_{J\Sigma}}. \tag{28}
\]

对称极限 \(d=0\) 恢复熟知的 \(E_J=E_{J\Sigma}|\cos(\pi\Phi_x/\Phi_0)|\)；绝对值来自始终围绕最近势阱极小值展开。

## 1. 第三章 A：由电容耦合到 Jaynes--Cummings 模型（式 29--34）

### 1.1 量子门电荷与完整电路哈密顿量

经典偏置 transmon 的充电项是 \(4E_C(n-n_g)^2\)。把门电压换成谐振器的量子电压，并采用论文约定 \(n_g\to-n_r\)，得到

\[
H=4E_C(n+n_r)^2-E_J\cos\varphi
+\sum_m\hbar\omega_m a_m^\dagger a_m. \tag{29, corrected}
\]

这里

\[
n_r=\sum_m\frac{C_g}{C_m}\frac{Q_m}{2e}.
\]

展开平方后，\(n_r^2\) 只重整化谐振器电容和频率；交叉项

\[
H_{\rm int}=8E_C n n_r
\]

才产生光--物质耦合。若令 \(C_g\to0\)，必须恢复正能 transmon 与正能谐振器之和，这排除了 arXiv 式 (29) 的负号。

### 1.2 单模、弱非简谐与旋波近似

只保留最接近 \(\omega_q\) 的谐振器模，并在 \(E_J/E_C\gg1\) 时把 transmon 展开到四阶：

\[
-E_J\cos\varphi\simeq -E_J+\frac{E_J}{2}\varphi^2-\frac{E_J}{24}\varphi^4.
\]

用零点涨落表示电荷和相位，整理二次项后得到 Duffing 模；交叉充电项给出

\[
H\simeq\hbar\omega_r a^\dagger a+\hbar\omega_q b^\dagger b
-\frac{E_C}{2}b^{\dagger2}b^2
-\hbar g(b^\dagger-b)(a^\dagger-a). \tag{30}
\]

相互作用展开为

\[
-\hbar g(b^\dagger a^\dagger-b^\dagger a-ba^\dagger+ba).
\]

在 \(|g|\ll\omega_r,\omega_q\) 下，\(b^\dagger a^\dagger\) 和 \(ba\) 以 \(\omega_r+\omega_q\) 快速旋转；保留交换项即

\[
H_{\rm RWA}=\hbar\omega_r a^\dagger a+\hbar\omega_qb^\dagger b
-\frac{E_C}{2}b^{\dagger2}b^2
+\hbar g(b^\dagger a+ba^\dagger). \tag{32}
\]

耦合常数的两种写法

\[
g=\omega_r\frac{C_g}{C_\Sigma}
\left(\frac{E_J}{2E_C}\right)^{1/4}
\sqrt{\frac{\pi Z_r}{R_K}} \tag{31}
\]

和

\[
g=\omega_r\frac{C_g}{C_\Sigma}
\left(\frac{E_J}{2E_C}\right)^{1/4}
\sqrt{\frac{Z_r}{Z_{\rm vac}}}\sqrt{2\pi\alpha} \tag{33}
\]

由 \(\alpha=Z_{\rm vac}/(2R_K)\) 立即相等；代码用独立函数计算两式并验证到机器精度。

最后把 transmon 截断到 \(|g\rangle,|e\rangle\)，作 \(b\to\sigma_-\)、\(b^\dagger\to\sigma_+\)，得到

\[
H_{\rm JC}=\hbar\omega_ra^\dagger a+
\frac{\hbar\omega_q}{2}\sigma_z+
\hbar g(a^\dagger\sigma_-+a\sigma_+). \tag{34}
\]

## 2. 第三章 B：Jaynes--Cummings 精确谱（式 35--39）

总激发数

\[
N_T=a^\dagger a+\sigma_+\sigma_-
\]

满足 \([H_{\rm JC},N_T]=0\)。因此每个 \(n\ge1\) 子空间
\(\{|g,n\rangle,|e,n-1\rangle\}\) 独立。加上论文使用的无关全局能移后，块矩阵是

\[
H_n=\hbar n\omega_r I+\frac{\hbar}{2}
\begin{pmatrix}
-\Delta&2g\sqrt n\\
2g\sqrt n&\Delta
\end{pmatrix}.
\]

特征方程

\[
\det(H_n-EI)=
(\hbar n\omega_r-E)^2-\frac{\hbar^2}{4}(\Delta^2+4g^2n)=0
\]

直接给出

\[
E_{\overline{g,n}/\overline{e,n-1}}
=\hbar n\omega_r\mp\frac{\hbar}{2}\sqrt{\Delta^2+4g^2n}. \tag{38}
\]

令

\[
\tan\theta_n=\frac{2g\sqrt n}{\Delta},
\]

对应的二维旋转给出式 (39) 的两个本征态。把所有 \(n\) 块写成算符函数，就得到论文的

\[
U=\exp\!\left[\Lambda(N_T)(a^\dagger\sigma_- -a\sigma_+)\right],\quad
\Lambda(N_T)=\frac{\arctan(2g\sqrt{N_T}/\Delta)}{2\sqrt{N_T}}. \tag{35--36}
\]

在共振点 \(\Delta=0\)，双重态劈裂严格为

\[
E_+-E_-=2\hbar g\sqrt n,
\]

这既是图 8 的核心特征，也是数值复现的第一目标。独立 `eigvalsh` 与解析式的最大误差为零到浮点精度。

## 3. 第三章 C.1：Schrieffer--Wolff 色散展开（式 40--44）

### 3.1 二阶虚跃迁

将式 (32) 写为 \(H=H_0+V\)，其中

\[
V=\hbar g(b^\dagger a+ba^\dagger).
\]

Duffing 裸态 \(|j,n\rangle\) 的能量为

\[
E^{(0)}_{j,n}/\hbar=n\omega_r+j\omega_q-\frac{\alpha_q}{2}j(j-1).
\]

相互作用只连接相邻 transmon 能级：

\[
|j,n\rangle\leftrightarrow|j-1,n+1\rangle,
\qquad
|j,n\rangle\leftrightarrow|j+1,n-1\rangle.
\]

两条虚过程的能量分母分别是

\[
\Delta-(j-1)\alpha_q,qquad-[\Delta-j\alpha_q].
\]

因此非简并二阶微扰给出

\[
\frac{\delta E^{(2)}_{j,n}}{\hbar}
=\frac{jg^2(n+1)}{\Delta-(j-1)\alpha_q}
-\frac{(j+1)g^2n}{\Delta-j\alpha_q}.
\]

定义

\[
\chi_{j-1,j}=\frac{jg^2}{\Delta-(j-1)\alpha_q},
\quad
\Lambda_j=\chi_{j-1,j},
\quad
\chi_j=\chi_{j-1,j}-\chi_{j,j+1},
\]

就有 \(\delta E^{(2)}_{j,n}/\hbar=\Lambda_j+n\chi_j\)，即式 (40)--(41)。等价的算符推导是选择反厄米生成元 \(S\) 使

\[
[H_0,S]=-V,
\]

并使用 BCH 展开

\[
e^{-S}He^S=H_0+\frac12[V,S]+O(g^3).
\]

### 3.2 两能级形式与适用边界

投影到 \(j=0,1\)，把共同频移吸收进 \(\omega_r',\omega_q'\)，得到

\[
H_{\rm disp}^{(2)}=\hbar\omega_r'a^\dagger a+
\frac{\hbar\omega_q'}2\sigma_z+
\hbar\chi a^\dagger a\sigma_z, \tag{42}
\]

其中

\[
\omega_r'=\omega_r-\frac{g^2}{\Delta-\alpha_q},\quad
\omega_q'=\omega_q+\frac{g^2}{\Delta},\quad
\chi=-\frac{g^2\alpha_q}{\Delta(\Delta-\alpha_q)}. \tag{43}
\]

这个结果有关键物理极限：\(\alpha_q\to0\) 时 \(\chi\to0\)。两个线性谐振子可以互相重整化频率，却不能产生依赖量子态的腔拉移。

微扰小参数不仅是 \(|g/\Delta|\)，还含玻色增强因子。比较相邻裸态的能差与耦合矩阵元，论文给出

\[
\bar n\ll n_{\rm crit}^{(j)}=
\frac{1}{2j+1}\left[
\frac{|\Delta-j\alpha_q|^2}{4g^2}-j
\right]. \tag{44}
\]

本复现选 \(|g/\Delta|=0.03\)、\(n\le3\)，远低于 \(n_{\rm crit}^{(0)}=277.78\) 与 \(n_{\rm crit}^{(1)}=144.34\)。式 (40) 与四能级 Duffing--JC 完整矩阵的独立对角化最大能量差约 \(3\times10^{-6}\)，最小裸态重叠约 0.993。

## 4. 第三章 C.2：Bogoliubov 正则模与 Kerr 项（式 45--51）

先把式 (32) 分成

\[
H_L/\hbar=\omega_ra^\dagger a+\omega_qb^\dagger b+g(a^\dagger b+ab^\dagger),
\qquad
H_{NL}=-\frac{E_C}{2}b^{\dagger2}b^2. \tag{45--46}
\]

线性部分对应矩阵

\[
M=\begin{pmatrix}\omega_r&g\\g&\omega_q\end{pmatrix}.
\]

以 \(U_{\rm disp}=\exp[\Lambda(a^\dagger b-ab^\dagger)]\) 旋转，非对角项为零要求

\[
\tan(2\Lambda)=\frac{2g}{\Delta}.
\]

故正则模频率是

\[
\widetilde\omega_{r/q}=\frac{\omega_r+\omega_q
\mp\sqrt{\Delta^2+4g^2}}2. \tag{49}
\]

再对四次项作同一旋转。若 \(b\to c b-s a\)，其中 \(c=\cos\Lambda,s=\sin\Lambda\)，保留数目守恒项可得

\[
H'_{NL}\supset
-\frac{E_C}{2}s^4a^{\dagger2}a^2
-\frac{E_C}{2}c^4b^{\dagger2}b^2
-2E_Cc^2s^2a^\dagger ab^\dagger b.
\]

与论文定义 \((\hbar K_a/2)a^{\dagger2}a^2\) 比较，得到

\[
K_a=-\frac{E_C}{\hbar}s^4
\simeq-\frac{E_C}{\hbar}\left(\frac g\Delta\right)^4.
\]

这证明正式 RMP 式 (53) 正确，也定位出 arXiv 式 (51) 额外的 \(1/2\)。同理 \(K_b\simeq-E_C/\hbar\)。仅靠上述直接旋转会给最低阶交叉项；论文进一步用一次 SW 变换消去 \(b^\dagger b a^\dagger b+\mathrm{H.c.}\)，得到改进的

\[
\chi_{ab}\simeq-\frac{2g^2\alpha_q}{\Delta(\Delta-\alpha_q)}=2\chi. \tag{51, corrected coefficient for }K_a
\]

该展开要求远离 \(\Delta=0\) 和 \(\Delta=\alpha_q\)；straddling 区应回到完整数值对角化。

## 5. 第三章 D：黑盒量子化（式 52--58）

把结的线性电感并入环境，剩余纯非线性为

\[
H_{NL}=-E_J\left(\cos\varphi+\frac{\varphi^2}{2}\right)
\simeq-\frac{E_J}{24}\varphi^4+O(\varphi^6). \tag{52}
\]

线性电磁环境先按经典正则模对角化，再写

\[
\varphi=\sum_m(\varphi_m a_m+\varphi_m^*a_m^\dagger). \tag{55}
\]

单模四次展开的数目守恒部分含组合因子 6：

\[
(a+a^\dagger)^4\xrightarrow{\rm RWA}
6a^{\dagger2}a^2+12a^\dagger a+3.
\]

不同模式的 \(n_mn_n\) 项有组合因子 24。代回 \(-E_J\varphi^4/24\) 得

\[
\hbar\chi_{mn}=-E_J\varphi_m^2\varphi_n^2,
\quad K_m=\frac{\chi_{mm}}2,
\quad \Delta_m=\frac12\sum_n\chi_{mn}. \tag{56--57}
\]

定义能量参与率

\[
p_m=\frac{2E_J}{\hbar\omega_m}\varphi_m^2,
\]

消去 \(\varphi_m\) 后即

\[
\chi_{mn}=-\frac{\hbar\omega_m\omega_n}{4E_J}p_mp_n. \tag{58}
\]

代码分别从相位零点涨落与参与率计算同一 Kerr 矩阵，误差为浮点舍入量级。

## 6. 第三章 E：任意多能级人工原子（式 59--62）

不再展开余弦，而是在电荷基中精确对角化

\[
H_T=4E_Cn^2-E_J\cos\varphi,
\]

得到 \(|j\rangle,\omega_j\) 与电荷矩阵元。系统哈密顿量写成

\[
H=\sum_j\hbar\omega_j|j\rangle\langle j|+
\hbar\omega_ra^\dagger a+
i\sum_{ij}\hbar g_{ij}|i\rangle\langle j|(a^\dagger-a). \tag{59--60}
\]

对每个虚中间态 \(|i,n\pm1\rangle\) 作二阶微扰。真空过程给 Lamb 位移

\[
\Lambda_j=\sum_i\frac{|g_{ij}|^2}{\omega_j-\omega_i-\omega_r},
\]

而产生和湮灭光子的两条通道之差给

\[
\chi_j=\sum_i\left[
\frac{|g_{ij}|^2}{\omega_j-\omega_i-\omega_r}
-\frac{|g_{ij}|^2}{\omega_i-\omega_j-\omega_r}
\right]. \tag{61--62}
\]

这就是比 Duffing 近似更一般的有效模型。数值实现遇到近零分母会显式拒绝，而不是暗中加入展宽。

## 7. 第三章 F：纵向耦合（式 63）

\[
H_z=\hbar\omega_ra^\dagger a+
\frac{\hbar\omega_q}{2}\sigma_z+
\hbar g_z(a+a^\dagger)\sigma_z. \tag{63}
\]

因为 \([H_z,\sigma_z]=0\)，两个 qubit 扇区不混合。配方得到

\[
H_z=\hbar\omega_r
\left(a^\dagger+\frac{g_z}{\omega_r}\sigma_z\right)
\left(a+\frac{g_z}{\omega_r}\sigma_z\right)
+\frac{\hbar\omega_q}{2}\sigma_z-\frac{\hbar g_z^2}{\omega_r},
\]

故

\[
E_{n,s}/\hbar=n\omega_r+s\frac{\omega_q}{2}-\frac{g_z^2}{\omega_r},
\qquad s=\pm1.
\]

有限 Fock 截断对两个扇区的前五个能级都复现该结果，最大误差约 \(8\times10^{-15}\)。

## 8. 第四章：连续传输线与微观耦合（式 64--67）

### 8.1 从离散模到连续模（式 64--65）

长度 \(d\) 的传输线有离散波数，\(d\to\infty\) 时模间隔趋于零。按

\[
b_m\to\sqrt{\Delta\omega}\,b_\omega,qquad
\sum_m\to\int\frac{d\omega}{\Delta\omega}
\]

缩放，离散对易关系变成

\[
[b_\omega,b_{\omega'}^\dagger]=\delta(\omega-\omega'),
\]

哈密顿量为

\[
H_{\rm tml}=\int_0^\infty d\omega\,\hbar\omega b_\omega^\dagger b_\omega. \tag{64}
\]

开路端的 standing-wave 模函数是 \(\cos(\omega x/v)\)。由每个模的零点涨落及 \(Q=c\dot\Phi\) 得

\[
\Phi_{\rm tml}(x)=\int_0^\infty d\omega
\sqrt{\frac{\hbar}{\pi\omega cv}}
\cos\frac{\omega x}{v}(b_\omega^\dagger+b_\omega),
\]

\[
Q_{\rm tml}(x)=i\int_0^\infty d\omega
\sqrt{\frac{\hbar\omega c}{\pi v}}
\cos\frac{\omega x}{v}(b_\omega^\dagger-b_\omega). \tag{65}
\]

一个场含 \(\omega^{-1/2}\)，另一个含 \(\omega^{1/2}\)，正好保证正则对易关系和 \(Q=c\dot\Phi\)。

### 8.2 电容耦合与旋波近似（式 66--67）

小耦合电容在最低阶产生 \(Q_rQ_{\rm tml}(0)\) 型交叉项。写入谐振器电荷零点涨落和上面的连续场，得到

\[
H=H_S+H_{\rm tml}-\hbar\int_0^\infty d\omega\,
\lambda(\omega)(b_\omega^\dagger-b_\omega)(a^\dagger-a), \tag{66}
\]

\[
\lambda(\omega)=\frac{C_\kappa}{\sqrt{cC_r}}
\sqrt{\frac{\omega_r\omega}{2\pi v}}.
\]

两个括号都是反厄米且作用在不同子空间，所以乘积厄米。有限维张量积检查残差为零。

高 \(Q\) 谐振器只响应 \(\omega\simeq\omega_r\) 的窄带，故取 \(\lambda(\omega)\simeq\lambda(\omega_r)\)，丢弃以 \(\omega+\omega_r\) 旋转的 \(ab_\omega\) 与 \(a^\dagger b_\omega^\dagger\)。正式发表版的厄米 RWA 形式为

\[
H_I^{\rm RWA}=\hbar\int_0^\infty d\omega\,
\lambda(\omega_r)(ab_\omega^\dagger+a^\dagger b_\omega). \tag{67, corrected}
\]

对浴模作相位变换 \(b_\omega\to ib_\omega\)，也可写成常见的

\[
H_I^{\rm RWA}=i\hbar\int d\omega\,
\lambda(\omega_r)(a^\dagger b_\omega-b_\omega^\dagger a).
\]

两者物理等价；arXiv 原式缺少使差式变为厄米的 \(i\)。矩阵检查中，原式厄米性残差约 0.594，而正式版为零。

## 9. 第四章：Born--Markov 主方程（式 68--69）

在相互作用绘景中，整体密度矩阵满足

\[
\dot\rho_{SB}^I(t)=-\frac{i}{\hbar}[H_I(t),\rho_{SB}^I(t)].
\]

积分一次再代回，取系统偏迹：

\[
\dot\rho_S^I(t)=-\frac{1}{\hbar^2}
\int_0^t d\tau\,
\operatorname{Tr}_B[H_I(t),[H_I(t-\tau),\rho_{SB}^I(t-\tau)]].
\]

依次使用：

1. Born 弱耦合：\(\rho_{SB}^I(t-\tau)\simeq\rho_S^I(t)\otimes\rho_B\)；
2. Markov 短记忆：把上限延到 \(\infty\)；
3. 热浴关联：
   \(\langle b_\omega^\dagger b_{\omega'}\rangle=\bar n(\omega)\delta(\omega-\omega')\)，
   \(\langle b_\omega b_{\omega'}^\dagger\rangle=[\bar n(\omega)+1]\delta(\omega-\omega')\)；
4. \(\int_0^\infty d\tau e^{\pm i(\omega_r-\omega)\tau}
=\pi\delta(\omega_r-\omega)\pm i\,\mathcal P(\omega_r-\omega)^{-1}\)。

主值虚部产生 Lamb 位移并吸收进 \(H_S\)，实部给

\[
\kappa=2\pi\lambda(\omega_r)^2
=Z_{\rm tml}\omega_r^2\frac{C_\kappa^2}{C_r}.
\]

最终

\[
\dot\rho_S=-\frac{i}{\hbar}[H_S,\rho_S]
+\kappa(\bar n_\kappa+1)\mathcal D[a]\rho_S
+\kappa\bar n_\kappa\mathcal D[a^\dagger]\rho_S, \tag{68}
\]

\[
\mathcal D[O]\rho=O\rho O^\dagger-\frac12\{O^\dagger O,\rho\}. \tag{69}
\]

迹守恒直接来自

\[
\operatorname{Tr}(O\rho O^\dagger)
=\operatorname{Tr}(O^\dagger O\rho),
\]

而 Lindblad 结构保证完全正。对数算符 \(n=a^\dagger a\)，伴随主方程给

\[
\frac{d\langle n\rangle}{dt}=-\kappa(\langle n\rangle-\bar n_\kappa),
\]

故

\[
\langle n(t)\rangle=\bar n_\kappa+
[\langle n(0)\rangle-\bar n_\kappa]e^{-\kappa t}.
\]

数值积分与解析式最大误差约 \(5\times10^{-11}\)，迹误差 \(6.7\times10^{-16}\)，最小密度矩阵本征值不低于数值容差。

## 10. 第四章：输入输出理论（式 70--75）

### 10.1 行波分解与边界条件（式 70--72）

把 standing wave 拆为右、左行波：

\[
\cos(\omega x/v)b_\omega
\longrightarrow
\frac12\left(b_{R\omega}e^{i\omega x/v}
+b_{L\omega}e^{-i\omega x/v}\right).
\]

在 \(x=0\)，电压分成入射与出射分量

\[
V_{\rm in/out}(t)=i\int_0^\infty d\omega
\sqrt{\frac{\hbar\omega}{4\pi cv}}
e^{i\omega t}b_{L/R,\omega}^\dagger+\mathrm{H.c.} \tag{70}
\]

Kirchhoff 电流定律把样品注入线中的电流与行波电压差联系起来：

\[
I(t)=\frac{V_{\rm out}(t)-V_{\rm in}(t)}{Z_{\rm tml}},
\qquad
I(t)=\frac{C_\kappa}{C_r}\dot Q_r(t). \tag{71}
\]

代入谐振器 \(Q_r\) 的模展开、仅保留 \(\omega\simeq\omega_r\) 的慢变项，得到输入输出边界关系。其符号随端口参考方向和场相位改变；论文写成

\[
b_{\rm out}(t)-b_{\rm in}(t)=\sqrt\kappa,a(t). \tag{72, paper convention}
\]

### 10.2 时间场归一化（式 73--74）

在载频 \(\omega_r\) 周围定义慢变包络

\[
b_{\rm in}(t)=\frac{-i}{\sqrt{2\pi}}
\int_{-\infty}^{\infty}d\omega\,
b_{L\omega}e^{-i(\omega-\omega_r)t}, \tag{73}
\]

\[
b_{\rm out}(t)=\frac{-i}{\sqrt{2\pi}}
\int_{-\infty}^{\infty}d\omega\,
b_{R\omega}e^{-i(\omega-\omega_r)t}. \tag{74}
\]

原本 \(\omega>0\) 的积分被扩展到整个实轴，是窄带 Markov 近似的一部分。由 Fourier 恒等式立即得到

\[
[b_{\rm in}(t),b_{\rm in}^\dagger(t')]=\delta(t-t'),
\]

所以 \(b^\dagger b\) 的量纲是光子流率。

### 10.3 Heisenberg--Langevin 方程与符号闭合（式 75）

从 RWA 系统--浴哈密顿量求 \(\dot b_\omega\)，形式积分后代回 \(\dot a\)。利用

\[
\int d\omega\,e^{-i(\omega-\omega_r)(t-t')}=2\pi\delta(t-t')
\]

得到阻尼项 \(-\kappa a/2\) 和入射噪声项。论文写作

\[
\dot a=i[H_S,a]-\frac\kappa2a+\sqrt\kappa,b_{\rm in}. \tag{75}
\]

这里同样隐含 \(\hbar=1\)。式 (72) 与 (75) 的两个相对符号不能独立选择。若照抄为“驱动加号、输出也加号”，对无内部损耗的一端口稳态腔，在旋转框架有

\[
a_{ss}=\frac{\sqrt\kappa}{i\Delta_d+\kappa/2}b_{\rm in},
\]

从而得到非被动的散射幅度。为让能流守恒，本复现固定为等价的自洽约定

\[
\dot a=-(i\Delta_d+\kappa/2)a+\sqrt\kappa,b_{\rm in},
\qquad
b_{\rm out}=b_{\rm in}-\sqrt\kappa,a.
\]

于是

\[
r(\Delta_d)=\frac{b_{\rm out}}{b_{\rm in}}
=1-\frac{\kappa}{i\Delta_d+\kappa/2}
=\frac{i\Delta_d-\kappa/2}{i\Delta_d+\kappa/2},
\]

并且对所有实 \(\Delta_d\)，

\[
|r(\Delta_d)|=1.
\]

若同时把 \(b_{\rm in}\) 或腔模改相位，边界式与驱动式会一起变号，物理散射不变。这里修复的是两式的相对号，而不是宣称某个单独符号具有绝对意义。数值扫描的最大通量守恒误差为 \(3.3\times10^{-16}\)。

## B. 第四章 C--F：退相干、Purcell 与相干控制（式 76--86）

### B.1 从热 Lindblad 方程读出 \(T_1,T_2\)

把式 (68) 的振子湮灭算符换成 transmon 的 \(b\)，再加纯退相干通道：

\[
\dot\rho=-i[H_q,\rho]+\gamma(\bar n+1)\mathcal D[b]\rho
+\gamma\bar n\mathcal D[b^\dagger]\rho
+2\gamma_\varphi\mathcal D[b^\dagger b]\rho. \tag{77--79}
\]

在二能级近似中，激发与弛豫率分别为

\[
\gamma_\uparrow=\bar n\gamma,\qquad
\gamma_\downarrow=(\bar n+1)\gamma.
\]

人口差方程

\[
\dot z=-(\gamma_\uparrow+\gamma_\downarrow)(z-z_{eq})
\]

给出

\[
T_1^{-1}=\gamma_1=\gamma_\uparrow+\gamma_\downarrow.
\]

非对角元逐项计算为

\[
\dot\rho_{ge}=-\left(i\omega_q+\frac{\gamma_1}{2}+\gamma_\varphi\right)\rho_{ge},
\]

因此

\[
T_2^{-1}=\gamma_2=\gamma_1/2+\gamma_\varphi. \tag{80}
\]

式 (78) 前面的 2 正是为了让二能级相干以 \(\gamma_\varphi\) 而非 \(\gamma_\varphi/2\) 衰减。

### B.2 色散变换为什么产生 Purcell 通道（式 81--83）

主方程的 collapse operator 也必须随 SW 变换。对 \(S=\lambda(a^\dagger b-ab^\dagger)\)、\(\lambda=g/\Delta\)，一阶 BCH 给出

\[
e^{-S}ae^S=a-\lambda b+O(\lambda^2),\qquad
e^{-S}be^S=b+\lambda a+O(\lambda^2).
\]

因此腔损耗项变成

\[
\kappa\mathcal D[a-\lambda b]\rho
\simeq \kappa\mathcal D[a]\rho+\lambda^2\kappa\mathcal D[b]\rho+\text{快旋交叉项}.
\]

丢弃快旋交叉项后立即识别

\[
\gamma_\kappa=(g/\Delta)^2\kappa,qquad
\kappa_\gamma=(g/\Delta)^2\gamma. \tag{83}
\]

同理，数目算符在色散变换后含 \(a^\dagger b+b^\dagger a\)，故低频纯退相干噪声在频率 \(\pm\Delta\) 产生 dressed-dephasing 跃迁，白噪声近似下

\[
\gamma_\Delta=2(g/\Delta)^2\gamma_\varphi.
\]

这也解释了纵向耦合没有 Purcell 混合：其 Hamiltonian 与 \(\sigma_z\) 对易，不需要交换型 SW 旋转。

### B.3 入射相干场等价于 Hamiltonian 驱动（式 84--86）

在 Langevin 方程中作

\[
b_{in}(t)\to b_{in}(t)+\beta(t),\qquad
\beta(t)=A(t)e^{-i\omega_dt-i\phi_d}.
\]

经典项 \(\sqrt\kappa\beta\) 可由

\[
H_d=\hbar[\varepsilon(t)a^\dagger e^{-i\omega_dt-i\phi_d}+\mathrm{H.c.}],
\qquad \varepsilon=i\sqrt\kappa A
\]

生成。若只保留该线性驱动，时间演化算符属于 Weyl 位移群，因而真空演化到

\[
|\alpha\rangle=D(\alpha)|0\rangle
=e^{-|\alpha|^2/2}\sum_{n=0}^\infty\frac{\alpha^n}{\sqrt{n!}}|n\rangle. \tag{85}
\]

归一化来自 Poisson 级数；BCH 给出 \(D^\dagger aD=a+\alpha\)，因此 \(\langle n\rangle=|\alpha|^2\)。

## C. 第五章：从行波电压到量子测量（式 87--120）

### C.1 单时域模、放大器幺正性与半量子噪声（式 87--93）

连续输出场不能直接当成单个玻色模。用归一化滤波器定义

\[
b[f]=\int dt\,f(t)b(t),\qquad \int dt|f(t)|^2=1.
\]

由 \([b(t),b^\dagger(t')]=\delta(t-t')\) 得 \([b[f],b^\dagger[f]]=1\)。

若相位保持放大器只写 \(b_{out}=\sqrt G b_{in}\)，则输出交换子会变为 \(G\)，不可能来自幺正演化。必须引入独立 idler 模：

\[
b_{out}=\sqrt G b_{in}+\sqrt{G-1}\,h^\dagger. \tag{88}
\]

因为 \([h^\dagger,h]=-1\)，输出交换子重新为 1。真空 idler 的对称噪声是 \(1/2\)，折算到输入端：

\[
N_{add}=\frac{G-1}{G}\frac12\xrightarrow{G\gg1}\frac12.
\]

多级链递推给 Friis 形式

\[
N_{sys}=N_1+\frac{N_2}{G_1}+\frac{N_3}{G_1G_2}+\cdots,
\]

相应量子效率

\[
\eta=\frac1{1+2N_{sys}}. \tag{92}
\]

### C.2 IQ 混频为何测到两个正交分量（式 94--99）

把窄带信号写为

\[
V_s(t)=I(t)\cos\omega_st-Q(t)\sin\omega_st
\]

并分别与相位相差 \(\pi/2\) 的本振相乘。积化和差后包含 \(\omega_s+\omega_{LO}\) 与 \(\omega_s-\omega_{LO}\)；低通滤除前者，只剩

\[
V_{IF}(t)=I(t)\cos\omega_{IF}t+Q(t)\sin\omega_{IF}t. \tag{96}
\]

相敏同相检测只保留一个旋转后的正交量

\[
X_\phi=\frac{ae^{-i\phi}+a^\dagger e^{i\phi}}{\sqrt2}. \tag{99}
\]

同时测两个正交量需要相位保持放大，因此与前述半量子 added-noise 极限一致。

### C.3 Wigner、位移奇偶与边缘分布（式 100--106）

定义 Weyl 特征函数

\[
C_\rho(\xi)=\mathrm{Tr}[\rho D(\xi)].
\]

Wigner 函数是其辛 Fourier 变换。利用

\[
D^\dagger(\alpha)\rho D(\alpha)
\]

把相空间点 \(\alpha\) 平移到原点，再利用原点 Wigner 值等于奇偶期望，可得可测形式

\[
W_\rho(\alpha)=\frac2\pi\mathrm{Tr}[D^\dagger(\alpha)\rho D(\alpha)P],
\qquad P=(-1)^{a^\dagger a}. \tag{102}
\]

对相干态，位移把它变为真空，故

\[
W_{|\beta\rangle}(\alpha)=\frac2\pi e^{-2|\alpha-\beta|^2}. \tag{103}
\]

在一个坐标上积分，Fourier 指数产生 delta 函数，留下对应正交量的 Born 概率，这就是式 (104) 的 marginal。Husimi 函数

\[
Q(\alpha)=\pi^{-1}\langle\alpha|\rho|\alpha\rangle
\]

等于 Wigner 与一个真空高斯卷积，因此总是非负，但分辨率比 Wigner 低一个真空噪声核。

### C.4 色散指针态方程（式 107--113）

在驱动频率旋转框架，对 qubit 本征值 \(s=\pm1\)，色散 Hamiltonian 将腔失谐改为 \(\delta_r+s\chi\)。线性系统保持相干态，因此联合态为

\[
|\psi(t)\rangle=c_g|g,\alpha_g(t)\rangle+c_e|e,\alpha_e(t)\rangle. \tag{108}
\]

Langevin 方程直接给

\[
\dot\alpha_s=-i\varepsilon-[i(\delta_r+s\chi)+\kappa/2]\alpha_s. \tag{109}
\]

常驱动、真空初态的完整解为

\[
\alpha_s(t)=\alpha_s^{ss}[1-e^{-[i(\delta_r+s\chi)+\kappa/2]t}],
\]

\[
\alpha_s^{ss}=\frac{-i\varepsilon}{i(\delta_r+s\chi)+\kappa/2}. \tag{110}
\]

这既生成图 18 的相空间轨迹，也生成图 19 的幅度和相位响应。两指针的欧氏距离 \(|\alpha_e-\alpha_g|\) 才是可区分信息，不是单独某一条轨迹的幅度。

### C.5 SNR、保真度与测量效率（式 114--120）

对最佳同相角积分输出记录，两个 qubit 假设下均值差累加、白噪声方差线性增长：

\[
\mathrm{SNR}^2=2\eta\kappa\int_0^\tau dt\,|\alpha_e(t)-\alpha_g(t)|^2. \tag{115}
\]

两个等方差 Gaussian 分布在中点作阈值判决，积分尾概率得

\[
F=\frac12\left[1+\mathrm{erf}\left(\frac{\mathrm{SNR}}2\right)\right]. \tag{116}
\]

长时间且共振驱动时，将式 (110) 代入可得到一个只依赖 \(2\chi/\kappa\) 的响应因子；求导显示在固定腔内光子数下最优点为

\[
2|\chi|/\kappa=1.
\]

环境通过未观测输出获得同样的 qubit 信息，导致

\[
\Gamma_\varphi=\frac\kappa2|\alpha_e-\alpha_g|^2.
\]

理想检测将全部退相干转成记录中的信息，故 \(\eta=\Gamma_{meas}/(2\Gamma_\varphi)=1\)；链路损失只减小 \(\Gamma_{meas}\)。纵向读出式 (119)--(120) 则直接对两个 qubit 状态施加相反腔驱动，不依赖静态色散混合。

## D. 第六章：耦合区与可观测谱（式 121--128）

### D.1 弱驱动 Maxwell--Bloch 闭合（式 121--124）

在 \(\omega_q=\omega_r\) 时，JC 第 \(n\) 激发流形的双重态为

\[
E_{n,\pm}=n\hbar\omega_r\pm\hbar g\sqrt n. \tag{121}
\]

加入弱探测后，期望值方程为

\[
\dot{\langle a\rangle}=-(i\delta_r+\kappa/2)\langle a\rangle
-ig\langle\sigma_-\rangle-i\varepsilon,
\]

\[
\dot{\langle\sigma_-\rangle}=-(i\delta_q+\gamma_2)\langle\sigma_-\rangle
+ig\langle a\sigma_z\rangle. \tag{122--123}
\]

弱驱动下 qubit 几乎在基态，\(\langle a\sigma_z\rangle\simeq-\langle a\rangle\)，于是稳态线性方程给

\[
\langle a\rangle_{ss}=\frac{-i\varepsilon}
{i\delta_r+\kappa/2+g^2/(i\delta_q+\gamma_2)}. \tag{124}
\]

分母的两个复极点统一描述坏腔、坏比特和强耦合。在 \(\kappa,\gamma_2\ll g\) 时实部相隔约 \(2g\)；在 \(g=0\) 时退回单腔 Lorentzian。

### D.2 坏腔消元与 Purcell 插值（式 125）

对 qubit 振幅消去腔自由度，其自能为

\[
\Sigma(\omega_q)=\frac{g^2}{\Delta+i\kappa/2}.
\]

虚部给额外衰减：

\[
\gamma_\kappa=-2\operatorname{Im}\Sigma
=\frac{g^2\kappa}{\Delta^2+(\kappa/2)^2}
=\frac{(g/\Delta)^2\kappa}{1+(\kappa/2\Delta)^2}. \tag{125}
\]

这在 \(|\Delta|\gg\kappa\) 回到色散 Purcell 率，在 \(\Delta\to0\) 时保持有限，说明简单 \((g/\Delta)^2\) 公式不能跨共振使用。

### D.3 光学 Bloch 稳态与功率展宽（式 126--128）

色散 Hamiltonian 给 qubit 频率

\[
\omega_q(n)=\omega_q+\chi+2\chi n. \tag{126}
\]

受驱二能级的 Bloch 方程

\[
\dot x=-\gamma_2x-\delta_qy,\quad
\dot y=\delta_qx-\gamma_2y-\Omega_Rz,\quad
\dot z=\Omega_Ry-\gamma_1(z+1)
\]

在稳态消去 \(x,y\) 得

\[
z_{ss}=-1+\frac{\Omega_R^2/(\gamma_1\gamma_2)}
{1+(\delta_q/\gamma_2)^2+\Omega_R^2/(\gamma_1\gamma_2)}. \tag{127}
\]

线宽因此从 \(\gamma_2\) 增长为 \(\gamma_2\sqrt{1+\Omega_R^2/(\gamma_1\gamma_2)}\)。若腔在相干态，每个 Poisson 权重 \(P_n=e^{-\bar n}\bar n^n/n!\) 产生中心在 \(\omega_q+\chi+2\chi n\) 的谱线；强色散时形成 photon-number splitting。

测量诱导退相干式 (128) 也可由相干态重叠推出：

\[
\langle\alpha_g|\alpha_e\rangle
=\exp[-|\alpha_e-\alpha_g|^2/2+i\operatorname{Im}(\alpha_g^*\alpha_e)].
\]

每个泄漏时间片携带距离 \(\sqrt\kappa(\alpha_e-\alpha_g)dt\)，连续乘积得到 \(\Gamma_\varphi=\kappa|\alpha_e-\alpha_g|^2/2\)。

## E. 第七章：控制、两比特门与玻色编码（式 129--157）

### E.1 旋转框架、Rabi 轴与 DRAG（式 129--133）

对

\[
H=H_q+\hbar\varepsilon(t)(b^\dagger e^{-i\omega_dt-i\phi_d}+\mathrm{H.c.})
\]

用 \(U=e^{-i\omega_dt b^\dagger b}\) 变换，得到

\[
H'=\hbar\delta_qb^\dagger b-\frac{E_C}{2}b^{\dagger2}b^2
+\hbar\varepsilon(t)(b^\dagger e^{-i\phi_d}+\mathrm{H.c.}). \tag{130}
\]

截断到二能级：

\[
H'_{TLS}=\frac{\hbar\delta_q}{2}\sigma_z
+\frac{\hbar\Omega_R(t)}2(\cos\phi_d\,\sigma_x+\sin\phi_d\,\sigma_y),
\quad \Omega_R=2\varepsilon. \tag{131}
\]

短 Gaussian 脉冲的带宽会驱动 \(|1\rangle\leftrightarrow|2\rangle\)。对相邻跃迁失谐 \(\alpha_q=E_C/\hbar\) 作绝热消元，泄漏幅度的领先项正比 \(\dot\Omega_x/\alpha_q\)。选第二正交量

\[
\Omega_y(t)\simeq-\dot\Omega_x(t)/\alpha_q
\]

可抵消领先非绝热项，这就是 DRAG。数值目标只比较该机制，不声称复现缺失的实验校准曲线。

### E.2 交换、总线、CZ、RIP 与 CR（式 134--147）

两个远失谐 qubit 通过总线耦合时，二阶 SW 的两条虚路径相加：

\[
J=\frac{g_1g_2}{2}\left(\frac1{\Delta_1}+\frac1{\Delta_2}\right),
\qquad H_{swap}=\hbar J(\sigma_+^{(1)}\sigma_-^{(2)}+\mathrm{H.c.}).
\]

共振演化时间 \(t=\pi/(2J)\) 交换一个激发，\(t=\pi/(4J)\) 产生 \(\sqrt{i\mathrm{SWAP}}\)。把 \(|11\rangle\) 调到 \(|02\rangle\) 共振时，其二能级块

\[
\hbar J_{11,02}(|11\rangle\langle02|+\mathrm{H.c.})
\]

完成一个闭合 Rabi 周期后 \(|11\rangle\) 获得相位 \(-1\)，实现 CZ。

RIP 门用腔驱动产生依赖联合 qubit 状态的闭合相空间回路，其几何相位转成 \(ZZ\)；CR 门则驱动控制 qubit 于目标频率。对交换耦合做 SW 后，驱动算符获得条件项

\[
H_{CR}\supset-\hbar\varepsilon(t)\frac{J E_{C1}}{\hbar\Delta_{12}}\sigma_z^{(1)}\sigma_x^{(2)}. \tag{146}
\]

有限非简谐性同时产生 \(IX\)、\(ZZ\) 等项，所以二能级直觉不足以决定实际校准。

### E.3 参数调制与 Jacobi--Anger 展开（式 148--153）

令耦合 \(J(t)=J_0+\tilde J\cos\omega_mt\)。在 qubit 自由旋转框架中，交换项带相位 \(e^{i(\omega_{q1}-\omega_{q2})t}\)。选择

\[
\omega_m=|\omega_{q1}-\omega_{q2}|
\]

后余弦的一支抵消该相位，RWA 留下

\[
H'\simeq\frac{\tilde J}{2}(\sigma_+^{(1)}\sigma_-^{(2)}+\mathrm{H.c.}). \tag{150}
\]

若调制的是 qubit 频率，累积相位含 \(z\cos\omega_mt\)。Jacobi--Anger 恒等式

\[
e^{iz\cos\theta}=\sum_{n=-\infty}^{\infty}i^nJ_n(z)e^{in\theta}
\]

把它分解成 sidebands；满足 \(n\omega_m=\Delta_{12}\) 的一支成为共振，有效耦合为 \(J J_n(\varepsilon/\omega_m)\)。

### E.4 单光子损失码的 Knill--Laflamme 条件（式 154--157）

最小 binomial 码

\[
|0_L\rangle=(|0\rangle+|4\rangle)/\sqrt2,
\qquad |1_L\rangle=|2\rangle \tag{154}
\]

满足

\[
\langle i_L|n|j_L\rangle=2\delta_{ij},\qquad
\langle i_L|a|j_L\rangle=0.
\]

因此对错误集合 \(\{I,a\}\)，

\[
P E_\mu^\dagger E_\nu P=c_{\mu\nu}P,
\]

即一阶 Knill--Laflamme 条件成立。显式作用

\[
a(c_0|0_L\rangle+c_1|1_L\rangle)
\propto c_0|3\rangle+c_1|1\rangle
\]

保留逻辑振幅，同时 parity 从偶变奇，因而错误可检测。四分量 cat 码把同一结构推广为模 4 光子数扇区；两分量 cat 码则在有限 \(|\alpha|\) 时只近似满足正交与等损失率。

## F. 第八章：参量放大、压缩与远程奇偶（式 158--164）

### F.1 从受泵 Kerr 模到 DPA（式 158--159）

以 \(\omega_p\simeq\omega_0\) 线性泵浦弱 Kerr 模：

\[
H=\hbar\omega_0a^\dagger a+\frac{\hbar K}{2}a^{\dagger2}a^2
+\hbar\varepsilon_p(a^\dagger e^{-i\omega_pt}+ae^{i\omega_pt}). \tag{158}
\]

先到泵浦旋转框架，再作位移 \(a\to a+\alpha\)。选择经典稳态 \(\alpha\) 消去所有线性项；Kerr 四次项展开后含 \(K\alpha^2a^{\dagger2}/2+\mathrm{H.c.}\)，于是小涨落 Hamiltonian 为

\[
H_{JPA}=\hbar\delta a^\dagger a
+\frac\hbar2(\varepsilon_2a^{\dagger2}+\varepsilon_2^*a^2)+H_{corr},
\qquad \varepsilon_2=K\alpha^2, \tag{159}
\]

其中 \(\delta=\omega_0+2K|\alpha|^2-\omega_p\)。小信号下忽略 \(H_{corr}\) 的 Kerr 饱和。Heisenberg--Langevin 方程同时耦合 \(a\) 与 \(a^\dagger\)，求逆得到 Bogoliubov 输入输出关系

\[
b_{out}=u b_{in}+v b_{in}^\dagger,\qquad |u|^2-|v|^2=1.
\]

最后一个条件由输出交换子强制，正是放大和压缩的共同量子约束。

### F.2 squeeze 算符、方差和 dB（式 160--163）

定义

\[
S(\xi)=\exp[(\xi^*a^2-\xi a^{\dagger2})/2],\qquad \xi=re^{i\theta}.
\]

对 \(S^\dagger aS\) 关于 \(r\) 求导，得到一对线性微分方程，解为

\[
S^\dagger aS=a\cosh r-e^{i\theta}a^\dagger\sinh r.
\]

代入正交量 \(X_\phi=(ae^{-i\phi}+a^\dagger e^{i\phi})/\sqrt2\)，在真空中得到主轴方差

\[
\Delta X_{\theta/2}^2=\frac12e^{-2r},\qquad
\Delta X_{\theta/2+\pi/2}^2=\frac12e^{2r}. \tag{162--163}
\]

乘积恒为 \(1/4\)，所以理想 squeezed vacuum 是 minimum-uncertainty state。相对真空的 squeezing dB 为

\[
S_{dB}=10\log_{10}(e^{-2r})=-\frac{20r}{\ln10};
\]

anti-squeezing 取相反号。图 33(b) 的曲线可直接由这个公式生成，不需要拟合原图像素。

### F.3 远程 parity 的共同腔拉动（式 164）

两个 qubit 与同一传播/腔模具有相同色散拉动：

\[
H=\hbar\chi(\sigma_z^{(1)}+\sigma_z^{(2)})a^\dagger a. \tag{164}
\]

奇 parity 状态 \(|ge\rangle,|eg\rangle\) 满足 \(\sigma_z^{(1)}+\sigma_z^{(2)}=0\)，而偶 parity 状态产生 \(\pm2\chi\) 拉动。若测量链只区分“零拉动”和“非零拉动”而不区分偶子空间内部的正负，就获得 parity 信息而不泄露该子空间中的逻辑振幅。

## G. 附录 A--C：三条推导闭环

### G.1 附录 A：电容矩阵的 Legendre 变换

将 transmon 节点和 LC 节点写成向量 \(\vec{\Phi}\)，二次动能为

\[
L_C=\tfrac12\dot{\vec{\Phi}}^{T}C\dot{\vec{\Phi}}
+\mathbf q_g^T\dot{\vec{\Phi}}.
\]

共轭电荷 \(\mathbf Q=C\dot{\vec{\Phi}}+\mathbf q_g\)，故

\[
H_C=\tfrac12(\mathbf Q-\mathbf q_g)^TC^{-1}(\mathbf Q-\mathbf q_g).
\]

对小 \(C_g\) 展开 \(C^{-1}\)，交叉项正比 \(Q_AQ_B\)，量子化后成为第三章式 (29)--(34) 的电荷--电压耦合。令 \(C_g=0\) 时矩阵对角且两子系统能量均为正，是校勘 arXiv 式 (29) 的独立依据。

### G.2 附录 B：BCH、SW 与 normal-mode 旋转

任意时变幺正框架满足

\[
H_U=U^\dagger HU-i\hbar U^\dagger\dot U. \tag{B1}
\]

对 \(U=e^{-S}\) 使用 BCH：

\[
e^SHe^{-S}=H+[S,H]+\tfrac12[S,[S,H]]+\cdots. \tag{B2}
\]

设 \(H=H_0+V\)，取 \([H_0,S^{(1)}]=-V\) 消去一阶非对角项，则二阶剩余

\[
H_{eff}=H_0+\frac12[S^{(1)},V]+O(V^3).
\]

这统一生成式 (40)--(44) 的色散位移和式 (136) 的总线交换。对两个线性 bosonic 模，生成元 \(a^\dagger b-ab^\dagger\) 是保持总激发数的 SU(2) 旋转；取 \(\tan2\Lambda=2g/\Delta\) 可精确对角化二次矩阵，再把 Josephson 四次项投影到 dressed modes，得到 self-/cross-Kerr。

### G.3 附录 C：半无限传输线的边界积分

带 \(\theta(x)\) 的半线 Hamiltonian 给波动方程。对 \(x=0\) 的微小邻域积分，空间二阶导数转成边界导数，也就是线电流；与耦合电容电流相等：

\[
\frac{V_{out}-V_{in}}{Z_{tml}}=\frac{C_\kappa}{C_r}\dot Q_r.
\]

把行波模代入并在 \(\omega_r\) 周围作窄带近似，得到

\[
b_{out}-b_{in}=\sqrt\kappa a,
\qquad \kappa=Z_{tml}C_\kappa^2\omega_r^2/C_r.
\]

再形式积分浴模，用

\[
\int d\omega e^{-i(\omega-\omega_r)(t-t')}=2\pi\delta(t-t')
\]

得到 \(-\kappa a/2\) 与输入噪声，从而闭合到式 (75)。数值端使用与能流守恒一致的端口相位；所有可测反射率与论文等价。

## 11. 全篇近似层级与失效条件

| 近似 | 小参数/条件 | 失效信号 | 应回退到 |
| --- | --- | --- | --- |
| transmon 四阶展开 | \(E_J/E_C\gg1\)，相位涨落小 | 高能级或强驱动 | 完整余弦的电荷基对角化 |
| 单模近似 | 一个模最接近 qubit | 多模 Purcell、相邻模参与 | 黑盒量子化或多模模型 |
| 系统内 RWA | \(g\ll\omega_r,\omega_q\) | Bloch--Siegert、超强耦合 | 完整量子 Rabi/Duffing 模型 |
| SW 色散展开 | \(g\sqrt n\) 远小于所有虚跃迁分母 | \(n\sim n_{crit}\)、\(\Delta\sim j\alpha_q\) | 完整矩阵对角化 |
| 黑盒四阶/RWA | \(\varphi_m\ll1\)，模间非简并 | 强非线性或模式近简并 | 更高阶 Josephson 展开/全电路 |
| Born | 系统--浴弱耦合、相关可忽略 | 强耦合回馈 | 非微扰开放系统方法 |
| Markov | 浴相关时间远短于系统时间 | 结构化阻抗、时延 | 频率依赖自能/记忆核 |
| 浴 RWA/窄带 | \(\lambda\ll\omega_r\)，带宽窄 | 超强耗散、宽带响应 | 式 (66) 的非 RWA 模型 |
| 弱驱动 Maxwell--Bloch | \(\langle\sigma_z\rangle\simeq-1\) | 饱和、多光子峰 | 完整 JC Lindblad 稳态 |
| Gaussian 测量噪声 | 线性链、积分时间足够 | 非 Gaussian 放大器/跳变 | 完整记录分布或轨迹模拟 |
| optical Bloch 稳态 | 二能级、Markov 退相干 | 高能级、强驱动 | 多能级 Lindblad |
| DRAG 一阶消元 | 脉冲包络相对 \(|\alpha_q|\) 缓变 | 极短门、更多能级 | 全多能级最优控制 |
| 线性 DPA | 小信号、泵不耗尽 | 增益饱和、分岔 | 保留 Kerr 与泵模动力学 |
| 截断 Fock Wigner | 截断尾概率可忽略 | 大 \(|\alpha|\) 或大 squeezing | 提高 Hilbert 截断并做收敛扫描 |

## 12. 公式--代码--证据闭环

| 公式组 | 代码入口 | 独立证据 |
| --- | --- | --- |
| 29--34 | `transmon_coupling*`, `duffing_jc_hamiltonian` | 两种 \(g\) 写法机器恒等；正能解耦极限 |
| 35--39 | `jc_block`, `jc_analytic_energies` | 解析谱对独立 2x2 对角化；\(2g\sqrt n\) |
| 40--44 | `transmon_dispersive_*`, `critical_photon_number` | 四能级 Duffing--JC 独立对角化与裸态重叠 |
| 45--51 | `linear_dressed_frequencies`, `bogoliubov_kerrs` | 2x2 线性矩阵；正式版 \(K_a\) 四次展开；\(\chi_{ab}=2\chi\) |
| 52--58 | `black_box_kerr` | 相位涨落式与参与率式交叉计算 |
| 59--62 | `generic_multilevel_shifts` | 三能级非共振实数/有限性检查 |
| 63 | `longitudinal_block`, `longitudinal_analytic_energy` | 完成平方谱与有限矩阵谱 |
| 66--67 | `discretized_bath_hamiltonians` | arXiv 原式与正式修订式的厄米性对照 |
| 68--69 | `lindblad_rhs`, `thermal_oscillator_evolution` | 迹、正性、热弛豫解析解 |
| 70--75 | `passive_one_port_response` | 无损端口 \(|r|=1\) |
| 1--19 | `full_rmp_reproduction` 的 LC/CPW 例程 | 正则对易、等间隔模、被动传输 |
| 20--28 | `transmon_charge_hamiltonian`, `transmon_spectrum` | 电荷截断收敛、\(n_g\) 周期性、Duffing 渐近 |
| 76--86 | 扩展 Lindblad/相干态例程 | \(T_1,T_2\)、Purcell 标度、Poisson 归一化 |
| 87--106 | 放大噪声与 `wigner_fock_state` | 交换子、半量子极限、Wigner 实数/归一化/奇偶 |
| 107--120 | `dispersive_pointer_*` | ODE 对稳态解析解、SNR 最优点、效率边界 |
| 121--125 | `linear_cqed_response` 与 JC Lindblad | 空腔极限、复极点、强耦合 \(2g\) 分裂 |
| 126--128 | `bloch_steady_state`, photon-number spectrum | Bloch 解析式对 Lindblad、Poisson 权重归一 |
| 129--153 | `drag_evolution` 与小矩阵门模型 | 幺正性、泄漏、交换/sideband 共振 |
| 154--157 | bosonic code constructors | Knill--Laflamme Gram 矩阵、parity 与损失空间 |
| 158--164 | squeezed covariance/Wigner | Bogoliubov 对易、方差积、dB 解析式 |
| Appendix A--C | 电容矩阵、SW、端口闭环检查 | 解耦正能、二阶误差标度、通量守恒 |

结论：本复现不是把论文公式翻译成代码，而是让每层有效模型都同时通过来源追踪、解析推导、极限检查和独立数值检查。整篇 30 个公式族已经打开公式门禁；接下来的数值阶段只能实现本节列出的离散化，不得绕过这些近似条件，也不得把缺作者数据的实验面板写成“已复现”。
