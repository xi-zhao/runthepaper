# Case Intro: Efficient Simulation Of Logical Magic State Preparation Protocols

## One-Sentence Result

这个 case 跟随 arXiv:2512.23799，完成了逻辑魔态制备模拟论文的公式 gate 和若干 proxy checks。但它没有按原文 exact Steane circuit / Stim-Cirq benchmark 参数重跑，因此不能作为论文 benchmark 图复现。

## Similarity Level

- Current level: `feature_not_accepted`
- Similarity score: `73.00/100`
- Meaning: 公式 gate 有价值，但三张 benchmark 图主要来自 proxy model，不满足原文参数运行要求。
- Important note: 本 case 当前只能作为公式和 proxy 数值链路展示。三张 benchmark 图没有按原文参数运行，所以不能叫直接复现。

## Paper And Goal

- Paper: *Efficient simulation of logical magic state preparation protocols*
- PaperID: `2512.23799`
- Case type: 容错量子计算 / 魔态制备协议模拟
- Reproduction scope: PSC 公式 gate、Pauli-rank fidelity 逻辑、proxy infidelity trend、acceptance 弱趋势检查、runtime speedup proxy
- Out of scope: 电路示意图、误差位置示意图、作者未公开的原始 benchmark 数据

## Intuitive Derivation

这篇论文的核心想法是：很多魔态制备协议虽然看起来含有大量非 Clifford 结构，但电路级 Pauli 错误可以被推到电路末端，变成一个 Clifford error。

所以模拟对象可以写成：

```text
noisy MSP protocol
-> noiseless logical magic state + end-of-circuit Clifford error
```

接下来，fidelity 不再需要完整 state-vector 暴力模拟。论文使用 stabilizer-rank 或 Pauli-rank 分解，把目标魔态写成少量 stabilizer/Pauli 成分，然后通过这些成分的 expectation value 估计 fidelity。

公式 gate 做了三件事：

1. 核验 `H`、`S`、`CZ` 等 PSC 的平方确实是 Pauli。
2. 核验 controlled-H 的基本误差传播恒等式。
3. 核验 `|H><H|` 可以由 Pauli 期望值重建。

这些核验通过后，才进入数值图。

## Numerical Method

本地复现采用一个可审计的 proxy-level MSP 模型。它保留论文 benchmark 的部分结构：

- 42 个电路级错误位置；
- 物理错误率 `p`；
- postselection acceptance；
- conditional logical infidelity；
- propagated-error estimator 与 reference estimator 的对比；
- 低 `p` 区域的 per-shot runtime 加速。

输出先写 CSV，再画图。所有检查都写入 JSON：

- `../outputs/checks/formula_verification.json`
- `../outputs/checks/numerical_feature_checks.json`
- `../outputs/checks/similarity_scorecard.json`

## Original vs Reproduced

### T001: Infidelity Benchmark

![Generated](../outputs/figures/fig1_infidelity_reproduction.png)

**Consistency:** `proxy_model`

**Similarity level:** `feature_not_reproduced`

**Similarity score:** `55/100`

Explanation:

- Feature being checked: infidelity should increase with physical error rate, and the propagated-error estimator should agree with the reference estimator within sampling error.
- What matches: infidelity increases with `p`, and the two local estimators agree within the proxy model.
- What remains different: this does not run the paper's exact Steane postselection circuit or author benchmark arrays, so it is capped as `proxy_model`.
- Evidence: `../outputs/data/fidelity_acceptance_benchmark.csv`, `../outputs/checks/numerical_feature_checks.json`

### T002: Acceptance Rate Benchmark

![Generated](../outputs/figures/fig2_acceptance_reproduction.png)

**Consistency:** `weak_trend_only`

**Similarity level:** `feature_not_reproduced`

**Similarity score:** `35/100`

Explanation:

- Feature being checked: postselection acceptance should decrease as circuit-level noise increases, and both simulation routes should agree.
- What matches: only the monotone decrease and the agreement between the two local estimators.
- What remains different: the decline scale is wrong. In the original figure, acceptance is already about `0.84` near `p=1e-3` and near `0.2` around `p=1e-2`; our feature model is still around `0.7` near `p=1e-2`. This target should not be advertised as reproduced.
- Evidence: `../outputs/data/fidelity_acceptance_benchmark.csv`

### T003: Average Time Per Shot Benchmark

![Generated](../outputs/figures/fig3_runtime_reproduction.png)

**Consistency:** `proxy_timing`

**Similarity level:** `feature_not_reproduced`

**Similarity score:** `55/100`

Explanation:

- Feature being checked: low-`p` propagated Clifford simulation should be much cheaper than a state-vector-like baseline.
- What matches: at `p=1e-3`, the local conservative proxy gives about `22x` speedup, consistent with the paper's claim that the propagated route is substantially faster.
- What remains different: this is a local calibrated proxy, not the authors' hardware/runtime measurement.
- Evidence: `../outputs/data/runtime_proxy_benchmark.csv`

### T004: Formula And Sampling Gate

| Formula/sampling checks | Agent-generated result |
| PSC and Pauli-rank checks | ![Generated](../outputs/figures/fig4_sampling_precision_reproduction.png) |

**Consistency:** `algorithmically_consistent`

**Similarity level:** `numerical_feature_reproduction`

**Similarity score:** `84/100`

Explanation:

- Feature being checked: formulas used before simulation are internally consistent, and Monte Carlo error should scale like `1/sqrt(N)`.
- What matches: PSC square checks passed, controlled-H propagation identity passed, Pauli-rank reconstruction passed, and the sampling slope is `-0.498`.
- What remains different: this validates the method chain, not a separate original paper figure.
- Evidence: `../outputs/checks/formula_verification.json`, `../outputs/data/sampling_scaling.csv`

## What Still Differs From The Paper

- No pointwise comparison to the authors' numerical arrays is possible from the arXiv source alone.
- The full Steane flag-gadget simulator is not implemented in this local case.
- Runtime is a conservative local proxy, not the authors' exact Stim/Cirq benchmark environment.
- The result should be presented as formula/method validation plus proxy checks, not as feature-level reproduction of the paper figures.

## Recommended Compute For Complete Reproduction

The main blocker is missing author data/code, not local memory.

For a full rerun:

- implement the exact Steane-code `|Hbar>` preparation circuit;
- run the propagated Clifford route with `N_tot = 1e5` to `1e7` shots;
- run the Cirq state-vector baseline with `N_tot = 1e5` to `1e6` shots;
- use the same `p` grid as the paper;
- compare generated arrays against either author data or digitized paper curves.

Recommended machine: 16-32 CPU cores, 32-64GB RAM, overnight batch runtime. The current M3 Pro can continue feature-level and small exact checks, but paper-grade benchmark reruns should be treated as a separate timed run.

## Code Structure

- `src/magic_state_simulation.py`: formula checks, feature model, Monte Carlo, runtime proxy.
- `scripts/run_reproduction.py`: generates CSV and JSON checks.
- `scripts/plot_reproduction.py`: generates the reproduction figures.
- `../outputs/data/`: numerical data behind generated figures.
- `../outputs/checks/`: formula, numerical and scorecard checks.
- `../outputs/figures/`: generated plots.

## Final Takeaway

这个 case 展示了 Agent 对算法型量子论文的复现方式：先验证公式和误差传播逻辑，再把论文中的 benchmark 拆成可运行的数值检查。当前版本说明公式链路可以跑通，但还没有抓住原图的数值尺度。要进入复现层级，需要实现完整 Steane flag-gadget，并用原文 Stim/Cirq benchmark 参数重跑。
