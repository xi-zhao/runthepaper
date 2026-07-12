# 给新入学研究生的复现笔记：非厄米 SSH 模型为什么需要非 Bloch 体边对应

面向对象：物理学新入学研究生

这份笔记先讲物理，再讲数值，最后才讲图像验收。读的时候不要先看像素，也不要先看某条曲线像不像；先问一个更基本的问题：我们算出来的对象是不是论文里真正要讨论的物理对象。

这篇文章的核心不是把几张图描出来，而是说明在非厄米系统里，普通 Bloch 体边对应会失效；要恢复体边对应，必须把 bulk 从单位圆上的 Bloch 波改成开边界条件下的非 Bloch 波。

## 1. 这篇文章到底在问什么

### 一句话版本

普通 Hermitian SSH 模型里，我们习惯用周期边界的 Bloch Hamiltonian 来判断开链有没有边界态。但这篇非厄米 SSH 模型里，周期边界和开边界看到的谱可以完全不一样，所以原来的 Bloch 体边对应不再可靠。

### 为什么这很反直觉

在 Hermitian 体系里，bulk 态通常是延展的，边界只影响边缘。可是在非厄米体系里，左右 hopping 不对称，很多本来应该在 bulk 里的本征态会一起堆到边界附近，这就是 non-Hermitian skin effect。这样一来，周期边界下的 bulk 波函数已经不是开链 bulk 态的正确极限。

### 这篇文章的解决办法

把 Bloch 因子 exp(ik) 换成更一般的复数 beta。beta 的模长不一定等于 1，它可以描述波函数沿链方向指数衰减或增长。真正的 bulk 不再生活在单位圆上，而是生活在一条叫广义布里渊区的复平面闭合曲线上。


## 2. 先备知识

### Bloch 体边对应

Bloch 体边对应说的是：用周期边界算 bulk 的拓扑不变量，就能预测开边界下会不会出现边界态。这里的关键假设是周期边界 bulk 态和开边界 bulk 态描述的是同一种物理。非厄米 skin effect 正是破坏了这个假设。

### 开边界和周期边界

周期边界把链首尾接起来，动量 k 是好量子数；开边界把链切开，真正要对角化的是有限长实空间 Hamiltonian。非厄米模型里，这两件事不能随便互换。

### 相似变换的直觉

当左右 hopping 不一样时，可以用一个随格点指数变化的相似变换，把不对称 hopping 映射成一个有效的对称 SSH 问题。这个变换不改变能谱，但会告诉我们开链态天然带有指数包络，所以 beta 的模长一般不是 1。

### 广义布里渊区

普通 Bloch 理论把 beta 固定在单位圆 beta = exp(ik)。非 Bloch 理论让 beta = r exp(ik)，其中 r 由开边界条件决定。所有这些 beta 构成的闭合曲线就是广义布里渊区。

### winding number

SSH 类模型的拓扑不变量可以看作一个复函数绕原点转了几圈。这里要强调：在非厄米开链问题中，绕数必须沿广义布里渊区算，而不是沿单位圆算。


## 3. 公式推导

### 推导 1：从 Pauli 矩阵形式得到 off-diagonal Bloch Hamiltonian

论文先给出 H(k) = d_x sigma_x + (d_y + i gamma/2) sigma_y。这里 gamma 是非厄米性来源，它让上下两个 off-diagonal 元素不再互为复共轭。

推导步骤：

1. 代入 sigma_x = [[0, 1], [1, 0]] 和 sigma_y = [[0, -i], [i, 0]]。
2. 上右矩阵元是 d_x - i(d_y + i gamma/2) = d_x - i d_y + gamma/2。
3. 下左矩阵元是 d_x + i(d_y + i gamma/2) = d_x + i d_y - gamma/2。
4. 在 t3 = 0 时，d_x - i d_y = t1 + t2 exp(-ik)，d_x + i d_y = t1 + t2 exp(+ik)。

```text
H(k) = [[0, d_x - i(d_y + i gamma/2)], [d_x + i(d_y + i gamma/2), 0]]
```

```text
H(k) = [[0, t1 + gamma/2 + t2 exp(-ik)], [t1 - gamma/2 + t2 exp(+ik), 0]]
```

### 推导 2：从 Bloch Hamiltonian 得到开链实空间方程

从 Bloch 形式回到实空间时，exp(+ik) 和 exp(-ik) 不再是相位因子，而是相邻 unit cell 之间的 hopping。开边界的关键是不要把链首和链尾接起来。

