# Public derivation summary

## Delayed-erasure information model

For every detected lossy qubit lifecycle, the paper enumerates compatible loss
times, cancels gates that occur after each possible loss, and builds a weighted
detector-error hypergraph. The production approximation sums the independently
constructed lifecycle models with the lossless Pauli model:

\[
D_{\mathrm{final}}=\sum_i D_i + D_{\mathrm{Pauli}}.
\]

The public Fig. 2(b) runner tests only the information-ordering mechanism. It
uses a distance-five repetition-code analogue and compares decoding without an
SSR flag, with a delayed SSR flag, and with perfect loss-time information. It is
not a surface-code or correlated-MLE implementation.

## Error-channel normalization

For a two-qubit entangling-gate error probability \(p_{CZ}\), the corresponding
per-qubit probability is

\[
p = 1-\sqrt{1-p_{CZ}}.
\]

The normalized loss fraction is \(L=p_{\mathrm{loss}}/p\), with the remaining
probability assigned to the selected Pauli channel.

## Lifecycle-threshold relation

Appendix H reports the non-SWAP loss-only fit

\[
p_{\mathrm{loss,th}}(\ell)=\frac{7}{\ell^{1/3}}\%,
\]

which the public code evaluates directly over \(1\leq\ell\leq16\). This is the
printed analytic trend; the unavailable finite-size markers are not claimed.

## Surface-code lifecycle counting

A rotated distance-\(d\) stabilizer round contains

\[
N_{\mathrm{CZ}}=4d(d-1)
\]

entangling gates. Counting gate endpoints and completed lifecycles gives the
data-, measure-, and all-qubit averages used for the Fig. 14(c) and Fig. 16(a)
feature checks. SWAP relabeling preserves the all-qubit endpoint count.

## Algorithm and Table-I counts

The Fig. 6(b) bars are evaluated from the Appendix-G lifecycle rules at
\(N_{\mathrm{GHZ}}=16\). Table I is evaluated for all seven methods at \(d=7\),
including the conventional space-time expression \(8d^3-4d\) and the
teleportation expression \(18d^3-6d\). Simulation-derived threshold and
effective-distance rows remain outside that analytic target.
