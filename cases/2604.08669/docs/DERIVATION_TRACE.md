# Derivation trace

## Vacuum-lifetime constraint

If the vacuum lifetime is `tau` and the target array has `N` atoms, assembly should finish well below `tau / N` to avoid losing atoms during rearrangement. This motivates the paper's target of completing a 10k-scale rearrangement in much less than 50 ms.

## Assignment object

Initial occupied atom sites and final target sites define a one-to-one assignment problem. Hungarian assignment gives the exact global baseline. The GNN path planner learns edge probabilities on a sparse candidate graph and needs a decoder to recover a consistent assignment.

The reproduction metrics for Fig. 3 are:

```text
average_distance = mean_j || atom_j - target_assignment(j) ||
maximum_distance = max_j || atom_j - target_assignment(j) ||
distance_gap = decoded_distance - Hungarian_distance
```

## P2WGS object

The SLM plane and the tweezer plane are Fourier-conjugate planes. The forward model is an FFT from the phase-only SLM field to the complex optical field in the tweezer plane.

The reduced implementation iterates:

```text
SLM field -> FFT -> tweezer field
replace target support with Gaussian amplitude and target phase
tweezer field -> iFFT -> SLM field
keep only SLM phase with fixed input amplitude
```

The paper's continuity metrics are encoded as:

```text
intensity_continuity_n =
  mean_j |I_{n+1}^{(j)} - I_n^{(j)}| / ((I_{n+1}^{(j)} + I_n^{(j)}) / 2)

phase_continuity_n =
  mean_j wrap(phi_{n+1}^{(j)} - phi_n^{(j)}) / (2 pi)
```

## Pipeline timing object

For a trajectory with `F` hologram frames, the reduced timing model is:

```text
T_total = T_path + T_transfer + F * max(T_generation_per_frame, T_SLM_refresh)
```

The kink in Fig. 5(b) appears when `T_generation_per_frame = T_SLM_refresh`.
