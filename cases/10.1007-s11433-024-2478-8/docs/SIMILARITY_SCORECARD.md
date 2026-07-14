# Similarity scorecard

Machine-readable scorecard: [`../outputs/checks/similarity_scorecard.json`](../outputs/checks/similarity_scorecard.json).
Overall audit score **84.6 / 100** across 6 targets. Scientific agreement is
reported separately from visual similarity, and generated data separately from
any source reference.

| Target | Paper item | Level | Score | Main point / cap |
| --- | --- | --- | --- | --- |
| T001 | Fig. 3 (a–c) single-photon CZ, hybrid | Complete reproduction | 95 | gate error 6.5e-6; curves match <0.7% RMS |
| T002 | Fig. 3 (d–f) single-photon CZ, amplitude | Complete reproduction | 94 | gate error 5.6e-5; W-shape populations match |
| T004 | Fig. 4 (a–c) two-photon CZ, hybrid | Numerical feature | 80 | populations <0.4% RMS; full-model error 1.3e-3 vs paper <1e-4 |
| T005 | Fig. 4 (d–f) two-photon CZ, amplitude | Numerical feature | 71 | structure reproduced, shallower dips; error 3.7e-3 |
| T006 | Fig. 5 dual-pulse Doppler | Numerical feature | 80 | conditional phase 0.99988π; first-order cancellation ~2600–32000× |
| T003 | Fig. 7 robustness colormap | Numerical feature | 80 | 2-D structure + >1% conclusion; peak ~25% low |

## Scientific gates (independent of visual similarity)

- **Parameter match**: `paper_exact` on all targets — the paper's own Fourier
  coefficients, `B = 2π·50 MHz`, `τ = 0.25 μs`, `Δ0 = 2π·5 GHz`.
- **Provenance**: `independent_numerics` — every curve comes from our own
  three-body integration, not from any source data.
- **Formula gate**: Fig. 3 sectors `verified` (eq. a4 cross-validated against a
  verbatim Morris–Shore transcription to <1e-8); two-photon ladder (a5/a6)
  `reconstructed`.

## Not scored / not reproduced

- **Fig. 6 (three-qubit Toffoli)**: multi-qubit buffer geometry underspecified;
  best-guess star geometry leaves 11% leakage.
- **Figs. a6–a8**: no published waveform coefficients.

See the per-target `remaining_gap` fields in the JSON for the exact boundaries.
