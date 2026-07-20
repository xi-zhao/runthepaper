"""Literal-consistency audit helpers for PRL-Bench idx90."""

from __future__ import annotations

from decimal import Decimal, localcontext
import math


PI_DECIMAL = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
)


def exact_kdos_component(
    epsilon0: float,
    omega: float,
    resonance: float,
    gamma: float,
    residue: complex,
) -> float:
    """Imaginary part implied by I/(omega-(Omega-i gamma))."""

    x = omega - resonance
    denominator = x * x + gamma * gamma
    return (
        2.0
        * epsilon0
        * omega
        / math.pi
        * (x * residue.imag - gamma * residue.real)
        / denominator
    )


def direct_complex_kdos_component(
    epsilon0: float,
    omega: float,
    resonance: float,
    gamma: float,
    residue: complex,
) -> float:
    """Direct complex-arithmetic negative control for the closed form."""

    pole = complex(resonance, -gamma)
    return 2.0 * epsilon0 * omega / math.pi * (residue / (omega - pole)).imag


def frozen_kdos_component(
    epsilon0: float,
    omega: float,
    resonance: float,
    gamma: float,
    residue: complex,
) -> float:
    """The globally sign-reversed decomposition printed in frozen Task 1."""

    x = omega - resonance
    denominator = x * x + gamma * gamma
    return (
        2.0
        * epsilon0
        * omega
        / math.pi
        * (gamma * residue.real - x * residue.imag)
        / denominator
    )


def radial_rate_prefactor(
    dipole_magnitude: float, omega: float, epsilon0: float, hbar: float
) -> float:
    """Prefactor after integrating d^3k=4 pi k^2 dk."""

    return dipole_magnitude**2 * omega / (8.0 * math.pi * epsilon0 * hbar)


def frozen_radial_rate_prefactor(
    dipole_magnitude: float, omega: float, epsilon0: float, hbar: float
) -> float:
    return dipole_magnitude**2 * omega / (32.0 * math.pi * epsilon0 * hbar)


def residual_after_frozen_pole_subtraction(k_pole: float, residue: float) -> float:
    """Residue left in k^2 rho_reg by the prompt's subtraction.

    If k^2 rho has residue R, the prompt subtracts R/(k-kR) from rho,
    so k^2 rho_reg retains R(1-kR^2)/(k-kR).
    """

    return residue * (1.0 - k_pole * k_pole)


def edge_signed_rate(
    *,
    omega_drive: float,
    epsilon0: float,
    a: float,
    b: float,
    j_edge: float,
    dipole_magnitude: float = 1.0,
    hbar: float = 1.0,
) -> float:
    """Literal signed edge contribution implied by Tasks 1-3.

    Positive is decay and negative is excitation.  The sign follows the
    benchmark's explicit Green-pole ansatz, not the source paper's differently
    normalized intensity convention.
    """

    return (
        -dipole_magnitude**2
        * epsilon0
        * omega_drive**4
        * j_edge
        * math.sqrt(b)
        / (32.0 * math.pi * hbar * a)
    )


def split_nonnegative_rate(signed_rate: float) -> tuple[float, float]:
    """Return (decay, excitation) from a signed kDOS contribution."""

    return max(signed_rate, 0.0), max(-signed_rate, 0.0)


def frozen_edge_formula(
    *,
    omega_drive: float,
    epsilon0: float,
    a: float,
    b: float,
    j_edge: float,
    dipole_magnitude: float = 1.0,
    hbar: float = 1.0,
) -> float:
    return (
        dipole_magnitude**2
        * omega_drive**2
        * j_edge
        * math.sqrt(b)
        / (64.0 * math.pi * epsilon0 * hbar * a)
    )


def toy_model_rates(*, precision: int = 80) -> dict[str, Decimal]:
    """Evaluate frozen Task 7 without floating-point root collapse."""

    with localcontext() as context:
        context.prec = precision
        omega_drive = Decimal(1)
        epsilon0 = Decimal(4)
        a = Decimal(2)
        b = Decimal(3)
        j_edge = Decimal(5)
        omega = Decimal("0.5") - Decimal("1e-9")
        k_edge = epsilon0.sqrt() * omega_drive / Decimal(2)
        gap = ((omega_drive / Decimal(2) - omega) / a) ** 2
        root = k_edge - gap
        residue_jacobian = Decimal(2) * j_edge * b.sqrt() / a
        excitation = omega**2 / (Decimal(4) * PI_DECIMAL) * root**2 * residue_jacobian
        magnitude_limit = (
            (omega_drive / Decimal(2)) ** 2
            / (Decimal(4) * PI_DECIMAL)
            * k_edge**2
            * residue_jacobian
        )
        frozen_closed = (
            omega_drive**2
            * j_edge
            * b.sqrt()
            / (Decimal(64) * PI_DECIMAL * epsilon0 * a)
        )
        frozen_reported = Decimal("0.02153628")
        return {
            "root": root,
            "literal_decay": Decimal(0),
            "literal_excitation": excitation,
            "literal_magnitude_limit": magnitude_limit,
            "frozen_task5_closed_formula": frozen_closed,
            "frozen_task7_reported": frozen_reported,
        }
