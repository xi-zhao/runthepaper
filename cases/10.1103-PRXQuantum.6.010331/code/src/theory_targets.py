from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .fidelity_response import appendix_fit


RYDBERG_DARK_LIFETIME_US = 78.0
RYDBERG_BRIGHT_LIFETIME_US = 166.0
RYDBERG_TOTAL_DECAY_PER_US = (
    1.0 / RYDBERG_DARK_LIFETIME_US + 1.0 / RYDBERG_BRIGHT_LIFETIME_US
)
INTENSITY_STANDARD_DEVIATION = 0.008


@dataclass(frozen=True)
class ErrorBudget:
    """Formula-resolved Fig. 7 terms without hidden noise amplitudes.

    The frequency and motion arrays are evaluated only when their variances are
    explicitly supplied. Their per-variance coefficients are always returned,
    so unavailable experimental inputs stay visible instead of being guessed.
    """

    rabi_frequency_mhz: np.ndarray
    frequency_per_mhz2: np.ndarray
    intensity: np.ndarray
    decay: np.ndarray
    motion_per_mhz2: np.ndarray
    known_total: np.ndarray
    frequency: np.ndarray | None
    motion: np.ndarray | None
    complete_total: np.ndarray | None


def error_budget(
    rabi_frequencies_mhz: np.ndarray,
    *,
    frequency_variance_mhz2: float | None = None,
    doppler_variance_mhz2: float | None = None,
    decay_rate_per_us: float = RYDBERG_TOTAL_DECAY_PER_US,
    intensity_standard_deviation: float = INTENSITY_STANDARD_DEVIATION,
) -> ErrorBudget:
    """Evaluate the independently specified quasistatic Fig. 7 model.

    Frequency response uses the Appendix-L symmetric-Haar zero-frequency
    coefficient. Motion uses the paper's printed coefficient 3.0. The decay
    term uses the two measured lifetimes and the printed factor 2.6.
    """

    rabi = np.asarray(rabi_frequencies_mhz, dtype=np.float64)
    if rabi.ndim != 1 or np.any(rabi <= 0.0):
        raise ValueError("rabi_frequencies_mhz must be a positive one-dimensional array")
    if decay_rate_per_us < 0.0 or intensity_standard_deviation < 0.0:
        raise ValueError("noise amplitudes must be non-negative")
    if frequency_variance_mhz2 is not None and frequency_variance_mhz2 < 0.0:
        raise ValueError("frequency_variance_mhz2 must be non-negative")
    if doppler_variance_mhz2 is not None and doppler_variance_mhz2 < 0.0:
        raise ValueError("doppler_variance_mhz2 must be non-negative")

    frequency_dc = float(
        appendix_fit(np.asarray([0.0]), "symmetric_haar", "frequency")[0]
    )
    intensity_dc = float(
        appendix_fit(np.asarray([0.0]), "symmetric_haar", "intensity")[0]
    )
    frequency_per_mhz2 = frequency_dc / np.square(2.0 * np.pi * rabi)
    intensity = np.full_like(rabi, intensity_dc * intensity_standard_deviation**2)
    decay = 2.6 * decay_rate_per_us / (2.0 * np.pi * rabi)
    motion_per_mhz2 = 3.0 / np.square(rabi)
    known_total = intensity + decay

    frequency = (
        None
        if frequency_variance_mhz2 is None
        else frequency_per_mhz2 * frequency_variance_mhz2
    )
    motion = (
        None
        if doppler_variance_mhz2 is None
        else motion_per_mhz2 * doppler_variance_mhz2
    )
    complete_total = (
        None
        if frequency is None or motion is None
        else known_total + frequency + motion
    )
    return ErrorBudget(
        rabi_frequency_mhz=rabi,
        frequency_per_mhz2=frequency_per_mhz2,
        intensity=intensity,
        decay=decay,
        motion_per_mhz2=motion_per_mhz2,
        known_total=known_total,
        frequency=frequency,
        motion=motion,
        complete_total=complete_total,
    )


def normalized_error_scalings(
    rabi_frequencies_mhz: np.ndarray,
    *,
    reference_rabi_mhz: float = 7.7,
) -> dict[str, np.ndarray]:
    """Return the four Fig. 7 asymptotic laws normalized at one Rabi rate."""

    rabi = np.asarray(rabi_frequencies_mhz, dtype=np.float64)
    if np.any(rabi <= 0.0) or reference_rabi_mhz <= 0.0:
        raise ValueError("Rabi frequencies must be positive")
    ratio = rabi / reference_rabi_mhz
    return {
        "rabi_frequency_mhz": rabi,
        "frequency": np.power(ratio, -2.0),
        "intensity": np.ones_like(rabi),
        "decay": np.power(ratio, -1.0),
        "motion": np.power(ratio, -2.0),
    }


