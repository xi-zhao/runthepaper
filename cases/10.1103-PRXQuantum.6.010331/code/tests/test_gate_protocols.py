from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))

from src.fidelity_response import gate_diagnostics  # noqa: E402
from src.gate_protocols import (  # noqa: E402
    control_hamiltonian,
    fromonteil_protocol_ii_variant_1,
    integrated_rydberg_population,
    levine_pichler_protocol,
    protocol_response,
    protocol_trajectory,
)


def test_protocol_hamiltonian_is_hermitian() -> None:
    for phase in (0.0, np.pi / 2.0, 3.90242):
        hamiltonian = control_hamiltonian(phase, detuning_over_omega=0.377371)
        assert np.allclose(hamiltonian, hamiltonian.conj().T)


def test_cited_protocol_durations() -> None:
    assert np.isclose(levine_pichler_protocol().duration, 2.0 * 4.29268)
    assert np.isclose(
        fromonteil_protocol_ii_variant_1().duration,
        2.0 * (2.0 + np.sqrt(2.0)) * np.pi,
    )


def test_protocols_close_to_controlled_phase_gates() -> None:
    for protocol in (
        levine_pichler_protocol(),
        fromonteil_protocol_ii_variant_1(),
    ):
        _, propagators, _ = protocol_trajectory(protocol, points_per_radian=30)
        diagnostics = gate_diagnostics(propagators[-1])
        assert diagnostics["max_return_leakage"] < 2.0e-9
        assert diagnostics["controlled_phase_error_radians"] < 2.0e-5
        assert diagnostics["minimum_return_probability"] > 1.0 - 2.0e-9


def test_fromonteil_protocol_has_zero_dc_intensity_response() -> None:
    frequencies = np.asarray([0.0, 0.25])
    robust, diagnostics = protocol_response(
        fromonteil_protocol_ii_variant_1(),
        frequencies,
        noise_kind="intensity",
        points_per_radian=40,
    )
    levine, _ = protocol_response(
        levine_pichler_protocol(),
        frequencies,
        noise_kind="intensity",
        points_per_radian=40,
    )
    assert diagnostics["unitarity_error"] < 1.0e-10
    assert robust[0] < 2.0e-5
    assert levine[0] > 1.0e-2


def test_rydberg_exposure_is_positive() -> None:
    for protocol in (
        levine_pichler_protocol(),
        fromonteil_protocol_ii_variant_1(),
    ):
        exposure = integrated_rydberg_population(
            protocol,
            points_per_radian=20,
        )
        assert 0.0 < exposure < protocol.duration
