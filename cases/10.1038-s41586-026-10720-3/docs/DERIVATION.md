# Derivation: stimulated Hawking backreaction in an optical analogue

## 1. Co-moving dispersion

For a mode with laboratory frequency `omega` and propagation constant
`beta(omega)`, the pulse frame uses

```text
omega'(omega) = omega - u beta(omega).
```

The published fibre coefficients are unavailable. The numerical case therefore
compresses the vector curve printed in Fig. 2 into a piecewise Chebyshev
representation. This is a source-derived input, not author data and not an
independent fibre measurement.

The pump marker drawn in Fig. 2 is the Raman-shifted carrier at the local
minimum of `omega'(omega)`, not the incident 800 nm laser frequency. The horizon
is the nearby local maximum. A second IR root at the probe co-moving frequency
gives the redshifted probe.

## 2. Ultraviolet phase-matching roots

The three ultraviolet roots satisfy

```text
omega'_NRR = -omega'_pump,
omega'_-   = -omega'_probe,
omega'_B   = omega'_pump - 2 omega'_probe.
```

Bracketed bisection on the ultraviolet branch gives

```text
NRR              233.383 nm
Hawking partner  233.011 nm
Backreaction     232.643 nm
```

so the backreaction peak is blue-shifted from the Hawking partner by
`0.368281 nm`.

## 3. Asymmetric sideband spectrum

Methods Eqs. (C.3), (C.4), and (D.1) describe an incoherent sum of shifted peak
profiles. For sideband order `m`, the public code evaluates

```text
I(omega) = sum_m W_m I_H((omega - omega_m) / Delta omega),
```

where the weights decay geometrically with `X^(2|m|)` and differ on the two
sides of the Hawking peak because the backreaction amplitude enters
asymmetrically. The peak profile is obtained from

```text
theta_mu(nu) = integral_0^|nu| sech^2(x^mu) dx
               / integral_0^infinity sech^2(x^mu) dx,
I_H(nu) = max(1 - theta_mu(nu)^2, 0).
```

Six fits were performed using only the red experimental markers to the left of
and at the Hawking peak. The paper's black curves were loaded only after all
parameters were frozen. Their mean blind NRMSE is `0.0653` and mean Pearson
correlation is `0.9810`.

## 4. Thermal slope relation

Methods Eq. (D.3) predicts a straight line in the plotted variables,

```text
ln p = a r + b,
```

where `r` is the frequency ratio. Regressing the two visible series gives

```text
a_H = -22.68965,
a_B = -22.22020,
|a_H / a_B| = 1.02113.
```

This reproduces the paper's reported ratio `1.02`. The vector line reveals a
minor analysis-policy inconsistency: the Hawking line uses all six points,
while the backreaction line excludes the 1100 nm point, although the Methods
text says both exclude it.

## Code mapping

- `code/src/optical_hawking/dispersion.py`: compressed Fig. 2 dispersion.
- `code/src/optical_hawking/analysis.py`: stationary points and UV roots.
- `code/src/optical_hawking/theory.py`: peak profile and Eq. (D.1).
- `code/scripts/run_main_figures.py`: public-safe figure and data generation.
