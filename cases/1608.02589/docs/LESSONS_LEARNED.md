# Lessons Learned

## New Failure Modes

- A small-size proxy can generate the right observable but still fail the paper's intended scaling claim. Fig. 3 is the example here.
- Feature-level reproduction needs target-specific acceptance text. "Data generated" is not enough.
- Floquet papers often mix three levels of evidence: time-domain response, spectrum/eigenstate diagnostics, and experimental realizability. These should be separated before coding.
- A derived observable can pass visually while its tensor index convention is wrong. Endpoint mutual information needed a limiting-state check before it became trustworthy.
- A large-scale target should not be left as a vague blocker. If the paper gives enough information, the case should preserve concrete parameters, grids, sample counts, and fit targets for the next execution round.
- The run scale should be chosen after recording the user's available compute budget. This separates the scientific goal from what is reasonable in the current local session.
- Resource limits need classification. If memory cannot fit the target, the local run should not start; if memory fits but runtime is long, the harness should offer an overnight or chunked time-for-compute plan.
- Time budget should be requested after a first local attempt, using measured runtime as evidence.

## Reusable Checks Or Tools

- Add a general trend-claim checklist to the harness docs: each feature target should state what trend is expected before plotting.
- Add a general observable-sanity checklist: before accepting a new observable, test it on a limiting state or analytic case where the answer is known.
- Keep domain-specific observables case-local. The harness should not store a library of Floquet/DTC checks.
- For future finite-size scaling cases, add a case-local scaling-quality JSON that records whether the collapse is accepted or rejected.
- For future large-scale targets, write a case-local rerun plan and machine-readable config even when the full computation is not launched locally.
- Add a compute-budget profile before deciding whether each target is smoke, feature, medium, final, or external.
- Add a memory-vs-time decision: reject memory-impossible targets locally, but offer staged long-running plans for slow feasible targets.
- Add a post-first-attempt time budget request with measured runtime and expected gains.

## Harness Backlog Updates

copied_to_backlog: `H014`
copied_to_backlog: `H015`
copied_to_backlog: `H016`
copied_to_backlog: `H017`
copied_to_backlog: `H018`
copied_to_backlog: `H019`
copied_to_backlog: `H020`

## Case-Specific Takeaway

The Agent should be allowed to mark a generated figure as not accepted. In this case, that prevented the first-pass mutual-information proxy from being over-sold. The second iteration then fixed the observable and moved Fig. 3a from proxy to feature-level reproduction.
