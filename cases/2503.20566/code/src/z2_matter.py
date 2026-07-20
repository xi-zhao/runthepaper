"""Gauge-invariant basis for Z2 gauge fields with hard-core bosons on OBC grids."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np


@dataclass(frozen=True)
class Edge:
    u: int
    v: int
    direction: str
    x: int
    y: int


@dataclass(frozen=True)
class Z2MatterOBC:
    lattice_size: int
    particle_number: int
    mass: float = 0.0
    h: float = 1.0
    g: float = 0.33
    hopping: float = 0.5

    def __post_init__(self) -> None:
        n_vertices = self.lattice_size**2
        if self.lattice_size < 2:
            raise ValueError("lattice_size must be at least 2")
        if not (0 <= self.particle_number <= n_vertices):
            raise ValueError("invalid particle number")
        if self.particle_number % 2:
            raise ValueError("Q=0 OBC sector requires even total matter parity")

    @property
    def n_vertices(self) -> int:
        return self.lattice_size**2

    @property
    def n_plaquettes(self) -> int:
        return (self.lattice_size - 1) ** 2

    @property
    def n_links(self) -> int:
        return 2 * self.lattice_size * (self.lattice_size - 1)

    def vertex(self, x: int, y: int) -> int:
        return y * self.lattice_size + x

    def edges(self) -> tuple[Edge, ...]:
        L = self.lattice_size
        edges: list[Edge] = []
        for y in range(L):
            for x in range(L - 1):
                edges.append(Edge(self.vertex(x, y), self.vertex(x + 1, y), "x", x, y))
        for y in range(L - 1):
            for x in range(L):
                edges.append(Edge(self.vertex(x, y), self.vertex(x, y + 1), "y", x, y))
        return tuple(edges)

    def edge_index(self) -> dict[tuple[int, int], int]:
        return {tuple(sorted((edge.u, edge.v))): idx for idx, edge in enumerate(self.edges())}

    def plaquette_edge_masks(self) -> tuple[int, ...]:
        L = self.lattice_size
        edge_index = self.edge_index()
        masks: list[int] = []
        for y in range(L - 1):
            for x in range(L - 1):
                vertices = [
                    self.vertex(x, y),
                    self.vertex(x + 1, y),
                    self.vertex(x + 1, y + 1),
                    self.vertex(x, y + 1),
                ]
                mask = 0
                for a, b in zip(vertices, vertices[1:] + vertices[:1]):
                    mask ^= 1 << edge_index[tuple(sorted((a, b)))]
                masks.append(mask)
        return tuple(masks)

    def edge_plaquette_masks(self) -> tuple[int, ...]:
        masks = [0] * self.n_links
        for plaquette, edge_mask in enumerate(self.plaquette_edge_masks()):
            for edge in range(self.n_links):
                if (edge_mask >> edge) & 1:
                    masks[edge] |= 1 << plaquette
        return tuple(masks)

    def matter_configurations(self) -> tuple[int, ...]:
        configs = []
        for occupied in combinations(range(self.n_vertices), self.particle_number):
            mask = 0
            for vertex in occupied:
                mask |= 1 << vertex
            configs.append(mask)
        return tuple(sorted(configs))

    def tree_child_data(self) -> tuple[tuple[int, int, int], ...]:
        """Return (child, edge, subtree_vertex_mask) for a fixed spanning tree."""

        L = self.lattice_size
        edges = self.edges()
        edge_index = self.edge_index()
        adjacency: list[list[tuple[int, int]]] = [[] for _ in range(self.n_vertices)]

        # Horizontal rows plus the leftmost vertical spine form a spanning tree.
        for idx, edge in enumerate(edges):
            if edge.direction == "x" or (edge.direction == "y" and edge.x == 0):
                adjacency[edge.u].append((edge.v, idx))
                adjacency[edge.v].append((edge.u, idx))

        parent = [-1] * self.n_vertices
        parent_edge = [-1] * self.n_vertices
        order = [0]
        for vertex in order:
            for neighbor, edge in adjacency[vertex]:
                if neighbor == parent[vertex]:
                    continue
                parent[neighbor] = vertex
                parent_edge[neighbor] = edge
                order.append(neighbor)
        if len(order) != self.n_vertices:
            raise AssertionError("reference tree is not connected")

        subtree = [1 << vertex for vertex in range(self.n_vertices)]
        for vertex in reversed(order[1:]):
            subtree[parent[vertex]] |= subtree[vertex]
        return tuple((vertex, parent_edge[vertex], subtree[vertex]) for vertex in order[1:])

    def reference_edge_mask(self, matter_mask: int) -> int:
        edge_mask = 0
        for _, edge, subtree_mask in self.tree_child_data():
            if (matter_mask & subtree_mask).bit_count() % 2:
                edge_mask |= 1 << edge
        return edge_mask

    def gauss_parity(self, matter_mask: int, edge_mask: int) -> np.ndarray:
        parity = np.array([(matter_mask >> v) & 1 for v in range(self.n_vertices)], dtype=np.int8)
        for edge_idx, edge in enumerate(self.edges()):
            if (edge_mask >> edge_idx) & 1:
                parity[edge.u] ^= 1
                parity[edge.v] ^= 1
        return parity

    def curl_lookup(self) -> dict[int, int]:
        lookup: dict[int, int] = {}
        plaquettes = self.plaquette_edge_masks()
        for plaquette_bits in range(1 << self.n_plaquettes):
            edge_mask = 0
            for plaquette, cycle in enumerate(plaquettes):
                if (plaquette_bits >> plaquette) & 1:
                    edge_mask ^= cycle
            lookup[edge_mask] = plaquette_bits
        if len(lookup) != 1 << self.n_plaquettes:
            raise AssertionError("plaquette curls are not independent on OBC")
        return lookup

    def hopping_plaquette_masks(self) -> tuple[int, ...]:
        lookup = self.curl_lookup()
        masks = []
        for edge_idx, edge in enumerate(self.edges()):
            endpoint_charges = (1 << edge.u) | (1 << edge.v)
            divergence_free = self.reference_edge_mask(endpoint_charges) ^ (1 << edge_idx)
            masks.append(lookup[divergence_free])
        return tuple(masks)

    @property
    def hilbert_dim(self) -> int:
        return len(self.matter_configurations()) * (1 << self.n_plaquettes)

    def central_region(self) -> tuple[set[int], tuple[int, ...], tuple[int, ...]]:
        """Lower-left 3x3 vertex block; symmetry makes the four choices equivalent."""

        if self.lattice_size < 3:
            vertices = set(range(self.n_vertices))
        else:
            vertices = {self.vertex(x, y) for y in range(3) for x in range(3)}
        central_edges = tuple(
            idx for idx, edge in enumerate(self.edges()) if edge.u in vertices and edge.v in vertices
        )
        central_plaquettes = tuple(
            y * (self.lattice_size - 1) + x
            for y in range(min(2, self.lattice_size - 1))
            for x in range(min(2, self.lattice_size - 1))
        )
        return vertices, central_edges, central_plaquettes
