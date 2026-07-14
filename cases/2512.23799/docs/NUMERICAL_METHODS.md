# Numerical Methods

## Exact Steane Protocol

The primary T001/T002 result is a dense state-vector Monte Carlo simulation of the reconstructed Steane `[[7,1,3]]` logical-H preparation circuit:

- non-fault-tolerant `|Hbar>` encoding;
- flagged transversal logical-H measurement;
- one six-stabilizer mutual-flag measurement round;
- postselection on all `+1` outcomes;
- ideal CSS/Hamming decoding before logical fidelity evaluation.

The circuit uses the paper's initialization, two-qubit depolarizing, idle, and measurement-flip noise rules. The accepted configuration is:

```text
stabilizer schedule = ASAP
idle policy        = active window
encoding noise     = initialization + gate noise, no encoding idles
```

## Paper-Grid Campaign

- Error-rate points: `linspace(1e-3, 1e-2, 9) + [0.02, 0.035, 0.05]`.
- Shot counts: `100000` below `p=0.006`, `50000` below `p=0.02`, otherwise `30000`.
- Total: `790000` shots.
- Stochastic locations in the selected schedule: `200`.
- Generated data: `outputs/data/steane_exact_benchmark.csv`.

Digitized paper point sets are used internally as a validation oracle but are not distributed. The public CSV contains independent generated quantities only.

## Structural Tests

`tests/test_steane_exact.py` verifies:

- deterministic noiseless acceptance;
- logical-H and six-stabilizer eigenvalue equations;
- the seven nonzero Hamming syndrome columns;
- ideal correction of all 21 single-qubit Pauli errors;
- the stochastic location-table structure;
- explicit preservation of the known infidelity residual.

## Legacy Supporting Checks

The earlier closed-form feature model remains as a lightweight formula/sampling demonstration and runtime proxy. It no longer supplies T001/T002 evidence. The runtime panel remains proxy timing because the author's benchmark environment is unavailable.

## Numerical Boundary

- Acceptance agrees at all 12 internally digitized validation points.
- Infidelity agrees at both edge regimes but is `0.42-0.68x` of the paper curve in the mid-range.
- The residual is attributed to unpublished gate/idle ordering that controls second-order damaging-pair counts.
- Increasing shots cannot identify that missing schedule detail.
