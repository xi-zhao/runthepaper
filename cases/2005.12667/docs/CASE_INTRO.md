# Circuit Quantum Electrodynamics - 整篇公式优先复现

## 一句话结果

本案例覆盖 arXiv:2005.12667 / RMP 93, 025005 正文 Eq. (1)-(164) 与附录 A-C：30 个公式族通过门禁，18 个独立数值/表格目标全部通过，24 个测试通过，综合相似度为 **90.28/100**。

## 核心模型

整篇综述可以压缩成一条连续模型链：

$$
\text{电路自由度}
\to\text{transmon 与谐振模式}
\to\text{JC / dispersive / Kerr}
\to\text{开放端口与测量}
\to\text{耦合区、控制与玻色编码}
\to\text{参量量子光学}.
$$

每次近似都在公式卡中声明小参数和失效条件，每个数值图都先生成 CSV，再由解析极限、守恒律或独立对角化验收。

## 证据边界

可由公开公式和参数定义的理论内容已经执行。Fig. 4(b-e) 的 COMSOL 场模，以及 Figs. 21、28、32 的实验 panel 缺作者级工程或原始数据，保持显式 blocker；理论重算不被标成实验复现。

详细入口：`DERIVATION_TRACE.md`、`TARGET_LEDGER.md`、`REPRODUCTION_REPORT.md` 与 `output/pdf/circuit-qed-rmp-full-reproduction.zh-CN.pdf`。