推导步骤：

1. 上右元 t1 + gamma/2 是同一个 unit cell 内 B_n 到 A_n 的 hopping。
2. 上右元 t2 exp(-ik) 对应 B_{n-1} 到 A_n 的 hopping。
3. 下左元 t1 - gamma/2 是同一个 unit cell 内 A_n 到 B_n 的 hopping。
4. 下左元 t2 exp(+ik) 对应 A_{n+1} 到 B_n 的 hopping。
5. 把这四个 hopping 写进 Schrödinger 方程，就得到开链 bulk 方程。

```text
t2 psi_{n-1,B} + (t1 + gamma/2) psi_{n,B} = E psi_{n,A}
```

```text
(t1 - gamma/2) psi_{n,A} + t2 psi_{n+1,A} = E psi_{n,B}
```

### 推导 3：为什么开边界转变点不是 Bloch gap closing

周期边界的 exceptional point 只告诉我们单位圆上的 Bloch 谱在哪里闭合；但开链谱要用开边界 Hamiltonian。对 t3 = 0，开链问题可以用一个对角相似变换化成有效 SSH 模型。

推导步骤：

1. 做随格点指数变化的相似变换 S，使左右不对称的胞内 hopping 变成同一个有效幅度。
2. 选择 r = sqrt(|(t1 - gamma/2) / (t1 + gamma/2)|)。
3. 相似变换后，有效胞内 hopping 满足 bar t1 = sqrt((t1 - gamma/2)(t1 + gamma/2))，胞间 hopping 仍为 bar t2 = t2。
4. SSH 模型的拓扑转变条件是 bar t1 = bar t2。
5. 代回去得到 (t1 - gamma/2)(t1 + gamma/2) = t2^2，因此 t1 = +/-sqrt(t2^2 + (gamma/2)^2)。

```text
r = sqrt(|(t1 - gamma/2) / (t1 + gamma/2)|)
```

```text
bar t1 = sqrt((t1 - gamma/2)(t1 + gamma/2)),  bar t2 = t2
```

```text
(t1 - gamma/2)(t1 + gamma/2) = t2^2
```

```text
t1 = +/- sqrt(t2^2 + (gamma/2)^2)
```

### 推导 4：beta ansatz 和广义布里渊区

非 Bloch 理论的核心是把 exp(ik) 放宽成 beta。beta 的相位给出振荡，模长给出沿链方向的指数包络。开链 bulk 态不是单位圆上的平面波，而是 beta 曲线上的指数波。

推导步骤：

1. 设 (phi_{n,A}, phi_{n,B}) = beta^n (phi_A, phi_B)。
2. 代入开链 bulk 方程，得到两个线性方程。
3. 消去 phi_A 和 phi_B，得到 [(t1 - gamma/2) + t2 beta][(t1 + gamma/2) + t2 beta^{-1}] = E^2。
4. 乘以 beta 后得到 beta 的二次方程。设两根为 beta_1 和 beta_2。
5. 由二次方程根的乘积得到 beta_1 beta_2 = (t1 - gamma/2) / (t1 + gamma/2)。
6. 长开链 bulk 态要求 |beta_1| = |beta_2|，因此 |beta| = sqrt(|(t1 - gamma/2)/(t1 + gamma/2)|)。这条圆就是 t3 = 0 的广义布里渊区。

```text
(phi_{n,A}, phi_{n,B}) = beta^n (phi_A, phi_B)
```

```text
[(t1 + gamma/2) + t2 beta^{-1}] phi_B = E phi_A
```

```text
[(t1 - gamma/2) + t2 beta] phi_A = E phi_B
```

```text
[(t1 - gamma/2) + t2 beta][(t1 + gamma/2) + t2 beta^{-1}] = E^2
```

```text
beta_1 beta_2 = (t1 - gamma/2) / (t1 + gamma/2)
```

```text
|beta| = sqrt(|(t1 - gamma/2) / (t1 + gamma/2)|)
```

### 推导 5：非 Bloch winding number

拓扑不变量仍然是绕数，但积分路径必须换成广义布里渊区 C_beta。为了数值稳定，我们不直接追踪本征矢相位，而是用 off-diagonal 元素 a(beta)、b(beta) 的 winding 差。

推导步骤：

