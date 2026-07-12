# Case Intro: Simulating The Sycamore Quantum Supremacy Circuits

## 一句话结果

我们把这篇论文里的 big-batch 思路跑成了一个可执行 case：先核验公式，再用小规模随机电路复现它最关键的数值特征，包括 Porter-Thomas 分布、post-selection XEB 曲线和条件概率分布。

## 相似度等级

当前等级：**数值特征复现**。

当前相似度分数：**70.0/100**。

这个 case 已经体现了原论文最关键的数值特征：batch 概率近似 Porter-Thomas 分布，完整 batch 的 XEB 接近 0，高概率 post-selection 会提高 XEB，条件概率重新归一化后仍保持同类分布。depth 20 的 post-selection 曲线与 `-log(fraction)` 的平均误差约 `0.0253`，depth 14 的误差约 `0.00233`，说明核心统计形状是对的。

它还不是“完整复现”，因为原论文的主结果是 53 qubit Sycamore 电路上的大规模张量网络收缩；当前本地 case 是 18 qubit 的独立小规模复现。它能证明 Agent 抓住了 big-batch 方法的数值机制，但没有重算论文的 53 qubit 原始概率表。

## 这篇文章在做什么

论文要解决的问题很直接：量子线路的输出空间很大，如果一个一个算 bitstring 概率，代价会非常高。作者提出的方法是固定一部分输出比特，枚举另一部分输出比特，把一次昂贵的张量网络收缩结果反复复用，于是一次得到一大批相关 bitstring 的概率。

在原文的大规模实验中，作者处理的是 53 比特 Sycamore 电路。这个 case 没有宣称在本机重跑 53 比特 GPU 集群实验，而是复现这篇文章真正可验证的数值结构。

## 直观公式

最终输出 bitstring 拆成两部分：

```text
s = (s1, s2)
```

`s1` 固定，`s2` 枚举。于是每个概率是：

```text
P_U(s) = P_U(s1, s2)
```

张量网络被切成 head 和 tail 两部分：

```text
psi(s1, s2) = v_head(s1) dot v_tail(s2)
```

这样 `v_head(s1)` 只需要算一次，就可以给所有 `s2` 复用。

验收时我们主要看：

```text
Np
F_XEB = mean(Np) - 1
P(s2 | s1) = P(s1, s2) / sum_s2 P(s1, s2)
```

## 数值方法

我们实现了一个小规模随机电路模拟器：

- 18 个 qubit；
- 固定 6 个 closed qubit；
- 枚举 12 个 open qubit，所以每轮有 4096 个相关 bitstring；
- 分别模拟 depth 20 和 depth 14；
- 先输出 CSV，再画图，再写 JSON 检查结果。

这个设置可以在本机快速跑完，同时保留论文的核心数值逻辑。

## Fig. 2: 20-cycle 概率分布和 post-selection XEB

原图左边显示 `Np` 服从 Porter-Thomas 分布，右边显示只选择高概率 bitstring 时，XEB 会升高。



我们的复现结果：

![Generated Fig. 2 reproduction](../outputs/figures/fig2_depth20_reproduction.png)

一致性说明：左图的蓝色直方图沿红色指数线下降，说明 batch 概率满足 Porter-Thomas 特征。右图的 XEB 随选择比例增加而下降，100% bitstring 时回到接近 0。检查文件里，完整 batch 的 XEB 是 `0.00494`，和论文中“完整固定子空间接近 0”的特征一致。

## Fig. 5: 14-cycle 概率分布和 post-selection XEB

原图展示的是 14-cycle 情形，结构和 Fig. 2 类似。



我们的复现结果：

![Generated Fig. 5 reproduction](../outputs/figures/fig5_depth14_reproduction.png)

一致性说明：生成图同样给出指数型概率分布和单调下降的 post-selection XEB 曲线。完整 batch 的 XEB 是 `-0.00252`，与论文中 `-0.00687` 同量级，都表达了“完整子空间本身不提高 XEB，但高概率筛选会提高 XEB”这个结论。

## Fig. 6: 条件概率分布

原图显示，把固定子空间内的概率重新归一化成 `P(s2|s1)` 后，条件概率仍然符合 Porter-Thomas 特征。



我们的复现结果：

![Generated conditional probability reproduction](../outputs/figures/fig6_conditional_probability_reproduction.png)

一致性说明：两个深度下，条件概率都已经归一化，直方图也沿红色指数线下降。检查文件确认归一化误差在数值精度内。

## Table II: 方法对比

我们把论文中的方法对比表转成结构化数据，并做了一个简洁的 log-scale 对比图。

![Generated table comparison](../outputs/figures/table2_method_comparison_reproduction.png)

一致性说明：这部分复现的是论文表格里的数值关系，不是重新跑 53 比特大规模收缩。它清楚展示了论文的核心 claim：作者方法一次拿到的 bitstring 数量远高于小 batch 方法，同时报告的时间复杂度低于 Alibaba 方法。

## 当前结论

这个 case 已经完成了论文核心数值特征的本地复现。公式链、概率提取、XEB、条件概率和 Porter-Thomas 检查都能闭环。

还没有完成的是 53 比特 Sycamore 原始全尺寸概率的精确重算。这需要原始电路数据、收缩阶、切片配置和多 GPU 资源。下一步如果要做精确复现，应该把作者释放的概率数据当作验证集，把电路文件当作 benchmark corpus，再逐步替换本地小规模模拟器。

## 还有哪些问题

与原论文之间的差异主要来自规模和数据源：

- 原论文是 53 qubit Sycamore 电路；当前是 18 qubit 随机电路。
- 原论文使用张量网络切分和 GPU 长时间收缩；当前用本地 statevector 小规模模拟来验证同一类概率结构。
- 当前图能体现 Porter-Thomas、post-selection XEB 和条件概率这些数值特征，但不能说明我们已经复现了作者报告的 53 qubit 计算时间和具体 bitstring 概率。
- Table II 的方法对比是论文表格转结构化数据后的核验，不是重新跑所有大规模方法。

没有出现“完全没有物理特征”的情况；本地结果已经清楚展示了论文方法要利用的概率分布特征。

## 推荐算力

如果目标是完整复现 53 qubit 结果，推荐：

- 原始 Sycamore 电路文件、bitstring 列表和作者概率输出作为验证集；
- 多 GPU 环境，至少 A100 级别 GPU，最好有多卡和批处理队列；
- 高内存 CPU/GPU 节点，用于保存 contraction path、切片任务和中间张量；
- 任务组织上按 bitstring batch 或 tensor-network slice 分发，保留可恢复的中间结果。

当前本地机器适合继续做方法验证和小规模统计特征复现，不适合直接重跑 53 qubit 完整实验。
