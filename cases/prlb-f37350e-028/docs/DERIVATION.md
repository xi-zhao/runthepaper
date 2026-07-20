# Derivation

## Task 1: stationary points and Morse indices

For `p=y`, write `K=omega_K`:

$$
U=-2K\lambda n_y-Kn_z^2.
$$

The constrained equations for `U+mu(n^2-1)` force `n_x=0`. Either `n_z=0`, giving `n_y=+-1`, or `mu=K`, giving

$$
(n_x,n_y,n_z)=(0,\lambda,\pm\sqrt{1-\lambda^2}),\qquad 0<\lambda\leq1.
$$

Near `+y`, tangent coordinates `(x,z)` give

$$
U=-2K\lambda+K\lambda x^2+K(\lambda-1)z^2+O(4).
$$

Thus `+y` is a saddle for `lambda<1`, a degenerate global minimum at `lambda=1`, and a global minimum for `lambda>1`. Near `-y` both tangent curvatures are negative, so it is always the global maximum. At each off-axis point the constrained Hessian eigenvalues are proportional to `1` and `1-lambda^2`, so both points are global minima, not saddles.

## Task 2: constrained MEP barrier

On the lower-maximal `n_y>=0` arc,

$$
n_y=\sin\theta,\quad n_z=\cos\theta,\quad
U(\theta)=-2K\lambda\sin\theta-K\cos^2\theta,
$$

and stationary points satisfy `cos(theta)(sin(theta)-lambda)=0`. Comparing endpoint, midpoint, and off-axis values gives

$$
\Delta U_{\rm MEP}=K\begin{cases}
(1-\lambda)^2,&0<\lambda\leq\tfrac12,\\
\lambda^2,&\tfrac12\leq\lambda\leq1,\\
2\lambda-1,&\lambda\geq1.
\end{cases}
$$

The competing `n_y<=0` arc has a strictly larger maximum for every positive `lambda`, so it cannot be the minimax MEP.

## Task 3: nonexistent interior saddle

With the stated tilt,

$$
\frac{U_\theta}{2K}=-\lambda\cos(\theta-\delta)+\sin\theta\cos\theta.
$$

For `lambda>1`, `theta=pi/2` has curvature `2K(lambda-1)>0`; it is the MEP minimum, while the MEP maximum is attained at an endpoint. Hence the requested “unique 1D saddle” does not exist. If one merely continues that interior minimum, implicit differentiation gives

$$
\theta'(0)=\frac{\lambda}{\lambda-1},\qquad
\left.\partial_\delta n_z\right|_0=-\frac{\lambda}{\lambda-1},
$$

not the frozen `1/(lambda^2-1)`.

## Task 4: exact rigid-precession branch

For `p=-z`, `theta` constant and `dot(phi)=Omega`,

$$
(p\times\dot n)\cdot n=(n\times p)\cdot\dot n=\Omega\sin^2\theta,
\qquad p\cdot n=-\cos\theta.
$$

Writing `c=cos(theta)`, the exact divided Euler-Lagrange-Rayleigh equations are

$$
c[\Omega^2+(1+\eta)\omega_F\Omega-2\omega_E\omega_K]
+\omega_E(1-\eta)\omega_F=0,
$$

$$
2\alpha\Omega-\omega_D[(1+\eta)+(1-\eta)c\Omega/\omega_E]=0.
$$

For sufficiently large nonzero `Omega`, choose

$$
c=-\frac{\omega_E(1-\eta)\omega_F}
{\Omega^2+(1+\eta)\omega_F\Omega-2\omega_E\omega_K},
\qquad
\omega_D=\frac{2\alpha\Omega}{(1+\eta)+(1-\eta)c\Omega/\omega_E}.
$$

Then `|c|<1`, `omega_D` is nonzero, and both residuals vanish. At `(omega_E,omega_K,omega_F,eta,alpha,Omega)=(100,1,1,0,0.1,20)`, one obtains `c=-5/11`, `omega_D=4.4`, and both residuals are exactly zero. The final answer is **Yes**.