1. 把 H(beta) 写成 [[0, b(beta)], [a(beta), 0]]。
2. 其中 a(beta) = t1 - gamma/2 + beta t2，b(beta) = t1 + gamma/2 + beta^{-1} t2。
3. 论文里的 Q(beta) 可以理解为 flattened Hamiltonian，二能带 chiral 情况下 q(beta) = -b(beta)/E(beta)。
4. 绕数 W = (i / 2 pi) integral q^{-1} dq。
5. 由于 q = -sqrt(b/a)，可避开平方根分支，直接算 W = (wind[a(beta)] - wind[b(beta)]) / 2。
6. 在拓扑区间内 W = 1，区间外 W = 0；这个 W 对应开链零模数。

```text
H(beta) = [[0, b(beta)], [a(beta), 0]]
```

```text
a(beta) = t1 - gamma/2 + beta t2
```

```text
b(beta) = t1 + gamma/2 + beta^{-1} t2
```

```text
W = (i / 2 pi) integral_{C_beta} q^{-1} dq
```

```text
W = (wind[a(beta)] - wind[b(beta)]) / 2
```

### 推导 6：t3 不为零时为什么变成四次 beta 方程

t3 打开后，左右两个 off-diagonal 元素都同时含 beta 和 beta^{-1}。所以能量方程乘以 beta^2 后不再是二次方程，而是四次方程。Fig. 5 的 middle beta roots 和非圆形 GBZ 都来自这一步。

推导步骤：

1. 非零 t3 时，上右元变成 t2 beta^{-1} + (t1 + gamma/2) + t3 beta。
2. 下左元变成 t3 beta^{-1} + (t1 - gamma/2) + t2 beta。
3. 两者相乘等于 E^2。
4. 为了去掉 beta^{-1}，两边乘以 beta^2。
5. 展开后得到 beta 的四次方程。开链 bulk 态取中间两根 beta 的模长相等作为 GBZ 条件。

```text
E^2 = [t2 beta^{-1} + (t1 + gamma/2) + t3 beta][t3 beta^{-1} + (t1 - gamma/2) + t2 beta]
```

```text
t2 t3 beta^4 + [(t1-gamma/2)t3 + (t1+gamma/2)t2] beta^3 + [t2^2 + (t1-gamma/2)(t1+gamma/2) + t3^2 - E^2] beta^2 + [(t1+gamma/2)t3 + (t1-gamma/2)t2] beta + t2 t3 = 0
```

```text
|beta_2| = |beta_3|  (middle-root GBZ condition after sorting roots by |beta|)
```


## 4. 数值怎么做

### 我们真正算了什么

- Fig. 2：构造开边界实空间 Hamiltonian，扫 t1，计算 |E|、Re(E)、Im(E)。
- Fig. 3：计算 beta 根、广义布里渊区和右本征矢 profile，确认 skin effect。
- Fig. 4：沿广义布里渊区计算整数 winding number。
- Fig. 5：在 t3 不为零时解四次 beta 方程，把 |E| 谱、winding、middle beta roots 和非圆形广义布里渊区分开计算。

### 公式到图像的对应关系

这张对照表是读图入口：先找到每张图依赖的公式，再看对应数值对象，最后才看 digitized curve 或 pixel layout 是否对齐。

- Fig. 2：EQC001 + EQC003 + EQC005 -> 开边界谱、零模区间和 Bloch exceptional point 的错位。
- Fig. 3：EQC006 + EQC007 -> beta 根、广义布里渊区 C_beta 和 skin profile。
- Fig. 4：EQC009 -> 沿 C_beta 计算非 Bloch winding，并把结果画成整数台阶。
- Fig. 5：EQC001 + EQC009 + EQC010 -> 非零 t3 的 |E| 谱、winding、middle beta roots 和非圆形 GBZ。

### 为什么不能只照着图描线

图里的每条线都有物理身份。谱线、零模线、winding 台阶、beta 根曲线、GBZ 轮廓不能因为看起来近就连在一起。复现时每条线必须来自对应的数值对象，并按对应的物理参数顺序连接。


## 5. 每张图应该怎么看

### Fig. 2：开链谱告诉你 Bloch 预测错在哪里

这张图要看的不是线密不密，而是零模区域的边界。真正的开边界转变出现在 |t1| = sqrt(t2^2 + (gamma/2)^2) 附近，而不是普通 Bloch exceptional point 给出的那些位置。

灰色谱线必须按同一条本征值分支随 t1 的变化来连；红色零模线是边界态，不能和 bulk branch 因为视觉上靠近就连起来。

