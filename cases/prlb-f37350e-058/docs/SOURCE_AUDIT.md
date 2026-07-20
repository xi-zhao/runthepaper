# Source audit

The direct source is verified: Tomasz Paterek and Arseni Goussev, “General
Quantum Backflow in Realistic Wave Packets,” *Physical Review Letters* **136**,
090202 (2026), DOI `10.1103/tm9s-pkg5`, arXiv:2511.10155v2.

The source directly supports the frozen Task 1 kernel and phase map. It also
supports the projection representation

```text
K = Q_x(t2) - Q_x(t1) - P_p(-),
```

and reports `sup sigma(K)=0.128100 +/- 0.000002`, with rigorous literature
bounds `0.128092 <= sup sigma(K) <= 0.192466`.

It does **not** claim `||K||=2`, does not study a fixed negative-momentum
marginal, and does not report `Lambda(1/2)`. Most decisively, the paper calls
smoothed spatial readout a “future” follow-up question. The Gaussian family and
`c2` in frozen Task 4 are benchmark-added claims, not source-paper results.

The source archive contains the TeX, Supplemental Material, figures, and every
published extrapolation table, but no executable code or plotted state arrays.
