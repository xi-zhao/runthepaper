from __future__ import annotations

import math
from collections.abc import Iterable


def lifecycle_threshold_percent(lifecycle_length: float) -> float:
    """Appendix-H non-SWAP fit, in percent."""
    if lifecycle_length <= 0.0:
        raise ValueError("lifecycle_length must be positive")
    return 7.0 / lifecycle_length ** (1.0 / 3.0)


def threshold_interpolation(
    loss_fraction: float,
    loss_only_threshold: float,
    pauli_only_threshold: float,
) -> float:
    """Main-text loss/Pauli threshold interpolation."""
    if not 0.0 <= loss_fraction <= 1.0:
        raise ValueError("loss_fraction must lie in [0, 1]")
    if loss_only_threshold <= 0.0 or pauli_only_threshold <= 0.0:
        raise ValueError("thresholds must be positive")
    numerator = loss_only_threshold * pauli_only_threshold
    denominator = (
        loss_fraction * (pauli_only_threshold - loss_only_threshold)
        + loss_only_threshold
    )
    return numerator / denominator


def effective_distance_endpoints(distance: int) -> tuple[float, float]:
    if distance < 1 or distance % 2 == 0:
        raise ValueError("surface-code distance must be a positive odd integer")
    return (distance + 1.0) / 2.0, float(distance)


def entangling_gates_per_round(distance: int) -> int:
    if distance < 1 or distance % 2 == 0:
        raise ValueError("surface-code distance must be a positive odd integer")
    return 4 * distance * (distance - 1)


def lifecycle_curves(distance: int, displayed_rounds: Iterable[int]) -> list[dict[str, float | int]]:
    """Count the Fig. 14(c)/16(a) lifecycle quantities.

    The displayed round count contains one noiseless boundary round, hence
    ``noisy_rounds = displayed_rounds - 1``.  SWAP changes which physical role
    ends a lifecycle but preserves the all-qubit endpoint count.
    """
    gates = entangling_gates_per_round(distance)
    data_qubits = distance**2
    measure_qubits = distance**2 - 1
    rows: list[dict[str, float | int]] = []
    for displayed in displayed_rounds:
        if displayed < 2:
            raise ValueError("displayed_rounds must be at least 2")
        noisy = displayed - 1
        conventional_data = gates * noisy / data_qubits
        conventional_measure = gates / measure_qubits
        all_qubits = 2.0 * gates * noisy / (data_qubits + measure_qubits * noisy)
        rows.append(
            {
                "displayed_se_rounds": displayed,
                "noisy_se_rounds": noisy,
                "conventional_data_lifecycle": conventional_data,
                "conventional_measure_lifecycle": conventional_measure,
                "conventional_all_lifecycle": all_qubits,
                "swap_period_1_all_lifecycle": all_qubits,
                "swap_period_2_all_lifecycle": all_qubits,
            }
        )
    return rows


def algorithm_lifecycles(ghz_qubits: int = 16) -> list[dict[str, float | str]]:
    if ghz_qubits < 2 or ghz_qubits & (ghz_qubits - 1):
        raise ValueError("ghz_qubits must be a power of two")
    log_n = math.log2(ghz_qubits)
    return [
        {"algorithm": f"GHZ N={ghz_qubits}", "average": log_n / 2.0, "maximum": math.floor(log_n)},
        {"algorithm": "15-to-1 distillation", "average": 4.0, "maximum": 5.0},
        {"algorithm": "H/T synthesis", "average": 7.0, "maximum": 8.0},
        {"algorithm": "Adder", "average": 9.0, "maximum": 13.0},
    ]


def table_i_analytic_rows(distance: int = 7) -> list[dict[str, str]]:
    if distance < 1 or distance % 2 == 0:
        raise ValueError("distance must be a positive odd integer")
    conventional_overhead = str(8 * distance**3 - 4 * distance)
    teleportation_overhead = str(18 * distance**3 - 6 * distance)
    return [
        {"method": "Conventional SE", "data_lifecycle": f"{4 * distance}", "measure_lifecycle": "4", "space_time_overhead": conventional_overhead},
        {"method": "SWAP SE period 1", "data_lifecycle": "8", "measure_lifecycle": "8", "space_time_overhead": conventional_overhead},
        {"method": "Direct conversion SE period 2", "data_lifecycle": "8", "measure_lifecycle": "4", "space_time_overhead": conventional_overhead},
        {"method": "Teleportation-based SE", "data_lifecycle": "4", "measure_lifecycle": "4", "space_time_overhead": teleportation_overhead},
        {"method": "Direct conversion SE period 1", "data_lifecycle": "4", "measure_lifecycle": "4", "space_time_overhead": conventional_overhead},
        {"method": "Direct conversion period 1 + exact loss info", "data_lifecycle": "1 detection / 4 replacement", "measure_lifecycle": "1 detection / 4 replacement", "space_time_overhead": conventional_overhead},
        {"method": "Direct conversion period 0.25 + exact loss info", "data_lifecycle": "1 detection / 1 replacement", "measure_lifecycle": "1 detection / 1 replacement", "space_time_overhead": conventional_overhead},
    ]
