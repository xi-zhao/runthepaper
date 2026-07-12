# Numerical Methods

## Local Reproduction Strategy

This case reconstructs SABRE from the paper text without using the authors' implementation.

The local pipeline is:

```text
QASM or synthetic circuit
-> coupling graph
-> initial logical-to-physical mapping
-> SABRE routing with SWAP insertion
-> routed circuit legality check
-> gate count and depth metrics
```

## Implemented Observables

- Inserted SWAP count.
- Additional CNOT-equivalent count.
- Routed circuit depth.
- Hardware compliance.
- Reverse-traversal improvement.
- Decay heuristic gate/depth trade-off.
- Table II input and output exact-match counts.

## Generated Data

- `outputs/data/paper_swap_example_ops.csv`
- `outputs/data/core_benchmarks.csv`
- `outputs/data/decay_tradeoff.csv`
- `outputs/data/table2_reproduction.csv`
- `outputs/data/table2_attempts.csv`

## Generated Figures

- `outputs/figures/paper_swap_example_trace.png`
- `outputs/figures/core_benchmarks_qft.png`
- `outputs/figures/decay_tradeoff.png`
- `outputs/figures/table2_gop_comparison.png`

## Checks

- `outputs/checks/paper_swap_example.json`
- `outputs/checks/core_benchmarks.json`
- `outputs/checks/decay_tradeoff.json`
- `outputs/checks/table2_reproduction.json`
- `outputs/checks/compute_budget_profile.json`

## Limitations

Exact Table II reproduction is not a pure compute problem. More time can increase randomized attempts, but exact reproduction also needs missing paper metadata and BKA baseline details.
