# Independent derivation

## 1. Tensor index

For `a(tau) proportional to |tau|^(1+beta)`, the 2016 source gives
`n_t=2 beta+4` and `epsilon=(beta+2)/(beta+1)`. Solving the latter for
`beta` and substituting into the former yields

$$
n_t=-\frac{2\epsilon}{1-\epsilon}.
$$

## 2. Transition asymptotics

The high-frequency WKB reflection from a finite step in
`U=a''/a` is

$$
\beta_k=\frac{U(\tau_1^-)-U(\tau_1^+)}{4k^2}e^{i\phi}
 + O(k^{-3}).
$$

Squaring gives the `k^-4` graviton-number tail. Moving the first discontinuity
to a higher derivative makes the tail decay faster.

## 3. Fourth-order amplitude and stress tensor

Set `t=-tau`, `V=m^2a^2-a''/a`, and solve the Riccati WKB equation through
fourth adiabatic order:

$$
W=k+\frac{V}{2k}-\frac{V^2+V''}{8k^3}+O(k^{-5}),
$$

$$
|u|^2=\frac{1}{2k}\left[1-\frac{V}{2k^2}
 +\frac{3V^2+V''}{8k^4}+O(k^{-6})\right].
$$

For `a=t^(1+beta)`, this expands exactly to the frozen amplitude. The same mode
also obeys

$$
\left|u'-\frac{a'}a u\right|^2
=|u|^2\left[W^2+\left(\frac{W'}{2W}+\frac{a'}a\right)^2\right].
$$

Substitution into the exact minimally coupled `rho_k,p_k` definitions yields
the corrected brackets written in `GOLD_AUDIT.md`. Their mass powers differ
from the frozen counterterms; in particular the frozen `m^2t^(3+beta)` terms
cannot arise from `m^2a^2=m^2t^(2+2beta)` under this substitution.

## 4. Massless residual equation of state

After fourth-order subtraction, let the common high-frequency factor be

```text
F = 5(beta-1)beta(beta+1)(beta+2)(beta+3)/(32 tau^6).
```

The derivative and gradient residuals combine as
`rho_re=2F(beta+1)` and `p_re=2F(beta+7)/3`, up to their common positive
spectral prefactor. Therefore

$$
w_{\rm scalar}=\frac{\beta+7}{3(\beta+1)}.
$$

The RGW source independently gives
`w_RGW=(beta-2)/(3(beta+4))`. Solving these rational equations gives the
fixed points recorded in the gold audit.

## 5. Reproduced source Fig. 2

For the source's `beta=-2`, the Hankel functions reduce to elementary forms.
With `x=|k tau|`:

$$
n_t(x)=\frac{2x^2}{1+x^2},\qquad
\alpha_t(x)=\frac{4x^2}{(1+x^2)^2}.
$$

They give `(0,0)` at `x=0`, `(1,1)` at `x=1`, and `(1.8,0.36)` at `x=3`,
exactly reproducing the paper curve geometry.
