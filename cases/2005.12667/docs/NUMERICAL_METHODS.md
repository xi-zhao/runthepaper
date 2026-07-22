# Numerical Methods

## 统一约定

除图轴明确标 GHz/MHz 外，代码取 $\hbar=1$ 并使用一致频率单位。所有参数冻结在 `experiments/paper_scope.json` 与 `experiments/full_rmp_scope.json`。没有随机采样，也没有从论文图像反推生成数据。

计算遵循同一接口：公式卡确定模型和适用域，runner 先写 CSV/JSON，再画图，再计算阈值；只有全部阈值通过才更新评分产物。

## Sec. II: 电路与 transmon

- T005: 用分布参数线的 $\omega_n=n\omega_1$ 和被动 Lorentzian response 构造 CPW 谐振峰；验收峰位和整数倍模式关系。
- T006: 在 $n=-N,\ldots,N$ 电荷基中对角化 $4E_C(n-n_g)^2-(E_J/2)(|n\rangle\langle n+1|+h.c.)$，再 Fourier 变换到相位基；验收波函数归一化与非谐性。
- T007: 对三个 $E_J/E_C$ 和 161 个 $n_g$ 点重复对角化；验收周期性与大 $E_J/E_C$ 下色散指数抑制。

## Sec. III-IV: JC、色散与开放系统

- T001: 按守恒总激发数拆成精确 $2\times2$ JC blocks，用 `eigvalsh` 对照 Eq. (38) 与 $2g\sqrt n$。
- T002: 构造 40 维四能级 Duffing-JC Hamiltonian，以最大裸态重叠和 Hungarian assignment 标记 dressed states，对照二阶 Schrieffer-Wolff 能量；同时输出 $|g/\Delta|$ 与 $n_{\rm crit}$。
- T003: 以小矩阵和直接代数检查耦合恒等、Bogoliubov 频率、Kerr 组合因子、black-box participation 与纵向耦合完成平方。
- T004: 把 16 维密度矩阵展平为 256 维复向量，用 adaptive `solve_ivp` 积分 thermal Lindblad 方程，`rtol=2e-10`、`atol=2e-12`；对照解析 $\langle n(t)\rangle$。系统-浴有限维张量积只用于厄米性审计；输入输出以全频段 $|r|=1$ 验收。

## Sec. V: 放大器与读出

- 相位保持放大器直接检查 Bogoliubov 输入输出变换的对易关系与高增益半量子附加噪声。
- T008: 用线性一阶 ODE 的闭式解计算两个 qubit-conditioned coherent pointer state，数值积分 $|\alpha_e-\alpha_g|^2$ 得有限时间 matched-filter SNR。
- T009: 对稳态腔振幅 $\alpha_{g/e}=-i\epsilon/[\kappa/2+i(\Delta\mp\chi)]$ 扫频，验收幅度对称与相位分离。

## Sec. VI: 耦合区与谱学

- T010: 一激发子空间使用 $2\times2$ 非厄米振幅生成元处理损耗；稳态弱驱动谱使用线性 cQED susceptibility；热内峰采用几何 thermal weights 加权 JC transitions。
- T011-T012: 用同一线性 response kernel 生成 vacuum-Rabi cuts 和二维 avoided crossing；共振劈裂必须接近 $2g$。
- T013: 使用稳态 optical Bloch 解析式，扫描 detuning 与 Rabi frequency；对照解析 power-broadened linewidth 和 $1/2$ 饱和极限。
- T014: 用 Poisson photon weights 叠加 number-conditioned qubit lines，每条线的 measurement-induced dephasing 随 $n$ 更新；验收峰间距 $2\chi$。
- T015: 在固定总激发数的 Duffing-JC blocks 中精确对角化，借最大重叠追踪 bare-transmon branch；避免不必要的 cavity tensor cutoff，并检查高光子数向裸腔频率回归。

## Sec. VII: DRAG 与玻色编码

- T016: 三能级 Duffing 模型中用 `solve_ivp` 积分 Gaussian $\pi$ pulse。DRAG 分支加入 $\Omega_y=\dot\Omega_x/\alpha$ 和一阶 AC-Stark 补偿，验收目标态误差、泄漏和范数。
- T017: 在有限 Fock 基中直接构造 binomial logical states，计算 $PIP$、$P\hat nP$、$P\hat aP$ 和损失态 Gram matrix。
- T018: coherent-state Fock coefficients 组成二分量/四分量 cat state；Wigner 函数使用广义 Laguerre 多项式的纯态解析 kernel，验收积分、宇称与负性。

## Sec. VIII: Wigner 与压缩

- T019: 对有限 Fock superposition 使用同一解析 Wigner kernel；161 乘 161 网格覆盖五个相位，验收每幅积分。
- T020: squeezed vacuum 由旋转协方差矩阵闭式生成二维 Wigner；相位方差使用 $V(\phi)=\frac12[e^{2r}\sin^2(\phi-\theta/2)+e^{-2r}\cos^2(\phi-\theta/2)]$，对照最小压缩 dB。

## 误差控制与复杂度

| 数值对象 | 主要误差源 | 显式控制 |
| --- | --- | --- |
| transmon | 电荷截断 | $N=24$，周期性与色散比检查 |
| Duffing-JC | 能级截断与错误标态 | 固定激发 block + 最大重叠 assignment |
| Lindblad | Fock cutoff 与 ODE tolerance | dimension 16 + 解析平均数 + CPTP 不变量 |
| DRAG | ODE tolerance 与三能级近似 | 范数误差、泄漏和门时扫描 |
| Wigner | Fock cutoff 与有限网格 | 积分、宇称、负性、最小不确定度 |

完整全篇 runner 当前约 25 秒，其中大振幅 cat Wigner 占主要时间；不需要 GPU、分布式计算或 checkpoint。
