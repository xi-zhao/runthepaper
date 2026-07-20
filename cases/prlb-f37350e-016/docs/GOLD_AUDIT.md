# Frozen-gold audit

## Task 1 — valid

For \(\Delta_{\mathbf k}=\Delta_0\cos2\varphi\), \(\Delta_0=30\) meV and \(\varphi=\pi/8\),

\[
\Delta_{\mathbf k}=21.2132034\ \mathrm{meV}.
\]

With \(\omega=50\) meV and \(\xi=15\) meV, the denominator is 1825 meV\(^2\), yielding

\[
G^{(0)}=\begin{pmatrix}
0.0356164&0.0116237\\
0.0116237&0.0191781
\end{pmatrix}\mathrm{meV}^{-1}.
\]

This agrees with the frozen rounded matrix.

## Task 2 — valid only with explicit convention

Using the frozen cutoff convention,

\[
g_0(\omega+i0^+)=-\frac{2\omega}{\pi\Delta_0}\ln\frac{2\Delta_0}{|\omega|}
-i\frac{|\omega|}{\Delta_0},
\]

gives \(-0.0996188-0.04i\) at 1.2 meV. The number is correct. Two qualifications are required:

- this normalized `g0` is dimensionless; it is not the same dimensional object as Task 1;
- the direct RMP source uses a `4 Delta0 / omega` cutoff and, as printed for positive real frequency, the opposite imaginary-part convention. It gives \(-0.1172697+0.04i\). The cutoff constant is scheme dependent, but the sign convention must also be named rather than silently merged.

The off-diagonal cancellation is exact under a C4-symmetric band/Fermi-surface integration and a symmetry-preserving nodal cutoff. It is not an unconditional statement for arbitrary asymmetric patches.

## Task 3 — invalid

The frozen algebra evaluates its printed expression to

\[
|\Omega|=4.484506\ \mathrm{meV},
\]

not meV\(^{-1}\). More importantly, placing the resonance on the physical sign branch, \(\Omega=-4.484506\) meV, and substituting it into the frozen Task 2 propagator gives

\[
g_0(\Omega)=0.2468289-0.1494835i,
\qquad
g_0(\Omega)-c=-0.0531711-0.1494835i.
\]

Thus the reported value does not solve \(g_0(\Omega)=0.3\). Its residual magnitude is 0.15866.

The frozen real expression can be reconstructed as the real part of a fixed-log complex approximation. The discarded pole is

\[
\Omega_{\rm frozen\ proxy}=(-4.4845-4.8731i)\ \mathrm{meV},
\]

so \(|\Omega''/\Omega'|=1.087\): there is no narrow, well-resolved resonance. The direct RMP logarithmic approximation gives

\[
\Omega_{\rm RMP}=(-6.6102-4.8550i)\ \mathrm{meV},
\]

with \(|\Omega''/\Omega'|=0.734\). At \(c=0.3\), its controlling logarithm is only 2.139, not \(\gg1\) as required by the source.

As a diagnostic only, solving the real part of the frozen cutoff-2 equation on its low-energy branch gives 6.25091 meV. A real-axis root is not the correct complex resonance pole, but its 1.77 meV disagreement is another direct demonstration that 4.484 is not an "exact" solution of the stated transcendental equation.

## Terminal verdict

`benchmark_gold_invalid`: Tasks 1-2 survive; Task 3 and the paper-source contract do not.
