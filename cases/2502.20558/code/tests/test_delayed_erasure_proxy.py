from __future__ import annotations

import pytest

from src.delayed_erasure_proxy import ProxyConfig, simulate_curve, simulate_round


def test_proxy_is_deterministic() -> None:
    config = ProxyConfig(shots=20_000, seed=17)
    assert simulate_round(config, 12) == simulate_round(config, 12)


def test_delayed_and_perfect_timing_match_in_marginalized_proxy() -> None:
    result = simulate_round(ProxyConfig(shots=30_000, seed=23), 20)
    assert result["delayed_erasure_failures"] == result["perfect_time_failures"]


def test_ssr_information_improves_deep_proxy_circuits() -> None:
    result = simulate_round(ProxyConfig(shots=100_000, seed=31), 30)
    assert result["delayed_erasure_error_rate"] < result["no_information_error_rate"]


def test_curve_uses_requested_rounds() -> None:
    rows = simulate_curve(ProxyConfig(shots=1_000, seed=11), [2, 4, 8])
    assert [row["rounds"] for row in rows] == [2, 4, 8]


def test_invalid_even_distance_is_rejected() -> None:
    with pytest.raises(ValueError):
        simulate_round(ProxyConfig(distance=4), 2)
