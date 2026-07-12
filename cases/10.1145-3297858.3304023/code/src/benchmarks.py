"""Local benchmark inputs for the SABRE reproduction."""

from __future__ import annotations

from qiskit import transpile
from qiskit.circuit.library import QFT

from sabre import Gate


def paper_swap_example() -> list[Gate]:
    """Return the six-CNOT example from Fig. 3, using zero-based labels."""

    return [
        Gate(0, 1),
        Gate(2, 3),
        Gate(1, 3),
        Gate(1, 2),
        Gate(2, 3),
        Gate(0, 3),
    ]


def path_ising(n_qubits: int, rounds: int = 8) -> list[Gate]:
    """Generate a nearest-neighbor Ising-style interaction circuit."""

    gates: list[Gate] = []
    for _ in range(rounds):
        for q in range(n_qubits - 1):
            gates.append(Gate(q, q + 1))
    return gates


def qft_cnot_dependencies(n_qubits: int) -> list[Gate]:
    """Generate QFT two-qubit dependencies locally without using routing."""

    circuit = QFT(n_qubits, do_swaps=False).decompose()
    decomposed = transpile(circuit, basis_gates=["u3", "cx"], optimization_level=0)
    gates: list[Gate] = []
    for instruction in decomposed.data:
        if instruction.operation.name == "cx":
            q1, q2 = [decomposed.qubits.index(q) for q in instruction.qubits]
            gates.append(Gate(q1, q2))
    return gates
