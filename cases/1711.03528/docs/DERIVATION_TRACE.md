# Derivation Trace

## 1. PXP Hamiltonian

The paper starts from a Rydberg blockade chain. Each site is either in the ground state `|circle>` or excited state `|bullet>`. Adjacent excitations are forbidden.

The effective Hamiltonian is

```text
H = sum_i P_i X_{i+1} P_{i+2}
```

Equivalently, a site can flip only when both neighbors are in the ground state. This gives the program rule:

```text
if left_neighbor == 0 and right_neighbor == 0:
    flip current site
```

The constrained basis contains only bitstrings with no adjacent `1`s. The code verifies the paper's Fibonacci counting:

- PBC: `D = F_{L-1} + F_{L+1}`
- OBC: `D = F_{L+2}`

For `L=6` with PBC, the code gets `18` states, matching the paper.

## 2. Z2 Initial State

The special initial state is the period-2 density wave:

```text
|Z2>  = |bullet circle bullet circle ...>
|Z2'> = |circle bullet circle bullet ...>
```

The paper's dynamical claim is that evolution from `|Z2>` keeps returning close to the same small part of Hilbert space. Numerically this should appear as:

- slow entanglement growth compared with other product states;
- visible oscillation in local correlation functions;
- return-probability revivals;
- a tower of high-overlap eigenstates when the spectrum is projected onto `|Z2>`.

## 3. Particle-Hole Symmetry

The paper states that `P = product_i Z_i` anticommutes with `H`.

The code checks:

```text
P H + H P = 0
```

The measured maximum absolute matrix element is `0.0`, so this gate passes.

## 4. Forward Scattering Approximation

The paper splits the Hamiltonian into

```text
H = H+ + H-
```

where `H+` moves the state farther away from `|Z2>` in Hamming distance and `H-` moves it back. Starting from `|Z2>`, repeated action of `H+` creates a short basis:

```text
|0>, |1>, ..., |L>
```

In that basis the approximate Hamiltonian is tridiagonal:

```text
H_FSA = sum_n beta_n ( |n><n+1| + |n+1><n| )
```

The code constructs this basis directly from the PXP Hamiltonian and verifies:

- `H = H+ + H-` exactly in the constrained Hilbert space;
- the projected FSA Hamiltonian is tridiagonal up to numerical precision;
- for `L=12`, the projected-minus-tridiagonal norm is `6.59e-15`.

This means the numerical code is using the same formula chain as the paper before any figure is generated.
