# 案例简介：SABRE 量子比特映射

## 一句话结论

这个案例记录了 RRAgent 如何从论文正文出发，重建 SABRE 量子比特映射算法，并生成可检查的数值结果。整个过程以论文文字、公式、表格和 benchmark 为依据，没有使用作者的代码实现。

目前进展可以分成四类：

- 核心算法机制：一致；
- 小规模论文例子：精确一致；
- 反向遍历和 decay 的关键特征：一致；
- Table II 全表数值：部分一致，还没有达到逐行精确复现。

## 相似度等级

当前等级：**数值特征复现**。

当前相似度分数：**61.71/100**。

这篇 case 已经体现了 SABRE 论文里的核心算法特征：front layer 驱动的 SWAP 搜索、look-ahead cost、reverse traversal 改善初始映射，以及 decay 带来的门数/深度权衡。Fig. 3 的小例子达到了完整一致。

还没有达到“完整复现”的部分是 Table II。Table II 要求对每一行 benchmark 复刻论文里的最优门数，这依赖随机初始映射、tie-breaking、尝试次数和 BKA baseline 等实现细节。我们已经把 Table II 的 26 个 benchmark 用原文表格参数全部跑完，并在 A100 远端机器上把每行随机尝试提高到 1000 次。`g_op` 精确匹配从 6/26 提升到 7/26 后不再继续提升，说明主要差距不是简单加时间，而是缺失的实现元信息。

这个 case 不是“没有体现算法特征”。它已经体现了核心机制，只是全表精确数字还没有达到原文级别。

## 案例文章

- Paper: *Tackling the Qubit Mapping Problem for NISQ-Era Quantum Devices*
- PaperID: `10.1145-3297858.3304023`
- 类型：algorithm / quantum compilation
- 复现目标：聚焦由算法运行得到的数值结果。论文中的背景图、示意图和硬件说明图用于理解算法，不作为复现目标。

## 直观方法推导

这篇文章解决的问题很直接：量子线路里有很多双量子比特门，真实芯片的连接却是稀疏的。两个逻辑量子比特如果被放在不相邻的物理位置上，就需要插入 SWAP，把它们移动到可以直接作用的位置。

我们把论文里的核心步骤整理成下面这条路线：

1. 先把硬件芯片看成一张图。两个物理量子比特之间能直接作用，就在图上连一条边。

2. 计算距离矩阵 `D`。`D[i][j]` 表示物理点 `i` 和 `j` 在芯片图上的最短距离。距离越大，说明两个逻辑量子比特要靠近需要更多 SWAP。

3. 维护当前最急需执行的一批门，也就是 front layer `F`。如果 front layer 里的门已经相邻，就直接执行；如果不相邻，就挑一个 SWAP。

4. 对候选 SWAP 打分。基础直觉是：一个好的 SWAP 应该让 front layer 里的量子比特距离变小。

   ```text
   H_basic = sum D[physical(q1), physical(q2)]
   ```

5. 当前 front layer 只能看到眼前的门，容易做出局部最优的选择。论文加入 look-ahead，把后面快要执行的门也纳入代价函数：

   ```text
   H = average_distance(front_layer)
       + W * average_distance(extended_set)
   ```

6. 门数和线路深度之间存在天然权衡。decay 机制会临时提高最近使用过的物理量子比特的代价，引导算法选择更容易并行的 SWAP：

   ```text
   H_decay = max(decay(q_i), decay(q_j)) * H
   ```

7. 最后，论文用 reverse traversal 改善初始映射：先正向跑一次，再把线路反过来跑一次，反向得到的 final mapping 作为最终正向运行的初始映射。

这些步骤构成了我们实现的数值核心。

## 数值方法

这个案例的数值对象是一套量子线路路由过程。给定原始线路和硬件连接图后，我们记录算法插入了多少 SWAP，生成的线路深度是多少，以及最终线路是否满足硬件相邻约束。

具体做法是：

1. 把 IBM Q20 Tokyo 芯片抽象成 coupling graph，并计算所有物理量子比特之间的最短路距离。

2. 把输入量子线路转成双量子比特门依赖 DAG。每一轮取出当前可以执行或最需要被满足的 front layer。

