# Derivation

## OBC eigenpairs

For the tridiagonal OBC matrix with diagonal `Delta`, upper hopping `J_+`, and lower hopping `J_-`, write

`J_- psi[j-1] + (Delta-lambda) psi[j] + J_+ psi[j+1] = 0`.

The two bulk roots satisfy `z1 z2 = J_-/J_+`. Boundary cancellation gives `theta_m=pi m/(N+1)`. With `r^2=|J_-/J_+|` and `delta=arg(J_-/J_+)`, the source eigenvector is

`psi_m,j = r^j exp(i delta j/2) sin(j theta_m)`.

$$
\theta_m=\frac{\pi m}{N+1},\qquad
(\psi_m)_j=r^j e^{i\delta j/2}\sin(j\theta_m),\qquad
r^2=\left|\frac{J_-}{J_+}\right|.
$$

For `theta=pi`, this phase/sign factor matters. When `gamma>J`, `J_-/J_+<0`, so `exp(i delta j/2)=i^j`; it cannot be absorbed into one global phase. When `gamma<J`, the frozen positive-real vector is paired with the wrong sign label. Direct residuals separate the correct and frozen pairs.

## Vacuum threshold

For `gamma<J`, every OBC eigenvalue has imaginary part `kappa-2 gamma`, so `kappa_c=2 gamma`. For `gamma>J`, mode `m=1` destabilizes first:

`kappa_c(N)=2 gamma-2 sqrt(gamma^2-J^2) cos(pi/(N+1))`.

$$
\kappa_c(N)=
\begin{cases}
2\gamma, & \gamma<J,\\
2\gamma-2\sqrt{\gamma^2-J^2}\cos\!\left(\frac{\pi}{N+1}\right), & \gamma>J.
\end{cases}
$$

The thermodynamic limit follows by replacing the cosine by one.

## Static bulk branches and PH symmetry

At `theta=pi`, a static plane wave requires `omega_q=-2J cos(q)=0`, hence `q=+pi/2` or `q=-pi/2`. Their densities are `kappa/Gamma` and `(kappa-4 gamma)/Gamma`, respectively. The second is nonzero for `kappa>4 gamma`.

$$
\rho^2_{+\pi/2}=\frac{\kappa}{\Gamma},\qquad
\rho^2_{-\pi/2}=\frac{\kappa-4\gamma}{\Gamma}>0
\quad\Longleftrightarrow\quad \kappa>4\gamma.
$$

For `alpha_j=r exp(i q j)`, the ratio `PH[alpha_j]/alpha_j` is site independent for both momenta. Thus PH compatibility does not uniquely select `q=+pi/2`.

## Frozen CEP protocol

The frozen rule first requires `||dot(alpha)||/sqrt(N)<1e-8`. Only accepted states may receive a finite-difference Jacobian and a CEP test. At frozen `kappa=2.38930`, the residual is `0.07712817`, so the point fails before eigenanalysis. The first accepted grid point is `2.38937`; there `lambda_2=-0.00377748` and the first two SVD nullities are `(1,1)`, not the required `(1,2)`.

$$
R(2.38930)=7.712817\times10^{-2}>10^{-8},\qquad
\operatorname{Re}\lambda_2(2.38937)=-3.77748\times10^{-3}\notin[-10^{-5},10^{-5}].
$$
