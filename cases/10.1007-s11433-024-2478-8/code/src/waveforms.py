"""Fourier-series waveforms for the BAM/ORMD gate (Sun 2024, DOI 10.1007/s11433-024-2478-8).

The paper (main text, page 4) defines every Rabi-frequency and detuning waveform
through a coefficient list ``[a0, a1, ..., aN]`` with the interpretation

    f(t) = 2*pi * ( a0 + sum_{n=1..N} [ a_n exp(2j*pi*n*t/tau) + conj(a_n) exp(-2j*pi*n*t/tau) ] )
           / (2N + 1)     [angular frequency, i.e. 2*pi * MHz]

for a reference time ``tau = 0.25 us``.  All published coefficients are real, so
this collapses to a real cosine series

    f(t) = 2*pi * ( a0 + 2 * sum_{n=1..N} a_n cos(2*pi*n*t/tau) ) / (2N + 1)   [rad/us]

Time is measured in microseconds and angular frequencies in rad/us throughout the
case, so a value of ``2*pi`` here corresponds to 1 MHz.

Self-consistency with Fig. 3(a) is used as a source-trace check (see tests):
  * every amplitude waveform starts at ~0 (smooth turn-on), and
  * the hybrid Omega_2 peaks at ~2*pi*16.4 MHz at the pulse centre t = tau/2,
    so Omega_1 = 0.686*Omega_2 peaks at ~2*pi*11.2 MHz, matching the blue solid
    curve of Fig. 3(a).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

TAU_US = 0.25  # reference time tau, microseconds (paper: 0.25 us)
TWO_PI = 2.0 * np.pi


def fourier_waveform(coeffs: Sequence[float], t, tau: float = TAU_US):
    """Evaluate the paper's truncated Fourier waveform, returning rad/us.

    ``coeffs`` = [a0, a1, ..., aN]; the normalisation is 1/(2N+1) with N = len-1.
    """
    a = np.asarray(coeffs, dtype=float)
    n_max = a.size - 1
    norm = 2 * n_max + 1
    t = np.asarray(t, dtype=float)
    value = np.full(t.shape, a[0], dtype=float)
    for n in range(1, a.size):
        value = value + 2.0 * a[n] * np.cos(TWO_PI * n * t / tau)
    return TWO_PI * value / norm  # 2*pi * MHz  ->  rad/us


@dataclass(frozen=True)
class ConstantWaveform:
    """A constant angular-frequency term, stored already in 2*pi*MHz (rad/us)."""

    value_mhz: float

    def __call__(self, t):
        t = np.asarray(t, dtype=float)
        return np.full(t.shape, TWO_PI * self.value_mhz, dtype=float)


@dataclass(frozen=True)
class FourierWaveform:
    """A Fourier waveform defined by real coefficients ``[a0..aN]`` (MHz-scaled)."""

    coeffs: tuple

    def __call__(self, t):
        return fourier_waveform(self.coeffs, t)


def scaled(coeffs: Sequence[float], factor: float) -> tuple:
    """Linearly scale a coefficient list (e.g. Omega_1 = 0.686 * Omega_2)."""
    return tuple(factor * c for c in coeffs)
