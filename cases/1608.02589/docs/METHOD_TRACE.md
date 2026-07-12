# Method Trace

## Local Numerical Method

The implementation uses exact small-size Floquet simulation:

1. Build the `z`-basis table for `L` spins.
2. Sample disorder fields and coupling disorder.
3. Apply the pulse `U1` as a product of single-qubit `x` rotations.
4. Apply `U2` as a diagonal phase in the `z` basis.
5. Evolve random product states and compute `R(n)`.
6. Fourier transform `R(n)` and extract the half-frequency response.
7. For smaller systems, explicitly diagonalize the Floquet unitary to compute quasienergy level statistics and endpoint mutual information.
8. Check sensitive observables against simple limiting states before using them for figure acceptance.

## Code

- `src/dtc_feature_sim.py`: model, evolution, observables, data generation.
- `scripts/run_reproduction.py`: runs all numerical targets.
- `scripts/plot_reproduction.py`: turns generated CSV files into figures.
- `scripts/run_reproduction_iteration2.py`: second-pass higher-scale scans and corrected mutual information.
- `scripts/plot_reproduction_iteration2.py`: second-pass figures.

## Parameter Scale

| Quantity | Paper | Local case |
| --- | --- | --- |
| Main time trace system size | `L = 14` | `L = 14` in iteration 2 |
| Disorder averages | up to `10^2-10^4` depending target | `O(10)` to `O(30)` samples |
| Mutual information scaling | `L = 8-18` | `L = 6, 8, 10` feature-flow check |
| Drive window | late stroboscopic periods | late stroboscopic periods |
| Disorder | `W = 2 pi` | `W = 2 pi` |

## Interpretation

The code now tests the paper's main numerical mechanism across all main-text numerical figures. The time-crystal rigidity, variance peaks, long-range variant, and mutual-information flow appear clearly. Critical scaling still requires larger exact diagonalization and more disorder samples than this local case runs.
