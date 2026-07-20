"""Exact dual-spin representation of open-boundary pure Z2 gauge theory.

The source Hamiltonian is

    H_B = -h sum_p (P_p + P_p^dagger)
    H_E =  g sum_l (2 - Q_l - Q_l^dagger).

For Z2, in the charge-free sector and with open boundaries, a lattice with
``L x L`` vertices has ``(L - 1)^2`` independent plaquette spins.  The mapping
is P_p -> tau_x,p and a link electric operator maps either to tau_z,p tau_z,q
(interior link) or tau_z,p (boundary link).  This module is deliberately
NumPy-only so that the physical model and its invariants can be tested without
the A100 runner.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class DualZ2OBC:
    """Charge-free pure Z2 lattice gauge theory in its exact dual basis."""

    lattice_size: int
    h: float = 1.0
    g: float = 0.1

    def __post_init__(self) -> None:
        if self.lattice_size < 2:
            raise ValueError("lattice_size must be at least 2")
        if self.h < 0 or self.g < 0:
            raise ValueError("h and g must be non-negative")

    @property
    def plaquette_side(self) -> int:
        return self.lattice_size - 1

    @property
    def n_plaquettes(self) -> int:
        return self.plaquette_side**2

    @property
    def hilbert_dim(self) -> int:
        return 1 << self.n_plaquettes

    @property
    def n_links(self) -> int:
        return 2 * self.lattice_size * (self.lattice_size - 1)

    def plaquette_index(self, x: int, y: int) -> int:
        """Return the row-major bit index for plaquette coordinate ``(x,y)``."""

        side = self.plaquette_side
        if not (0 <= x < side and 0 <= y < side):
            raise ValueError(f"plaquette {(x, y)} outside 0..{side - 1}")
        return y * side + x

    def electric_terms(self) -> tuple[tuple[int, int | None], ...]:
        """Return every link as an interior pair or a one-plaquette boundary."""

        side = self.plaquette_side
        terms: list[tuple[int, int | None]] = []

        # Links between horizontally or vertically adjacent plaquettes.
        for y in range(side):
            for x in range(side - 1):
                terms.append((self.plaquette_index(x, y), self.plaquette_index(x + 1, y)))
        for y in range(side - 1):
            for x in range(side):
                terms.append((self.plaquette_index(x, y), self.plaquette_index(x, y + 1)))

        # Every outer link touches one plaquette. Corners correctly contribute
        # two different boundary links.
        for x in range(side):
            terms.append((self.plaquette_index(x, 0), None))
            terms.append((self.plaquette_index(x, side - 1), None))
        for y in range(side):
            terms.append((self.plaquette_index(0, y), None))
            terms.append((self.plaquette_index(side - 1, y), None))

        if len(terms) != self.n_links:
            raise AssertionError(f"dual link count {len(terms)} != {self.n_links}")
        return tuple(terms)

    @staticmethod
    def z_value(state: int, bit: int) -> int:
        return 1 - 2 * ((state >> bit) & 1)

    def diagonal_energy(self, state: int) -> float:
        """Electric energy of one tau-z basis state."""

        if not 0 <= state < self.hilbert_dim:
            raise ValueError("state index outside Hilbert space")
        electric_sum = 0
        for a, b in self.electric_terms():
            z = self.z_value(state, a)
            if b is not None:
                z *= self.z_value(state, b)
            electric_sum += z
        return 2.0 * self.g * (self.n_links - electric_sum)

    def diagonal_vector(self) -> np.ndarray:
        return np.fromiter(
            (self.diagonal_energy(s) for s in range(self.hilbert_dim)),
            dtype=np.float64,
            count=self.hilbert_dim,
        )

    def matvec(self, vector: np.ndarray) -> np.ndarray:
        """Apply the exact dual Hamiltonian to a dense state vector."""

        vector = np.asarray(vector)
        if vector.shape != (self.hilbert_dim,):
            raise ValueError(f"expected vector shape {(self.hilbert_dim,)}, got {vector.shape}")
        out = self.diagonal_vector() * vector
        indices = np.arange(self.hilbert_dim, dtype=np.int64)
        for bit in range(self.n_plaquettes):
            out = out - 2.0 * self.h * vector[indices ^ (1 << bit)]
        return out

    def dense_hamiltonian(self) -> np.ndarray:
        """Build a dense matrix for small-lattice reference tests only."""

        dim = self.hilbert_dim
        if dim > 4096:
            raise ValueError("dense_hamiltonian is restricted to dimension <= 4096")
        matrix = np.diag(self.diagonal_vector())
        for state in range(dim):
            for bit in range(self.n_plaquettes):
                matrix[state, state ^ (1 << bit)] += -2.0 * self.h
        return matrix

    def apply_boundary_vison(self, state: np.ndarray, x: int = 0, y: int = 0) -> np.ndarray:
        """Apply the boundary-link sigma_z, which maps to tau_z on one plaquette."""

        state = np.asarray(state)
        if state.shape != (self.hilbert_dim,):
            raise ValueError(f"expected state shape {(self.hilbert_dim,)}, got {state.shape}")
        bit = self.plaquette_index(x, y)
        signs = 1 - 2 * ((np.arange(self.hilbert_dim, dtype=np.int64) >> bit) & 1)
        return state * signs

    def plaquette_expectation(self, state: np.ndarray, x: int, y: int) -> float:
        """Return <tau_x> for a normalized state; this is the plotted Z2 plaquette."""

        state = np.asarray(state)
        bit = self.plaquette_index(x, y)
        indices = np.arange(self.hilbert_dim, dtype=np.int64)
        value = np.vdot(state, state[indices ^ (1 << bit)])
        return float(np.real(value))


def exact_ground_state(model: DualZ2OBC) -> tuple[float, np.ndarray]:
    """Dense reference ground state for tests and tiny smoke runs."""

    values, vectors = np.linalg.eigh(model.dense_hamiltonian())
    return float(values[0]), vectors[:, 0]


def evolve_exact(
    model: DualZ2OBC,
    state: np.ndarray,
    times: Iterable[float],
) -> dict[float, np.ndarray]:
    """Dense spectral evolution for tiny reference lattices."""

    values, vectors = np.linalg.eigh(model.dense_hamiltonian())
    coeff = vectors.conj().T @ np.asarray(state, dtype=np.complex128)
    return {
        float(time): vectors @ (np.exp(-1j * values * float(time)) * coeff)
        for time in times
    }
