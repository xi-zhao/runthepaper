# Equation-level derivation

This document collects every equation used by the public reproduction of
arXiv:2607.15597. Status labels distinguish equations verified from the
manuscript from reconstructed feature models and source-only projections.

## Conditional atom-ion gate

### EQC001 — state-dependent forces (`verified`)

Expanding the charge-induced-dipole potential

\[
V=-C_4(d+x_i-x_a)^{-4}
\]

to first order gives the displacement coupling
\(4C_4d^{-5}(x_i-x_a)\). After matching it to the optical Magnus force,
the four logical branches use the ion/atom force pairs

\[
(q,0),\quad(-q,0),\quad(2q,-q),\quad(0,-q),
\qquad q=\omega_g/\omega.
\]

Implementation: `code/src/gate_model.py::branch_forces`.

### EQC002 — forced oscillator (`verified`)

For a constant dimensionless force \(f\) and \(\theta=\omega t\),

\[
\alpha_f=f(1-e^{i\theta}),\qquad
\phi_f=f^2(\theta-\sin\theta).
\]

At every integer period, \(\alpha_f=0\), while the enclosed phase-space area
remains as the geometric phase. Implementation:
`code/src/gate_model.py::displacement` and `::geometric_phase`.

### EQC003 — CZ operating point (`verified`)

The branch-phase invariant after one trap period is

\[
\Phi_{CZ}=-8\pi q^2.
\]

Thus \(q=1/(2\sqrt2)\) gives \(\Phi_{CZ}=-\pi\), up to removable local
single-qubit phases. Implementation: `code/src/gate_model.py::GateParameters`.

### EQC004 — motion-traced spin state (`verified`)

For the equal four-branch input and two motional modes,

\[
\rho_{jk}=\frac14 e^{i(\phi_j-\phi_k)}
\exp\!\left[-\frac12\sum_m|\alpha_{jm}-\alpha_{km}|^2\right].
\]

The reproduction evaluates rotated-basis populations and Wootters
concurrence from this density matrix. Implementation:
`code/src/gate_model.py::reduced_spin_state` and `::concurrence`.

### EQC005 — process-averaged decay (`verified`)

Only half the equal computational input occupies the Rydberg branch, so

\[
\epsilon_{decay}=\frac12(1-e^{-T/\tau_r}).
\]

Implementation: `code/src/gate_model.py::decay_infidelity`.

### EQC012 — CZ distance (`verified`)

Combining the matched force with the CZ condition gives

\[
d_{CZ}=\left(8\sqrt2 C_4\ell_i/(\hbar\omega)\right)^{1/5}.
\]

Implementation: `code/src/gate_model.py::cz_distance_m`.

## Multi-ion and thermal models

### EQC011 — simultaneous mode closure (`verified`)

For a piecewise constant toggle sequence, every normalized mode \(\nu_m\)
closes when

\[
\sum_j s_j\left(e^{i\nu_m\tau_{j+1}}-e^{i\nu_m\tau_j}\right)=0.
\]

Positive segment durations are represented by softmax variables and optimized
against all ten complex residuals. Implementation:
`code/src/ion_chain.py::optimize_toggle_schedule`.

### EQC006 — anharmonic thermal feature model (`reconstructed`)

The disclosed frequency shift and checkpoints are represented by

\[
\epsilon_{anh}=\epsilon_0+\frac12\frac{x^2}{1+x^2},\qquad
x=10\pi\eta q(\bar n+1/2).
\]

This preserves the low-occupation \(\eta^2\) scaling but is not the author's
unreleased five-order QuTiP sweep. Implementation:
`code/src/gate_model.py::anharmonic_infidelity`.

### EQC007 — chain-duration contract (`reconstructed`)

The manuscript states a 5 microsecond plateau through \(N=25\), linear growth,
and the \(N=100\) endpoint. The minimum matching surrogate is

\[
T_g(N)=5\ \mu s\quad(N\le25),\qquad
T_g(N)=5+10(N-25)/75\ \mu s\quad(N>25).
\]

Implementation: `code/src/gate_model.py::chain_gate_duration_us`.

### EQC013 — circular-state error floor (`source_only`)

\[
\epsilon_{circ}=\frac12(1-e^{-T/\tau_{circ}})
+\epsilon_{anh}(\eta_{circ},\bar n)+\epsilon_{tech}.
\]

The lifetimes, polarizabilities, and technical floors are manuscript inputs;
they are not new atomic-structure calculations. Implementation:
`code/src/gate_model.py::total_gate_infidelity`.

## Architecture projections

### EQC008 — interconnect timing (`reconstructed`)

\[
t_{hyb}=2T+L/v,\qquad t_{ph}=1/R_{ph},\qquad
t_{ion}=600+5L\quad[\mu s].
\]

The hybrid and photon terms use disclosed parameters. The compact ion-QCCD
law is reconstructed because no transport equation is supplied.

### EQC009 — passive-memory amortization (`verified`)

One write and one read cost \(2p_T\), hence

\[
p_{hybrid/op}=2p_T/N_{ops}.
\]

Its derivative is negative. The manuscript raster visually slopes in the
opposite direction, so the scientific reproduction follows the stated formula
and records the conflict separately.

### EQC010 — qLDPC Fowler projection (`source_only`)

\[
p_L(d)=A_{BB}(p_{eff}/p_{th})^{(d+1)/2}.
\]

The public result regenerates the disclosed projection curves and 66-fold
herald factor. It does not claim to rerun the unavailable circuit-level Monte
Carlo anchors.

For the longer reasoning chain, see [DERIVATION_TRACE.md](DERIVATION_TRACE.md).
