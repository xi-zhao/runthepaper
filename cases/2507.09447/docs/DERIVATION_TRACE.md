# Derivation trace

## Finite-range Hamiltonian

For hopping range `M=2`, the real-space equation is

```text
t_2 psi_(n+2) + t_1 psi_(n+1) + (t_0(n)-E) psi_n
+ t_-1 psi_(n-1) + t_-2 psi_(n-2) = 0.
```

Solving for `psi_(n+2)` produces a four-dimensional companion transfer matrix.
The product of these matrices defines four ordered Lyapunov exponents
`gamma_1 <= gamma_2 <= gamma_3 <= gamma_4` after repeated QR stabilization.

## Thouless potentials

For the convention used by the code, the two potentials are

```text
Phi_OBC(E) = log|t_2| + gamma_3(E) + gamma_4(E)
Phi_PBC(E) = log|t_2| + sum_s max(gamma_s(E), 0).
```

Applying the two-dimensional Laplacian to either potential yields the
corresponding spectral density. The OBC expression fixes the number of growing
directions, whereas the PBC expression changes whenever a Lyapunov exponent
crosses zero.

## State and topology rules

- `gamma_2 < 0 < gamma_3`: Anderson-localized state.
- A central exponent at zero: unidirectional critical state or mobility edge.
- Central exponents with the same sign: skin state.
- With `M=2`, the winding is `nu = 2 - n_positive`, where `n_positive` counts
  positive Lyapunov exponents.

The implementation is in
[`lyapunov_band.py`](../code/src/lyapunov_band.py), and the numeric acceptance
results are in
[`paper_scientific_similarity.json`](../outputs/checks/paper_scientific_similarity.json).
