# Equation Cards

This file is the first derivation layer for the paper. Code and numerical
targets should point back to these cards instead of reinterpreting the PDF each
time.

## EQC001: Bloch Hamiltonian

- Source: `nonHermitian.tex`, model section, Eq. label `nHSSH`
- Status: `derived`
- Used by: DU001, NT001, NT003, NT006

Paper equation:

```text
H(k) = d_x sigma_x + (d_y + i gamma/2) sigma_y
d_x = t1 + (t2 + t3) cos(k)
d_y = (t2 - t3) sin(k)
```

Using

```text
sigma_x = [[0, 1], [1, 0]]
sigma_y = [[0, -i], [i, 0]]
```

the matrix form is

```text
H(k) = [[0, d_x - i(d_y + i gamma/2)],
        [d_x + i(d_y + i gamma/2), 0]]
```

For the first part of the paper, `t3 = 0`, so

```text
d_x - i d_y = t1 + t2 exp(-ik)
d_x + i d_y = t1 + t2 exp(+ik)
```

and

```text
H(k) = [[0, t1 + gamma/2 + t2 exp(-ik)],
        [t1 - gamma/2 + t2 exp(+ik), 0]]
```

Numerical form:

- periodic Bloch spectrum uses this `2 x 2` matrix;
- open-chain real-space matrix is obtained by replacing the phase factors with
  nearest-neighbor hopping.

## EQC002: Bloch Eigenvalues and Exceptional Points

- Source: model section immediately after `nHSSH`
- Status: `derived`
- Used by: DU001, comparison markers in NT001

Because `H(k)` is off-diagonal and chiral,

```text
E_+(k), E_-(k) = +/- sqrt(d_x^2 + (d_y + i gamma/2)^2)
```

The Bloch gap closes when `E = 0`. With real `d_x, d_y`,

```text
d_x^2 + (d_y + i gamma/2)^2 = 0
```

requires

```text
d_y = 0
d_x = +/- gamma/2
```

For `t3 = 0`, `d_y = t2 sin(k)`, so the relevant high-symmetry momenta are
`k = 0` and `k = pi`. This gives:

```text
k = pi: t1 = t2 +/- gamma/2
k = 0:  t1 = -t2 +/- gamma/2
```

Numerical form:

- These are Bloch-theory reference markers only.
- They are not the true open-boundary zero-mode transition.

## EQC003: Open-Chain Real-Space Equations

- Source: generalizable solution section
- Status: `derived`
- Used by: DU002, NT001, NT002, NT005

From EQC001 at `t3 = 0`, the real-space open-chain bulk equations are:

```text
t2 psi_{n-1,B} + (t1 + gamma/2) psi_{n,B} = E psi_{n,A}
(t1 - gamma/2) psi_{n,A} + t2 psi_{n+1,A} = E psi_{n,B}
```

The finite open-chain Hamiltonian in basis
`(A1, B1, A2, B2, ..., AL, BL)` therefore has:

```text
H[A_n, B_n]     = t1 + gamma/2
H[B_n, A_n]     = t1 - gamma/2
H[A_n, B_{n-1}] = t2
H[B_n, A_{n+1}] = t2
```

Numerical form:

- implemented by `src/nonhermitian_ssh.py::open_chain_hamiltonian`;
- spectrum for NT001 uses the chiral block structure of this matrix.

## EQC004: Similarity Transform Shortcut

- Source: shortcut solution section
- Status: `derived_for_t3_zero`
- Used by: DU003, DU004, NT001 checks

Define the diagonal similarity transform

```text
bar H = S^{-1} H S
S = diag(1, r, r, r^2, r^2, ..., r^{L-1}, r^{L-1}, r^L)
```

With the basis above, this gives transformed intracell hoppings:

```text
B_n -> A_n: r (t1 + gamma/2)
A_n -> B_n: r^{-1} (t1 - gamma/2)
```

Choose

```text
r = sqrt(|(t1 - gamma/2) / (t1 + gamma/2)|)
```

For the branch where `|t1| > |gamma/2|`, this maps the asymmetric intracell
hoppings to an effective SSH hopping magnitude

