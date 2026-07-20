from __future__ import annotations

import math


def split_error_rate(total_error: float, loss_fraction: float) -> tuple[float, float]:
    """Split a total error rate into loss and Pauli contributions."""
    if not 0.0 <= total_error <= 1.0:
        raise ValueError("total_error must lie in [0, 1]")
    if not 0.0 <= loss_fraction <= 1.0:
        raise ValueError("loss_fraction must lie in [0, 1]")
    return loss_fraction * total_error, (1.0 - loss_fraction) * total_error


def error_model_a(p_cz: float, loss_fraction: float, bias: float) -> dict[str, float]:
    """Return unconditional Error-Model-A probabilities from Appendix F.

    ``bias`` is eta in the paper.  The returned X/Y/Z probabilities already
    include the ``1-L`` Pauli-channel weight, so all four errors sum to the
    per-qubit probability ``1-sqrt(1-p_cz)``.
    """
    if not 0.0 <= p_cz <= 1.0:
        raise ValueError("p_cz must lie in [0, 1]")
    if bias < 0.0:
        raise ValueError("bias must be nonnegative")
    per_qubit = 1.0 - math.sqrt(1.0 - p_cz)
    p_loss, p_pauli = split_error_rate(per_qubit, loss_fraction)
    p_x = p_pauli / (2.0 * (1.0 + bias))
    p_y = p_x
    p_z = bias * p_pauli / (1.0 + bias)
    return {
        "per_qubit_error": per_qubit,
        "loss": p_loss,
        "x": p_x,
        "y": p_y,
        "z": p_z,
    }


def movement_error(p_idle: float, duration: float, slot_duration: float) -> float:
    """Appendix-C accumulated movement error."""
    if not 0.0 <= p_idle <= 1.0:
        raise ValueError("p_idle must lie in [0, 1]")
    if duration < 0.0 or slot_duration <= 0.0:
        raise ValueError("duration must be nonnegative and slot_duration positive")
    return 1.0 - (1.0 - p_idle) ** (duration / slot_duration)
