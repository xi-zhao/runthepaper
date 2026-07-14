# 复现《Buffer-atom-mediated quantum logic gates with off-resonant modulated driving》

Y. Sun, *Sci. China-Phys. Mech. Astron.* **67**, 120311 (2024). DOI
[10.1007/s11433-024-2478-8](https://doi.org/10.1007/s11433-024-2478-8)。

## 1. 论文主张

在两个 qubit 原子之间放一个**缓冲原子（buffer atom）**，通过 Rydberg 偶极-偶极
（Förster）相互作用、用平滑的离共振调制（ORMD）激光波形，即可实现受控 Z（CZ）门。
缓冲原子制备在 `|1>`、qubit 寄存态 `|0>` 为暗态，于是每个两比特输入都映射到一个独立
的少态扇区。论文报告**单光子（图 3）和双光子（图 4）方案的门误差均 < 1e-4**，并扩展到
多普勒不敏感的双脉冲方案（图 5）、三比特 Toffoli 相位门（图 6），以及对 Rabi 幅度比例
误差的鲁棒性（图 7）。

## 2. 我们复现了什么

凡是论文给出明确系数的部分，全部用**独立重建的三体哈密顿量**复现：

- **图 3（单光子 CZ，两套协议）——完整复现。** 门误差 `6.5e-6`（hybrid）/
  `5.6e-5`（amplitude），条件相位 ≈ ±π。波形、返回布居、累积相位与原图吻合到
  < 0.7% RMS。重建的三体哈密顿量与论文 Morris–Shore 约化式 eq.(a4) 的逐字转写
  做了交叉验证（一致到 < 1e-8）。
- **图 4（双光子 CZ）。** 建立 eq.(a5)/(a6) 的完整三能级阶梯模型（`|1>,|e>,|r>`）。
  hybrid 协议布居吻合到 < 0.4% RMS。诚实说明：全模型门误差为 `1.3e-3`，高于论文的
  < 1e-4（见 §6）。
- **图 5（多普勒不敏感双脉冲）。** 单个脉冲给 π/2，双脉冲合成完整 CZ（条件相位
  `0.99988π`）。第二个脉冲把多普勒频移符号翻转后，门末端的多普勒相位偏差被压制
  **~2600 倍（|00>）到 ~32000 倍（|11>）**——即论文的一阶抵消。
- **图 7（鲁棒性）。** 在 ±1% 缓冲/qubit 幅度比例上的二维门误差色标图，重现了论文的
  结构（主对角暗谷、反对角亮角）及"需要 ~1% 控制精度"的结论。

## 3. 原图 vs 复现

左列 = 论文图的**最小引用**（Y. Sun, Sci. China-Phys. Mech. Astron. **67**, 120311
(2024), [DOI](https://doi.org/10.1007/s11433-024-2478-8)）；右列 = 本案例独立生成。
这些面板验证的是**物理结构与关键数值特征**，**不是**作者数据级或逐点等价。

![Fig. 3 单光子 CZ：论文 vs 复现](../docs/comparisons/fig3_singlephoton_comparison.png)

![Fig. 4 双光子 CZ：论文 vs 复现](../docs/comparisons/fig4_twophoton_comparison.png)

![Fig. 5 双脉冲多普勒：论文 vs 复现](../docs/comparisons/fig5_dualpulse_comparison.png)

![Fig. 7 鲁棒性色标图：论文 vs 复现](../docs/comparisons/fig7_robustness_comparison.png)

## 4. 推导（关键方程）

完整逐步推导（含每个矩阵）见 **[docs/DERIVATION_TRACE.md](../docs/DERIVATION_TRACE.md)**。
核心（$\hbar=1$，旋转坐标系，$\tau=0.25\,\mu s$，$B=2\pi\cdot50$ MHz）：

- **波形** — 每个 Rabi/失谐都是截断 Fourier 级数
  $f(t)=\frac{2\pi}{2N+1}\big(a_0+2\sum_{n\ge1}a_n\cos\frac{2\pi n t}{\tau}\big)$ MHz。
- **单原子驱动** — $H=\frac{\Omega}{2}(|1\rangle\langle r|+\mathrm{h.c.})+\Delta|r\rangle\langle r|$。
- **Förster 相互作用** — 每个相邻（缓冲,qubit）对上 $H_{\rm int}=B(|rr'\rangle\langle qq'|+\mathrm{h.c.})+\delta_q|qq'\rangle\langle qq'|$。
- **扇区** — $|00\rangle$：$2\times2$（a1）；$|01\rangle$：$5\times5$（a3）；$|11\rangle$：$9\times9$ 乘积基（a4），并与论文逐字的 Morris–Shore 6 态形式（$\langle111|H|B_1\rangle=\frac{\sqrt2}{2}\Omega_2$ 等）交叉验证到 $<10^{-8}$。
- **CZ 度量** — 条件相位 $\Phi=\varphi_{11}+\varphi_{00}-2\varphi_{01}$；Pedersen 平均门误差 $1-F_{\rm avg}$，对单比特 $Z$ 优化。
- **双光子（a5/a6）** — 把每个 $|1\rangle\!\leftrightarrow\!|r\rangle$ 换成阶梯 $\frac{\Omega_p}{2}|1\rangle\langle e|+\frac{\Omega_S}{2}|e\rangle\langle r|+\mathrm{h.c.}+\Delta_0|e\rangle\langle e|+\delta|r\rangle\langle r|$，$\Delta_0=2\pi\cdot5$ GHz。
- **双脉冲** — 两个脉冲 $\pm kv$ 符号翻转，$\varphi(+kv)+\varphi(-kv)=2\varphi(0)+\mathcal{O}(v^2)$：一阶多普勒抵消。

每个扇区用 SciPy `DOP853` 积分 $i\dot\psi=H(t)\psi$（模守恒 ~1e-14）。复现是**自证伪**的：
错误的哈密顿量不可能用论文自己的系数凑出 < 1e-4 的门误差。

## 5. 如何运行

见 [../code/README.md](../code/README.md)。案例根目录下：

```bash
python code/scripts/run_fig3.py
python code/scripts/run_fig4.py
python code/scripts/run_fig5.py
python code/scripts/run_fig7.py
python -m pytest code/tests/ -q
```

全部在笔记本 CPU 上数秒到几分钟完成，无需 GPU 或集群。

## 6. 复现边界——请务必阅读

- 我们得到的**双光子**门误差（`1.3e-3` hybrid、`3.7e-3` amplitude）是**忠实的完整
  三能级模型**在论文波形下的诚实值。我们验证了绝热消除的有效模型更差（`1.9e-2`），
  所以全模型才是正确选择；残差最可能来自论文在约化/有效模型里优化其波形。布居与相位
  （图的内容）仍然吻合。
- **图 7** 角点峰值比论文色标上限低约 25%。
- **图 6（Toffoli）** 未复现：多 qubit 缓冲几何未给出，星形几何残留 11% 泄漏。
- **图 a6–a8** 不可复现：没有给系数。
- 我们不再分发论文 PDF、原始图或数字化源数据。视觉吻合不等于作者数据级等价。