```text
bar t1 = sqrt((t1 - gamma/2)(t1 + gamma/2))
bar t2 = t2
```

The effective Bloch Hamiltonian is

```text
bar H(k) = (bar t1 + t2 cos(k)) sigma_x + t2 sin(k) sigma_y
```

Numerical form:

- this explains why direct Bloch markers fail for the open chain;
- it gives the analytic transition used in NT001 checks.

## EQC005: Open-Boundary Transition

- Source: shortcut solution and beta-root discussion
- Status: `derived`
- Used by: DU004, NT001, NT006

The standard SSH transition occurs at

```text
bar t1 = bar t2
```

Using EQC004:

```text
(t1 - gamma/2)(t1 + gamma/2) = t2^2
```

so

```text
t1 = +/- sqrt(t2^2 + (gamma/2)^2)
```

For Fig. 2 parameters:

```text
t2 = 1
gamma = 4/3
|t1| = sqrt(1 + (2/3)^2) = 1.201850425...
```

Numerical form:

- used as a physics check for Fig. 2;
- not estimated by fitting the finite-size plot.

## EQC006: Beta Ansatz and Bulk Equation

- Source: generalizable solution, Eq. labels `ansatz`, `bulkeigen`, `betazero`
- Status: `derived`
- Used by: DU005, NT003, NT004

Use the exponential ansatz

```text
(phi_{n,A}, phi_{n,B}) = beta^n (phi_A, phi_B)
```

Substituting into EQC003 gives

```text
[(t1 + gamma/2) + t2 beta^{-1}] phi_B = E phi_A
[(t1 - gamma/2) + t2 beta] phi_A = E phi_B
```

Eliminating `phi_A, phi_B` gives

```text
[(t1 - gamma/2) + t2 beta]
[(t1 + gamma/2) + t2 beta^{-1}] = E^2
```

Multiplying by `beta` gives a quadratic in `beta`, with roots:

```text
beta_{1,2}(E) =
[E^2 + gamma^2/4 - t1^2 - t2^2
 +/- sqrt((E^2 + gamma^2/4 - t1^2 - t2^2)^2
          - 4 t2^2 (t1^2 - gamma^2/4))]
/
[2 t2 (t1 + gamma/2)]
```

In the `E -> 0` limit:

```text
beta_1 = -(t1 - gamma/2) / t2
beta_2 = -t2 / (t1 + gamma/2)
```

Numerical form:

- Fig. 3(a) can be generated from these beta roots;
- the zero-energy limit is used to re-derive the transition.

## EQC007: Generalized Brillouin Zone for t3 = 0

- Source: generalizable solution, Eq. label `bulkbeta`
- Status: `derived`
- Used by: DU006, NT004, NT006

For bulk states in a long open chain, the boundary equation requires:

```text
|beta_1(E)| = |beta_2(E)|
```

The product of roots from EQC006 is

```text
beta_1 beta_2 = (t1 - gamma/2) / (t1 + gamma/2)
```

Therefore the generalized Brillouin zone is the circle:

```text
|beta| = r = sqrt(|(t1 - gamma/2) / (t1 + gamma/2)|)
beta = r exp(i k)
```

Numerical form:

- Fig. 3(b) is generated from this circle for `t1 = 1`;
- open-boundary bulk spectra can be computed by substituting `beta = r exp(i k)`.

## EQC008: Open-Boundary Bulk Spectrum

- Source: equation label `spectra`
- Status: `derived`
- Used by: NT003 and finite-size checks

Substitute `beta = r exp(i k)` into EQC006. The paper gives:

```text
E^2(k) =
t1^2 + t2^2 - gamma^2/4
+ t2 sqrt(|t1^2 - gamma^2/4|)
  [sgn(t1 + gamma/2) exp(i k) + sgn(t1 - gamma/2) exp(-i k)]
```

The gap-closing condition of this spectrum gives the same transition as EQC005.

Numerical form:

- can generate thermodynamic-limit curves for comparison with finite open-chain
  eigenvalues.

## EQC009: Non-Bloch Hamiltonian and Winding Number

