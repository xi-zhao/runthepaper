# Derivation Trace

## 1. Output Probability

For a circuit `U` applied to the all-zero state, the output state is:

```text
|psi> = U |0...0>
```

For a bitstring `s`, the probability is:

```text
P_U(s) = |<s|psi>|^2
```

This is the starting point shared by statevector simulation and tensor-network contraction.

## 2. Split The Bitstring

The paper splits the final bitstring into closed and open parts:

```text
s = (s1, s2)
```

So the same probability can be written as:

```text
P_U(s) = P_U(s1, s2)
```

Fixing `s1` and enumerating all `s2` gives a correlated batch of output probabilities.

## 3. Head-Tail Amplitude Factorization

The tensor network is cut into two parts connected by a bottleneck. After contraction:

```text
G_head -> v_head(s1)
G_tail -> v_tail(s2)
```

The amplitude is:

```text
psi(s1, s2) = v_head(s1) dot v_tail(s2)
```

Then:

```text
P_U(s1, s2) = |psi(s1, s2)|^2
```

The important point is reuse: once `v_head(s1)` is computed, the same vector is used for every open bitstring `s2`.

## 4. XEB Fidelity

For `L` selected bitstrings, the paper uses:

```text
F_XEB = (2^n / L) * sum_i P_U(s_i) - 1
```

Equivalently:

```text
F_XEB = mean(N p_i) - 1
```

where `N = 2^n` and `p_i = P_U(s_i)`.

In this case:

- the full fixed-subspace batch has XEB close to zero;
- selecting only the highest-probability bitstrings raises XEB;
- selecting all bitstrings returns XEB close to zero.

## 5. Porter-Thomas Distribution

The paper compares scaled probabilities to the Porter-Thomas distribution:

```text
Prob(p) = N exp(-N p)
```

Let:

```text
x = Np
```

Then:

```text
Prob(x) = exp(-x)
```

That is why the histogram becomes a straight red line on the log-scale plots.

## 6. Conditional Probability

For a fixed closed bitstring:

```text
P_U(s1) = sum_s2 P_U(s1, s2)
```

The conditional distribution over open bitstrings is:

```text
P_U(s2 | s1) = P_U(s1, s2) / P_U(s1)
```

After normalization:

```text
sum_s2 P_U(s2 | s1) = 1
```

The check file verifies this to numerical precision.

## 7. Formula Gate Result

`outputs/checks/formula_verification.json` records:

- batch amplitude extraction equals direct amplitude lookup;
- conditional probabilities normalize to one;
- XEB formula is applied as `mean(Np)-1`;
- Porter-Thomas comparison is done in the scaled variable `Np`;
- no formula remains closed before numerical plotting.
