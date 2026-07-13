# Derivation Trace

## 1. Floquet Drive

The paper defines a binary periodic drive:

```text
H_f(t) = H1, 0 < t < T1
H_f(t) = H2, T1 < t < T1 + T2
```

With `T1 = T2 = 1`, the one-period Floquet unitary is:

```text
U_f = U2 U1 = exp(-i H2) exp(-i H1)
```

## 2. Pulse Hamiltonian

The pulse is:

```text
H1 = (pi/2 - epsilon) sum_i sigma_i^x
```

If `epsilon = 0`, each spin is flipped by a perfect pi rotation. If `epsilon` is nonzero, a noninteracting spin accumulates a frequency shift away from the exact half-frequency response.

For a single spin initially along `z`:

```text
R(n) = cos[(pi - 2 epsilon) n]
```

So the Fourier peak moves away from `1/2` by approximately:

```text
delta f = epsilon / pi
```

This gives the noninteracting curve in the reproduction.

## 3. Interaction / Disorder Hamiltonian

The second part of the drive is:

```text
H2 = sum_i J_i^z sigma_i^z sigma_{i+1}^z + B_i^z sigma_i^z
```

with:

```text
J_i^z in [0.8 J_z, 1.2 J_z]
B_i^z in [0, 2 pi]
```

In the computational `z` basis, `H2` is diagonal. This lets the implementation apply `exp(-i H2)` exactly as a phase for each bitstring.

## 4. Autocorrelation

The paper studies the stroboscopic spin autocorrelation:

```text
R(n) = <sigma_i^z(n) sigma_i^z(0)>
```

The local case estimates this using random product states and disorder samples:

```text
R(n) = average_i z_i(0) <sigma_i^z(n)>
```

The important feature is not the exact microscopic trace, but whether the Fourier spectrum has a rigid peak at frequency `1/2`.

## 5. Fourier Peak

For each time trace:

```text
R(0), R(1), ..., R(N)
```

the case computes a normalized FFT over the same kind of late-time window used in the paper. The accepted feature is:

```text
J_z = 0: peak shifts with epsilon
J_z > 0: peak remains locked near 1/2
```

## 6. Level Statistics

Floquet quasienergies are extracted from eigenvalues:

```text
U_f |phi_n> = exp(-i E_n) |phi_n>
```

After sorting quasienergies around the unit circle, the adjacent-gap ratio is:

```text
r_n = min(delta_n, delta_{n+1}) / max(delta_n, delta_{n+1})
```

The paper uses this to diagnose the localization transition. The local case generates the same observable for smaller `L`.

## 7. Variance Of The Half-Frequency Peak

For each disorder sample, define `h` as the Fourier amplitude at frequency `1/2`. The transition is indicated by enhanced sample-to-sample fluctuation:

```text
Var(h)
```

The case reproduces this diagnostic for both nearest-neighbor and long-range interaction variants.

## 8. Endpoint Mutual Information

For a Floquet eigenstate `|psi>`, the endpoint reduced density matrix is obtained by tracing out the middle spins:

```text
rho_1L = Tr_{2,...,L-1} |psi><psi|
```

The mutual information between the first and last site is:

```text
I(1:L) = S(rho_1) + S(rho_L) - S(rho_1L)
```

with:

```text
S(rho) = -Tr rho log rho
```

The second iteration added a direct sanity check before accepting this observable:

```text
GHZ endpoint mutual information = log 2
epsilon = 0 Floquet eigenstates also give log 2
large epsilon drives the endpoint mutual information toward 0
```

This check caught and fixed the first-pass axis-order issue in the two-site reduced density matrix.

## Formula Gate

`outputs/checks/formula_verification.json` records that the case uses the paper's Floquet unitary, pulse angle, diagonal `H2`, autocorrelation definition, subharmonic criterion, quasienergy gap-ratio definition, and endpoint-mutual-information construction before plotting.
