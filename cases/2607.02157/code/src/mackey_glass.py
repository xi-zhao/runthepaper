"""Mackey-Glass chaotic drive generation (paper Eq. 18 + Methods).

dx/dt = beta_MG * x(t - tau_MG) / (1 + x(t - tau_MG)^10) - gamma_MG * x(t)
with (beta_MG, gamma_MG, tau_MG) = (0.2, 0.1, 18). RK4 integration, transient
discarded, sampled every dt_samp = 3 time units, each sequence linearly
rescaled to [-1, 1].

Assumptions (not published in the paper): random initial history in [0.8, 1.6]
per sequence; internal RK4 step 0.1. The paper's verbal preprocessing ("linearly
rescaled to [-1,1]") cannot simultaneously give its stated statistics (mean ~ 0,
sigma_s^2 ~= 0.11, Fig. S1a2): a min-max rescale yields mean 0.14, var 0.24.
We therefore calibrate to the *published statistics*: each sequence is centered
and linearly scaled so the ensemble variance equals SIGMA_S2_TARGET = 0.11;
samples then lie within [-1,1] (max|s| ~ 0.77). This affine choice changes only
the drive amplitude convention and is recorded in EQUATION_CARDS.json (EQC002).
"""
from __future__ import annotations

import numpy as np

BETA_MG = 0.2
GAMMA_MG = 0.1
TAU_MG = 18.0
DT_SAMP = 3.0
DT_INT = 0.1  # internal RK4 step; tau/dt_int and dt_samp/dt_int are integers
SIGMA_S2_TARGET = 0.11  # paper's stated empirical drive variance (SI III.B)


def _mg_rhs(x_now: np.ndarray, x_delay: np.ndarray) -> np.ndarray:
    return BETA_MG * x_delay / (1.0 + x_delay**10) - GAMMA_MG * x_now


def generate_mg_sequences(
    n_sequences: int,
    n_samples: int,
    *,
    transient_samples: int = 300,
    seed: int = 0,
) -> np.ndarray:
    """Return an (n_sequences, n_samples) array of rescaled MG samples.

    All sequences are integrated in parallel with RK4. The delay term is
    evaluated on the integration grid (tau_MG / DT_INT steps back); RK4
    substeps reuse the two neighboring history points (linear interpolation
    at the half step), which is standard for delay equations at this step size.
    """
    rng = np.random.default_rng(seed)
    delay_steps = int(round(TAU_MG / DT_INT))
    steps_per_sample = int(round(DT_SAMP / DT_INT))
    total_samples = transient_samples + n_samples
    total_steps = total_samples * steps_per_sample

    # history buffer: constant random initial history per sequence
    history = np.empty((n_sequences, delay_steps + total_steps + 1), dtype=np.float64)
    history[:, : delay_steps + 1] = rng.uniform(0.8, 1.6, size=(n_sequences, 1))

    for step in range(total_steps):
        idx = delay_steps + step
        x_now = history[:, idx]
        x_del0 = history[:, idx - delay_steps]
        x_del1 = history[:, idx - delay_steps + 1]
        x_del_half = 0.5 * (x_del0 + x_del1)

        k1 = _mg_rhs(x_now, x_del0)
        k2 = _mg_rhs(x_now + 0.5 * DT_INT * k1, x_del_half)
        k3 = _mg_rhs(x_now + 0.5 * DT_INT * k2, x_del_half)
        k4 = _mg_rhs(x_now + DT_INT * k3, x_del1)
        history[:, idx + 1] = x_now + (DT_INT / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    samples = history[:, delay_steps::steps_per_sample][:, :total_samples]
    samples = samples[:, transient_samples:]

    centered = samples - samples.mean(axis=1, keepdims=True)
    scale = np.sqrt(SIGMA_S2_TARGET / centered.var())
    rescaled = centered * scale
    if np.abs(rescaled).max() > 1.0:  # keep the paper's [-1,1] support guarantee
        rescaled /= np.abs(rescaled).max()
    return rescaled


def sequence_statistics(samples: np.ndarray) -> dict:
    """Mean/variance and dominant angular frequency (per sampled step) of the ensemble."""
    mean = float(samples.mean())
    var = float(samples.var())
    centered = samples - samples.mean(axis=1, keepdims=True)
    power = np.abs(np.fft.rfft(centered, axis=1)) ** 2
    avg_power = power.mean(axis=0)
    freqs = 2.0 * np.pi * np.fft.rfftfreq(samples.shape[1], d=1.0)
    peak_idx = 1 + int(np.argmax(avg_power[1:]))
    return {
        "mean": mean,
        "variance": var,
        "omega_peak": float(freqs[peak_idx]),
        "freqs": freqs,
        "avg_power": avg_power,
    }


if __name__ == "__main__":
    seqs = generate_mg_sequences(64, 2000, seed=1)
    stats = sequence_statistics(seqs)
    print({k: v for k, v in stats.items() if k in ("mean", "variance", "omega_peak")})