def principal_quantum_number_scaling(
    principal_quantum_numbers: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """Evaluate the fixed-power scalings fixed by the two printed anchors.

    This function intentionally stops before adding unpublished lifetime,
    electric-field, and laser-noise arrays. It therefore reproduces the
    independently determined kinematic part of Fig. 8, not its total curve.
    """

    n_values = np.asarray(principal_quantum_numbers, dtype=np.float64)
    if np.any(n_values <= 0.0):
        raise ValueError("principal quantum numbers must be positive")
    rabi_exponent = float(np.log(13.0 / 7.7) / np.log(61.0 / 44.0))
    rabi_mhz = 7.7 * np.power(61.0 / n_values, rabi_exponent)
    spacing_um = 3.3 * np.power(n_values / 61.0, 25.0 / 12.0)
    return {
        "principal_quantum_number": n_values,
        "rabi_frequency_mhz": rabi_mhz,
        "blockade_limited_spacing_um": spacing_um,
        "rabi_scaling_exponent": rabi_exponent,
    }


def spin_lock_response(
    frequencies_mhz: np.ndarray,
    *,
    locking_rabi_mhz: float,
    duration_us: float,
) -> np.ndarray:
    """Evaluate Appendix H's finite-time sinc-squared response."""

    frequencies = np.asarray(frequencies_mhz, dtype=np.float64)
    if locking_rabi_mhz <= 0.0 or duration_us <= 0.0:
        raise ValueError("locking_rabi_mhz and duration_us must be positive")
    positive = np.sinc((locking_rabi_mhz + frequencies) * duration_us)
    resonant = np.sinc((locking_rabi_mhz - frequencies) * duration_us)
    return 0.5 * np.pi**2 * duration_us**2 * (positive**2 + resonant**2)


def spin_lock_decay_rate(
    frequency_psd_hz2_per_hz: np.ndarray,
    *,
    decay_rate_per_us: float = RYDBERG_TOTAL_DECAY_PER_US,
) -> np.ndarray:
    """Map an independently sourced numerical PSD to the long-time rate."""

    psd = np.asarray(frequency_psd_hz2_per_hz, dtype=np.float64)
    if np.any(psd < 0.0) or decay_rate_per_us < 0.0:
        raise ValueError("PSD and decay rate must be non-negative")
    rydberg_floor_per_second = 0.5 * decay_rate_per_us * 1.0e6
    return np.pi**2 * psd + rydberg_floor_per_second


def cavity_power_transfer(
    frequencies_mhz: np.ndarray,
    *,
    linewidth_mhz: float = 0.14,
) -> np.ndarray:
    """Return the explicitly reconstructed single-pole cavity power transfer."""

    frequencies = np.asarray(frequencies_mhz, dtype=np.float64)
    if linewidth_mhz <= 0.0:
        raise ValueError("linewidth_mhz must be positive")
    return 1.0 / (1.0 + np.square(frequencies / linewidth_mhz))


def cavity_filtered_psd(
    frequencies_mhz: np.ndarray,
    psd_hz2_per_hz: np.ndarray,
    *,
    linewidth_mhz: float = 0.14,
) -> np.ndarray:
    """Apply the cavity transfer to an independently sourced numerical PSD."""

    psd = np.asarray(psd_hz2_per_hz, dtype=np.float64)
    if np.any(psd < 0.0):
        raise ValueError("PSD must be non-negative")
    return psd * cavity_power_transfer(
        frequencies_mhz,
        linewidth_mhz=linewidth_mhz,
    )


def phase_flip_fidelities(
    phase_flip_probabilities: np.ndarray,
) -> dict[str, np.ndarray]:
    """Evaluate the two exact state-average formulas printed in Appendix D."""

    p_values = np.asarray(phase_flip_probabilities, dtype=np.float64)
    if np.any((p_values < 0.0) | (p_values > 1.0)):
        raise ValueError("phase-flip probabilities must lie in [0, 1]")
    return {
        "phase_flip_probability": p_values,
        "product_state_fidelity": 1.0 - 4.0 * p_values / 3.0 + 8.0 * p_values**2 / 15.0,
        "symmetric_state_fidelity": 1.0 - 5.0 * p_values / 3.0 + p_values**2,
    }


def ssb_return_probability_first_order(
    n_cz: np.ndarray,
    *,
    phase_flip_probability: float,
    depolarizing_strength: float,
    single_qubit_gate_count: int,
) -> np.ndarray:
    """Evaluate the Appendix-D return-probability equation through O(p)."""

    counts = np.asarray(n_cz, dtype=np.float64)
    p_value = float(phase_flip_probability)
    d_value = float(depolarizing_strength)
    if np.any(counts < 0.0) or single_qubit_gate_count < 0:
        raise ValueError("gate counts must be non-negative")
    if not 0.0 <= p_value <= 1.0 or not 0.0 <= d_value <= 1.0:
        raise ValueError("channel probabilities must lie in [0, 1]")
    phase_prefactor = 1.0 - 5.0 * single_qubit_gate_count * p_value / 3.0
    survival = np.power(1.0 - d_value, counts)
    return phase_prefactor * survival + 0.25 * (1.0 - survival)


def phase_flip_proxy(
    phase_flip_probabilities: np.ndarray,
    symmetric_infidelities: np.ndarray,
    *,
    single_qubit_gate_count: int,
) -> dict[str, np.ndarray]:
    """Evaluate the printed first-order SSB slope, without fitted image data."""

    p_values = np.asarray(phase_flip_probabilities, dtype=np.float64)
    symmetric = np.asarray(symmetric_infidelities, dtype=np.float64)
    if np.any((p_values < 0.0) | (p_values > 1.0)):
        raise ValueError("phase-flip probabilities must lie in [0, 1]")
    if np.any((symmetric < 0.0) | (symmetric > 0.75)):
        raise ValueError("symmetric infidelities must lie in [0, 0.75]")
    slopes = 1.0 - 5.0 * single_qubit_gate_count * p_values / 9.0
    inferred = slopes[:, None] * symmetric[None, :]
    return {
        "phase_flip_probability": p_values,
        "symmetric_infidelity": symmetric,
        "first_order_slope": slopes,
        "first_order_ssb_infidelity": inferred,
    }
