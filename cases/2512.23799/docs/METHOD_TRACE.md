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
- the complete reconstructed Steane `|Hbar>` preparation circuit for exact-circuit infidelity and acceptance Monte Carlo;
- a legacy Monte Carlo feature model retained only as a lightweight supporting check;
- a local calibrated runtime proxy for state-vector-like versus propagated-error simulation;
- a sampling-precision check with slope close to `-1/2`.

The full reconstructed flag-gadget circuit is implemented. The remaining scientific gap is the unpublished panel-(c) gate/idle schedule that controls second-order damaging-pair counts; runtime equality also requires the authors' hardware/software environment.

## M003: Acceptance Gates

The exact-circuit numerical run is accepted only if:

- all 12 acceptance points pass the declared internal validation tolerance;
- infidelity agrees in the edge regimes and any mid-range residual is recorded explicitly;
- circuit structure and ideal decoding tests pass;
- runtime proxy shows a low-`p` speedup above `10x`;
- sampling standard deviation scales close to `1/sqrt(N)`.

The exact-circuit record is `outputs/checks/steane_exact_benchmark.json`; legacy feature and sampling gates remain in `outputs/checks/numerical_feature_checks.json`.
