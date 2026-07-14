# Formula verification

The public implementation verifies the following identities before accepting
the generated results:

| Object | Verification |
| --- | --- |
| Site transfer matrix | Reduces the fourth-order lattice equation to a one-step companion update. |
| Clean Lyapunov limit | Matches `log|beta_s|` from the four roots of the clean characteristic polynomial. |
| OBC/PBC potentials | Uses the required ordered/positive Lyapunov sums and the `log|t_2|` constant. |
| State classification | Depends only on the signs of the two central exponents. |
| Winding | Lyapunov positive-count rule agrees with a direct twisted-boundary determinant check. |
| Anderson fraction | Counts independently classified OBC eigenstates and remains in `[0,1]`. |

The formal Science Bulletin supplementary material was used to check the QR
formulation, but the reproduced figures and parameter target remain those of
arXiv v1.
