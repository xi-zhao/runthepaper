"""Independent checks for PRL-Bench record idx16.

The frozen task mixes three distinct objects: a dimensional momentum-space
Green function, a density-of-states-normalized local Green function, and an
asymptotic complex resonance pole.  Keeping those objects separate makes the
normalization, cutoff, and validity assumptions explicit.
"""

from __future__ import annotations

import math


def d_wave_gap(delta_0: float, phi: float) -> float:
    """Return Delta(phi)=Delta_0 cos(2 phi)."""

    if delta_0 <= 0.0:
        raise ValueError("delta_0 must be positive")
    return delta_0 * math.cos(2.0 * phi)


def clean_green_matrix(
    omega: float, xi: float, delta: float
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Return the real clean Nambu Green matrix away from its poles."""

    denominator = omega * omega - xi * xi - delta * delta
    if denominator == 0.0:
        raise ZeroDivisionError("the selected point is on a quasiparticle pole")
    return (
        ((omega + xi) / denominator, delta / denominator),
        (delta / denominator, (omega - xi) / denominator),
    )


def local_green_low_energy(
    omega: float,
    delta_0: float,
    *,
    cutoff_factor: float = 2.0,
    imaginary_sign: float = -1.0,
) -> complex:
    """Frozen/RMP low-energy scalar Green function on the real axis.

    The result is dimensionless because it is normalized by the normal-state
    density of states.  ``cutoff_factor=2, imaginary_sign=-1`` reproduces the
    frozen convention.  RMP Eq. (impdwave3), as printed for positive real
    frequency, uses ``cutoff_factor=4, imaginary_sign=+1``.
    """

    if delta_0 <= 0.0 or cutoff_factor <= 0.0:
        raise ValueError("delta_0 and cutoff_factor must be positive")
    if imaginary_sign not in {-1.0, 1.0}:
        raise ValueError("imaginary_sign must be -1 or +1")
    if omega == 0.0:
        return 0.0j
    real = -(2.0 * omega) / (math.pi * delta_0) * math.log(
        cutoff_factor * delta_0 / abs(omega)
    )
    imag = imaginary_sign * abs(omega) / delta_0
    return complex(real, imag)


def frozen_resonance_energy(c: float, delta_0: float) -> float:
    """Return the absolute real-energy formula printed in the frozen gold."""

    _validate_resonance_inputs(c, delta_0)
    log_term = math.log(math.pi * abs(c) / 4.0)
    numerator = -2.0 * math.pi * abs(c) * delta_0 * log_term
    denominator = 4.0 * log_term * log_term + math.pi * math.pi
    return abs(numerator / denominator)


def frozen_fixed_log_pole(c: float, delta_0: float) -> complex:
    """Complex fixed-log pole whose real part is the frozen expression.

    This reconstruction exposes the width discarded by the benchmark.  It is
    not an exact solution of the transcendental pole equation.
    """

    _validate_resonance_inputs(c, delta_0)
    sign = 1.0 if c > 0.0 else -1.0
    logarithm = math.log(4.0 / (math.pi * abs(c)))
    return -sign * (math.pi * abs(c) * delta_0 / 2.0) / complex(
        logarithm, -math.pi / 2.0
    )


def rmp_logarithmic_pole(c: float, delta_0: float) -> complex:
    """Return RMP Eq. (impdwave1), valid only at logarithmic accuracy."""

    _validate_resonance_inputs(c, delta_0)
    sign = 1.0 if c > 0.0 else -1.0
    logarithm = math.log(8.0 / (math.pi * abs(c)))
    scale = -sign * delta_0 * (math.pi * abs(c) / 2.0) / logarithm
    return scale * complex(1.0, math.pi / (2.0 * logarithm))


def low_branch_real_axis_root(
    c: float,
    delta_0: float,
    *,
    cutoff_factor: float = 2.0,
    iterations: int = 200,
) -> float:
    """Solve Re G_0(-sign(c)|Omega|)=c on the low-energy branch.

    This is deliberately only a real-axis diagnostic: a d-wave impurity state
    is a complex resonance, not a true real bound-state pole.
    """

    _validate_resonance_inputs(c, delta_0)
    if cutoff_factor <= 0.0:
        raise ValueError("cutoff_factor must be positive")
    magnitude = abs(c)

    def residual(x: float) -> float:
        return 2.0 * x / math.pi * math.log(cutoff_factor / x) - magnitude

    lower = 1.0e-15
    upper = cutoff_factor / math.e
    if residual(upper) <= 0.0:
        raise ValueError("no low-branch real root for this c and cutoff")
    for _ in range(iterations):
        midpoint = 0.5 * (lower + upper)
        if residual(midpoint) > 0.0:
            upper = midpoint
        else:
            lower = midpoint
    return delta_0 * 0.5 * (lower + upper)


def pole_residual_at_frozen_energy(c: float, delta_0: float) -> complex:
    """Return G_0(Omega_frozen)-c using the frozen cutoff convention."""

    energy = frozen_resonance_energy(c, delta_0)
    omega = -math.copysign(energy, c)
    return local_green_low_energy(omega, delta_0, cutoff_factor=2.0) - c


def width_to_energy(pole: complex) -> float:
    """Return |Im pole / Re pole|."""

    if pole.real == 0.0:
        return math.inf
    return abs(pole.imag / pole.real)


def _validate_resonance_inputs(c: float, delta_0: float) -> None:
    if c == 0.0:
        raise ValueError("c=0 is a limiting case, not a finite logarithmic input")
    if delta_0 <= 0.0:
        raise ValueError("delta_0 must be positive")
    if math.pi * abs(c) >= 4.0:
        raise ValueError("the strong-scattering logarithm requires pi|c|<4")
