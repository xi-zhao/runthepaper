# Method Trace

## MTH001 — hybrid error-correction accounting

- Source: Supplement Tables S7-S12 and Fig. S5.
- Role: connect physical atom-ion transfers to logical-code cost and projected logical error.
- Inputs: code length/logical count, atom-ion gate count, physical error, threshold, distance, herald boost, syndrome-round timing.
- Outputs: atom-ion gates per logical pair, Fowler-projected logical error, architecture timing curves.
- Steps: (1) divide disclosed transfer gates by logical pairs; (2) evaluate the disclosed Fowler ansatz; (3) apply the paper’s 66× herald factor as a separately labelled projection; (4) combine with stated round-time scaling.
- Parameters: Steane `[[7,1,3]]`; BB `[[72,12,6]]`; thresholds `5.7e-3` and `3.4e-3`; boost 66.
- Code: `scripts/run_reproduction.py::reproduce_gate_counts` and `::reproduce_qldpc_projection`.
- Checks: Table S7 arithmetic exact; output provenance labels projections separately from unavailable Monte Carlo markers.
- Status: arithmetic reproduced; Monte Carlo workflow blocked by missing matrices/circuits/decoder metadata.
- Open question: exact BB/APM instances, syndrome schedules, noise placement, seeds and stopping criteria.
