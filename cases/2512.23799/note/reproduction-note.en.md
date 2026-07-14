# 2512.23799 Reproduction Note

## Result

This case now runs the reconstructed full Steane `[[7,1,3]]` `|Hbar>` preparation circuit rather than a toy acceptance/infidelity model. The published campaign covers the paper's 12 physical-error-rate points and 790,000 state-vector Monte Carlo shots.

Status: `exact_circuit_partial_reproduction` · Audit score: `73.00/100`.

- Acceptance: all 12 internally digitized validation points pass.
- Logical infidelity: the trend and both edge regimes agree; the mid-range is `0.42–0.68x` of the paper curve.
- Runtime: still a local proxy, not author wall-clock timing.

## Exact Protocol

The implementation contains the non-fault-tolerant Steane `|Hbar>` encoder, the flagged transversal logical-H measurement, one mutual-flag stabilizer round, circuit-level Pauli noise, postselection, and ideal logical decoding.

Tests verify the noiseless logical-H eigenstate, all six stabilizers, the perfect Hamming syndrome map, and correction of every single-qubit Pauli error.

## Paper Comparison

The orange curves below were digitized internally from the published PNGs solely for validation. The source-derived points are not distributed, the comparison panels are outside the repository's open-content license, and the panels do not establish author-data-level equivalence. Paper: [PRX Quantum 7, 020329 (2026)](https://doi.org/10.1103/fby6-xjbm).

### Logical infidelity

![Exact-circuit infidelity comparison](../outputs/figures/steane_exact_infidelity_comparison.png)

Difference reason: in the mid-range, second-order damaging-pair counts depend on reconstructed panel-(c) gate/idle ordering. The author implementation is not public. More shots would reduce Monte Carlo error but cannot identify that schedule detail.

### Postselection acceptance

![Exact-circuit acceptance comparison](../outputs/figures/steane_exact_acceptance_comparison.png)

Difference reason: no numerical residual is accepted—12/12 points pass within `max(0.012, 3 sigma)`. The remaining boundary is that exact time-slice details were reconstructed from the paper rather than confirmed against author code.

### Runtime

![Runtime proxy](../outputs/figures/fig3_runtime_reproduction.png)

Difference reason: the paper's wall-clock values depend on the authors' hardware, Stim/Cirq versions, compiler, and benchmark harness. The public curve remains explicitly labeled as proxy timing.

## Stop Decision

The remaining scientific discrepancy is not compute-limited. The 790,000-shot exact campaign is complete, and additional shots cannot recover unpublished circuit scheduling. The mid-range residual is recorded as `author_implementation_detail_required`; author wall-clock equality is `author_environment_required`.

See `../outputs/checks/completion_assessment.json` for the machine-readable decision.

## Run

Smoke profile:

```bash
cd cases/2512.23799/code
python scripts/run_steane_exact_benchmark.py --profile smoke
```

Full profile:

```bash
python scripts/run_steane_exact_benchmark.py --profile paper
python scripts/plot_steane_exact_comparison.py
```

The public runner generates independent data only; digitized source point sets are not redistributed.
