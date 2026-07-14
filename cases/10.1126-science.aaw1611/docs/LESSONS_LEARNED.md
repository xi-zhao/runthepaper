# Lessons learned

1. **Conserved sectors are the right core model.** The nominal local Hilbert
   space is irrelevant here; particle-number conservation reduces the problem
   to matrices of size 78 or less without approximating the paper physics.
2. **Use one Hamiltonian builder for all controls.** Calibrated, free-boson, and
   hard-core variants differ through explicit parameters and basis rules, so
   special cases do not leak into observable code.
3. **Test invariants before image similarity.** Norm, total occupation,
   correlator sum rules, and limiting-model distances provide stronger failure
   signals than a visually plausible heatmap.
4. **Frequency units must be explicit.** Treating MHz as angular frequency
   changes the time scale by `2*pi`; the conversion belongs next to parameter
   ingestion and is tested through the velocity benchmark.
5. **A pixel audit is supplementary evidence.** Rasterization, anti-aliasing,
   missing experimental arrays, and absent author theory tables prevent an
   author-data identity claim even when theoretical panel interiors agree well.
6. **Compute backend is infrastructure, not physics.** CPU and A100 runs share
   the same model and are compared through numerical signatures, keeping
   hardware-specific behaviour outside the scientific rules.
