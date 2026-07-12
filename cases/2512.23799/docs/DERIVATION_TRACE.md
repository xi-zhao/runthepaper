# Derivation Trace

## Core Logic

The paper studies magic-state-preparation protocols whose circuit-level Pauli errors can be pushed to the end of the circuit as Clifford errors. Once that is true, the hard non-Clifford circuit is replaced by a cleaner problem:

```text
noiseless encoded magic state + stochastic end-of-circuit Clifford error
```

The numerical benchmark then estimates fidelity and acceptance under a circuit-level Pauli noise model.

## D001: Magic States As PSC Eigenstates

The paper defines:

```text
|T> = (|0> + exp(i pi/4)|1>) / sqrt(2)
|H> = cos(pi/8)|0> + sin(pi/8)|1>
```

These states are eigenstates of Clifford operators that square to Paulis. A Pauli-square-root Clifford, or PSC, is a non-Pauli Clifford `U` such that:

```text
U^2 is a Pauli
```

In the formula gate we checked common examples:

```text
H^2 = I
S^2 = Z
CZ^2 = I
(X tensor CZ)^2 = I
```

All passed numerically in `outputs/checks/formula_verification.json`.

## D002: Why Pauli Errors Stay Manageable

The key controlled-H identity used in the toy propagation argument is:

```text
C(H) (X tensor I) = (X tensor H) C(H)
```

This says an `X` error on the control of a controlled-H gate becomes a Clifford error at the end. The case checks this as a matrix identity. The residual error is `3.16e-16`, which is numerical roundoff.

This is the local version of the paper's broader statement: under the protocol family studied here, circuit-level Pauli noise propagates into an end-of-circuit Clifford error.

## D003: Fidelity From Pauli-Rank Expansion

For a density matrix, the paper uses a Pauli expansion:

```text
rho = I / 2^n + (1 / 2^n) sum_i beta_i P_i
```

For a single `|H>` state, the formula gate reconstructs:

```text
|H><H| = I/2 + (X + Z)/(2 sqrt(2))
```

The reconstruction error is `2.78e-17`, so the Pauli-expectation route is internally consistent.

For two logical qubits, the paper's toy example notes that `(|H><H|)^tensor 2` has eight nontrivial Pauli terms. That is why fidelity can be estimated through Pauli logical expectation values instead of a full non-Clifford state-vector simulation.

## D004: Numerical Benchmark Model

The paper's proof-of-principle benchmark uses a Steane-code `|Hbar>` preparation protocol under uniform circuit-level Pauli noise. It compares a propagated-error stabilizer route with a Cirq state-vector baseline.

The arXiv source gives the final benchmark PNGs but not the arrays. For this case, the executable model keeps the paper-derived structure:

```text
M = 42 error locations
p = physical error rate
u = probability that an error remains undetected
l = conditional logical-error probability per undetected error
```

The acceptance probability is:

```text
A(p) = (1 - p + p u)^M
```

The conditional logical infidelity is:

```text
I(p) = 1 - (1 - p + p u (1-l))^M / A(p)
```

This model is not the exact Steane simulator. It is a feature-level executable check for the benchmark behavior: the two estimators agree, acceptance decreases with `p`, infidelity increases with `p`, and the propagated-error route is cheaper at low `p`.

## Verification

- Formula gate: `outputs/checks/formula_verification.json`
- Numerical feature gate: `outputs/checks/numerical_feature_checks.json`
- Code pointer: `src/magic_state_simulation.py`
