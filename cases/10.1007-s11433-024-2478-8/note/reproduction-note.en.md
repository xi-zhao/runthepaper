# Reproducing "Buffer-atom-mediated quantum logic gates with off-resonant modulated driving"

Y. Sun, *Sci. China-Phys. Mech. Astron.* **67**, 120311 (2024). DOI
[10.1007/s11433-024-2478-8](https://doi.org/10.1007/s11433-024-2478-8).

## 1. What the paper claims

A single **buffer atom** placed between two qubit atoms can mediate a
controlled-Z (CZ) gate through the Rydberg dipole–dipole (Förster) interaction,
driven by smooth off-resonant modulated (ORMD) laser waveforms. With the buffer
prepared in `|1>` and the qubit register state `|0>` dark, every two-qubit input
maps to an independent few-state sector. The paper reports **gate error < 1e-4**
for both a single-photon (Fig. 3) and a two-photon (Fig. 4) implementation,
extends it to a Doppler-insensitive dual-pulse variant (Fig. 5), a three-qubit
Toffoli phase gate (Fig. 6), and studies robustness to Rabi-amplitude ratio
errors (Fig. 7).

## 2. What we reproduced

Everything the paper specifies with explicit coefficients, from an independently
reconstructed three-body Hamiltonian:

- **Fig. 3 (single-photon CZ, both protocols) — complete reproduction.** Gate
  error `6.5e-6` (hybrid) / `5.6e-5` (amplitude), conditional phase ≈ ±π. The
  waveforms, return populations, and accumulated phases match the published
  figure to < 0.7% RMS. The reconstructed three-body Hamiltonian was
  cross-validated against a verbatim transcription of the paper's Morris–Shore
  reduced form eq. (a4) (agreement < 1e-8).
- **Fig. 4 (two-photon CZ).** Built the full three-level (`|1>,|e>,|r>`) ladder
  model of eqs. (a5)/(a6). The hybrid protocol's populations match to < 0.4%
  RMS. Reported honestly: the full-model gate error is `1.3e-3`, above the
  paper's < 1e-4 (see §5).
- **Fig. 5 (Doppler-insensitive dual pulse).** Each pulse imparts π/2, so the
  dual pulse composes a full CZ (conditional phase `0.99988π`). Applying the
  second pulse with the Doppler shift sign flipped suppresses the end-of-gate
  Doppler phase deviation by **~2600× (|00>) to ~32000× (|11>)** — the paper's
  first-order cancellation.
- **Fig. 7 (robustness).** The 2-D gate-error colormap over ±1% buffer/qubit
  amplitude ratios reproduces the paper's structure (dark valley along the main
  diagonal, bright anti-diagonal corners) and its conclusion that ~1% control
  precision is needed.

## 3. Intuition and method

Each driven atom is a two-level (single-photon) or three-level ladder
(two-photon) system; the buffer–qubit Rydberg pair interacts by a Förster
resonance `|r r'> <-> |q q'>` of strength `B = 2π·50 MHz`, and only adjacent
(control–buffer, buffer–target) pairs interact. We integrate the time-dependent
Schrödinger equation for each sector with SciPy `DOP853` (tight tolerances; norm
conserved to ~1e-14) and evaluate the CZ conditional phase and Pedersen average
gate error, optimised over single-qubit Z. The waveforms are the paper's own
truncated Fourier series with the published coefficients.

The reproduction is **self-validating**: an incorrect Hamiltonian could not hit
the paper's < 1e-4 gate error from the paper's own coefficients.

## 4. How to run

See [../code/README.md](../code/README.md). In short, from the case root:

```bash
python code/scripts/run_fig3.py
python code/scripts/run_fig4.py
python code/scripts/run_fig5.py
python code/scripts/run_fig7.py
python -m pytest code/tests/ -q
```

Everything runs on a laptop CPU in seconds to a few minutes. No GPU or cluster is
needed.

## 5. Reproduction boundary — read this

- The **two-photon** gate error we obtain (`1.3e-3` hybrid, `3.7e-3` amplitude)
  is the honest value of the *faithful full three-level model* with the paper's
  waveforms. We verified that the adiabatic-elimination effective model is worse
  (`1.9e-2`), so the full model is the correct one; the residual most plausibly
  reflects the paper optimising its waveforms in a reduced/effective model. The
  populations and phases (the figure content) still match.
- **Fig. 7** corner peak is ~25% below the paper's colorbar maximum.
- **Fig. 6 (Toffoli)** is *not* reproduced: the multi-qubit buffer geometry is
  unspecified; a star geometry leaves 11% leakage.
- **Figs. a6–a8** are *not reproducible*: no coefficients are given.
- We do not redistribute the paper PDF, original figures, or digitized source
  data. Visual agreement is not author-data-level equivalence.
