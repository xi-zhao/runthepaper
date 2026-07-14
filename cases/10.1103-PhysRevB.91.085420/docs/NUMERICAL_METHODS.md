# Numerical Methods

## Bloch / Floquet layer (`code/src/cdhm.py`)

- Per quasimomentum k the CDHM reduces to a 3x3 Bloch Hamiltonian
  H(k,t;beta) = h_hop(k) + K cos(2 pi t/tau) V(beta), with V diagonal.
- The one-period Floquet operator U(k,beta) is the time-ordered product of midpoint
  short-time propagators exp(-i H(t_mid) dt), n_sub substeps per period, batched over
  k via Hermitian eigendecomposition. U is unitary to 1e-14; eigenphases converge by
  n_sub ~ 80-120.

## Wave-packet dynamics (`code/src/observables.py`)

- The adiabatic cycle holds beta fixed per driving period, so one cycle is the
  ordered product of T operators U(k,beta_j), beta_j = 2 pi (j + 0.5)/T.
- `evolve_fast`: a Strang split with exp(-i h_hop dt) precomputed once per k
  (independent of beta and t) and the diagonal potential applied as an elementwise
  phase. About 30x faster than rebuilding U each period; validated against the exact
  eigendecomposition propagator.
- `x_expectation`: the gauge-free k-space mean position
  `<x> = i integral dk sum_j phi_j* d_k phi_j + sum_j j |phi_j|^2`, with the
  k-derivative taken spectrally by FFT. Because phi_j(k) is smooth and periodic over
  the Brillouin zone, this equals sum_l l |<l|Psi>|^2 exactly and stays
  well-conditioned even when the packet width (~2T sites) far exceeds the center
  displacement. Converged at Nk ~ 2T (verified: T=6144 stable for Nk >= 12288).

## Analytic theory (`code/src/theory.py`)

- Berry curvature and dgamma/dk: Fukui-Hatsugai-Suzuki plaquettes on the (k, beta)
  torus; Chern numbers come out as exact integers summing to zero.
- W(0) kernel: `<psi_n | d_beta U | psi_m> / (lam_m - lam_n)` then divided by
  (1 - exp(i(omega_n - omega_m))), from a single diagonalization and no beta-gauge
  fixing. The physical combination C*_n C_m W_{nm} is gauge-invariant.
- Average quasienergy E_{n,k} = (1/2 pi) integral omega d beta; dE/dk by central
  difference.
- Delta<x> theory (Eq. 13) = (a/2 pi)[ Berry-curvature integral term - 2 (IBC term) ],
  a = N = 3; the overall prefactor is fixed by the Thouless limit Delta x = a C_n for
  a filled band and confirmed against the exact dynamics.
- Delta rho theory (Eq. 8) uses the exact discrete accumulated phase
  Omega_n(1) = sum_j omega_n(beta_j).

## Grids / parameters actually run

All targets are at paper parameters: n_sub 100-160; Nk 241-12288 depending on the
target; the 61-point J-scan is parallelised over 8 cores. See `../code/scripts/`.
