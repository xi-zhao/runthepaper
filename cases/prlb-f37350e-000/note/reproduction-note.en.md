# Polarized X-Ray Emission from Magnetized Neutron Stars: Signature of Strong-Field Vacuum Polarization: public reproduction note

## Result

Recomputes the vacuum-resonance density, adiabatic threshold, Landau-Zener conversion, polarization branches, and a paper-exact reconstruction of PRL Fig. 1. The audit also identifies one exponent error and two underdetermined polarization answers in the frozen benchmark.

The public status of this case is **Paper-figure feature reproduction and PRL-Bench gold audit**.  Its audit score measures the strength and coverage of the published evidence; it does not mean that every figure and table in the source paper has been reproduced.  When a frozen PRL-Bench answer conflicts with the source equations, the case preserves the independent calculation and reports the failed gold instead of changing the physical model to match it.

## Method

The reproduction starts from source-derived equations or algorithms, gates them with analytic identities, small-system numerics, or normalization and conservation checks, and only then generates structured data and figures.  The public package contains the independent implementation, generated data, generated images, and machine-readable checks.  It excludes the paper PDF, standalone source figures, digitized reference curves, and the internal error-correction history.

## Main evidence

- PRL Fig. 1: Paper-parameter ellipticity branches across the vacuum resonance (figure: `../outputs/figures/prl_fig1_reproduced.png`; check: `../outputs/checks/gold_audit_check.json`)

## Run

Execute the following commands from this case's `code` directory:

```bash
python scripts/run_gold_audit.py
python scripts/render_prl_fig1.py
python scripts/render_idx0_audit.py
```

The scripts write generated artifacts to `outputs/data`, `outputs/figures`, and `outputs/checks` at the case root.  GPU-scale reruns, when applicable, are listed separately in the main README; the default command path favors a locally inspectable regeneration step.

## Boundary

Only PRL Fig. 1 is independently reconstructed. The benchmark record is outside the declared 2025-2026 PRL window, and source Figs. 3-4 require atmosphere-model arrays and implementation details that are not public.

This case should therefore be read as an executable numerical or feature-level reproduction with an explicit boundary, not as a replacement for all author data, presentation choices, or experimental conditions.
