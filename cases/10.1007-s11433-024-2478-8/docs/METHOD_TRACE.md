# Method trace

The paper's numerical recipe and where each choice is pinned.

- **Model.** Time-dependent Schrödinger equation per register sector, `ħ = 1`,
  rotating frame. Single-photon: 2/5/9-state sectors. Two-photon: per-atom
  `{|1>,|e>,|r>,|q>}` product (3/16/64 states for the CZ sectors).
- **Parameters (paper-exact).** `B = 2π·50 MHz`, `δ_q = 0`, `τ = 0.25 μs`,
  two-photon one-photon detuning `Δ0 = 2π·5 GHz`. Waveforms are the paper's
  truncated Fourier series with the published coefficients (`src/coefficients.py`,
  each tagged with its source location).
- **Integrator.** SciPy `solve_ivp` with `DOP853`. Single-photon: `rtol 1e-11`,
  `atol 1e-12`, `max_step τ/400`. Two-photon: `rtol 1e-10`, `atol 1e-12`,
  `max_step τ/4000` to resolve the fast `Δ0` oscillation (convergence checked:
  identical to < 1e-6 at `τ/4000`, `τ/20000`, `τ/60000`). Norm conserved to
  ~1e-14.
- **Gate metric.** Conditional phase `Φ = φ11 + φ00 − 2 φ01`; Pedersen average
  gate error `1 − F_avg` against the ideal CZ, optimised over single-qubit Z
  phases (Nelder–Mead) — the paper's "typical way [48,49]".
- **Doppler (Fig. 5).** Add `±k·v` to the qubit-atom detunings, sign-flipped
  between the two pulses; compare the flipped-dual end-phase deviation to the
  un-flipped one to quantify first-order cancellation.
- **Robustness (Fig. 7).** 81×81 grid over `[0.99, 1.01]²`, gate error per point,
  multiprocessing across CPU cores.

## Validation checks

`code/tests/test_bam_gate.py` (9 tests): analytic Rabi limit, unitarity + dark
states, product-vs-verbatim eq. (a4) agreement (< 1e-8), both Fig. 3 CZ gates
< 1e-4, Fig. 5 single pulse = π/2, Fig. 7 corner structure, and two-photon
Hamiltonian Hermiticity/decoupling. Per-figure numeric checks live in
`../outputs/checks/`.
