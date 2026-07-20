"""Exact fully-frustrated dual model for the odd open-boundary Z2 theory."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class OddLink:
    a: int
    b: int | None
    eta: int
    direction: str
    x: int
    y: int


@dataclass(frozen=True)
class OddZ2OBC:
    lattice_size: int
    h: float = 1.0
    g: float = 0.4

    def __post_init__(self) -> None:
        if self.lattice_size < 2 or self.lattice_size % 2:
            raise ValueError("uniform odd charge with OBC requires an even lattice size")

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
        return y * self.plaquette_side + x

    def links(self) -> tuple[OddLink, ...]:
        """Return a reference odd-charge field dressed by dual plaquette bits.

        The reference has E=1 on horizontal links whose left endpoint has even
        x and E=0 elsewhere.  Every vertex then touches exactly one occupied
        reference link, satisfying Q_x=1.  ``eta=(-1)^E_ref``.
        """

        L = self.lattice_size
        side = self.plaquette_side
        links: list[OddLink] = []
        for y in range(L):
            for x in range(L - 1):
                adjacent: list[int] = []
                if y > 0:
                    adjacent.append(self.plaquette_index(x, y - 1))
                if y < side:
                    adjacent.append(self.plaquette_index(x, y))
                links.append(
                    OddLink(
                        adjacent[0],
                        adjacent[1] if len(adjacent) == 2 else None,
                        -1 if x % 2 == 0 else 1,
                        "x",
                        x,
                        y,
                    )
                )
        for y in range(L - 1):
            for x in range(L):
                adjacent = []
                if x > 0:
                    adjacent.append(self.plaquette_index(x - 1, y))
                if x < side:
                    adjacent.append(self.plaquette_index(x, y))
                links.append(
                    OddLink(
                        adjacent[0],
                        adjacent[1] if len(adjacent) == 2 else None,
                        1,
                        "y",
                        x,
                        y,
                    )
                )
        if len(links) != self.n_links:
            raise AssertionError("odd-Z2 link count mismatch")
        return tuple(links)

    def reference_vertex_parities(self) -> np.ndarray:
        parity = np.zeros((self.lattice_size, self.lattice_size), dtype=np.int8)
        for link in self.links():
            if link.eta == 1:
                continue
            parity[link.y, link.x] ^= 1
            if link.direction == "x":
                parity[link.y, link.x + 1] ^= 1
            else:
                parity[link.y + 1, link.x] ^= 1
        return parity

    @staticmethod
    def z_value(state: int, bit: int) -> int:
        return 1 - 2 * ((state >> bit) & 1)

    def link_z(self, state: int, link: OddLink) -> int:
        value = link.eta * self.z_value(state, link.a)
        if link.b is not None:
            value *= self.z_value(state, link.b)
        return value

    def diagonal_observables(self, state: int) -> tuple[float, float, float]:
        electric = 0.0
        dx = 0.0
        dy = 0.0
        norm = self.lattice_size * (self.lattice_size - 1)
        for link in self.links():
            bar_e = 2.0 - 2.0 * self.link_z(state, link)
            electric += self.g * bar_e
            if link.direction == "x":
                dx += ((-1) ** link.x) * bar_e / norm
            else:
                dy += ((-1) ** link.y) * bar_e / norm
        return electric, dx, dy

    def dense_hamiltonian(self) -> np.ndarray:
        if self.hilbert_dim > 4096:
            raise ValueError("dense reference restricted to dimension <= 4096")
        diagonal = np.array([self.diagonal_observables(s)[0] for s in range(self.hilbert_dim)])
        matrix = np.diag(diagonal)
        for state in range(self.hilbert_dim):
            for bit in range(self.n_plaquettes):
                matrix[state, state ^ (1 << bit)] -= 2.0 * self.h
        return matrix
