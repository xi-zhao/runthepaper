# Formula Verification

This document records which formulas are allowed to feed the numerical
reproduction. Machine-readable result: `../outputs/checks/formula_verification.json`.

Every card is source-traced from the paper and symbolically consistent with the
implementation. The physics consistency checks that gate these formulas before any
figure is trusted are in `../code/scripts/qa_cdhm.py` (results in
`../outputs/checks/qa_cdhm.json`).

Run:

```bash
cd cases/10.1103-PhysRevB.91.085420/code
python scripts/qa_cdhm.py
```

## Gate Summary

| Formula | Role | Gate | Reason |
| --- | --- | --- | --- |
| `cdhm_hamiltonian` | CDHM Bloch Hamiltonian H(k,t;beta), Eq. 14 | verified | Source-traced; undriven K=0 limit matches the analytic hopping bands and U is unitary to 1e-14. |
| `floquet_eigenphases` | Floquet eigen-equation, Eqs. 1/A1 | verified | Three gapped bands with omega/pi in the Fig. 1(a) extent; parallel-transport gauge. |
| `initial_populations` | Initial band populations rho_{n,k}(0), Fig. 1b | verified | Populations are non-negative and sum to 1 to 1e-10; k-reflection symmetric. |
| `transition_amplitude_W` | Kernel W_{nm,k}(s), Eqs. 4-6/A4-A11 | verified | Gauge-free single-diagonalization form; the physical combination C*_n C_m W_{nm} is gauge-invariant. |
| `population_change_delta_rho` | Population change Delta rho, Eq. 8 | verified | Sum over bands is zero to 1e-9; theory tracks the exact dynamics at correlation ~0.9 per band. |
| `berry_curvature` | Berry curvature and dgamma/dk, Eq. 11 | verified | Fukui-Hatsugai-Suzuki Chern numbers are integers summing to zero. |
| `avg_quasienergy` | Average quasienergy E_{n,k}, Eq. 12 | verified | Midpoint beta-average; dE/dk by central difference. |
| `displacement_delta_x` | One-cycle displacement Delta<x>, Eqs. 9-13/A26 | verified | Theory total agrees with the exact one-cycle displacement to ~2%; prefactor fixed by the Thouless limit. |

## Notes On Conventions

- The overall orientation of the (k, beta) torus is a gauge choice: the computed
  Chern numbers are the paper's (4,-8,4) -> (-8,16,-8) up to a global sign, and the
  physical Delta<x> is reported with the paper's positive sign, aligned to the exact
  dynamics.
- Eq. (8) uses the accumulated dynamical phase Omega_n(1) = sum_j omega_n(beta_j) on
  the exact discrete protocol; the phase enters as Phi_{nm} = (gamma_n - gamma_m) -
  (Omega_n - Omega_m), consistent with the exp(-i omega) eigenphase convention used
  throughout the code.
