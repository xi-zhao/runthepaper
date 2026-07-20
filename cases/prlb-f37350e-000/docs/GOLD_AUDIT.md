# Frozen-gold audit

## Verdict

`benchmark_gold_invalid`: R1–R5 and R7–R10 are correct; R6 and R11–R12 are not valid as written. The score-bearing split is 9/12 points.

## R6

The source has `H_rho^(-1/3)`. At Set-C it gives `2.10769601279 keV`, agreeing with frozen R7. The displayed frozen `H_rho^(-1)` formula instead gives `1.06096881704 keV`, a 49.66% error.

## R11–R12

For outward high-to-low-density propagation, an initial X-mode gives frozen signs: adiabatic `Q/I=+1`, nonadiabatic `Q/I=-1`. An initial O-mode gives exactly the opposite signs. The prompt defines the axes but never declares the incident mode, so neither requested output is unique.

Machine-readable evidence is in `outputs/data/idx0_gold_audit.json`.
