# Lessons Learned

## New Failure Modes

### Source PNGs Without Benchmark Arrays

Pitfall: arXiv source can include final benchmark PNGs while omitting the CSV arrays and author simulation code.

Why it happens: many physics papers store plots as rendered images and keep data/code available only by request.

How to avoid it: record `source_figure_only` in the case, cap similarity below complete reproduction, and write the remaining exact-rerun plan.

copied_to_backlog: H029

### Runtime Figures Need Stronger Labels

Pitfall: a local runtime proxy can be mistaken for the authors' exact runtime benchmark.

Why it happens: runtime plots look authoritative even when they are calibrated feature checks.

How to avoid it: every runtime target must say whether it is author timing, local rerun timing, or proxy timing.

copied_to_backlog: H030

## Reusable Checks Or Tools

- Formula gate for PSC square checks.
- Matrix identity check for controlled-H propagation.
- Pauli-rank reconstruction check for `|H><H|`.
- `source_figure_only` cap rule for benchmark images without data.
- Runtime evidence label: `author_timing`, `local_rerun_timing`, or `proxy_timing`.

## Case-Specific Knowledge

The exact Steane `|Hbar>` circuit and the chosen toy probabilities are case-specific. They should stay in this case and should not enter the reusable harness as domain knowledge.
