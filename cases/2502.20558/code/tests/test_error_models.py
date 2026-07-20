from __future__ import annotations

import math

import pytest

from src.error_models import error_model_a, movement_error, split_error_rate


def test_loss_fraction_split_preserves_total() -> None:
    loss, pauli = split_error_rate(0.03, 0.4)
    assert loss == pytest.approx(0.012)
    assert pauli == pytest.approx(0.018)


@pytest.mark.parametrize("loss_fraction", [0.0, 0.25, 0.5, 1.0])
@pytest.mark.parametrize("bias", [0.0, 1.0, 10.0, 500.0])
def test_error_model_a_is_normalized(loss_fraction: float, bias: float) -> None:
    probabilities = error_model_a(0.02, loss_fraction, bias)
    total = sum(probabilities[key] for key in ("loss", "x", "y", "z"))
    assert total == pytest.approx(probabilities["per_qubit_error"], abs=1e-14)
    assert probabilities["per_qubit_error"] == pytest.approx(1.0 - math.sqrt(0.98))


def test_movement_error_limits_and_monotonicity() -> None:
    assert movement_error(0.001, 0.0, 1.0) == 0.0
    assert movement_error(0.0, 10.0, 1.0) == 0.0
    assert movement_error(0.001, 20.0, 1.0) > movement_error(0.001, 10.0, 1.0)
