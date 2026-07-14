# Derivation trace

How the paper's physics becomes runnable code, step by step.

1. **Register encoding.** Buffer atom prepared in `|1>`; qubit register `|0>` is
   dark (undriven). Each two-qubit input therefore evolves in an independent
   sector: `|00> -> |010>` (buffer only), `|01>/|10> -> |011>/|110>` (buffer +
   one qubit), `|11> -> |111>` (full three-body).

2. **Local driving.** Buffer atom `1<->r` with `(Ω1, Δ1)`; each qubit atom
   `1<->r'` with `(Ω2, Δ2)`. Convention `H = (Ω/2)(|g><e|+h.c.) + Δ|e><e|`,
   `ħ = 1`.

3. **Interaction.** Rydberg dipole–dipole modelled (appendix) as a Förster
   resonance: an adjacent `(buffer, qubit)` pair in `|r r'>` couples with strength
   `B` to `|q q'>` at extra energy `δ_q`. Only the two adjacent pairs
   (control–buffer, buffer–target) interact; the distant control–target pair is
   neglected. Here `B = 2π·50 MHz`, `δ_q = 0`.

4. **Sector Hamiltonians.** `|11>` is assembled directly in the 9-state product
   basis and shown equivalent to the paper's Morris–Shore reduced eq. (a4) — the
   symmetric qubit combinations reproduce the √2 couplings while the antisymmetric
   ones stay dark from `|111>`. This avoids an OCR-ambiguous transcription while
   keeping a verbatim eq. (a4) form as an independent cross-check.

5. **Two-photon extension.** For the two-photon transition (Fig. 4/6) each
   `1<->r` step becomes a ladder `1<->e<->r` through an intermediate state `|e>`
   at a large one-photon detuning `Δ0 = 2π·5 GHz` (eqs. a5/a6). The interaction
   structure is unchanged; only the ground–Rydberg coupling changes.

6. **Dynamics and metric.** Integrate `iψ̇ = H(t)ψ` per sector, read off the four
   accumulated phases, and form the CZ conditional phase and Pedersen average
   gate error (optimised over local Z).

7. **Dual pulse (Fig. 5).** Each single pulse imparts π/2; applying it twice —
   the second with the qubit-atom Doppler shift `±k·v` sign-flipped — composes a
   full CZ while cancelling the first-order velocity phase.

8. **Robustness (Fig. 7).** Scale the buffer (`Ω1`) and qubit (`Ω2`) amplitudes
   of the Fig. 3(a) waveforms by overall ratios over `[0.99, 1.01]²` and map the
   gate error.

Acceptance is the paper's own scalar claim: the reconstructed Hamiltonian must
reproduce gate error < 1e-4 from the published coefficients — a falsifiable test
that a wrong model cannot pass.
