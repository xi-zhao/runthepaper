# Derivation

## 1. Rotating-frame spectrum

Writing `xi=g exp(i phi)` and removing the pump and coupling phases gives

$$
\dot u=A u,\qquad
A=\begin{pmatrix}-\lambda-i\delta&g\\g&-\lambda+i\delta\end{pmatrix}.
$$

Therefore

$$
\mu_\pm=-\lambda\pm\chi,\qquad \chi=\sqrt{g^2-\delta^2},
$$

on the principal branch. Exponential instability is exactly

$$
g^2>\lambda^2+\delta^2.
$$

For `|delta| >= g`, the splitting is imaginary and both real parts equal `-lambda`; hence the sharp uniform-stability detuning cut is `|delta|=g`.

## 2. Physical finite-time gain

Set `A=-lambda I+B`; then `B^2=chi^2 I` and

$$
e^{AT}=e^{-\lambda T}(cI+sB),
$$

where, for real splitting, `c=cosh(chi T)` and `s=sinh(chi T)/chi`; for imaginary splitting these continue to `cos(omega T)` and `sin(omega T)/omega`.

For the physical initial vector `(z,z*)`, the first component is

$$
\sigma(T)=e^{-\lambda T}\left[(c-i\delta s)z+gsz^*\right].
$$

The identity `|c-i delta s|^2=1+g^2s^2` yields the exact phase optimum

$$
\boxed{\mathcal G(T)=e^{-2\lambda T}
\left(\sqrt{1+g^2s(T)^2}+|g s(T)|\right)^2.}
$$

The absolute value is physical: in the oscillatory regime the maximizing input phase switches whenever `sin(omega T)` changes sign. The frozen Task 3 expression instead contains `lambda/chi` and is neither this phase optimum nor a valid global continuation.

## 3. Interior transient peak

For real positive `chi`, define `x=(g/chi)sinh(chi T)`. Then

$$
\log \mathcal G=-2\lambda T+2\operatorname{asinh}x.
$$

The stationary condition gives

$$
\sinh^2(\chi T_\star)=
\frac{\chi^2(g^2-\lambda^2)}{g^2(\lambda^2-\chi^2)}.
$$

Thus stability `chi<lambda` is insufficient: a positive interior peak exists only when `g>lambda`. When it exists,

$$
\boxed{T_\star=\frac{1}{\chi}\operatorname{asinh}\left[
\frac{\chi}{g}\sqrt{\frac{g^2-\lambda^2}{\lambda^2-\chi^2}}
\right],}
$$

and `G(T_star)` is obtained by substituting this exact time into the boxed gain. At `lambda=1`, `g=0.9`, `delta=0.6`, all frozen assumptions hold but no positive peak exists. At `g=1.1`, the exact peak is `(0.9496056902, 1.1175693580)`; the frozen time `1.7375073233` is not stationary.

## 4. Vacuum occupation

At resonance and real pump, the moment equations are

$$
\dot n=-2\lambda n+g(m+m^*),\qquad
\dot m=-2\lambda m+g(2n+1),
$$

where `n=<b†b>` and `m=<bb>`. The unique stable solution is

$$
\boxed{n=\frac{g^2}{2(\lambda^2-g^2)}=\frac{r^2}{2(1-r^2)}.}
$$

The frozen Task 5 result is exactly twice too large.

## 5. High-precision threshold

With the frozen parameters,

$$
\alpha=\Gamma\kappa+|G_{29}|^2N=1405,\qquad
\lambda=\frac{16}{1405},\qquad |\xi|_{\rm crit}=\lambda\sqrt{1+0.7^2}.
$$

Inverting the two-photon coefficient gives

$$
|G_{38}\Omega_{28}|_{\rm crit}=
\frac{|\xi|_{\rm crit}\alpha\sqrt{\Gamma^2+\Delta_8^2}}
{N|\Omega_{39}||G_{29}|}
=2.1026760061563297316841976613\ldots
$$

The frozen decimal differs by `1.2835580e-16`, safely below the requested `1e-12` tolerance.
