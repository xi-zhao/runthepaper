# Method Trace

## Method Summary

The paper's method starts from a quantum circuit tensor network. A final bitstring `s` is split into two parts:

```text
s = (s1, s2)
```

- `s1`: closed bits. These are fixed.
- `s2`: open bits. These are enumerated as a batch.

The tensor network is partitioned into a head network and a tail network:

```text
G_head -- bottleneck C -- G_tail
```

After contraction, the expensive part produces a reusable vector:

```text
v_head(s1)
```

For each open bitstring, the tail gives:

```text
v_tail(s2)
```

The amplitude is the final inner product:

```text
psi(s1, s2) = v_head(s1) dot v_tail(s2)
```

The key saving is that `v_head(s1)` is computed once, then reused for all `2^n2` open bitstrings.

## Implementation Used In This Case

The local implementation in `src/big_batch_feature_sim.py` uses a small random quantum circuit rather than the original 53-qubit Sycamore circuit.

It keeps the same mathematical structure:

1. Build a circuit statevector.
2. Split final qubits into closed and open groups.
3. Fix one representative closed bitstring.
4. Enumerate all open bitstrings in one batch.
5. Compute probabilities, scaled probabilities `Np`, XEB, and conditional probabilities.
6. Check that direct amplitude lookup and batch extraction agree exactly.

This gives a faithful local test of the paper's probability logic, even though it does not reproduce the original multi-GPU contraction workload.

## Algorithm Steps

```text
Input:
  n qubits
  circuit depth
  closed qubits
  open qubits

Procedure:
  1. Generate a random layered circuit.
  2. Simulate the statevector.
  3. Choose a closed bitstring whose marginal probability is close to its expected value.
  4. Slice the state tensor at the closed bitstring.
  5. Flatten the remaining open axes to obtain all open-bitstring amplitudes.
  6. Convert amplitudes to probabilities.
  7. Generate histograms, post-selection curves, conditional distributions, and check files.

Output:
  probabilities for all open bitstrings
  post-selection XEB curve
  conditional probabilities
  feature checks
```

## Scale Difference

| Item | Paper | Local case |
| --- | --- | --- |
| Circuit | Sycamore 53 qubits | Random 18-qubit circuit |
| Open bitstrings | `2^21` or `2^19` | `2^12 = 4096` |
| Backend | Tensor-network contraction on GPUs | Dense statevector simulation on CPU |
| Goal | Exact large-scale contraction | Feature-level reproduction and formula validation |

The local case is intentionally smaller. It is meant to verify the derivation and numerical behavior before attempting a hardware-scale contraction.
