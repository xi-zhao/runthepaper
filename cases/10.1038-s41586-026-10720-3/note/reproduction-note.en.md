# Backreaction of stimulated Hawking radiation — reproduction note

## Result

This case reproduces the numerical content of the Nature paper's main-text
Figs. 2, 4, and 5 without using author code. Fig. 2 reconstructs the co-moving
dispersion and seven labelled phase-matching landmarks. Fig. 4 independently
evaluates all six Eq. (D.1) sideband spectra after red-marker-only fitting.
Fig. 5 recomputes the thermal slope ratio as `1.0211`, matching the reported
`1.02`.

## Important physical correction

The pump state drawn in Fig. 2 is not the incident 800 nm carrier. It is the
Raman-shifted carrier at the local minimum of the co-moving dispersion. Keeping
these states separate yields the NRR, Hawking-partner, and backreaction roots
at `233.383`, `233.011`, and `232.643 nm`.

## Validation

The six Fig. 4 curves were fitted without access to the paper's black theory
paths. After freezing the parameters, blind comparison gave mean NRMSE `0.0653`
and correlation `0.9810`. Pixel-registered presentation diagnostics for Figs. 2,
4, and 5 were `0.8238`, `0.7348`, and `0.8201`.

## Public boundary

The public package contains the physical model, frozen fit parameters,
equation-generated curves, checks, and limited comparison panels. It does not
contain the paper PDF, standalone original figures, raw vector coordinates,
digitized point sets, or internal process history. The public Fig. 4 output
therefore shows generated theory only, and the public Fig. 5 output shows the
fitted lines without the source-derived points.

Fig. 1 is a conceptual schematic. Fig. 3 is an experimental acquisition and
cannot be independently regenerated because the raw photon counts were not
published. The result is numerical feature reproduction, not author-data-level
exact reproduction.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install torch
cd cases/10.1038-s41586-026-10720-3/code
python scripts/run_main_figures.py
```

See [`../docs/DERIVATION.md`](../docs/DERIVATION.md) for the physics derivation
and [`../docs/SIMILARITY_SCORECARD.md`](../docs/SIMILARITY_SCORECARD.md) for the
evidence boundary.
