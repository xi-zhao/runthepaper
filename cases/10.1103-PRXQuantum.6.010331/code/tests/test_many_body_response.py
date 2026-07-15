from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))

from src.many_body_response import (  # noqa: E402
    AdiabaticSchedule,
    ManyBodyModel,
    adiabatic_controls,
    adiabatic_response,
    dense_hamiltonian,
    noise_operator,
    quench_response,
    z2_probabilities,
)


def test_many_body_hamiltonian_and_noise_operators_are_hermitian() -> None:
    model = ManyBodyModel(sites=3, rabi_frequency_mhz=1.0, duration_us=0.5)
    hamiltonian = dense_hamiltonian(
        model,
        omega_per_us=model.omega_per_us,
        detuning_per_us=0.3 * model.omega_per_us,
    )
    assert np.allclose(hamiltonian, hamiltonian.conj().T)
    for noise_kind in ("frequency", "intensity"):
        operator = noise_operator(
            model,
            omega_per_us=model.omega_per_us,
            noise_kind=noise_kind,
        )
        assert np.allclose(operator, operator.conj().T)


def test_quench_response_is_finite_and_nonnegative() -> None:
    model = ManyBodyModel(sites=3, rabi_frequency_mhz=1.0, duration_us=0.5)
    frequencies = np.linspace(0.0, 2.0, 9)
    for noise_kind in ("frequency", "intensity"):
        response = quench_response(model, frequencies, noise_kind=noise_kind)
        assert np.all(np.isfinite(response))
        assert np.all(response >= 0.0)


def test_adiabatic_schedule_has_published_endpoint_magnitudes() -> None:
    model = ManyBodyModel(sites=3, rabi_frequency_mhz=1.0, duration_us=1.0)
    omega, detuning = adiabatic_controls(
        model,
        AdiabaticSchedule(),
        np.asarray([0.0, 0.5, 1.0]),
    )
    assert np.allclose(omega[[0, 2]], 0.0, atol=1.0e-12)
    assert np.isclose(omega[1], model.omega_per_us)
    assert np.allclose(
        detuning[[0, 2]] / model.omega_per_us,
        [-10.0, 10.0],
    )


def test_small_adiabatic_tangent_run_preserves_norm() -> None:
    model = ManyBodyModel(
        sites=3,
        rabi_frequency_mhz=0.4,
        duration_us=0.8,
        nearest_neighbor_interaction_over_omega=8.0,
    )
    response, diagnostics = adiabatic_response(
        model,
        np.linspace(0.0, 2.0, 5),
        noise_kind="frequency",
        time_steps=300,
    )
    assert diagnostics["norm_error"] < 2.0e-5
    assert np.all(np.isfinite(response))
    assert np.all(response >= 0.0)
    probabilities = z2_probabilities(model, diagnostics["final_state"])
    assert 0.0 <= probabilities["total"] <= 1.0 + 1.0e-8
