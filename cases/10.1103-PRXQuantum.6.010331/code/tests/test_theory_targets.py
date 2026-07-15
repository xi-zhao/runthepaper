from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))

from src.theory_targets import (  # noqa: E402
    INTENSITY_STANDARD_DEVIATION,
    cavity_power_transfer,
    error_budget,
    normalized_error_scalings,
    phase_flip_fidelities,
    phase_flip_proxy,
    principal_quantum_number_scaling,
    spin_lock_response,
    ssb_return_probability_first_order,
)


def test_error_budget_keeps_unpublished_variances_explicit() -> None:
    rabi = np.asarray([3.0, 7.7])
    budget = error_budget(rabi)
    assert budget.frequency is None
    assert budget.motion is None
    assert budget.complete_total is None
    assert np.all(budget.intensity > 0.0)
    assert np.all(budget.decay > 0.0)
    assert np.allclose(budget.known_total, budget.intensity + budget.decay)

    completed = error_budget(
        rabi,
        frequency_variance_mhz2=0.01,
        doppler_variance_mhz2=0.02,
    )
    assert completed.complete_total is not None
    assert np.allclose(
        completed.complete_total,
        completed.known_total + completed.frequency + completed.motion,
    )


def test_fig7_asymptotic_scalings() -> None:
    curves = normalized_error_scalings(np.asarray([3.85, 7.7, 15.4]))
    assert np.allclose(curves["frequency"], [4.0, 1.0, 0.25])
    assert np.allclose(curves["intensity"], 1.0)
    assert np.allclose(curves["decay"], [2.0, 1.0, 0.5])
    assert np.allclose(curves["motion"], [4.0, 1.0, 0.25])


def test_fixed_power_scaling_hits_both_printed_anchors() -> None:
    scaling = principal_quantum_number_scaling(np.asarray([44.0, 61.0]))
    assert np.allclose(scaling["rabi_frequency_mhz"], [13.0, 7.7])
    assert np.isclose(scaling["blockade_limited_spacing_um"][1], 3.3)
    assert np.isclose(scaling["blockade_limited_spacing_um"][0], 1.7, atol=0.04)


def test_spin_lock_filter_is_resonant_at_rabi_frequency() -> None:
    frequencies = np.asarray([0.0, 1.0, 2.0])
    response = spin_lock_response(
        frequencies,
        locking_rabi_mhz=1.0,
        duration_us=20.0,
    )
    assert response[1] > response[0]
    assert response[1] > response[2]
    assert np.isclose(response[1], 0.5 * np.pi**2 * 20.0**2)


def test_cavity_transfer_has_correct_limits() -> None:
    transfer = cavity_power_transfer(np.asarray([0.0, 0.14, 1.4]))
    assert np.isclose(transfer[0], 1.0)
    assert np.isclose(transfer[1], 0.5)
    assert transfer[2] < 0.011


def test_appendix_d_phase_flip_formulas_and_limits() -> None:
    p_values = np.asarray([0.0, 0.01])
    fidelities = phase_flip_fidelities(p_values)
    assert np.isclose(fidelities["product_state_fidelity"][0], 1.0)
    assert np.isclose(fidelities["symmetric_state_fidelity"][0], 1.0)
    assert fidelities["symmetric_state_fidelity"][1] < fidelities["product_state_fidelity"][1]

    counts = np.arange(2, 11)
    perfect = ssb_return_probability_first_order(
        counts,
        phase_flip_probability=0.0,
        depolarizing_strength=0.0,
        single_qubit_gate_count=10,
    )
    assert np.allclose(perfect, 1.0)

    proxy = phase_flip_proxy(
        p_values,
        np.asarray([0.0, 0.003]),
        single_qubit_gate_count=10,
    )
    assert np.isclose(proxy["first_order_slope"][0], 1.0)
    assert np.allclose(proxy["first_order_ssb_infidelity"][:, 0], 0.0)
    assert INTENSITY_STANDARD_DEVIATION == 0.008
