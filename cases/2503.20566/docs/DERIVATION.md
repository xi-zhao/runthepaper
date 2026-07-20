# Derivation

For charge-free open-boundary pure gauge theory, a lattice of LxL vertices has
(L-1)^2 independent plaquette variables. An interior electric link is the
difference/product of its two adjacent plaquette variables; a boundary link
touches one. This gives dimensions 3^16 for the 5x5 Z3 target and 2^25 for the
6x6 Z2 target.

For the pure-gauge targets, the implemented Hamiltonian is

$$
H=-h\sum_{\ell}P_{\ell}-g\sum_{p}\left(Q_p+Q_p^\dagger\right),
$$

where $P_\ell$ is diagonal in the electric basis and $Q_p$ applies the oriented
plaquette cycle. In the $\mathbb Z_2$ case $Q_p=Q_p^\dagger$, so the frozen
normalization is implemented as one plaquette-flip term per plaquette rather
than counting it twice.

The first benchmark target is evaluated by the same centered finite-difference
stencil encoded in the frozen record,

$$
E'(g)\simeq \frac{E(g+\delta)-E(g-\delta)}{2\delta},\qquad
E''(g)\simeq \frac{E(g+\delta)-2E(g)+E(g-\delta)}{\delta^2}.
$$

Odd Z2 is the same plaquette orbit over a reference electric field with one
occupied horizontal dimer incident on every vertex. Its electric signs make the
dual Ising model fully frustrated. For dynamical matter, each half-filled matter
mask receives a spanning-tree Gauss-law reference field; the nine plaquette
cycles span the remaining gauge freedom, giving C(16,8) x 2^9 = 6,589,440
physical states. Gauge-dressed hopping changes the matter mask and a uniquely
determined plaquette-cycle mask.

The physical-space reduction used by the matter solver is therefore

$$
\dim\mathcal H_{\rm phys}=\binom{16}{8}2^{(4-1)^2}
=12{,}870\times512=6{,}589{,}440.
$$
