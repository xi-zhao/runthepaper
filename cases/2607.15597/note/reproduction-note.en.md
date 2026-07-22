# Reproducing an ultrafast atom-ion entangling gate

This public case follows Mu Qiao's preprint, “Deterministic atom-shuttle
interconnects via ultrafast atom-ion entangling gate”
([arXiv:2607.15597](https://arxiv.org/abs/2607.15597)). It separates three
questions: whether the geometric CZ mechanism is executable, which multi-ion
and architecture features can be recovered from disclosed inputs, and how
closely independent figures can be registered to the paper layout without
claiming access to author data.

## Main result

The Rydberg charge-induced-dipole force and an optical Magnus force give four
logical branches different oscillator displacements. All trajectories close
after one trap period, while their geometric phases retain the invariant

\[
\Phi_{CZ}=-8\pi(\omega_g/\omega)^2.
\]

Choosing \(\omega_g/\omega=1/(2\sqrt2)\) produces a CZ phase. The independent
calculation gives a maximum displacement residual of about `1.7e-16` and
concurrence essentially equal to one at `t=T`, followed by disentanglement at
`2T`.

For ten ions, the code obtains equilibrium positions and axial modes from the
Coulomb-crystal Hessian, then optimizes a deterministic 25-segment toggle
sequence against all ten complex closure residuals. The highest normalized
mode is about `6.576`, and the residuals close at numerical precision. This
demonstrates the disclosed mechanism; it does not claim to recover the
author's unpublished pulse vector.

At the architecture level, the hybrid shuttle and the stated 250 Hz photonic
link cross near `2 mm`. The passive-memory term follows the caption formula
`2 pT / Nops` and therefore decreases with operation count. Because the raster
in Fig. 4(b) visually moves in the opposite direction, the scientific output
follows the equation and exposes the inconsistency as a separate check.

## Run it

From the RunThePaper repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/2607.15597/code
python scripts/run_reproduction.py
```

The command regenerates 17 CSV files, eight scientific figures, and the core
JSON verdict. See the [runnable script](../code/scripts/run_reproduction.py)
and the [equation-level derivation](../docs/DERIVATION.md).

## Pixel registration

Eight additional PNGs use the paper's original canvas dimensions and measured
axes geometry. All eight pass the dimension check. The best full-image SSIM is
`0.8297`, the mean is `0.7524`, and none reaches the strict `0.95` threshold.
The correct label is therefore pixel-registered, not pixel-exact. Missing curve
points, author fonts, and editor transforms are not replaced by copying the
paper image.

## Boundary

The scientific evidence score is `75.21/100`, a numerical-feature
reproduction. Exact formulas and disclosed tables are independently recovered.
Intermediate Fig. 3 schedules, the thermal QuTiP sweep, the MQDT/Stark map,
and qLDPC circuit-level Monte Carlo remain bounded by unavailable author inputs
or run metadata. Reconstructed, source-only, and proxy targets remain labelled
as such in the scorecard.
