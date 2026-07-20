"""Independent formulas for the PRL-Bench idx9 source and gold audit.

The frozen record combines relic gravitational waves with two different scalar-
field papers.  This module keeps those sectors explicit and exposes both the
derived counterterms and the incompatible frozen expressions.
"""

from __future__ import annotations

import cmath


def slow_roll_epsilon(beta: float) -> float:
    """Return epsilon=(beta+2)/(beta+1) for power-law inflation."""

    if beta == -1.0:
        raise ValueError("beta=-1 makes the power-law relation singular")
    return (beta + 2.0) / (beta + 1.0)


def tensor_index_from_beta(beta: float) -> float:
    """Long-wavelength tensor index n_t=2 beta+4."""

    return 2.0 * beta + 4.0


def tensor_index_from_epsilon(epsilon: float) -> float:
    """Exact algebraic form of the tensor index in epsilon."""

    if epsilon == 1.0:
        raise ValueError("epsilon=1 is singular")
    return -2.0 * epsilon / (1.0 - epsilon)


def leading_bogolyubov_coefficient(
    k: float, jump_a2_over_a: float, phase: float = 0.0
) -> complex:
    """Leading transition coefficient for a finite jump in a''/a."""

    if k <= 0.0:
        raise ValueError("k must be positive")
    return jump_a2_over_a * cmath.exp(1j * phase) / (4.0 * k * k)


def fig2_tensor_index(x: float) -> float:
    """Exact beta=-2 curve n_t(x) from source Eqs. (23)-(24)."""

    x2 = x * x
    return 2.0 * x2 / (1.0 + x2)


def fig2_running(x: float) -> float:
    """Exact beta=-2 curve alpha_t(x) from source Eqs. (23)-(24)."""

    x2 = x * x
    return 4.0 * x2 / (1.0 + x2) ** 2


def wkb_amplitude_bracket(beta: float, mass: float, t: float, k: float) -> float:
    """Bracket in |u_k^(4)|^2=(2k)^-1 bracket through k^-4.

    Here t=-tau>0 and a=t^(1+beta).  This part of the frozen answer is valid.
    """

    _validate_positive(t=t, k=k)
    mass2 = mass * mass
    mass4 = mass2 * mass2
    t_mass = t ** (4.0 + 2.0 * beta)
    order2 = -(mass2 * t_mass - beta - beta * beta) / (2.0 * t * t * k * k)
    order4_numerator = (
        2.0 * mass2 * t_mass
        + 3.0 * mass4 * t ** (8.0 + 4.0 * beta)
        - 6.0 * beta
        - 3.0 * beta * beta
        - 2.0 * mass2 * t_mass * beta * beta
        + 6.0 * beta**3
        + 3.0 * beta**4
    )
    order4 = order4_numerator / (8.0 * t**4 * k**4)
    return 1.0 + order2 + order4


def correct_counterterm_brackets(
    beta: float, mass: float, t: float, k: float
) -> tuple[float, float]:
    """Return independently derived (rho,p) fourth-order brackets.

    The physical spectra are k^4/(8 pi^2 a^4) times these brackets.  The
    derivation uses W=k+V/(2k)-(V^2+V'')/(8k^3), V=m^2a^2-a''/a, in the exact
    stress-tensor definitions printed by the frozen prompt.
    """

    _validate_positive(t=t, k=k)
    mass2 = mass * mass
    mass4 = mass2 * mass2
    tm = t ** (4.0 + 2.0 * beta)
    tm4 = t ** (8.0 + 4.0 * beta)
    rho2 = ((beta + 1.0) ** 2 + mass2 * tm) / (t * t * k * k)
    rho4 = (
        3.0 * beta**4
        + 12.0 * beta**3
        + 15.0 * beta * beta
        + 6.0 * beta
        + 2.0 * (beta + 1.0) ** 2 * mass2 * tm
        - mass4 * tm4
    ) / (4.0 * t**4 * k**4)
    pressure2 = (
        beta * beta + 4.0 * beta + 3.0 - mass2 * tm
    ) / (3.0 * t * t * k * k)
    pressure4 = (
        3.0 * beta**4
        + 24.0 * beta**3
        + 51.0 * beta * beta
        + 30.0 * beta
        + (2.0 - 2.0 * beta * beta) * mass2 * tm
        + 3.0 * mass4 * tm4
    ) / (12.0 * t**4 * k**4)
    return 2.0 + rho2 + rho4, 2.0 / 3.0 + pressure2 + pressure4


def frozen_counterterm_brackets(
    beta: float, mass: float, t: float, k: float
) -> tuple[float, float]:
    """Literal rho/p brackets printed by the frozen benchmark answer."""

    _validate_positive(t=t, k=k)
    mass2 = mass * mass
    mass4 = mass2 * mass2
    t31 = t ** (3.0 + beta)
    t42 = t ** (4.0 + 2.0 * beta)
    t73 = t ** (7.0 + 3.0 * beta)
    t84 = t ** (8.0 + 4.0 * beta)

    rho2 = (1.0 + mass2 * t31 + 2.0 * beta + beta * beta) / (t * t * k * k)
    rho4_numerator = (
        2.0 * mass2 * t42
        - 2.0 * mass4 * t73
        + mass4 * t84
        + 6.0 * beta
        + 2.0 * mass2 * t31 * beta
        + 2.0 * mass2 * t42 * beta
        + 15.0 * beta * beta
        + 2.0 * mass2 * t31 * beta * beta
        + 12.0 * beta**3
        + 3.0 * beta**4
    )
    frozen_rho = 2.0 + rho2 + rho4_numerator / (4.0 * t**4 * k**4)

    pressure2 = (
        3.0
        - 3.0 * mass2 * t31
        + 2.0 * mass2 * t42
        + 4.0 * beta
        + beta * beta
    ) / (3.0 * t * t * k * k)
    pressure_subtracted_numerator = (
        -2.0 * mass2 * t42
        - 6.0 * mass4 * t73
        + 3.0 * mass4 * t84
        - 30.0 * beta
        + 6.0 * mass2 * t31 * beta
        - 6.0 * mass2 * t42 * beta
        - 51.0 * beta * beta
        + 6.0 * mass2 * t31 * beta * beta
        - 4.0 * mass2 * t42 * beta * beta
        - 24.0 * beta**3
        - 3.0 * beta**4
    )
    frozen_pressure = (
        2.0 / 3.0
        + pressure2
        - pressure_subtracted_numerator / (12.0 * t**4 * k**4)
    )
    return frozen_rho, frozen_pressure


def scalar_high_frequency_w(beta: float) -> float:
    """Correct massless minimally coupled scalar ratio p_re/rho_re."""

    if beta == -1.0:
        raise ValueError("rho leading coefficient vanishes at beta=-1")
    return (beta + 7.0) / (3.0 * (beta + 1.0))


def frozen_scalar_high_frequency_w(beta: float) -> float:
    """Reciprocal ratio printed in the frozen answer."""

    if beta == -7.0:
        raise ValueError("frozen ratio is singular at beta=-7")
    return 3.0 * (beta + 1.0) / (beta + 7.0)


def rgw_high_frequency_w(beta: float) -> float:
    """Relic-gravitational-wave ratio from source Eq. (96)."""

    if beta == -4.0:
        raise ValueError("RGW leading energy coefficient vanishes at beta=-4")
    return (beta - 2.0) / (3.0 * (beta + 4.0))


def _validate_positive(*, t: float, k: float) -> None:
    if t <= 0.0 or k <= 0.0:
        raise ValueError("t=-tau and k must be positive")
