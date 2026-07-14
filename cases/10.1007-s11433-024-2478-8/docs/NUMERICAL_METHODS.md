# Numerical methods

## Equations solved

For each register sector we integrate the time-dependent Schrödinger equation

```
i dψ/dt = H(t) ψ,    ħ = 1,   t ∈ [0, τ],  τ = 0.25 μs
```

with `H(t)` the sector Hamiltonian built from the paper's waveforms. Frequencies
are in rad/μs (`2π·MHz`). Populations are `|⟨init|ψ(t)⟩|²`; phases are
`arg⟨init|ψ(t)⟩`.

## Sectors and dimensions

| Input | Single-photon | Two-photon |
| --- | --- | --- |
| `|00>` | 2 states | 3–4 (`{1,e,r,q}`) |
| `|01>/|10>` | 5 states | 16 states |
| `|11>` | 9 states | 64 states |

## Solver settings

- Method: `scipy.integrate.solve_ivp`, `DOP853`.
- Single-photon: `rtol = 1e-11`, `atol = 1e-12`, `max_step = τ/400`.
- Two-photon: `rtol = 1e-10`, `atol = 1e-12`, `max_step = τ/4000`. The large
  one-photon detuning `Δ0 = 2π·5 GHz` drives a fast intermediate-state
  oscillation (period ~2e-4 μs); the step cap resolves it. Convergence verified:
  the `|111>` amplitude is identical to < 1e-6 at `max_step = τ/4000`, `τ/20000`,
  and `τ/60000`, so the reported two-photon gate error (~1.3e-3) is physical, not
  numerical.
- Norm drift < ~1e-14 over the gate (used as a unitarity check).

## Gate error

The realised computational gate is a diagonal, slightly sub-unitary
`U = diag(a00, a01, a10, a11)` with `a10 = a01` by symmetry. We compute the
Pedersen average gate error `1 − F_avg` against the ideal CZ, maximised over the
free single-qubit Z rotations `(α, β)` (Nelder–Mead). This is the paper's
"evaluated in the typical way [48,49]".

## Cost

Everything runs on a laptop CPU. Fig. 3 sectors take milliseconds; Fig. 4/5 take
~1 minute each (fast `Δ0` oscillation); the Fig. 7 81×81 scan takes a few minutes
across CPU cores. No GPU, cluster, or remote resource is required.
