# Lessons learned

## New Failure Modes

- Figure axes may report switches per trial while a benchmark silently requests switches per force evaluation.
- Qualitative source language such as “mostly mediated” cannot be converted into an exact fraction without event counts.
- A ratio can be arithmetically correct while both numerator and denominator are invented.
- Moving one term outside a global model coefficient changes the entire free-energy family.

## Reusable Checks Or Tools

- Require numerator, denominator, and their source locations for every efficiency ratio.
- Search the full main/SI source for claimed run values before accepting derived speedups.
- Regenerate at least one deterministic panel to catch model-parenthesis errors.
