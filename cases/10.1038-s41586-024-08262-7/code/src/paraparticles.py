"""Core paraparticle single-mode statistics for Wang & Hazzard, Nature 637, 314 (2025).

Everything here is the *free-paraparticle* single-mode object defined by an
R-matrix through its Hilbert series (single-mode partition function)

    z_R(x) = Tr[e^{-beta eps n}] = sum_n d_n x^n ,   x = e^{-beta eps}      (Eq. single_mode_Z)

where d_n is the dimension of the n-particle single-mode space (the generalized
exclusion statistics).  The thermal occupation of a free-paraparticle mode is

    <n>_beta = x z'_R(x) / z_R(x) = sum_n n d_n x^n / sum_n d_n x^n .        (Eq. n_k_expectation)

The four R-matrix examples of Table 1 and the ordinary fermion/boson limits are
encoded by their d_n sequences (SI Sec. "Calculation of exclusion statistics",
arXiv:2308.05203).  No fitting, no digitization: these are closed-form integers
and rational functions of x.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import comb
import numpy as np


@dataclass(frozen=True)
class Species:
    """A single-mode statistics specified by its exclusion sequence {d_n}."""

    key: str
    label: str
    d: tuple[int, ...] | None  # finite d_n; None means the geometric boson tower d_n=1
    m: int | None = None

    def degeneracies(self, n_max: int) -> np.ndarray:
        """d_0..d_{n_max}."""
        if self.d is None:  # boson: d_n = 1 for all n
            return np.ones(n_max + 1, dtype=float)
        out = np.zeros(n_max + 1, dtype=float)
        upto = min(n_max + 1, len(self.d))
        out[:upto] = self.d[:upto]
        return out

    def occupation(self, beta_eps: np.ndarray) -> np.ndarray:
        """<n>_beta = x z'(x)/z(x) with x = e^{-beta eps}.

        Boson uses the closed form x/(1-x); it diverges as beta eps -> 0+ and is
        undefined for beta eps <= 0, so we mask that half-line with NaN exactly
        as the paper plots it.
        """
        be = np.asarray(beta_eps, dtype=float)
        x = np.exp(-be)
        if self.d is None:  # boson
            out = np.full_like(be, np.nan)
            pos = be > 0.0
            out[pos] = x[pos] / (1.0 - x[pos])
            return out
        d = np.asarray(self.d, dtype=float)
        n = np.arange(len(d), dtype=float)
        # z = sum d_n x^n ; numerator sum n d_n x^n ; both are finite polynomials.
        xn = x[..., None] ** n  # (..., len(d))
        z = xn @ d
        num = xn @ (n * d)
        return num / z


def species_table(m3: int = 2, m4: int = 3) -> list[Species]:
    """The exact species drawn in Fig. 2 (see FIGURE_CLASSIFICATION.md).

    The published figure legend uses Ex.2 (m=2), Ex.3 (m=2), Ex.4 (m=3) -- NOT
    m=5 as the main-text prose (line 603 of the source) states.  We reproduce the
    figure, so m3=2, m4=3 are the paper-exact parameters.
    """
    m2 = m3  # Ex.2 in the figure is drawn at m=2 as well
    return [
        Species("fermion", "fermion", d=(1, 1)),
        Species("boson", "boson", d=None),
        Species("ex2", f"Ex.2 (m={m2})", d=tuple(comb(m2, n) for n in range(m2 + 1)), m=m2),
        Species("ex3", f"Ex.3 (m={m3})", d=(1, m3), m=m3),
        Species("ex4", f"Ex.4 (m={m4})", d=(1, m4, 1), m=m4),
    ]
