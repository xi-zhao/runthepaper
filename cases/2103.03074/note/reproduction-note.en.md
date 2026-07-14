# Reproduction Report

## Scope

This case reproduces the numerical behavior of arXiv:2103.03074 at feature level.

Similarity score: `70.0/100` (`numerical_feature_reproduction`).

Completed:

- arXiv PDF and TeX source ingested.
- All figures classified.
- Core formulas traced before numerical work.
- Local code implemented for batch probability extraction.
- Structured data generated before plots.
- Fig. 2, Fig. 5, and Fig. 6 numerical features reproduced.
- Complexity tables transcribed and checked.

Not completed:

- Exact 53-qubit Sycamore contractions.
- Exact recomputation of Table III example amplitudes.

## Commands

Run the case from the project root:

```bash
python3 cases/2103.03074/code/scripts/run_reproduction.py
python3 cases/2103.03074/code/scripts/plot_reproduction.py
```

The machine-readable stop decision is recorded in `../outputs/checks/completion_assessment.json`.

## Code

- `code/src/big_batch_feature_sim.py`: local random-circuit simulation, batch extraction, XEB checks, table data.
- `code/scripts/run_reproduction.py`: generates CSV and JSON checks.
- `code/scripts/plot_reproduction.py`: generates figures from CSV.

## Main Results

| Target | Result |
| --- | --- |
| Formula gate | Passed |
| Big-batch extraction vs direct amplitude lookup | Max error `0.0` |
| Depth 20 full-batch XEB | `0.00494` |
| Depth 14 full-batch XEB | `-0.00252` |
| Conditional probability normalization | Passed |
| Post-selection XEB monotonicity | Passed |
| Table complexity consistency | Partial, table values checked but full contraction not rerun |

## Interpretation

The local reproduction shows that the mathematical mechanism in the paper is working:

- fixing `s1` and enumerating `s2` produces a correlated batch;
- the batch probabilities have the same Porter-Thomas feature as the original figures;
- post-selecting high-probability bitstrings raises XEB;
- conditional probabilities remain Porter-Thomas-like after normalization.

The remaining gap is scale. The original claim relies on a carefully optimized 53-qubit tensor-network contraction. This local case validates the formula and observable behavior, but it does not validate the original large-scale engineering result.

The exact 53-qubit targets are classified as `memory_impossible` for direct statevector simulation and `external_required` for tensor-network rerun. A complex128 statevector would require 128 PiB; the paper-reported tensor-network estimate is 149 days on one A100. The current case also lacks a runnable circuit/path/slicing/validation asset bundle, so no large campaign is launched.

Difference reason shown on the figures: generated probability panels use an 18-qubit random-circuit feature check, while the table panel contains paper-reported estimates rather than a measured 53-qubit rerun.