3. front layer 中已经满足相邻约束的门会直接执行。其余情况只枚举与 front layer 相关的候选 SWAP，将搜索空间控制在可运行范围内。

4. 对每个候选 SWAP 计算 look-ahead cost 和 decay cost，选择代价最低的 SWAP，更新 logical-to-physical mapping。

5. 对 reverse traversal 目标，执行 forward-backward-forward 三次遍历，用反向线路得到更好的初始映射。

6. 对每个目标输出结构化数据：插入 SWAP 数、额外 CNOT-equivalent gate 数、输出深度、是否硬件合法，以及和论文表格中的 `g_ori`、`g_la`、`g_op` 的差异。

7. 每个目标先生成结构化数据和机器检查，再生成展示图。验收依据来自 `../outputs/checks/*.json` 和 `../outputs/data/*.csv`，图片用于直观展示这些结果。

## 原图与复现结果对比

### Target 1: Fig. 3 小线路 SWAP 例子

| 原文中的例子 | Agent 生成的运行轨迹 |
![Reproduced Fig. 3 trace](../outputs/figures/paper_swap_example_trace.png)

**一致性结论：`exact_match`**

这个目标用于检查算法的最小闭环：front layer 无法执行时，Agent 是否能插入正确的 SWAP，并继续完成后续门。

核验结果完全一致：原始双量子比特门数为 6，插入 1 个 SWAP，等价增加 3 个 CNOT，输出深度为 8。这个结果和论文 Fig. 3 的文字说明一致。

证据文件：

- `../outputs/checks/paper_swap_example.json`
- `../outputs/data/paper_swap_example_ops.csv`
- `scripts/run_paper_swap_example.py`

### Target 2: Reverse Traversal 改善初始映射

| 原文中的 reverse traversal 机制 | Agent 生成的 QFT 风格 benchmark 结果 |
![Reverse traversal reproduction](../outputs/figures/core_benchmarks_qft.png)

**一致性结论：`feature_match`**

论文 Fig. 5 描述的是反向遍历机制。这里的验收问题很明确：反向遍历能否改善最终映射结果。

我们用 QFT-6、QFT-8、QFT-10 三个线路做了检查。结果显示，forward-backward-forward 后的额外 CNOT 数和输出深度都优于第一次正向遍历：

| Benchmark | 额外 CNOT: first | 额外 CNOT: F-B-F | 深度: first | 深度: F-B-F |
| --- | ---: | ---: | ---: | ---: |
| qft6 | 21 | 9 | 34 | 31 |
| qft8 | 42 | 21 | 70 | 57 |
| qft10 | 54 | 36 | 109 | 92 |

这组结果直接对应论文机制中的关键数值特征：反向遍历提升了初始映射质量，并带来更少的额外门和更低的深度。

证据文件：

- `../outputs/checks/core_benchmarks.json`
- `../outputs/data/core_benchmarks.csv`
- `scripts/run_core_benchmarks.py`

### Target 3: Decay 机制带来的门数/深度权衡

| 原文中的 trade-off 图 | Agent 生成的 decay sweep |
![Decay tradeoff reproduction](../outputs/figures/decay_tradeoff.png)

**一致性结论：`feature_match`**

论文这里关注的是 decay 带来的搜索偏好变化：参数调整后，算法会在“少插入门”和“降低深度”之间移动。

我们的复现结果抓住了这个特征。局部 benchmark 中，baseline 深度为 160；开启合适 decay 后，最优深度降到 142，同时额外 CNOT 从 195 变为 198。这个结果体现了论文强调的门数/深度权衡。

这个目标属于特征一致。论文 Fig. 9 使用的完整 benchmark 组合和运行细节没有全部公开，因此这里采用同一算法机制下的本地 sweep 来验收。

证据文件：

- `../outputs/checks/decay_tradeoff.json`
- `../outputs/data/decay_tradeoff.csv`
- `scripts/run_decay_tradeoff.py`

### Target 4: Table II benchmark 结果

| 原文 Table II | Agent 生成的 `g_op` 对比 |
![Table II g_op comparison](../outputs/figures/table2_gop_comparison.png)

