from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))

from src.fidelity_response import (  # noqa: E402
    GateParameters,
    appendix_fit,
    frequency_noise_operator,
    ideal_hamiltonian,
    input_projector,
    intensity_noise_operator,
    scale_universal_response,
    universal_responses,
)


def test_hamiltonian_and_noise_operators_are_hermitian() -> None:
    params = GateParameters()
    for time in (0.0, 0.37 * params.duration, params.duration):
        hamiltonian = ideal_hamiltonian(time, params)
        intensity = intensity_noise_operator(time, params)
        assert np.allclose(hamiltonian, hamiltonian.conj().T)
        assert np.allclose(intensity, intensity.conj().T)
    frequency = frequency_noise_operator()
    assert np.allclose(frequency, frequency.conj().T)


def test_input_projectors_have_expected_ranks() -> None:
    for metric, dimension in (("haar", 4), ("symmetric_haar", 3)):
        projector, returned_dimension = input_projector(metric)
        assert returned_dimension == dimension
        assert np.allclose(projector @ projector, projector)
        assert np.isclose(np.trace(projector), dimension)


def test_scaling_round_trip() -> None:
    normalized = np.linspace(0.0, 5.0, 101)
    g_frequency = appendix_fit(normalized, "haar", "frequency")
    g_intensity = appendix_fit(normalized, "haar", "intensity")
    physical = np.linspace(0.0, 15.0, 101)
    scaled_frequency, scaled_intensity = scale_universal_response(
        normalized,
        g_frequency,
        g_intensity,
        physical,
        3.0,
    )
    expected_x = physical / 3.0
    assert np.allclose(
        scaled_frequency * (2.0 * np.pi * 3.0) ** 2,
        np.interp(expected_x, normalized, g_frequency),
    )
    assert np.allclose(scaled_intensity, np.interp(expected_x, normalized, g_intensity))


def test_appendix_l_reference_values() -> None:
    frequencies = np.asarray([0.0, 0.5, 1.2, 3.0])
    haar_frequency = appendix_fit(frequencies, "haar", "frequency")
    haar_intensity = appendix_fit(frequencies, "haar", "intensity")
    assert np.allclose(
        haar_frequency,
        [115.54324516596891, 74.98560295167107, 120.5807295193262, 0.0010486306080755379],
    )
    assert np.allclose(
        haar_intensity,
        [1.1001108950400547, 1.0751009249877332, 0.0745801624599095, 7.545416421594899e-7],
    )


def test_small_direct_response_is_nonnegative_and_finite() -> None:
    frequencies = np.linspace(0.0, 2.0, 9)
    curves, diagnostics = universal_responses(frequencies, time_points=301)
    assert diagnostics["unitarity_error"] < 1.0e-10
    for curve in curves.values():
        assert np.all(np.isfinite(curve))
        assert float(np.min(curve)) >= -1.0e-8
