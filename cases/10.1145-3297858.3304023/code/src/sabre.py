"""SABRE reconstruction from the paper text.

This module intentionally does not call any existing SABRE implementation.
It implements the paper's front-layer search, look-ahead heuristic, decay
penalty, and forward-backward-forward traversal.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
import random

import networkx as nx


@dataclass(frozen=True)
class Gate:
    """A two-qubit gate in logical-qubit coordinates."""

    q1: int
    q2: int
    name: str = "cx"


@dataclass(frozen=True)
class Operation:
    """An output operation in logical-qubit coordinates."""

    name: str
    q1: int | None
    q2: int | None
    p1: int | None = None
    p2: int | None = None


@dataclass
class RouteResult:
    routed_ops: list[Operation]
    initial_layout: list[int]
    final_layout: list[int]
    swaps: list[tuple[int | None, int | None]]
    original_two_qubit_gates: int
    additional_cnot_gates: int
    output_depth: int
    runtime_sec: float
    hardware_compliant: bool


def tokyo_20_graph() -> nx.Graph:
    """Return the symmetric IBM Q20 Tokyo coupling graph used in the paper."""

    edges = {
        (0, 1), (1, 2), (2, 3), (3, 4),
        (5, 6), (6, 7), (7, 8), (8, 9),
        (10, 11), (11, 12), (12, 13), (13, 14),
        (15, 16), (16, 17), (17, 18), (18, 19),
        (0, 5), (5, 10), (10, 15),
        (1, 6), (6, 11), (11, 16),
        (2, 7), (7, 12), (12, 17),
        (3, 8), (8, 13), (13, 18),
        (4, 9), (9, 14), (14, 19),
        (1, 7), (2, 6), (3, 9), (4, 8),
        (5, 11), (6, 10), (7, 13), (8, 12),
        (10, 16), (11, 15), (12, 18), (13, 17),
    }
    graph = nx.Graph()
    graph.add_nodes_from(range(20))
    graph.add_edges_from(edges)
    return graph


def square_4_graph() -> nx.Graph:
    """Return the four-qubit square coupling graph from the paper example."""

    graph = nx.Graph()
    graph.add_nodes_from(range(4))
    graph.add_edges_from([(0, 1), (1, 3), (3, 2), (2, 0)])
    return graph


def distance_lookup(graph: nx.Graph) -> dict[int, dict[int, int]]:
    return dict(nx.all_pairs_shortest_path_length(graph))


def identity_layout(n_logical: int) -> list[int]:
    return list(range(n_logical))


def random_layout(n_logical: int, n_physical: int, rng: random.Random) -> list[int]:
    physical = list(range(n_physical))
    rng.shuffle(physical)
    return physical[:n_logical]


def route_sabre(
    gates: list[Gate],
    graph: nx.Graph,
    initial_layout: list[int],
    extended_size: int = 20,
    lookahead_weight: float = 0.5,
    decay_delta: float = 0.001,
    decay_reset_interval: int = 5,
    use_decay: bool = True,
) -> RouteResult:
    """Run one SABRE traversal on a fixed gate order and initial layout."""

    start = perf_counter()
    distances = distance_lookup(graph)
    state = _SearchState(gates=gates)
    layout = list(initial_layout)
    occupant = _occupant_from_layout(layout, graph.number_of_nodes())
    routed_ops: list[Operation] = []
    swaps: list[tuple[int | None, int | None]] = []
    decay = {physical: 1.0 for physical in graph.nodes}
    swap_steps_since_reset = 0

    while state.front_layer:
        executable = [
            gid
            for gid in sorted(state.front_layer)
            if _is_gate_executable(gates[gid], layout, graph)
        ]
        if executable:
            for gid in executable:
                gate = gates[gid]
                routed_ops.append(Operation(gate.name, gate.q1, gate.q2))
                state.execute(gid)
            for physical in decay:
                decay[physical] = 1.0
            swap_steps_since_reset = 0
            continue

        candidates = _candidate_physical_swaps(state.front_layer, gates, layout, occupant, graph)
        if not candidates:
            raise RuntimeError("no candidate SWAPs available")
        extended = state.extended_set(extended_size)
        best = min(
            candidates,
            key=lambda edge: (
                _heuristic_score(
                    edge=edge,
                    gates=gates,
                    front_layer=state.front_layer,
                    extended_set=extended,
                    layout=layout,
                    occupant=occupant,
                    distances=distances,
                    lookahead_weight=lookahead_weight,
                    decay=decay,
                    use_decay=use_decay,
                ),
                edge,
            ),
        )
        p1, p2 = best
        logical_1, logical_2 = occupant[p1], occupant[p2]
        routed_ops.append(Operation("swap", logical_1, logical_2, p1, p2))
        swaps.append((logical_1, logical_2))
        _apply_physical_swap(layout, occupant, p1, p2)

        if use_decay:
            decay[p1] = 1.0 + decay_delta
            decay[p2] = 1.0 + decay_delta
            swap_steps_since_reset += 1
            if decay_reset_interval > 0 and swap_steps_since_reset >= decay_reset_interval:
                for physical in decay:
                    decay[physical] = 1.0
                swap_steps_since_reset = 0

    depth = compute_depth(routed_ops)
    runtime = perf_counter() - start
    return RouteResult(
        routed_ops=routed_ops,
        initial_layout=list(initial_layout),
        final_layout=layout,
        swaps=swaps,
        original_two_qubit_gates=len(gates),
        additional_cnot_gates=3 * len(swaps),
        output_depth=depth,
        runtime_sec=runtime,
        hardware_compliant=check_hardware_compliance(routed_ops, initial_layout, graph),
    )


def sabre_forward_backward_forward(
    gates: list[Gate],
    graph: nx.Graph,
    attempts: int = 5,
    seed: int = 7,
    extended_size: int = 20,
    lookahead_weight: float = 0.5,
    decay_delta: float = 0.001,
    use_decay: bool = True,
) -> RouteResult:
    """Run the paper's forward-backward-forward initial mapping optimization."""

    rng = random.Random(seed)
    n_logical = 1 + max(max(g.q1, g.q2) for g in gates) if gates else 0
    best: RouteResult | None = None

    for _ in range(attempts):
        temporary = random_layout(n_logical, graph.number_of_nodes(), rng)
        first = route_sabre(
            gates=gates,
            graph=graph,
            initial_layout=temporary,
            extended_size=extended_size,
            lookahead_weight=lookahead_weight,
            decay_delta=decay_delta,
            use_decay=use_decay,
        )
        reverse = route_sabre(
            gates=list(reversed(gates)),
            graph=graph,
            initial_layout=first.final_layout,
            extended_size=extended_size,
            lookahead_weight=lookahead_weight,
            decay_delta=decay_delta,
            use_decay=use_decay,
        )
        final = route_sabre(
            gates=gates,
            graph=graph,
            initial_layout=reverse.final_layout,
            extended_size=extended_size,
            lookahead_weight=lookahead_weight,
            decay_delta=decay_delta,
            use_decay=use_decay,
        )
        if best is None or _result_key(final) < _result_key(best):
            best = final

    if best is None:
        raise RuntimeError("no SABRE attempt executed")
    return best


