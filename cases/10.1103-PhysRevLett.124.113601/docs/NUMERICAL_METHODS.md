# Numerical Methods

## NUM001 — AA/GAA eigenstates and state thresholds

- Target: T001 / Fig. 2.
- Equations: EQ001, EQ002, EQ004–EQ006.
- Parameters: `L=377`, `chi/J=2.1`, exact golden `gamma`, `gamma_c=0.8`, `J'/J=-0.23`, `J2/J=0.072`, `chi'/J=-0.016`.
- Boundary: periodic, inferred from the absence of source edge-state spikes.
- Site origin: `j=1`; together with exact golden `gamma`, this reproduces all 377 vector-source IPR points with RMSE `1.85e-6`.
- Solver: dense symmetric diagonalization for GAA; tridiagonal/dense symmetric diagonalization for AA.
- Output: one CSV row per model/eigenstate with energy, IPR, localization flag, overlap, response and `eta_c`.
- Checks: Hermiticity, analytic clean spectrum, mobility-edge index/energy, all-localized AA limit.

## NUM002 — Ground susceptibility and momentum channels

- Target: T002 / Fig. 3 and T003 / Fig. 4(b).
- Equations: EQ001, EQ004–EQ007.
- Parameters: exact golden `gamma`, `L=377`, `gamma_c=0.8` or the plotted `gamma_c` grid.
- Solver: full tridiagonal eigensystem, direct overlap matrix, direct Fourier sum on `q in [-2,2]`.
- Grids: 301 disorder points, 1601 momentum points, 401 cavity-wave-vector points.
- Checks: clean `eta_c`, Parseval-scale symmetry, analytic channel indices, harmonic-minimum positions, localized zero threshold.

## NUM003 — Nonlinear cavity continuation

- Target: T003 / Fig. 4(a).
- Equations: EQ003 and EQ008.
- Solver: lowest tridiagonal eigenpair alternated with the complex cavity fixed point; state/field damping `0.35`; branch continuation from `eta/J=0.25` downward.
- Grid: 126 pump values for each of `chi/J=0.5,1,2.03`.
- Tolerance: maximum density/field update below `1e-10`; 5000-iteration ceiling.
- Checks: convergence fraction, onset windows, source-scale endpoint photon numbers.

## NUM004 — Self-consistent density profiles

- Target: T004 / Fig. S1.
- Boundary: open; exact golden `gamma`; disclosed finite-chain site-origin shift `233`.
- Pump samples: `eta/J={0.25,0.198,0.164,0.02,0.12}` for `chi/J={0,0.5,1,1.9,2.03}`; reconstructed from source peak heights.
- Checks: normalization, convergence, peak-height windows, IPR/peak sharpening at `chi/J=2.03`.

## NUM005 — Size and trap diagnostic

- Target: D001.
- Sizes: `L=300,377,1000,3000,10000`.
- Solver: lowest tridiagonal eigenpair only.
- Weak trap: quadratic curvature giving a `0.01J` edge offset at `L=377`.
- Checks: decreasing extended IPR, size-stable localized IPR, finite localized cavity overlap, preserved deep-localized state under the trap.

## Numerical Risks

- Exact rational approximants can introduce finite-chain momentum aliases; the raw `gamma_c=0.5` value is preserved and the plotted clean curve uses the two-sided thermodynamic limit.
- Critical slowing near nonlinear onsets requires more than 1000 fixed-point iterations.
- Missing S1 pump samples prevent final-reproduction status even though the visible features match.
- Source and published detuning conventions differ by a factor of two; using one global convention corrupts at least one target.
