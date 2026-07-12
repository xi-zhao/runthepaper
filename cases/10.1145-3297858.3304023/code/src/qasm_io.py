"""Small OpenQASM 2 reader for benchmark accounting.

This parser is intentionally narrow. It extracts qubit count, total operation
count, ASAP depth, and two-qubit CX dependencies from benchmark QASM files.
It does not use any routing or mapping implementation from external projects.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from sabre import Gate


_QREG_RE = re.compile(r"qreg\s+([A-Za-z_]\w*)\[(\d+)\]\s*;")
_QUBIT_RE = re.compile(r"([A-Za-z_]\w*)\[(\d+)\]")


@dataclass(frozen=True)
class QasmCircuit:
    path: Path
    n_qubits: int
    total_ops: int
    original_depth: int
    cx_gates: list[Gate]


def load_qasm_circuit(path: Path) -> QasmCircuit:
    register_offsets: dict[str, int] = {}
    n_qubits = 0
    operations: list[tuple[str, list[int]]] = []

    for raw_line in path.read_text().splitlines():
        line = raw_line.split("//", 1)[0].strip()
        if not line:
            continue
        qreg = _QREG_RE.fullmatch(line)
        if qreg:
            name, size_text = qreg.groups()
            register_offsets[name] = n_qubits
            n_qubits += int(size_text)
            continue
        if _is_header_or_non_operation(line):
            continue

        op_name = line.split(None, 1)[0].split("(", 1)[0]
        qubits = [
            register_offsets[register] + int(index)
            for register, index in _QUBIT_RE.findall(line)
            if register in register_offsets
        ]
        if not qubits:
            continue
        operations.append((op_name, qubits))

    cx_gates = [
        Gate(qubits[0], qubits[1])
        for op_name, qubits in operations
        if op_name == "cx" and len(qubits) == 2
    ]
    return QasmCircuit(
        path=path,
        n_qubits=n_qubits,
        total_ops=len(operations),
        original_depth=_operation_depth(operations),
        cx_gates=cx_gates,
    )


def _is_header_or_non_operation(line: str) -> bool:
    return (
        line.startswith("OPENQASM")
        or line.startswith("include")
        or line.startswith("creg")
        or line.startswith("barrier")
        or line.startswith("measure")
    )


def _operation_depth(operations: list[tuple[str, list[int]]]) -> int:
    available: dict[int, int] = {}
    max_finish = 0
    for _op_name, qubits in operations:
        start = max((available.get(qubit, 0) for qubit in qubits), default=0)
        finish = start + 1
        for qubit in qubits:
            available[qubit] = finish
        max_finish = max(max_finish, finish)
    return max_finish