def compute_depth(ops: list[Operation]) -> int:
    """Compute ASAP depth. A SWAP has CNOT-equivalent duration 3."""

    available: dict[int, int] = {}
    max_finish = 0
    for op in ops:
        qubits = [q for q in [op.q1, op.q2] if q is not None]
        if not qubits:
            continue
        duration = 3 if op.name == "swap" else 1
        start = max(available.get(q, 0) for q in qubits)
        finish = start + duration
        for q in qubits:
            available[q] = finish
        max_finish = max(max_finish, finish)
    return max_finish


def check_hardware_compliance(ops: list[Operation], initial_layout: list[int], graph: nx.Graph) -> bool:
    layout = list(initial_layout)
    occupant = _occupant_from_layout(layout, graph.number_of_nodes())
    for op in ops:
        if op.name == "swap":
            if op.p1 is None or op.p2 is None or not graph.has_edge(op.p1, op.p2):
                return False
            if occupant[op.p1] != op.q1 or occupant[op.p2] != op.q2:
                return False
            _apply_physical_swap(layout, occupant, op.p1, op.p2)
        elif op.name == "cx":
            if op.q1 is None or op.q2 is None:
                return False
            if not graph.has_edge(layout[op.q1], layout[op.q2]):
                return False
    return True


class _SearchState:
    def __init__(self, gates: list[Gate]) -> None:
        self.gates = gates
        self.predecessor_count, self.successors = _build_dependencies(gates)
        self.remaining = set(range(len(gates)))
        self.front_layer = {
            idx for idx, count in enumerate(self.predecessor_count) if count == 0
        }

    def execute(self, gate_id: int) -> None:
        if gate_id not in self.front_layer:
            raise ValueError(f"gate {gate_id} is not in front layer")
        self.front_layer.remove(gate_id)
        self.remaining.remove(gate_id)
        for successor in self.successors[gate_id]:
            self.predecessor_count[successor] -= 1
            if self.predecessor_count[successor] == 0:
                self.front_layer.add(successor)

    def extended_set(self, limit: int) -> list[int]:
        if limit <= 0:
            return []
        seen = set(self.front_layer)
        queue = sorted(self.front_layer)
        extended: list[int] = []
        while queue and len(extended) < limit:
            current = queue.pop(0)
            for successor in sorted(self.successors[current]):
                if successor in seen or successor not in self.remaining:
                    continue
                seen.add(successor)
                extended.append(successor)
                queue.append(successor)
                if len(extended) >= limit:
                    break
        return extended


