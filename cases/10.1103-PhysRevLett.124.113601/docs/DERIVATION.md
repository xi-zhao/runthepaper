# Core derivation

The public calculation starts from the finite Aubry–André Hamiltonian

\[
H_0=-J\sum_j(c_j^\dagger c_{j+1}+\mathrm{h.c.})
   +\chi\sum_j\cos(2\pi\gamma j)\,n_j,
\]

and the generalized model used in Fig. 2 adds the printed next-nearest,
hopping-modulation, and disorder-modulation terms.  The cavity mode couples
through the profile \(\cos(2\pi\gamma_c j)\).  For a normalized eigenstate
\(|\psi_\alpha\rangle\), the response is evaluated from the scattering
matrix elements

\[
s_{\alpha\beta}=\langle\psi_\alpha|\cos(2\pi\gamma_c j)|\psi_\beta\rangle
\]

and excitation denominators \(\epsilon_\beta-\epsilon_\alpha\).  The critical
pump follows from the linear cavity susceptibility.  The nonlinear branches
are obtained by iterating the atomic ground state and the steady cavity field
until both the orbital and cavity amplitude converge.

The important convention is target-local.  Fig. 2 uses the exact golden ratio,
periodic boundaries, and a one-site phase origin; this reproduces all 377 IPR
samples visible in the PDF vector path.  Supplement Fig. S1 uses open
boundaries and a separately reconstructed finite-chain origin because the
supplement does not publish its pump samples or phase convention.

The published text and the arXiv/source curve differ in one detuning-shift
factor.  The linear plots use the source-curve-selected convention; nonlinear
Fig. 4(a) uses the literal published steady-state equation.  This split is
recorded explicitly and is why Fig. 4 remains a paper-subset result.