- Source: non-Bloch topological invariant section
- Status: `derived_for_t3_zero`
- Used by: DU007, DU008, NT006

The non-Bloch Hamiltonian is obtained from the Bloch Hamiltonian by

```text
exp(i k) -> beta
exp(-i k) -> beta^{-1}
```

For `t3 = 0`:

```text
H(beta) =
(t1 - gamma/2 + beta t2) sigma_-
+ (t1 + gamma/2 + beta^{-1} t2) sigma_+
```

Define

```text
a(beta) = t1 - gamma/2 + beta t2
b(beta) = t1 + gamma/2 + beta^{-1} t2
```

Then

```text
H(beta) = [[0, b(beta)],
           [a(beta), 0]]
E(beta)^2 = a(beta) b(beta)
```

The paper defines biorthogonal right/left eigenvectors and a `Q(beta)` matrix.
For the two-band chiral form this can be derived without choosing a continuous
eigenvector gauge. Let `P_+ = |u_R><u_L|` and
`P_- = |tilde u_R><tilde u_L|`. Since

```text
H = E P_+ - E P_-
```

and the paper defines

```text
Q = P_- - P_+
```

we have the flattened Hamiltonian identity

```text
Q(beta) = -H(beta) / E(beta)
```

Therefore

```text
Q(beta) = [[0, q(beta)],
           [q(beta)^{-1}, 0]]
q(beta)      = -b(beta) / E(beta)
q(beta)^{-1} = -a(beta) / E(beta)
```

The winding is

```text
W = (i / 2 pi) integral_{C_beta} q^{-1} dq
```

Because `q = -sqrt(b/a)` up to a continuous branch choice, the same winding can
be computed without explicitly tracking the square-root branch:

```text
W = (wind[a(beta)] - wind[b(beta)]) / 2
```

where both winds are measured as `beta` traverses `C_beta` counterclockwise.
This gives `W = 1` in the zero-mode region and `W = 0` outside it for the Fig. 2
parameters.

Numerical form:

- use `beta = r exp(i k)` with `r` from EQC007;
- compute either the unwrapped phase of `q(beta)` or the branch-free winding
  difference of `a(beta)` and `b(beta)`;
- avoid direct eigenvector phase tracking, because it introduces gauge
  discontinuities.

## EQC010: Nonzero t3 Beta Equation

- Source: supplemental nonzero `t3` section, Eq. label `t3E`
- Status: `derived_beta_quartic`
- Used by: NT007, NT008

For nonzero `t3` the bulk equations become:

```text
[t2 beta^{-1} + (t1 + gamma/2) + t3 beta] phi_B = E phi_A
[t3 beta^{-1} + (t1 - gamma/2) + t2 beta] phi_A = E phi_B
```

and

```text
E^2 =
[t2 beta^{-1} + (t1 + gamma/2) + t3 beta]
[t3 beta^{-1} + (t1 - gamma/2) + t2 beta]
```

Numerical form:

- this is a quartic equation in `beta`;
- after multiplying by `beta^2`, the quartic is

```text
t2 t3 beta^4
+ [(t1-gamma/2)t3 + (t1+gamma/2)t2] beta^3
+ [t2^2 + (t1-gamma/2)(t1+gamma/2) + t3^2 - E^2] beta^2
+ [(t1+gamma/2)t3 + (t1-gamma/2)t2] beta
+ t2 t3 = 0
```

- for Fig. 5, the brute-force construction uses open-chain eigenenergies and
  keeps the middle two roots by modulus as the bulk pair satisfying
  `|beta_i|=|beta_j|`;
- for the Fig. 5 transition, set `E=0`, collect the two roots from `a(beta)=0`
  and the two roots from `b(beta)=0`, and sort the four roots by `|beta|`;
- the winding changes when the middle two moduli meet. Numerically this gives
  `t1 ~= +/-1.562` for `t2=1`, `gamma=4/3`, `t3=1/5`, matching the reported
  transition near `|t1|=1.56`;
- inside the topological interval, the two smallest zero-energy roots come from
  the same off-diagonal factor (`aabb` ordering); outside, the ordering is
  alternating (`abab`).
