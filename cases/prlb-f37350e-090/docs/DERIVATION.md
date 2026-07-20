# Derivation

## 1. Literal pole sign

For `x=omega-Omega`, `omega_alpha=Omega-i gamma`, and `I=a+ib`,

$$
\operatorname{Im}\frac{I}{\omega-\omega_\alpha}
=\operatorname{Im}\frac{(a+ib)(x-i\gamma)}{x^2+\gamma^2}
=\frac{x b-\gamma a}{x^2+\gamma^2}.
$$

Thus the benchmark's explicit ansatz implies

$$
\boxed{\rho_p=\frac{2\epsilon_0\omega}{\pi}\sum_\alpha
\frac{(\omega-\Omega_\alpha)\operatorname{Im}I_\alpha-
\gamma_\alpha\operatorname{Re}I_\alpha}
{(\omega-\Omega_\alpha)^2+\gamma_\alpha^2}.}
$$

The frozen Task 1 numerator is exactly its negative. The paper avoids this contradiction because its projected Green tensor contains another external minus and its `I_alpha` is not the direct Green residue.

## 2. Distributional limit

Using `gamma/[pi(x^2+gamma^2)] -> delta(x)` and `Im I -> 0`, the literal prompt gives

$$
\boxed{\rho_p\longrightarrow-2\epsilon_0\omega
\sum_\alpha\operatorname{Re}I_\alpha\,
\delta(\omega-\Omega_\alpha).}
$$

The frozen positive delta weight belongs to the paper's normalized-intensity convention, not the benchmark's pole ansatz.

## 3. Radial rate

From the supplied power formula and `d^3k=4 pi k^2 dk`,

$$
\Gamma(\omega)=\frac{|p|^2\omega}{8\pi\epsilon_0\hbar}
\int_0^\infty k^2\rho_p(k,\omega)\,dk.
$$

The frozen prefactor `1/(32 pi)` is smaller by four.

## 4. Simple pole and subtraction

If `k^2 rho=R/(k-k_R)+O(1)`, the ordinary one-sided improper integrals diverge logarithmically. Task 4 is valid unless a Cauchy principal value is separately declared.

The benchmark defines

$$
\rho_{\rm reg}=\rho-\frac{R}{k-k_R}.
$$

Multiplying by `k^2` shows that the remaining pole residue is

$$
\boxed{R_{\rm remain}=R(1-k_R^2),}
$$

which is generically nonzero and is dimensionally incompatible. A cancellation would require subtracting `R/[k^2(k-k_R)]` from `rho`, or subtracting directly from `k^2 rho`.

## 5. Edge limit

The Puiseux law gives

$$
\left|\frac{d\Omega_+}{dk}\right|^{-1}
\sim\frac{2}{a}\sqrt{k_{\rm EP}-k},
$$

while `Re I -> J_EP sqrt(b)/sqrt(k_EP-k)`. Their product tends to `2 J_EP sqrt(b)/a`.

After retaining the literal signs and prefactors of Tasks 1-3, the signed edge contribution is

$$
\boxed{\Gamma_{\rm signed}=-
\frac{|p|^2\epsilon_0\Omega^4}{32\pi\hbar}
\frac{J_{\rm EP}\sqrt b}{a}.}
$$

Positive means decay and negative means excitation. Since the prompt states only `J_EP != 0`, its sign does not determine a unique nonnegative decay rate. The frozen formula also has incompatible `epsilon_0` and `Omega` powers.

Without Petermann divergence, the residue stays finite and the inverse slope forces the magnitude to zero, so Task 6 remains valid.

## 6. Toy model

At `omega=0.5-1e-9`, 80-digit arithmetic gives

$$
k(\omega)=0.99999999999999999975.
$$

For the specified positive `J_EP`, the literal delta term is negative: decay is zero and excitation is

$$
\Gamma_E=0.1722902791301488967980654485\ldots
$$

with magnitude limit `0.1722902798193100...`. This is eight times the frozen reported `0.02153628...` and 32 times the frozen Task 5 closed formula evaluated at `epsilon0=4`.
