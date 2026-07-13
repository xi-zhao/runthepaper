# Lessons Learned

## Case Summary

This case shows a recurring pattern in physics reproduction: the formulas may be easy to implement, while the paper's actual claim depends on large finite-size scaling.

The local run was useful. It validated the formula chain and showed several physical features. It also exposed a risk: a harness should not apply paper-scale monotonic scaling tests to a small smoke run.

## New Failure Modes

### 1. Scale-sensitive feature checks can be too strict for smoke runs

Pitfall: The first version required strict monotonic `W_1^*` finite-size scaling at `L<=7`.

Why it happened: The original paper extracts `W_1^*` from much larger systems. Small systems mix weak-disorder crossover, finite-size degeneracy, and localization effects.

Future rule: Split checks into local smoke features and paper-scale fit targets.

### 2. A correct formula implementation can still miss the paper figure

Pitfall: The susceptibility formula and Hamiltonian are correct, but the central Fig. 1 peaks are not reproduced quantitatively.

Why it happened: The figure depends on large volume, enough central eigenstates, disorder averaging, and careful peak fitting.

Future rule: Score formula correctness, feature visibility, and paper-scale coverage separately.

### 3. Spectral-function exponents should not be fitted from tiny systems

Pitfall: The code can compute `|f(omega)|^2`, but the exponent claim is unstable at small `L`.

Why it happened: The fitted range and low-frequency bins require many more states.

Future rule: Treat exponent extraction as a large-scale target unless the local data has enough decades and samples.

## Reusable Checks Or Tools

- Add a scale-aware acceptance template that distinguishes:
  - smoke feature;
  - local feature;
  - paper-scale fit;
  - complete reproduction.
- Add a scorecard warning when a critical target scores below 60 but the weighted case score barely passes 60.
- Add a finite-size-scaling plan template with required `L`, grid, samples, and fit formula.

## copied_to_backlog

- Added H027: scale-aware finite-size acceptance.
- Added H028: critical-target floor warning.

## copied_to_experience

- Added experience item 10: smoke-run feature checks must not impersonate paper-scale finite-size scaling.
