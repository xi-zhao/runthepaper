from __future__ import annotations

import pytest

from src.analytic_targets import (
    algorithm_lifecycles,
    effective_distance_endpoints,
    entangling_gates_per_round,
    lifecycle_curves,
    lifecycle_threshold_percent,
    table_i_analytic_rows,
    threshold_interpolation,
)


def test_threshold_interpolation_hits_pure_noise_axes() -> None:
    assert threshold_interpolation(0.0, 0.07, 0.015) == pytest.approx(0.015)
    assert threshold_interpolation(1.0, 0.07, 0.015) == pytest.approx(0.07)


def test_lifecycle_threshold_is_strictly_decreasing() -> None:
    values = [lifecycle_threshold_percent(value) for value in range(1, 17)]
    assert values[0] == pytest.approx(7.0)
    assert all(left > right for left, right in zip(values, values[1:]))


def test_effective_distance_endpoints_for_d7() -> None:
    assert effective_distance_endpoints(7) == (4.0, 7.0)


def test_rotated_surface_code_gate_count() -> None:
    assert entangling_gates_per_round(3) == 24
    assert entangling_gates_per_round(9) == 288


def test_all_qubit_lifecycle_invariant_and_limits() -> None:
    rows = lifecycle_curves(9, range(2, 21))
    assert all(row["conventional_all_lifecycle"] == pytest.approx(row["swap_period_1_all_lifecycle"]) for row in rows)
    assert all(row["swap_period_1_all_lifecycle"] == pytest.approx(row["swap_period_2_all_lifecycle"]) for row in rows)
    assert rows[-1]["conventional_all_lifecycle"] < 8.0 * 9.0 / 10.0
    assert rows[-1]["conventional_all_lifecycle"] > rows[0]["conventional_all_lifecycle"]


def test_algorithm_counts_match_appendix_g() -> None:
    rows = algorithm_lifecycles(16)
    assert [(row["average"], row["maximum"]) for row in rows] == [(2.0, 4), (4.0, 5.0), (7.0, 8.0), (9.0, 13.0)]


def test_table_i_analytic_rows() -> None:
    rows = table_i_analytic_rows(distance=7)
    assert len(rows) == 7
    assert rows[0]["data_lifecycle"] == "28"
    assert rows[1]["data_lifecycle"] == "8"
    assert rows[3]["space_time_overhead"] == str(18 * 7**3 - 6 * 7)
