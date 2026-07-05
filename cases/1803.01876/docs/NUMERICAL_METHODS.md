# Numerical Methods

## Environment

The pilot uses Python with NumPy, SymPy, and Matplotlib. The checked scripts run
in the local `python` environment; the system `python3` environment is missing
some scientific packages.

## Comparison Policy

Acceptance is data/feature-first. The generated figure is used to inspect the
result, but the primary checks are numerical features:

- positions of transition points;
- topological invariant values;
- equality or separation of beta-root moduli;
- generalized Brillouin-zone radius;
- eigenvalue symmetry;
- boundary localization metrics.

The source EPS/PDF rendering is a visual reference only unless the underlying
curve data is digitized and included as a separate numeric comparison.

## T001 Solver

- Construct a dense `2L x 2L` complex Hamiltonian.
- Use the chiral block structure `H = [[0, C], [D, 0]]` and compute
  `E = +/- sqrt(eig(CD))`.
- When `CD` is the `t3=0` open-chain tridiagonal product, replace the direct
  non-normal eigenproblem by its similar symmetric tridiagonal form before
  diagonalization. This keeps the same squared-energy spectrum but removes
  roundoff-generated imaginary branches near the asymmetric hopping point
  `t1 = -gamma/2`.
- Sweep `t1` on a fixed grid.
- Emit one CSV row per eigenvalue per `t1`.
- Plot `|E|`, `Re(E)`, and `Im(E)` from the CSV.

For `L=40`, the matrix is `80 x 80`; direct dense diagonalization is fast, but
it is not reliable enough near strongly non-normal parameter values. The
structured block method preserves the exact spectral symmetry and exposes direct
diagonalization residuals as a diagnostic.

The `CD` block itself can still be highly non-normal on the negative side of the
scan. In particular, direct `eig(CD)` produced a spurious imaginary tail near
`t1 ~= -0.8` for the Fig. 2 parameters even though this region lies outside the
`|t1| < gamma/2` complex-spectrum window. The current solver detects the
tridiagonal open-chain structure and solves the equivalent symmetric problem
instead.

## Checks

The first target checks:

- nearest-neighbor chiral residual for the `E -> -E` symmetry;
- near-zero mode splitting well inside the predicted topological interval;
- absence of near-zero modes outside the predicted interval;
- finite-size gap suppression near the analytic transition.

These are analytic/structural checks. Later iterations should add digitized
curve comparison against the paper figure.

## T004 Solver

- Verify that `EQC006`, `EQC007`, and `EQC009` have open formula gates.
- Use `beta = r exp(i k)` with `N_beta=150`, matching Fig. 4.
- Compute `a(beta)` and `b(beta)` for `H(beta) = [[0,b],[a,0]]`.
- Use the branch-stable formula `W = (wind[a] - wind[b]) / 2`.
- Sweep `t1 in [-3,3]` and emit one CSV row per `t1`.

The check compares the resulting step function to the verified transition
`|t1| = sqrt(t2^2 + (gamma/2)^2)`.

Feature-level acceptance:

- `W=1` inside the topological interval and `W=0` outside it;
- transition occurs at the verified `|t1|`;
- no mismatches away from the finite grid tolerance near the transition.

## T003 Solver

- Verify that `EQC003`, `EQC006`, and `EQC007` have open formula gates.
- Fig. 3(a): evaluate the two beta roots from Eq. `bulkeigen` on real `E` for
  `t1=1` and for the transition point.
- Fig. 3(b): draw `C_beta` from `beta = r exp(i k)` with
  `r = sqrt(|(t1-gamma/2)/(t1+gamma/2)|)` and compare to the unit circle.
- Fig. 3(c): use the analytic left zero-mode profile and deterministic open-chain
  right eigenvectors for representative bulk states.

Checks:

- `C_beta` radius matches `sqrt(0.2)` for `t1=1`.
- On the bulk-energy branch, `|beta_1|=|beta_2|`.
- The zero mode and selected bulk right eigenvectors are localized near the left
  boundary.

These checks are independent of plot styling and would remain valid if the
figure were redrawn with different colors, marker spacing, or layout.

## T005 Solver

- Verify that `EQC001`, `EQC009`, and `EQC010` have open formula gates.
- Use the nonzero-`t3` quartic beta equation from the supplemental material.
- For the lower-panel invariant, evaluate the four `E=0` beta roots and sort
  them by modulus. The topological interval is the region where the two smallest
  roots come from the same off-diagonal factor; the transition occurs when the
  middle two moduli meet.
- For `C_beta` at `t1=1.1`, solve open-chain energies, compute the four beta
  roots for each energy, and retain the middle pair when their moduli agree.
  The plotted curve preserves `root_branch` identity and connects each branch in
  `angle_beta` order; it does not average different middle roots into one line.

Checks:

- transition points are near the caption value `t1 ~= +/-1.56`;
- `W=1` inside and `W=0` outside the transition interval;
- reconstructed `C_beta` is inside the unit circle but has a nonzero radius
  range, so it is not the `t3=0` circle;
- middle-root pairing error stays below the configured tolerance.

## Supplemental Targets

Supplemental Fig. 1 compares open-chain complex spectra against the theoretical
non-Bloch spectrum for `t1 = 0.2, 0.6, 1.0`; acceptance uses nearest-curve
distances in the complex plane.

Supplemental Fig. 2 repeats the spectrum and invariant check at `gamma=2.4`.
The accepted features are the four transition points and the plateau sequence
`0, 1, 0, 1, 0` as `t1` moves from negative to positive values.
