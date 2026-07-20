# Source audit

The record maps to Falkner, Coretti, and Dellago, “Enhanced Sampling of Configuration and Path Space in a Generalized Ensemble by Shooting Point Exchange,” PRL 132, 128001 (2024), arXiv:2302.08757v2. The source is authoritative but outside the benchmark time window.

The main text explicitly gives the full detailed-balance acceptance criterion and channel fractions. Neither the main paper nor embedded SI contains `27.3×10^-3`, the alleged optimized-coordinate rerun, force-evaluation totals, or exchange-triggered switch counts.

The SI potential is `alpha/4 * [(r^2-4)^2 + (x1)^2]`; the frozen prompt moves `(x1)^2` outside the `alpha/4` factor.