### Fig. 3：广义布里渊区和 skin effect 是同一件事的两面

beta 根告诉我们开链 bulk 态应该选哪条复平面曲线；C_beta 是这条曲线本身；profile 图说明右本征态确实向边界堆积。这里 profile 必须来自开链右本征矢，不能从原图的像素曲线倒推出来。

### Fig. 4：winding 是整数台阶，不是平滑曲线

winding number 表示复函数绕原点几圈。它应该是整数平台，跳变位置对应拓扑相变。画图时不能把这些点平滑插值成连续曲线。

### Fig. 5：t3 不为零时，不能再用 t3 = 0 的圆形 GBZ

t3 打开后 beta 方程变成四次方程。可见 |E| 谱线来自开链 Hamiltonian；winding plateau 来自非 Bloch winding；middle beta roots 决定相变和 GBZ；C_beta 是非圆形轮廓。这四件事相关，但不是同一个数值对象。当前灰色谱和 C_beta 能量输入均使用论文的 L=100，并以 35 位高精度求解，避免双精度非正规矩阵产生病态伪线。


## 6. 复现到什么程度

### 这次复现声称什么

- 声称：公式链条、数值对象和图像中的主要物理结构是一致的。
- 声称：digitized curve 和 pixel layout 可以作为验收，说明我们算出的曲线落在原文图像结构上。
- 声称：Fig. 5 的灰色开链谱和 C_beta 使用论文的 L=100，并由 35 位高精度独立数值生成。
- 不声称：我们拿到了作者原始作图数据。
- 不声称：这是 100% 作者数据等价复现。

### 为什么还要做像素级对比

像素级对比不是物理证明本身，而是验收手段。物理证明来自公式、边界条件、数值对象和拓扑量；图像对齐说明这些对象画出来以后确实对应原文的主要数值图。

- 注意：不要先看像素再反推物理；应该先把物理对象算对，再用像素和 digitized curve 检查画出来是否对齐。


- validator 状态：`passed`
- 作者原始作图数据等价：不声明
- 精确作图数据复现：不声明

## 附录：机器可检查证据

这一节是给复查和自动验收看的。正文里讲物理，这里保留对象 ID、证据 ID 和连接规则，方便追溯。

### 数值对象索引

- `OBJ_FIG2_OBC_SPECTRUM`：Open-chain complex eigenvalue spectrum and zero modes.；来源 `independent_numerics`。
- `OBJ_FIG3_BETA_ROOTS`：Root moduli that determine the non-Bloch bulk branch.；来源 `independent_numerics`。
- `OBJ_FIG3_C_BETA`：Generalized Brillouin-zone contour selected by |beta1| = |beta2|.；来源 `independent_numerics`。
- `OBJ_FIG3_SKIN_PROFILES`：Site-resolved right eigenvector profiles showing non-Hermitian skin localization.；来源 `independent_numerics`。
- `OBJ_FIG4_WINDING`：Integer winding of q(beta) along C_beta.；来源 `analytic_reference`。
- `OBJ_FIG5_OBC_ABS_SPECTRUM`：Ordered open-chain absolute energy levels in the nonzero-t3 model.；来源 `independent_numerics`。
- `OBJ_FIG5_WINDING`：Integer non-Bloch winding plateau for the nonzero-t3 model.；来源 `independent_numerics`。
- `OBJ_FIG5_MIDDLE_BETA_ROOTS`：Middle beta roots whose equal modulus condition defines the nonzero-t3 GBZ.；来源 `independent_numerics`。
- `OBJ_FIG5_C_BETA`：Non-circular generalized Brillouin zone for nonzero t3.；来源 `independent_numerics`。

### 图中线条的连接规则

- `FIG002`：阶段 `final_reproduction`；参数匹配 `paper_exact`。
  - `FIG2_BRANCHES`：连 `connect_within_branch_id_in_t1_order`；禁止 `connect_by_band_index`。
  - `FIG2_ZERO_MODES`：连 `connect_zero_mode_pair_in_t1_order`；禁止 `connect_to_bulk_branch_by_visual_nearest_neighbor`。
- `FIG003`：阶段 `final_reproduction`；参数匹配 `paper_exact`。
  - `FIG3_BETA_ROOTS`：连 `connect_within_root_label`；禁止 `connect_by_pixel_nearest_neighbor`。
  - `FIG3_C_BETA`：连 `connect_in_theta_order`；禁止 `connect_by_raster_path_order`。
  - `FIG3_SKIN_PROFILES`：连 `connect_profile_id_by_site_index`；禁止 `infer_profile_from_zero_mode_digitized_curve`。