def _build_dependencies(gates: list[Gate]) -> tuple[list[int], list[list[int]]]:
    predecessor_sets = [set() for _ in gates]
    successors = [[] for _ in gates]
    last_gate_for_qubit: dict[int, int] = {}
    for idx, gate in enumerate(gates):
        for qubit in (gate.q1, gate.q2):
            if qubit in last_gate_for_qubit:
                pred = last_gate_for_qubit[qubit]
                predecessor_sets[idx].add(pred)
                successors[pred].append(idx)
            last_gate_for_qubit[qubit] = idx
    predecessor_count = [len(preds) for preds in predecessor_sets]
    return predecessor_count, successors


def _is_gate_executable(gate: Gate, layout: list[int], graph: nx.Graph) -> bool:
    return graph.has_edge(layout[gate.q1], layout[gate.q2])


def _occupant_from_layout(layout: list[int], n_physical: int) -> list[int | None]:
    occupant: list[int | None] = [None] * n_physical
    for logical, physical in enumerate(layout):
        occupant[physical] = logical
    return occupant


def _candidate_physical_swaps(
    front_layer: set[int],
    gates: list[Gate],
    layout: list[int],
    occupant: list[int | None],
    graph: nx.Graph,
) -> list[tuple[int, int]]:
    physical_front = set()
    for gate_id in front_layer:
        gate = gates[gate_id]
        physical_front.add(layout[gate.q1])
        physical_front.add(layout[gate.q2])
    candidates = set()
    for physical in physical_front:
        for neighbor in graph.neighbors(physical):
            edge = tuple(sorted((physical, neighbor)))
            if occupant[physical] is not None or occupant[neighbor] is not None:
                candidates.add(edge)
    return sorted(candidates)


def _heuristic_score(
    edge: tuple[int, int],
    gates: list[Gate],
    front_layer: set[int],
    extended_set: list[int],
    layout: list[int],
    occupant: list[int | None],
    distances: dict[int, dict[int, int]],
    lookahead_weight: float,
    decay: dict[int, float],
    use_decay: bool,
) -> float:
    temp_layout = list(layout)
    temp_occupant = list(occupant)
    _apply_physical_swap(temp_layout, temp_occupant, edge[0], edge[1])
    front_cost = _average_distance(sorted(front_layer), gates, temp_layout, distances)
    extended_cost = _average_distance(extended_set, gates, temp_layout, distances)
    score = front_cost + lookahead_weight * extended_cost
    if use_decay:
        score *= max(decay[edge[0]], decay[edge[1]])
    return score


def _average_distance(
    gate_ids: list[int],
    gates: list[Gate],
    layout: list[int],
    distances: dict[int, dict[int, int]],
) -> float:
    if not gate_ids:
        return 0.0
    total = 0
    for gate_id in gate_ids:
        gate = gates[gate_id]
        total += distances[layout[gate.q1]][layout[gate.q2]]
    return total / len(gate_ids)


def _apply_physical_swap(
    layout: list[int],
    occupant: list[int | None],
    p1: int,
    p2: int,
) -> None:
    logical_1, logical_2 = occupant[p1], occupant[p2]
    occupant[p1], occupant[p2] = logical_2, logical_1
    if logical_1 is not None:
        layout[logical_1] = p2
    if logical_2 is not None:
        layout[logical_2] = p1


def _find_empty_neighbor(physical: int, occupant: list[int | None], graph: nx.Graph) -> int | None:
    for neighbor in graph.neighbors(physical):
        if occupant[neighbor] is None:
            return neighbor
    return None


def _result_key(result: RouteResult) -> tuple[int, int, float]:
    return result.additional_cnot_gates, result.output_depth, result.runtime_sec
