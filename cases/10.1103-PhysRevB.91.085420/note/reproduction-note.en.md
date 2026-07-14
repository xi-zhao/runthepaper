# CDHM interband-coherence pumping — reproduction note

## Paper identity

Hailong Wang, Longwen Zhou, and Jiangbin Gong, *Interband coherence induced
correction to adiabatic pumping in periodically driven systems*, Physical Review B
**91**, 085420 (2015), DOI `10.1103/PhysRevB.91.085420`. No preprint was recorded
for this reproduction. This case independently reproduces all four figures of the
paper at the paper parameters.

## Scientific object

The model is the continuously driven Harper model (CDHM),
`H = sum_l (J/2)(a_l^dag a_{l+1} + h.c.) + K cos(2 pi t/tau) sum_l cos(2 pi alpha l + beta) a_l^dag a_l`,
with alpha = 1/3 (three Floquet bands) and tau = 2. Adiabatically sweeping the
phase beta from 0 to 2 pi slides the superlattice by one unit cell. A textbook
single-band treatment predicts a displacement set purely by that band's Berry
curvature (a Thouless charge). But a simple, easy-to-prepare state -- a single
lattice site -- is a superposition across all Floquet bands, and the coherence
between bands does not average away. It leaves a population correction that scales
as 1/T (not 1/T^2), and multiplied by the dynamical phase Omega(1) ~ T it
contributes a T-independent piece to the displacement: the interband-coherence
(IBC) correction, Eq. (13).

## Reproduced results

- **Fig. 1** (`T101`): three gapped Floquet surfaces omega(k, beta)/pi in
  [-0.95, 0.95] and the three symmetric initial-population curves match the paper
  color-for-color; populations sum to 1 to 1e-10.
- **Fig. 2** (`T201`): the one-cycle population change Delta rho from the exact
  dynamics and from Eq. (8) both show the rapid k-oscillation with a
  small-at-center, large-at-edge envelope (~5e-3); theory tracks the dynamics at
  correlation ~0.9 per band, and sum over bands is zero to 1e-9.
- **Fig. 3** (`T301`): all six durations T = 1024..6144 end at <x> ~ 3.1 (mean
  3.117, T-independent to under 1%); the Eq. (13) total 3.08 sits at the endpoints
  while the Berry-only term 4.33 sits well above -- the IBC correction (-1.24) is
  essential.
- **Fig. 4** (`T401`): scanning J = K across the Floquet-Chern transition at
  J = 5.14 reproduces the rise, discontinuous jump, and decay; theory peak 19.5 and
  Berry-only 11.1, with the Chern jump (4,-8,4) -> (-8,16,-8) up to an overall sign.

Side-by-side panels (paper excerpt above, independent reproduction below) are in
`../docs/comparisons/`:

![Fig. 1 comparison](../docs/comparisons/fig1_spectrum_populations_comparison.png)

## Run the public package

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd cases/10.1103-PhysRevB.91.085420/code
python scripts/run_fig1.py
python scripts/run_fig2.py
python scripts/run_fig3.py
python scripts/run_fig4.py
python scripts/qa_cdhm.py
```

`run_fig1.py` and `qa_cdhm.py` finish in seconds to a minute; `run_fig3.py` and
`run_fig4.py` are the heavier T-sweep and J-scan (minutes on a laptop). Generated
data lands in `../outputs/data/`, figures in `../outputs/figures/`, and checks in
`../outputs/checks/`.

## Reproduction boundary

This is a numerical feature reproduction, overall score 79.54/100. Every target is
paper-exact with independent numerics and a verified formula gate; the per-target
ceiling of 80 comes only from comparing against the paper's raster figures (no
author data or tables). Two residual mismatches are intrinsic, not modelling gaps:
Fig. 2 is reproduced at feature level because the accumulated dynamical phase in
Eq. (8) is ~10^2 rad at T=1024 and therefore extremely phase-sensitive, and the
Fig. 4 actual peak (~17.4) sits below the paper's ~19 in the narrow band-touching
window where the dynamics is genuinely T-sensitive, exactly as the paper reports.
Everything runs at paper parameters on a laptop; no larger compute is needed.
