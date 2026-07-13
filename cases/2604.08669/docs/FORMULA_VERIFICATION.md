# Formula and method verification

## Verified in this reduced pass

- Assignment-distance metrics for Fig. 3 are computed directly from atom and target coordinates.
- P2WGS intensity continuity follows the relative frame-to-frame trap-intensity definition in the paper.
- P2WGS phase continuity uses wrapped phase differences normalized by `2 pi`.
- The Fig. 5 timing model encodes the bottleneck switch at `generation_time = SLM_refresh_time`.
- The software assembly run feeds measured local P2WGS generation time into the same timing formula after decoding one assignment.
- The sweep preserves the same formula chain across multiple scales and P2WGS iteration counts.
- The CPU modified-auction decoder produces valid one-to-one assignments and recovers the Hungarian labels when the optimal edges are scored as one.
- The Stage 13 metric-contract audit confirms the Fig. 3 path-planning contract
  at paper geometry: use Euclidean average and maximum movement distances for
  reporting, but keep squared-distance Hungarian labels for training. On 32
  `127 x 127` to `101 x 101` paper-geometry samples with target spacing `1.26`,
  squared labels give mean average distance `0.5162` and mean maximum distance
  `1.9079` versus the paper Hungarian baselines `0.5112` and `1.82`; Euclidean
  labels give mean average distance `0.5122` but mean maximum distance `2.2871`.
  The audit therefore selects `squared_distance`.

## Not yet verified at paper scale

- Paper's GPU-parallel modified-auction implementation and timing.
- Full `127 x 127` to `101 x 101` path-planning benchmark with 1024 random instances.
- `N=10201` P2WGS continuity statistics and error bars.
- RTX 5090 timing in Fig. 5.
- Closed-loop atom feedback and hardware execution.
