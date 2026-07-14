# Numerical Methods

## Local Reproduction Strategy

The original paper uses tensor-network contraction to handle 53-qubit Sycamore circuits. This local case uses a smaller random circuit so the method can run on a normal machine while preserving the same numerical structure.

The local pipeline is:

```text
random circuit
-> statevector
-> fixed closed bitstring
-> batch over all open bitstrings
-> probabilities
-> XEB and Porter-Thomas checks
-> plots
```

## Parameters

| Parameter | Value |
| --- | --- |
| Local qubits | 18 |
| Closed qubits | 6 |
| Open qubits | 12 |
| Batch size | `2^12 = 4096` |
| Depths | 20 and 14 |
| Simulation backend | Dense statevector |
| Gate model | Random one-qubit and two-qubit Haar gates in alternating nearest-neighbor layers |

## Why This Is A Valid Local Check

The paper's core observable is not the exact visual style of the plots. It is the behavior of scaled probabilities:

```text
x = Np
```

For chaotic random circuits, these scaled probabilities follow the Porter-Thomas exponential law:

```text
Prob(x) = exp(-x)
```

The local simulation checks the same features:

- the histogram follows the exponential red line;
- the full fixed-subspace batch has XEB close to zero;
- top-probability post-selection raises XEB;
- conditional probabilities normalize and follow the same exponential feature.

## Generated Data

- `outputs/data/depth20_big_batch_probabilities.csv`
- `outputs/data/depth20_postselection_xeb.csv`
- `outputs/data/depth14_big_batch_probabilities.csv`
- `outputs/data/depth14_postselection_xeb.csv`
- `outputs/data/table1_complexity_arxiv.csv`
- `outputs/data/table2_method_comparison_arxiv.csv`

## Generated Figures

- `outputs/figures/fig2_depth20_reproduction.png`
- `outputs/figures/fig5_depth14_reproduction.png`
- `outputs/figures/fig6_conditional_probability_reproduction.png`
- `outputs/figures/table2_method_comparison_reproduction.png`

## Checks

- `outputs/checks/formula_verification.json`
- `outputs/checks/depth20_feature_check.json`
- `outputs/checks/depth14_feature_check.json`
- `outputs/checks/table_reproduction_check.json`
- `outputs/checks/completion_assessment.json`

## Stop Boundary

The 53-qubit direct statevector would require 128 PiB in complex128. The paper's
tensor-network table reports `4.51e18` head-contraction operations and 149 days
on one A100. Because the runnable circuit, contraction-path, slicing, and
validation-amplitude bundle is also absent from this public case, the full
contraction is not launched under the current resource policy.
