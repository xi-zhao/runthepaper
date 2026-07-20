"""Exact open-boundary dual basis for charge-free pure Z_N gauge theory."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class DualZNOBC:
    lattice_size: int
    group_order: int
    h: float = 1.0
    g: float = 0.1

    def __post_init__(self) -> None:
        if self.lattice_size < 2:
            raise ValueError("lattice_size must be at least 2")
        if self.group_order < 2:
            raise ValueError("group_order must be at least 2")

    @property
    def plaquette_side(self) -> int:
        return self.lattice_size - 1

    @property
    def n_plaquettes(self) -> int:
        return self.plaquette_side**2

    @property
    def hilbert_dim(self) -> int:
        return self.group_order**self.n_plaquettes

    @property
    def n_links(self) -> int:
        return 2 * self.lattice_size * (self.lattice_size - 1)

    @property
    def powers(self) -> tuple[int, ...]:
        return tuple(self.group_order**bit for bit in range(self.n_plaquettes))

    def plaquette_index(self, x: int, y: int) -> int:
        side = self.plaquette_side
        if not (0 <= x < side and 0 <= y < side):
            raise ValueError(f"plaquette {(x, y)} outside 0..{side - 1}")
        return y * side + x

    def electric_terms(self) -> tuple[tuple[int, int | None], ...]:
        side = self.plaquette_side
        terms: list[tuple[int, int | None]] = []
        for y in range(side):
            for x in range(side - 1):
                terms.append((self.plaquette_index(x, y), self.plaquette_index(x + 1, y)))
        for y in range(side - 1):
            for x in range(side):
                terms.append((self.plaquette_index(x, y), self.plaquette_index(x, y + 1)))
        for x in range(side):
            terms.append((self.plaquette_index(x, 0), None))
            terms.append((self.plaquette_index(x, side - 1), None))
        for y in range(side):
            terms.append((self.plaquette_index(0, y), None))
            terms.append((self.plaquette_index(side - 1, y), None))
        if len(terms) != self.n_links:
            raise AssertionError("dual electric-link count mismatch")
        return tuple(terms)

    def digit(self, state: int, bit: int) -> int:
        return (state // self.powers[bit]) % self.group_order

    def electric_coefficient(self, state: int) -> float:
        coefficient = 0.0
        for a, b in self.electric_terms():
            electric = self.digit(state, a)
            if b is not None:
                electric = (electric - self.digit(state, b)) % self.group_order
            coefficient += 2.0 - 2.0 * np.cos(2.0 * np.pi * electric / self.group_order)
        return coefficient

    def diagonal_vector(self) -> np.ndarray:
        return self.g * np.fromiter(
            (self.electric_coefficient(state) for state in range(self.hilbert_dim)),
            dtype=np.float64,
            count=self.hilbert_dim,
        )

    def matvec(self, vector: np.ndarray) -> np.ndarray:
        vector = np.asarray(vector)
        if vector.shape != (self.hilbert_dim,):
            raise ValueError("vector shape does not match Hilbert space")
        out = self.diagonal_vector() * vector
        indices = np.arange(self.hilbert_dim, dtype=np.int64)
        for power in self.powers:
            digits = (indices // power) % self.group_order
            plus = np.where(digits == self.group_order - 1, indices - (self.group_order - 1) * power, indices + power)
            minus = np.where(digits == 0, indices + (self.group_order - 1) * power, indices - power)
            out = out - self.h * (vector[plus] + vector[minus])
        return out

    def dense_hamiltonian(self) -> np.ndarray:
        if self.hilbert_dim > 4096:
            raise ValueError("dense reference restricted to dimension <= 4096")
        dim = self.hilbert_dim
        matrix = np.diag(self.diagonal_vector())
        for state in range(dim):
            for power in self.powers:
                digit = (state // power) % self.group_order
                plus = state - (self.group_order - 1) * power if digit == self.group_order - 1 else state + power
                minus = state + (self.group_order - 1) * power if digit == 0 else state - power
                matrix[state, plus] -= self.h
                matrix[state, minus] -= self.h
        return matrix
