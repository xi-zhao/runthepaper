# Lessons learned

1. For algorithm papers, reproduce the story order first. Here that means path planning, then potential generation, then runtime.
2. Source-panel PDFs are useful visual references, but they are not generated figures and should not be registered as `rendered_figures`.
3. Private software names in the paper should become explicit provenance boundaries. Zhuifeng is mentioned but not included in the arXiv source.
4. Reduced-scale pilots are useful only if the compute-scale boundary is recorded as a repair item.
5. For ML-method papers, the trained model must be a first-class artifact. A plot alone is not enough; the case needs a checkpoint, training history, reload path, and held-out evaluation.

## New Failure Modes

- `author_software_unavailable`: the paper names Zhuifeng, but the arXiv package does not include the implementation.
- `hardware_mismatch`: Fig. 5 reports RTX 5090 timing, while our available campaign target is A100.
- `decoder_implementation_gap`: a CPU auction decoder can validate the assignment object, but it does not reproduce the paper's GPU-parallel decoder timing.
- `missing_model_artifact`: metric-only pilots cannot support a trained-model reproduction claim.
- `geometry_contract_mismatch`: a same-spacing centered `101 x 101` target
  subarray makes the Fig. 3 Hungarian baseline an order of magnitude too large.
  The paper-target geometry uses target spacing `1.26` across the `127 x 127`
  field.

## Reusable Checks Or Tools

- Check that source-panel copies are not registered as generated figures.
- Require generated figure rows in `outputs/data`, not only PNG files.
- Keep compute-scale blockers as repair work items instead of hidden caveats.
- Require checkpoint reload tests for any target whose physical or algorithmic object is a trained model.

## Stage13 Training Debugging Rules

- Treat loss descent as a weak signal only. A training objective is not useful until
  it improves decoder-facing metrics: `rank1_rate`, `mean_positive_rank`, and
  `average_distance_gap`.
- Compare training objectives in the same score space. A sigmoid audit can make
  a high-logit model look tied or saturated even when the raw-logit ranking is
  still informative; report both the score transform and the decoder input.
- High-logit objectives must report saturation diagnostics: positive/negative
  logit means, score margin, tie count, and optimistic rank. A lower loss with
  inflated logits and unchanged rank/gap is a stop signal, not progress.
- Do not open `shard16`, `shard128`, or curriculum while a paper-size single
  sample still fails the rank/gap gate. Curriculum is valid only after the model
  can solve the simple fixed case and then degrades on harder or more varied
  samples.
- Keep the model, decoder, and dataset fixed when testing a loss target. Change
  one axis at a time; otherwise a lower loss cannot identify the cause of better
  or worse assignment quality.
- Use oracle/model score interpolation before another long training run. If
  `alpha=1.0` oracle scores do not drive the decoder gap near zero, debug the
  score-to-decoder path before training. If interpolation works but learned
  scores fail, the next target is loss/ranking alignment.
- Prefer short loss-target probes with hard-negative or margin ranking objectives
  after score interpolation passes. Only promote a loss if it improves rank and
  gap together; raw BCE or Sinkhorn loss reduction alone is not a go signal.
- Before changing loss, learning rate, architecture, or curriculum, freeze the
  metric contract: squared-distance Hungarian labels for training, Euclidean
  average/max movement distances for reporting, and target spacing `1.26` for
  the paper `127 x 127` to `101 x 101` benchmark.
- For the Fig. 3 shard32 top-k hard-negative line, the mid-run checkpoint audit
  must be allowed to stop or continue the run. The `update_00000256` logits audit
  on 2026-07-03 improved rank/gap without logit inflation, so continuing to the
  formal `1024`-update gate was justified.
- In objective-pair training probes, the paired delta is the evidence. In the
  Stage13 source+target top-k probe, treatment beat the older baseline but did
  not beat the paired control on rank1 or mean positive rank, so the result is
  not a pass. When control already clears the old baseline, baseline comparison
  is a sanity guard only.
- A fresh optimizer is a confound check, not a promotion rule. In the Stage13
  fresh-opt fallback, treatment improved average gap and reduced the
  `winner_geometrically_closer` failure fraction, but it lost on rank1 and mean
  positive rank against paired control. The correct decision is
  `falsified_stop`, not a control rerun or a larger run.
- Diagnostics helpers should own their artifact directories. The fresh-opt run
  reached `512/512`, then failed only because `diagnose_fixed_shard_training_set`
  wrote `train_diagnostics_progress.jsonl` before creating its output directory.
  Recovery should reuse the existing checkpoint and regenerate missing
  diagnostics, not retrain.