**一致性结论：`partial_match`**

这部分是最严格的验收目标，因为它要求对整批 benchmark 逐行对齐。我们已经把 Table II 的 26 个输入 benchmark 都纳入了本地 corpus，并且用论文表格中的 `g_ori` 做了输入核验。

当前状态：

- `g_ori` 输入门数：26/26 匹配；
- `n` 逻辑量子比特数：24/26 匹配；
- 路由结果硬件合法性：26/26 通过；
- `g_op` 精确匹配：7/26；
- `g_la` 精确匹配：0/26。

这说明 Agent 已经拿到了正确输入并生成了合法路由结果，但还没有完全复刻论文 Table II 的逐行最优数值。2026-06-18 的 A100 严格重跑使用 26 个 Table II benchmark、每行 1000 次随机初始映射、16 个并行 worker；`g_op` 仍然停在 7/26，`g_la` 因 best-of-1000 选到更低但不同于论文表格的值，exact match 变为 0/26。主要缺口来自论文没有完全公开随机初始映射、相同分数时的 tie-breaking 规则、best-of-N 选择策略，以及 BKA baseline 的完整可复现环境。

证据文件：

- `../outputs/checks/table2_reproduction.json`
- `../outputs/data/table2_reproduction.csv`
- `../outputs/data/table2_attempts.csv`
- Table II 的历史生成结果保留在公开输出中；由于完整 benchmark corpus 和验收输入不在公开边界内，对应批量脚本不作为公开 quick run 发布。

## 代码结构

这个案例沉淀成一个可以继续迭代的最小复现仓库：

- `src/sabre.py`: SABRE 路由器、front layer、候选 SWAP、look-ahead、decay、reverse traversal。
- `src/benchmarks.py`: QFT 和局部 benchmark 构造。
- `src/qasm_io.py`: benchmark corpus 读取和线路解析。
- `scripts/run_paper_swap_example.py`: Fig. 3 小例子复现。
- `scripts/run_core_benchmarks.py`: reverse traversal 特征检查。
- `scripts/run_decay_tradeoff.py`: decay trade-off 检查。
- Table II 全表结果是历史复现产物；公开 quick run 只包含不依赖内部 benchmark corpus 的三个独立脚本。

## 还有哪些问题

这里的问题就是和原论文之间还没有对齐的地方：

- Table II 还不是完整复现。输入 `g_ori` 已经全部对齐，输出 `g_op` 在 1000 次/行搜索后仍只有 7/26 逐行精确一致。
- `sym6_145` 和 `sym9_193` 的 qubit 数与论文表格不一致，说明 benchmark 元数据仍需要继续核对。
- 当前 SABRE 实现能生成合法路由，并体现 reverse traversal 和 decay 特征，但未必复刻了论文作者的全部随机种子策略、相同分数下的选择规则和工程细节。
- BKA baseline 没有完整复现环境，因此 Table II 里 BKA 对比还只能作为参考，不是本地重算结果。

## 推荐算力

这篇的主要瓶颈不是内存，而是大量随机尝试和缺失元信息：

- 本地 CPU 已经足够跑 feature-level 和几百次尝试；
- 推荐 16 核以上 CPU 工作站或批处理队列，把每个 benchmark、每个 seed 分发成独立任务；
- 若只靠时间，1000 次/行已经证明提升有限；下一步应优先记录/搜索 seed policy、初始 mapping 和 tie-breaking 规则，而不是继续盲目加大尝试次数；
- 若要完整复现，除了算力，还需要作者的 seed policy、tie-breaking 规则、attempt count、BKA 实现或可信输出。

## 这个案例展示了 Agent 的什么能力

这个案例展示了一条完整的科研跟读复现路径：

1. 先区分数值结果、示意图和背景材料；
2. 从论文中抽取算法推导和核心代价函数；
3. 把公式和算法步骤转成可运行代码；
4. 生成数值数据和图；
5. 用数字特征检查一致性；
6. 对没有完全一致的部分给出清楚原因。

因此，这个案例目前适合作为一个“可展示的部分复现案例”：核心机制已经对齐，关键小例子精确通过，Table II 仍然保留为继续迭代的精确复现目标。
