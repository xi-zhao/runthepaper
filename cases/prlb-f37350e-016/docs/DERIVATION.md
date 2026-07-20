# Derivation

## Clean matrix

Inverting \(\omega\sigma_0-\xi\sigma_3-\Delta\sigma_1\) gives

$$
G^{(0)}(\mathbf k,\omega)=
\frac{\omega\sigma_0+\xi_{\mathbf k}\sigma_3+\Delta_{\mathbf k}\sigma_1}
{\omega^2-\xi_{\mathbf k}^2-\Delta_{\mathbf k}^2}.
$$

This is the dimensional momentum-resolved Green function used in Task 1.

## Local nodal propagator

Linearizing \(\xi\) and \(\Delta\) around four d-wave nodes produces four anisotropic Dirac cones. Under a symmetry-preserving integration, the gap-odd \(\sigma_1\) numerator changes sign between C4-related sectors and cancels. After normalizing out the normal-state density of states, the remaining scalar term has logarithmic real and linear imaginary parts:

$$
g_0(\omega+i0^+)=-\frac{2\omega}{\pi\Delta_0}
\ln\frac{C\Delta_0}{|\omega|}-i\frac{|\omega|}{\Delta_0}.
$$

The frozen record fixes \(C=2\); RMP Eq. `impdwave3` uses \(C=4\).
The RMP expression also prints the opposite positive-frequency imaginary sign;
the audit preserves each convention separately instead of treating the two
expressions as identical.

## Pole audit

For a scalar impurity, \(T_{11}=1/[c-g_{11}]\), so a resonance is a complex zero of \(c-g_{11}(\Omega)\). The RMP solves this only to logarithmic accuracy:

$$
\Omega=-\Delta_0\frac{\pi c/2}{\ln[8/(\pi c)]}
\left(1+\frac{i\pi}{2\ln[8/(\pi c)]}\right).
$$

The frozen expression instead rationalizes a fixed logarithm and retains only the real part. Substituting that real part into the original (g_0) is therefore the decisive consistency test; it fails at the requested parameter.
