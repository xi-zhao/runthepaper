# Frozen-gold audit

Verdict: `benchmark_gold_invalid`.

- Task 1 is correct for symmetric coupling: the dispersion and immiscibility condition match source Eqs. S10–S12.
- Task 2 is invalid. For `gamma=k sqrt(2S-k^2)`, the frozen `c=d gamma/dk=2(S-k^2)/sqrt(2S-k^2)` is positive and strictly decreasing on `0<k<sqrt(S)`, with infimum zero that is not attained. Thus neither `V_MI` nor a minimizing `kmin` exists under the frozen definition.
- The source uses the stable branch: `d omega/dk` on `k>sqrt(2S)` has `kmin=sqrt(3S)` and `V=4 sqrt(S)`.
- Task 3's maximizing mixture is valid because both alleged and source speeds are monotone in `S`. Its speed is not: the frozen formula evaluates to `0.2503450686758295`, not the printed `0.250370248905988`; the source speed is `0.4336103783708565`.
- Task 4's `kmax=0.1533044194694486` is valid. The paper-consistent `kmin` is `0.1877588015068721`, not `0.0885103478486455`.
- Task 5 is downstream of the undefined frozen speed. Even accepting its prefactor, the displayed cubic coefficient drops another factor of two; the consistent frozen-prefactor value is `-0.2535007076986708`, while the source coefficient is `-0.4390761054887646`.