- `FIG004`：阶段 `final_reproduction`；参数匹配 `paper_exact`。
  - `FIG4_WINDING_STEP`：连 `render_as_integer_step_vertices`；禁止 `smooth_interpolation`。
- `FIG005`：阶段 `final_reproduction`；参数匹配 `paper_exact`。
  - `FIG5_SPECTRUM_LEVELS`：连 `connect_ordered_abs_energy_level_in_t1_order`；禁止 `claim_full_eigenvector_continuation`。
  - `FIG5_WINDING_STEP`：连 `render_as_integer_step_vertices`；禁止 `smooth_interpolation`。
  - `FIG5_C_BETA`：连 `connect_middle_pair_locus_in_angle_order`；禁止 `reuse_circular_t3_zero_gbz`。

### 验收证据索引

- `VAL_FIG2_DIGITIZED`：`digitized_source_reference`，作用 `alignment_validation_only`，对象 `OBJ_FIG2_OBC_SPECTRUM`，上限 `not_author_data_equivalence`。
- `VAL_FIG3_DIGITIZED`：`digitized_source_reference`，作用 `alignment_validation_only`，对象 `OBJ_FIG3_BETA_ROOTS`，上限 `not_author_data_equivalence`。
- `VAL_FIG4_DIGITIZED`：`digitized_source_reference`，作用 `alignment_validation_only`，对象 `OBJ_FIG4_WINDING`，上限 `not_author_data_equivalence`。
- `VAL_FIG5_SPECTRUM_DIGITIZED`：`digitized_source_reference`，作用 `alignment_validation_only`，对象 `OBJ_FIG5_OBC_ABS_SPECTRUM`，上限 `not_author_data_equivalence`。
- `VAL_FIG5_WINDING_DIGITIZED`：`digitized_source_reference`，作用 `alignment_validation_only`，对象 `OBJ_FIG5_WINDING`，上限 `not_author_data_equivalence`。
- `VAL_FIG5_ROOT_ORDERING`：`independent_numerics`，作用 `internal_consistency_validation`，对象 `OBJ_FIG5_MIDDLE_BETA_ROOTS`，上限 `internal_consistency_only`。
- `VAL_FIG5_CBETA_DIGITIZED`：`digitized_source_reference`，作用 `alignment_validation_only`，对象 `OBJ_FIG5_C_BETA`，上限 `not_author_data_equivalence`。
- `VAL_PXT_FIG2_ABS`：`digitized_source_reference`，作用 `pixel_layout_validation_only`，对象 `OBJ_FIG2_OBC_SPECTRUM`，上限 `layout_validation_only`。
- `VAL_PXT_FIG2_REAL`：`digitized_source_reference`，作用 `pixel_layout_validation_only`，对象 `OBJ_FIG2_OBC_SPECTRUM`，上限 `layout_validation_only`。
- `VAL_PXT_FIG2_IMAG`：`digitized_source_reference`，作用 `pixel_layout_validation_only`，对象 `OBJ_FIG2_OBC_SPECTRUM`，上限 `layout_validation_only`。
- `VAL_PXT_FIG3_ABSBETA`：`digitized_source_reference`，作用 `pixel_layout_validation_only`，对象 `OBJ_FIG3_BETA_ROOTS`，上限 `layout_validation_only`。
- `VAL_PXT_FIG3_CBETA`：`digitized_source_reference`，作用 `pixel_layout_validation_only`，对象 `OBJ_FIG3_C_BETA`，上限 `layout_validation_only`。
- `VAL_PXT_FIG3_PROFILE`：`digitized_source_reference`，作用 `pixel_layout_validation_only`，对象 `OBJ_FIG3_SKIN_PROFILES`，上限 `layout_validation_only`。
- `VAL_PXT_FIG4`：`digitized_source_reference`，作用 `pixel_layout_validation_only`，对象 `OBJ_FIG4_WINDING`，上限 `layout_validation_only`。
- `VAL_PXT_FIG5`：`digitized_source_reference`，作用 `pixel_layout_validation_only`，对象 `OBJ_FIG5_OBC_ABS_SPECTRUM`，上限 `layout_validation_only`。

最终校验状态：`passed`
