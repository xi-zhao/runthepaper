# Method Trace

## M001: Propagate Errors, Then Simulate A Stabilizer Problem

The paper's method can be read as a compiler pass:

```text
noisy MSP circuit
-> sample circuit-level Pauli errors
-> propagate them through PSC/stabilizer measurements
-> store the final error as a Clifford circuit
-> evaluate fidelity/acceptance using stabilizer-rank or Pauli-rank data
```

The value of this method is that the runtime depends polynomially on the number of qubits and on the nonstabilizerness rank of the target magic state. It avoids a direct state-vector simulation of every noisy non-Clifford circuit instance.

## M002: What This Case Implements

This case implements:

- PSC formula checks;
- a controlled-H propagation identity check;
- Pauli-rank reconstruction for `|H><H|`;
- a Monte Carlo feature model for infidelity and acceptance;
- a local calibrated runtime proxy for state-vector-like versus propagated-error simulation;
- a sampling-precision check with slope close to `-1/2`.

The case does not implement the full Steane flag-gadget circuit from scratch. That is the remaining work needed for exact paper-scale reproduction.

## M003: Acceptance Gates

The numerical run is accepted at feature level only if:

- `A(p)` is monotone decreasing;
- infidelity is monotone increasing;
- Monte Carlo estimates agree with the reference curve within sampling error;
- runtime proxy shows a low-`p` speedup above `10x`;
- sampling standard deviation scales close to `1/sqrt(N)`.

All gates passed in `outputs/checks/numerical_feature_checks.json`.
