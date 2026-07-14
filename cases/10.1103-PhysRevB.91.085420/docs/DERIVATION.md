# Derivation

Equation-level derivation for the continuously driven Harper model (CDHM)
reproduction of Wang, Zhou & Gong, *Phys. Rev. B* **91**, 085420 (2015). Each
block is an equation the reproduction depends on, with its paper location and a
code pointer. For the narrative walk-through see `DERIVATION_TRACE.md`.

All eight equation cards are `verified`: source-traced and symbolically
consistent with the implementation.

## Equations

### cdhm_hamiltonian — Continuously driven Harper model H(k,t;beta) (Eq. 14)

```text
H = sum_l (J/2)(a_l^dag a_{l+1} + h.c.)
    + K cos(2 pi t / tau) sum_l cos(2 pi alpha l + beta) a_l^dag a_l,
    alpha = 1/3,  tau = 2.
```

Bloch reduction with l = 3n + j (j in {0,1,2}) gives a 3x3 per-k Hamiltonian:
`h_hop(k)` with intra-cell hops J/2 and inter-cell hop (J/2) exp(i 3k); onsite
diagonal K cos(2 pi t/tau) diag(cos beta, cos(2 pi/3 + beta), cos(4 pi/3 + beta)).
Superlattice constant a = N = 3, so k in [-pi/3, pi/3].

Code: `code/src/cdhm.py` — `CDHM.hamiltonian`, `CDHM.h_hop`, `CDHM.floquet_operator`.

### floquet_eigenphases — Floquet eigen-equation and eigenphases omega_{n,k}(beta) (Eqs. 1, A1)

```text
U(beta) |psi_{n,k}(beta)> = exp(-i omega_{n,k}(beta)) |psi_{n,k}(beta)>.
```

Three gapped Floquet bands for alpha = 1/3, in the parallel-transport gauge
`<psi | d psi / d beta> = 0`.

Code: `code/src/cdhm.py` — `floquet_bands`; `code/src/theory.py` — `_floquet_eig`.

### initial_populations — Initial band populations rho_{n,k}(0) = |C_{n,k}(0)|^2 (Fig. 1b)

```text
C_{n,k}(0) = <psi_{n,k}(beta=0) | e_0>,  e_0 = (1,0,0),
rho_{n,k}(0) = |C_{n,k}(0)|^2,  sum_n rho_{n,k}(0) = 1.
```

The site-0 initial state projects onto the k-component vector e_0.

Code: `code/src/cdhm.py` — `initial_populations`; `code/src/theory.py` — `initial_amplitudes`.

### transition_amplitude_W — First-order amplitude C_{n,k}(1) and kernel W_{nm,k}(s) (Eqs. 4-6, A4-A11)

```text
dC_{n,k}/ds = - sum_{m != n} exp(i(Omega_n - Omega_m)) C_{m,k} <psi_n | d psi_m/ds>.
Integrating by parts:
C_{n,k}(1) = C_{n,k}(0) + (1/T) sum_{m != n} C_{m,k}(0) [W_{nm,k}(s)] evaluated 0..1,
W_{nm,k}(0) = 2 pi <psi_n | d_beta psi_m> / (1 - exp(i(omega_n - omega_m))).
```

The gauge-free numerical form uses `<psi_n | d_beta psi_m> = <psi_n | d_beta U | psi_m> / (lam_m - lam_n)`
for n != m, so no beta-gauge fixing is needed; the physical combination
`C*_n C_m W_{nm}` is gauge-invariant.

Code: `code/src/theory.py` — `W0_kernel`.

### population_change_delta_rho — Population change Delta rho_{n,k} after one cycle (Eq. 8, Fig. 2)

```text
Delta rho_{n,k} = (2/T) Re[ sum_{m != n} C*_n(0) C_m(0) (W_{nm,k} evaluated 0..1) ],
W_{nm} evaluated 0..1 = W_{nm}(0) [ exp(i Phi_{nm}) - 1 ],
Phi_{nm} = (gamma_n - gamma_m) - (Omega_n(1) - Omega_m(1)),
Omega_n(1) = sum_j omega_n(beta_j)  (exact discrete accumulated phase).
```

Delta rho scales as 1/T for a general multi-band initial state (the
interband-coherence, IBC, cross term is nonzero) versus 1/T^2 for a single-band
initial state.

Code: `code/src/theory.py` — `delta_rho_theory`, `accumulated_Omega`, `berry_phase`.

### berry_curvature — Berry curvature B_n(beta,k) and dgamma/dk (Eq. 11)

```text
B_n(beta,k) = i[ <d_k psi_n | d_beta psi_n> - <d_beta psi_n | d_k psi_n> ],
d gamma_{n,k}/dk = integral_0^{2 pi} d beta B_n(beta,k),
double integral of B_n over (k, beta) = 2 pi C_n  (Chern number).
```

Computed gauge-invariantly by the Fukui-Hatsugai-Suzuki plaquette method on the
(k, beta) torus.

Code: `code/src/theory.py` — `berry_flux_strips`.

### avg_quasienergy — Average quasienergy E_{n,k} along the cycle (Eq. 12)

```text
E_{n,k} = (1/T) Omega_{n,k}(1) = integral_0^1 omega_{n,k}[beta(s)] ds
        = (1/2 pi) integral_0^{2 pi} omega_{n,k}(beta) d beta.
```

dE_{n,k}/dk enters the IBC correction of Eq. (13).

Code: `code/src/theory.py` — `avg_quasienergy`.

### displacement_delta_x — One-cycle displacement Delta<x> (Eqs. 9-13, A26)

```text
Delta<x> = sum_n integral dk integral d beta B_n(beta,k) rho_{n,k}(0)
         - 2 sum_{m != n} integral dk Re[ C*_n(0) C_m(0) (dE_{n,k}/dk) W_{nm,k}(0) ].
```

Both terms are independent of T; the second (IBC) term survives the adiabatic
limit. Units: atomic spacing. A filled band gives Delta x = a C_n (a = N = 3),
which fixes the a/(2 pi) prefactor on both terms.

Code: `code/src/theory.py` — `delta_x_theory`; `code/src/observables.py` — `x_expectation`, `evolve_fast`.
