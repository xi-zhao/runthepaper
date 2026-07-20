from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ProxyConfig:
    distance: int = 5
    p_loss: float = 0.01
    partner_flip_probability: float = 0.25
    shots: int = 200_000
    seed: int = 250220558

    def validate(self) -> None:
        if self.distance < 3 or self.distance % 2 == 0:
            raise ValueError("distance must be an odd integer >= 3")
        if not 0.0 <= self.p_loss <= 1.0:
            raise ValueError("p_loss must lie in [0, 1]")
        if not 0.0 <= self.partner_flip_probability <= 1.0:
            raise ValueError("partner_flip_probability must lie in [0, 1]")
        if self.shots <= 0:
            raise ValueError("shots must be positive")


def _majority_decode(bits: np.ndarray, active: np.ndarray, ties: np.ndarray) -> np.ndarray:
    ones = np.sum(bits & active, axis=1)
    active_count = np.sum(active, axis=1)
    zeros = active_count - ones
    return (ones > zeros) | ((ones == zeros) & ties)


def simulate_round(config: ProxyConfig, rounds: int, seed_offset: int = 0) -> dict[str, float | int]:
    """Run a transparent repetition-code analogue of delayed erasure.

    Each data bit has one loss opportunity per displayed round.  SSR identifies
    the lost bit only at the final measurement.  A loss randomizes that readout
    and may flip the next bit, representing a gate-cancellation partner error.
    The flag-aware decoder removes randomized lost readouts before majority
    decoding.  In this timing-marginalized proxy, perfect time information adds
    no further correction, matching the paper's near-overlap feature by design.
    """
    config.validate()
    if rounds < 1:
        raise ValueError("rounds must be positive")
    rng = np.random.default_rng(config.seed + seed_offset)
    opportunities = rng.random((config.shots, config.distance, rounds))
    loss_events = opportunities < config.p_loss
    lost = np.any(loss_events, axis=2)

    partner_flips = lost & (rng.random(lost.shape) < config.partner_flip_probability)
    bits = np.roll(partner_flips, shift=1, axis=1)
    randomized_lost_readout = rng.random(lost.shape) < 0.5
    bits = np.where(lost, randomized_lost_readout, bits)

    no_information_ties = rng.random(config.shots) < 0.5
    no_information_failure = _majority_decode(
        bits,
        np.ones_like(lost, dtype=bool),
        no_information_ties,
    )

    delayed_ties = rng.random(config.shots) < 0.5
    delayed_failure = _majority_decode(bits, ~lost, delayed_ties)
    perfect_time_failure = delayed_failure.copy()

    no_failures = int(np.count_nonzero(no_information_failure))
    delayed_failures = int(np.count_nonzero(delayed_failure))
    perfect_failures = int(np.count_nonzero(perfect_time_failure))
    mean_lost = float(np.mean(np.sum(lost, axis=1)))

    return {
        "rounds": rounds,
        "shots": config.shots,
        "no_information_failures": no_failures,
        "delayed_erasure_failures": delayed_failures,
        "perfect_time_failures": perfect_failures,
        "no_information_error_rate": no_failures / config.shots,
        "delayed_erasure_error_rate": delayed_failures / config.shots,
        "perfect_time_error_rate": perfect_failures / config.shots,
        "no_information_plot_rate": (no_failures + 0.5) / (config.shots + 1.0),
        "delayed_erasure_plot_rate": (delayed_failures + 0.5) / (config.shots + 1.0),
        "perfect_time_plot_rate": (perfect_failures + 0.5) / (config.shots + 1.0),
        "mean_flagged_losses": mean_lost,
    }


def simulate_curve(config: ProxyConfig, rounds: list[int]) -> list[dict[str, float | int]]:
    return [simulate_round(config, value, seed_offset=10_007 * index) for index, value in enumerate(rounds)]
