# Similarity Scorecard

## Case Score

- Overall score: `79.89/100`
- Similarity level: `numerical_feature_reproduction`
- Scoring object: scientific numerical features, not color, line width, layout,
  or typography.
- Score scope: only T001-T002, the two targets with paper-exact analytic
  references. T003-T009 are reported separately because missing author arrays
  make pixel-level similarity an invalid scientific metric.

## Target Scores

| Target | Weight | Feature | Numeric | Scope | Final score |
| --- | ---: | ---: | ---: | ---: | ---: |
| T001 Fig. 15 | 1.0 | 42/50 | 28/35 | 15/15 | 85.0 |
| T002 Fig. 6 | 0.8 | 40/50 | 26/35 | 7.5/15 | 73.5 |

T001 的分数同时反映 Appendix-L 包络的高一致性和两个未保留的强度响应小峰。T002 的 panel ledger 只给 panel (a) 满额，panel (b) 为实验背景不计分，panel (c) 未复现，因此 scope 上限为 7.5。

## Expanded Formula Coverage

| Target | Paper content | Numerical provenance | Honest status |
| --- | --- | --- | --- |
| T003 | Fig. 1(f)/Fig. 7 power laws | formula numerics | published subset complete; absolute PSD/Doppler terms blocked |
| T004 | Fig. 8 public-anchor scaling | formula numerics | anchor-constrained reconstruction |
| T005 | Fig. 9(a,b) protocol responses | independent Hamiltonian numerics | computed; Fig. 9(c) blocked |
| T006 | Fig. 10 spin-lock filter | formula numerics | analytic filter complete; absolute data curve blocked |
| T007 | Fig. 12 cavity transfer | formula numerics | disclosed transfer reconstruction |
| T008 | Fig. 17 SSB proxy | formula numerics | printed formulas complete; circuit inset partial |
| T009 | Fig. 11 seven-site response | independent many-body numerics | physical reconstruction, not paper-exact |

These targets are not assigned visual-similarity points. Their acceptance is
based on equation traces, limiting cases, gate closure, norm/convergence checks,
and explicit parameter provenance.

## What Prevents A Higher Score

- 缺少 Fig. 15 底层优化相位轨迹，无法独立生成论文原始数值响应。
- Appendix-L 本身是近似拟合，未保留 Fig. 15(b) 的全部高频细结构。
- 缺少 Fig. 6(b,c) 的原始 PSD 数组和误差样本。
- 当前比较依据为论文解析参考，而不是作者原始数值数组。
- T003-T009 的精确原图比较分别受 PSD、硬件校准、原子几何、精确
  ramp/pulse identity 或电路离散参数限制；这些空缺没有通过像素拟合补齐。

完整机器记录：`outputs/checks/similarity_scorecard.json`；无像素输入审计：
`outputs/checks/computational_provenance_audit.json`。
