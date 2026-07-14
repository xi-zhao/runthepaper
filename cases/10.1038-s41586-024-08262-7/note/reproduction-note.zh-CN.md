# 超越费米子与玻色子的粒子交换统计：复现讲义

## 论文信息

Zhiyuan Wang 与 Kaden R. A. Hazzard，*Particle exchange statistics beyond
fermions and bosons*，Nature **637**, 314–318 (2025)，DOI
`10.1038/s41586-024-08262-7`；预印本为 arXiv:2308.05203。

这篇论文问了一个很基础的问题：三维及更高维中，量子粒子的交换统计是否只能是费米或玻色？作者构造了与二者物理上不等价的 **paraparticles（仲统计粒子）**，并给出了广义排斥统计、自由粒子热力学、二次量子化以及局域可解自旋模型。

## 这次复现了什么

公开 case 聚焦论文中可直接数值复现的主图，并增加一项独立物理验证：

1. 从论文给出的单模配分函数重新计算费米子、玻色子和三个仲统计例子的简并度序列 `d_n`。
2. 用同一组闭式表达式计算热平均占据数 `<n>_beta` 随 `beta*epsilon` 的变化。
3. 严格对角化论文的一维可解自旋模型，把完整多体谱与自由仲统计粒子预测逐能级比较。

最终图采用图例中的论文参数：Ex.2 `m=2`、Ex.3 `m=2`、Ex.4 `m=3`。这里值得特别记录：正文另有一处写成 `m=5`，与图例不一致；因为复现对象是该图，所以最终结果遵循图例，而不是自行选择更方便的参数。

## 从一个核心对象得到整张图

一个模态中有 `n` 个仲统计粒子时，独立态空间的维数记为 `d_n`。把这些整数装进单模配分函数

```text
z_R(x) = sum_n d_n x^n,    x = exp(-beta*epsilon)
```

即可得到热平均占据数

```text
<n>_beta = x z'_R(x) / z_R(x).
```

因此左图和右图不是两个独立拟合：左图给出 `d_n`，右图由同一个 `z_R` 直接推出。这个结构也是本 case 的核心模型。

论文图例中的五类统计对应：

| 物种 | `z_R(x)` | 单模最高占据 |
| --- | --- | ---: |
| 费米子 | `1+x` | 1 |
| 玻色子 | `1/(1-x)` | 无上限 |
| Ex.2 (`m=2`) | `(1+x)^2` | 2 |
| Ex.3 (`m=2`) | `1+2x` | 1 |
| Ex.4 (`m=3`) | `1+3x+x^2` | 2 |

代码没有描线、数字化或拟合原图。`d_n` 由闭式表达式生成，热力学曲线再由上式计算。`beta*epsilon=0` 时，费米子、Ex.3、Ex.2/Ex.4 的占据数分别为 `1/2`、`2/3`、`1`；所有断言都以 `1e-9` 容差通过。

## 独立数值验证

只把公式画成图还不够。论文同时给出一维局域可解自旋模型，并说明它可以映射为自由仲统计粒子。我们直接构造 `(m+1)^N` 维多体 Hamiltonian，严格对角化后与自由粒子预测

```text
E = sum_{k in S} epsilon_k,    multiplicity = m^|S|
```

逐能级比较。`N=4,5, m=2` 以及 `N=4, m=3` 的完整谱最大偏差约为 `1e-14`，粒子数守恒对易子也在机器精度内为零。这说明图中使用的 `z_R=1+mx` 不只是形式上的母函数，而对应一个真实局域模型的精确自由准粒子谱。

## 运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1038-s41586-024-08262-7/code
python scripts/gen_fig2.py
python scripts/run_ed_validation.py
```

生成数据位于 `../outputs/data/`，复现图位于 `../outputs/figures/`，数值检查位于 `../outputs/checks/`。

## 复现程度与边界

当前状态为 **Complete reproduction**，审计分数 **90/100**。分数表示公开证据的覆盖强度，不表示“90% 的物理正确”，也不是论文之间的排名。

分数停在 90 的原因是作者没有公开作图数据表，Nature 图为栅格图；当前最强参照是论文的闭式公式与独立严格对角化，而不是作者数据的逐点残差。两项物理检查均通过。二维可解 KDH 模型、八体 plaquette 项和编织演示不在本 case 的复现范围内。

更完整的逐步推导见 [`../docs/DERIVATION_WALKTHROUGH.zh-CN.md`](../docs/DERIVATION_WALKTHROUGH.zh-CN.md)，评分依据见 [`../docs/SIMILARITY_SCORECARD.md`](../docs/SIMILARITY_SCORECARD.md)。
