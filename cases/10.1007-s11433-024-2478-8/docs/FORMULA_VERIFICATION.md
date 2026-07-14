# Formula verification

Machine-readable card set: [`../outputs/checks/formula_verification.json`](../outputs/checks/formula_verification.json).
Every equation used is transcribed from the paper with its source location and
carries at least one check.

## 1. Truncated Fourier waveform `f(t)` (main text p. 4)

`f(t) = 2π·(a0 + Σ_{n≥1} 2 a_n cos(2π n t / τ)) / (2N+1)` MHz, `τ = 0.25 μs`.
Check: the hybrid `Ω2` turns on ~0 at `t=0` and peaks ~`2π·16.4 MHz` at `t=τ/2`,
matching Fig. 3(a). Code: `src/waveforms.py`.

## 2. Single-photon sector Hamiltonians (eqs. a1, a3, a4)

- `H_sector00` (a1): buffer alone, 2 states.
- `H_sector01` (a3): buffer + one qubit, 5 states, Förster `|rr'> <-> |qq'>`.
- `H_sector11` (a4): full three-body, 9-state product basis.

**Verified** (derivation_status = `verified`): the reconstructed 9-state product
Hamiltonian is cross-validated against a **verbatim transcription of the paper's
Morris–Shore reduced eq. (a4)** (`h_sector11_bright`). Starting from `|111>`, the
two forms produce **identical `|111>` dynamics to < 1e-8**
(`test_product_and_bright_sector11_agree`). The antisymmetric qubit combinations
stay dark to < 1e-10 (`test_unitarity_and_dark_states`), reproducing the
published √2 symmetric couplings. Code: `src/hamiltonians.py`.

## 3. Two-photon ladder (eqs. a5, a6)

`H_local = (Ω_p/2)|1><e| + (Ω_S/2)|e><r| + h.c. + Δ0|e><e| + δ|r><r|`. Per the
paper, the two-photon many-body Hamiltonian is the single-photon eq. (a4) with
every `|1><->|r>` coupling replaced by this ladder. We build it as a per-atom
`{|1>,|e>,|r>,|q>}` product; the sectors are Hermitian and leave the all-`|1>`
state decoupled when the drive is off (`test_twophoton_model_is_hermitian_and_reduces`).
derivation_status = `reconstructed` — the full tensor model additionally contains
the triple-excitation states that the reduced (a4) form omits (negligible, 2.6e-8
population). Code: `src/hamiltonians_2p.py`.

## 4. CZ gate metric (main text, refs [48,49])

Conditional phase `Φ = φ11 + φ00 − 2 φ01` and the Pedersen average gate error
`1 − F_avg` vs the ideal CZ, optimised over single-qubit Z. Check: Fig. 3 hybrid
`Φ = −1.0000π`, error `6.5e-6 < 1e-4`. Code: `src/gate.py`.
