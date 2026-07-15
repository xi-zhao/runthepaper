# Computational Provenance

## Non-negotiable rule

Every published data point is generated from a documented equation, Hamiltonian,
public control parameter, or explicitly labelled reconstruction assumption. No
paper-figure pixel, traced curve, digitized point, or fitted raster feature is
used as a computational input.

The calculation flow is:

`equations + parameters -> numerical data -> generated figure -> optional visual comparison`

Paper images appear only in the two already-rendered comparison composites.
The public code does not read those composites or any source image, and the
panels are not used to tune model parameters.

## Provenance classes

- `analytic_reference`: direct numerical sampling of formulas and coefficients
  printed in the paper, used for T001 and T002.
- `formula_numerics`: numerical evaluation of disclosed analytical models or
  public-anchor scaling laws, used for T003, T004, T006, T007 and T008.
- `independent_hamiltonian_numerics`: propagation of the common eight-dimensional
  infinite-blockade Hamiltonian, used for T005 and diagnostic D001.
- `independent_many_body_numerics`: independent seven-site, 128-dimensional
  state-vector/tangent propagation, used for T009.

## Automated audit

`outputs/checks/computational_provenance_audit.json` records the source scan,
the allowed generated-data provenance values and the absence of image reads in
the computational path.

## Reproduction boundary

Exact paper-specific curves are intentionally not claimed where the authors did
not publish the necessary numerical PSD arrays, hardware calibration arrays,
atomic geometry, exact ramp/pulse trajectory, or discrete circuit metadata.
Those missing inputs are recorded as limitations; they are never reconstructed
from source pixels.
