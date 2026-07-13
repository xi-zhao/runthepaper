"""Exact Steane-code |H>-state preparation protocol from Fig. CH-meas-circ.

Implements the paper's benchmark protocol as a Monte Carlo state-vector
simulation (the paper's own Cirq baseline):

- (a) non-FT unitary encoding of |Hbar> on the [[7,1,3]] Steane code
  (10 CNOTs, transcribed from the vector paths of steane_code_circuit.pdf);
- (b) flag-based measurement of the transversal logical Hbar with one
  ancilla and one flag, gate order taken from the paper's error-location
  table (Appendix "Magic state |H> simulation details");
- (c) one round of stabilizer measurements: the three supports
  {2,3,4,7}, {1,2,6,7}, {4,5,6,7} each measured in X and Z, with the
  X-type ancillas doubling as flags for the Z-type ancillas
  (mutual-flag construction, transcribed gate-by-gate from the figure).

Noise model (Appendix "Error Model"), uniform strength p:
- init |0>: X with prob p; |+>: Z with prob p; |H>: Y with prob p;
- after each 2-qubit gate: uniform 2-qubit depolarizing (15 Paulis, p/15);
- idling qubits: single-qubit depolarizing per timeslice (X/Y/Z, p/3);
- before X-basis measurement: Z with prob p; before Z-basis: X with prob p.

All measurements are postselected on +1. Outputs per shot: accepted or
not; if accepted, fidelity |<target|psi>|^2 of the 7-qubit data state
against the noiseless protocol output.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

SQRT_HALF = 1.0 / np.sqrt(2.0)
H_GATE = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=np.complex128) * SQRT_HALF
X_GATE = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
Y_GATE = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=np.complex128)
Z_GATE = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
PAULI_1Q = {"X": X_GATE, "Y": Y_GATE, "Z": Z_GATE}
PAULI_LABELS_2Q = [
    (a, b)
    for a in ("I", "X", "Y", "Z")
    for b in ("I", "X", "Y", "Z")
    if not (a == "I" and b == "I")
]

# |H> = cos(pi/8)|0> + sin(pi/8)|1> is the +1 eigenstate of the Hadamard.
KET_H = np.array([np.cos(np.pi / 8.0), np.sin(np.pi / 8.0)], dtype=np.complex128)
KET_0 = np.array([1.0, 0.0], dtype=np.complex128)
KET_PLUS = np.array([SQRT_HALF, SQRT_HALF], dtype=np.complex128)

# --- Circuit spec (data qubits 0..6 = paper q1..q7) ---

DATA_INITS = ["H", "+", "0", "+", "0", "0", "+"]

# Panel (a): timeslices of CNOT(control, target), transcribed from the PDF.
ENCODING_SLICES = [
    [(3, 2), (6, 4)],
    [(0, 5)],
    [(6, 2)],
    [(1, 5)],
    [(0, 4)],
    [(6, 0)],
    [(1, 4)],
    [(1, 2), (3, 5)],
    [(3, 0)],
]

# Panel (b): appendix error-table order. ("CH", data) means CH(anc -> data);
# ("CXF",) is CNOT(anc -> flag).
GADGET_SLICES = [
    [("CH", 6)],
    [("CXF",)],
    [("CH", 5)],
    [("CH", 4)],
    [("CH", 3)],
    [("CH", 2)],
    [("CH", 1)],
    [("CXF",)],
    [("CH", 0)],
]

# Panel (c): 28 sequential 2-qubit gates in drawn (x) order.
# Ancillas: A1,A5,A6 are X-type (|+>, control into data / flag CX into
# Z-ancillas); A2,A3,A4 are Z-type (|0>, targets of data controls).
# Entries are (control, target) with names resolved at build time.
STAB_ROUND_GATES = [
    ("A1", "q2"),
    ("q7", "A2"),
    ("q6", "A3"),
    ("A1", "A3"),
    ("A1", "q3"),
    ("q2", "A2"),
    ("q5", "A3"),
    ("A1", "q4"),
    ("q1", "A2"),
    ("q7", "A3"),
    ("A1", "A2"),
    ("A1", "q7"),
    ("q6", "A2"),
    ("q4", "A3"),
    ("q2", "A4"),
    ("A5", "q7"),
    ("A6", "q6"),
    ("A6", "A4"),
    ("q3", "A4"),
    ("A5", "q2"),
    ("A6", "q5"),
    ("q4", "A4"),
    ("A5", "q1"),
    ("A6", "q7"),
    ("A5", "A4"),
    ("q7", "A4"),
    ("A5", "q6"),
    ("A6", "q4"),
]
STAB_ANCILLA_INITS = {"A1": "+", "A2": "0", "A3": "0", "A4": "0", "A5": "+", "A6": "+"}
STAB_ANCILLA_BASES = {"A1": "X", "A2": "Z", "A3": "Z", "A4": "Z", "A5": "X", "A6": "X"}
STAB_ANCILLA_ORDER = ["A1", "A2", "A3", "A4", "A5", "A6"]


def asap_schedule(gates: list[tuple[str, str]]) -> list[list[int]]:
    """Greedy order-preserving circuit compaction (canonical ASAP slices)."""

    per_qubit: dict[str, list[int]] = {}
    for index, (control, target) in enumerate(gates):
        per_qubit.setdefault(control, []).append(index)
        per_qubit.setdefault(target, []).append(index)
    slices: list[list[int]] = []
    placed: set[int] = set()
    while len(placed) < len(gates):
        used: set[str] = set()
        this_slice: list[int] = []
        for index, (control, target) in enumerate(gates):
            if index in placed or control in used or target in used:
                continue
            ready = all(
                j in placed
                for q in (control, target)
                for j in per_qubit[q]
                if j < index
            )
            if ready:
                this_slice.append(index)
                used.update((control, target))
        slices.append(this_slice)
        placed.update(this_slice)
    return slices


# Schedule configuration for panel (c). The paper's appendix pins the (b)
# timeline exactly but gives no error-location table for (c); the slice
# structure and idle policy below are reconstructed and validated against
# the paper's acceptance-rate and infidelity curves.
STAB_SCHEDULE_MODE = "sequential"   # "sequential" | "asap"
IDLE_POLICY = "all"                 # "all" | "active_window"
# "explicit"          : (a) with init + gate + per-column idle noise
# "explicit_no_idle"   : (a) with init + gate noise, no idles
# "explicit_gates_only": (a) with gate noise only
# "pauli_frame"        : noiseless (a), then per-qubit X^a Z^b, a,b~Bern(p)
ENCODING_MODE = "explicit"


def set_protocol_config(mode: str, idle_policy: str, encoding: str = "explicit") -> None:
    global STAB_SCHEDULE_MODE, IDLE_POLICY, ENCODING_MODE, LOCATIONS, _TARGET_CACHE
    STAB_SCHEDULE_MODE = mode
    IDLE_POLICY = idle_policy
    ENCODING_MODE = encoding
    LOCATIONS = build_location_table()
    _TARGET_CACHE = None


def set_stab_schedule(mode: str, idle_policy: str) -> None:
    set_protocol_config(mode, idle_policy, ENCODING_MODE)


def _stab_slices() -> list[list[int]]:
    if STAB_SCHEDULE_MODE == "asap":
        return asap_schedule(STAB_ROUND_GATES)
    return [[i] for i in range(len(STAB_ROUND_GATES))]


def _idle_windows(slices: list[list[int]]) -> dict[tuple, tuple[int, int]]:
    """Per-qubit slice window inside which idling noise is applied for (c)."""

    n_slices = len(slices)
    last_gate_slice: dict[tuple, int] = {}
    for slice_index, gate_ids in enumerate(slices):
        for gate_id in gate_ids:
            control, target = STAB_ROUND_GATES[gate_id]
            last_gate_slice[_tag(control)] = slice_index
            last_gate_slice[_tag(target)] = slice_index
    windows: dict[tuple, tuple[int, int]] = {}
    all_tags = [("data", q) for q in range(7)] + [(name,) for name in STAB_ANCILLA_ORDER]
    for tag in all_tags:
        if IDLE_POLICY == "active_window":
            windows[tag] = (0, last_gate_slice.get(tag, -1))
        else:
            windows[tag] = (0, n_slices - 1)
    return windows


@dataclass
class ShotResult:
    accepted: bool
    fidelity: float | None
    had_error: bool


class StateVector:
    """Minimal dense state-vector register with qubit append/remove."""

    def __init__(self) -> None:
        self.psi = np.array([1.0], dtype=np.complex128)
        self.n = 0

    def append_qubit(self, amplitudes: np.ndarray) -> int:
        self.psi = np.kron(self.psi, amplitudes)
        self.n += 1
        return self.n - 1

    def apply_1q(self, gate: np.ndarray, qubit: int) -> None:
        psi = self.psi.reshape(2**qubit, 2, -1)
        self.psi = np.einsum("ab,ibj->iaj", gate, psi).reshape(-1)

    def apply_2q(self, gate: np.ndarray, q_a: int, q_b: int) -> None:
        """Apply a 4x4 gate with tensor order (q_a, q_b)."""

        n = self.n
        psi = self.psi.reshape((2,) * n)
        psi = np.moveaxis(psi, (q_a, q_b), (0, 1)).reshape(4, -1)
        psi = gate @ psi
        psi = psi.reshape((2, 2) + (2,) * (n - 2))
        self.psi = np.moveaxis(psi, (0, 1), (q_a, q_b)).reshape(-1)

    def measure_and_remove(self, qubit: int, basis: str, rng: np.random.Generator) -> int:
        """Born-rule sample a Z or X basis measurement, project, drop the qubit."""

        if basis == "X":
            self.apply_1q(H_GATE, qubit)
        psi = self.psi.reshape(2**qubit, 2, -1)
        p0 = float(np.sum(np.abs(psi[:, 0, :]) ** 2))
        outcome = 0 if rng.random() < p0 else 1
        branch = psi[:, outcome, :]
        norm = np.linalg.norm(branch)
        self.psi = (branch / norm).reshape(-1)
        self.n -= 1
        return outcome


def controlled_gate(gate_1q: np.ndarray) -> np.ndarray:
    out = np.eye(4, dtype=np.complex128)
    out[2:, 2:] = gate_1q
    return out


CX_CT = controlled_gate(X_GATE)
CH_CT = controlled_gate(H_GATE)


def build_location_table() -> list[tuple]:
    """Enumerate every stochastic error location in circuit order.

    Location kinds:
      ("init", qubit_tag, pauli)          init flip with prob p
      ("dep2", tag_a, tag_b)              2q depolarizing after a gate
      ("idle", qubit_tag)                 1q depolarizing for one timeslice
      ("meas", qubit_tag, pauli)          flip before measurement
    Qubit tags are phase-local names resolved by the simulator.
    """

    locations: list[tuple] = []
    init_pauli = {"H": "Y", "+": "Z", "0": "X"}

    # (a) explicit: init slice + 9 gate slices with idles.
    # pauli_frame: the encoding is noiseless and its noise is twirled into
    # one per-qubit depolarizing frame at the gadget input (paper t1 blue
    # boxes, eq:pauli_init_frame_H).
    if ENCODING_MODE.startswith("explicit"):
        if ENCODING_MODE != "explicit_gates_only":
            for q, state in enumerate(DATA_INITS):
                locations.append(("init", ("data", q), init_pauli[state]))
        for slice_gates in ENCODING_SLICES:
            active = {q for pair in slice_gates for q in pair}
            for control, target in slice_gates:
                locations.append(("dep2", ("data", control), ("data", target)))
            if ENCODING_MODE == "explicit":
                for q in range(7):
                    if q not in active:
                        locations.append(("idle", ("data", q)))
    else:
        # Twirled encoding frame X^a Z^b with independent a, b ~ Bernoulli(p)
        for q in range(7):
            locations.append(("init", ("data", q), "X"))
            locations.append(("init", ("data", q), "Z"))

    # (b) t1: anc/flag init; t2..t10 one gate + idles over the 9 gadget qubits
    locations.append(("init", ("anc",), "Z"))
    locations.append(("init", ("flag",), "X"))
    for slice_gates in GADGET_SLICES:
        gate = slice_gates[0]
        if gate[0] == "CH":
            pair_tags = [("anc",), ("data", gate[1])]
        else:
            pair_tags = [("anc",), ("flag",)]
        locations.append(("dep2", pair_tags[0], pair_tags[1]))
        all_tags = [("data", q) for q in range(7)] + [("anc",), ("flag",)]
        for tag in all_tags:
            if tag not in pair_tags:
                locations.append(("idle", tag))
    locations.append(("meas", ("anc",), "Z"))   # X-basis measurement
    locations.append(("meas", ("flag",), "X"))  # Z-basis measurement

    # (c) ancilla inits, scheduled gate slices with idles, measurements
    for name in STAB_ANCILLA_ORDER:
        locations.append(("init", (name,), "Z" if STAB_ANCILLA_INITS[name] == "+" else "X"))
    slices = _stab_slices()
    windows = _idle_windows(slices)
    all_tags_c = [("data", q) for q in range(7)] + [(name,) for name in STAB_ANCILLA_ORDER]
    for slice_index, gate_ids in enumerate(slices):
        busy = set()
        for gate_id in gate_ids:
            control, target = STAB_ROUND_GATES[gate_id]
            pair_tags = [_tag(control), _tag(target)]
            busy.update(pair_tags)
            locations.append(("dep2", pair_tags[0], pair_tags[1]))
        for tag in all_tags_c:
            lo, hi = windows[tag]
            if tag not in busy and lo <= slice_index <= hi:
                locations.append(("idle", tag))
    for name in STAB_ANCILLA_ORDER:
        flip = "Z" if STAB_ANCILLA_BASES[name] == "X" else "X"
        locations.append(("meas", (name,), flip))

    return locations


def _tag(name: str) -> tuple:
    if name.startswith("q"):
        return ("data", int(name[1:]) - 1)
    return (name,)


LOCATIONS = build_location_table()


def sample_errors(p: float, rng: np.random.Generator) -> dict[int, tuple]:
    """Sample the triggered locations and their Pauli content."""

    triggered = np.nonzero(rng.random(len(LOCATIONS)) < p)[0]
    errors: dict[int, tuple] = {}
    for index in triggered:
        kind = LOCATIONS[index][0]
        if kind in ("init", "meas"):
            errors[int(index)] = (LOCATIONS[index][2],)
        elif kind == "idle":
            errors[int(index)] = (("X", "Y", "Z")[rng.integers(3)],)
        else:  # dep2
            errors[int(index)] = PAULI_LABELS_2Q[rng.integers(15)]
    return errors


class ProtocolSimulator:
    """Runs one trajectory of the full (a)+(b)+(c) protocol."""

    def __init__(self, errors: dict[int, tuple], rng: np.random.Generator) -> None:
        self.errors = errors
        self.rng = rng
        self.cursor = 0
        self.state = StateVector()
        self.index_of: dict[tuple, int] = {}

    def _maybe_apply(self, *tags: tuple) -> None:
        error = self.errors.get(self.cursor)
        self.cursor += 1
        if error is None:
            return
        for pauli, tag in zip(error, tags):
            if pauli != "I":
                self.state.apply_1q(PAULI_1Q[pauli], self.index_of[tag])

    def _init_qubit(self, tag: tuple, ket: np.ndarray) -> None:
        self.index_of[tag] = self.state.append_qubit(ket)
        self._maybe_apply(tag)

    def run(self) -> tuple[bool, np.ndarray]:
        state, index_of = self.state, self.index_of
        kets = {"H": KET_H, "+": KET_PLUS, "0": KET_0}

        # (a)
        if ENCODING_MODE.startswith("explicit"):
            if ENCODING_MODE != "explicit_gates_only":
                for q, init in enumerate(DATA_INITS):
                    self._init_qubit(("data", q), kets[init])
            else:
                for q, init in enumerate(DATA_INITS):
                    index_of[("data", q)] = state.append_qubit(kets[init])
            for slice_gates in ENCODING_SLICES:
                active = {q for pair in slice_gates for q in pair}
                for control, target in slice_gates:
                    state.apply_2q(CX_CT, index_of[("data", control)], index_of[("data", target)])
                    self._maybe_apply(("data", control), ("data", target))
                if ENCODING_MODE == "explicit":
                    for q in range(7):
                        if q not in active:
                            self._maybe_apply(("data", q))
        else:
            for q, init in enumerate(DATA_INITS):
                index_of[("data", q)] = state.append_qubit(kets[init])
            for slice_gates in ENCODING_SLICES:
                for control, target in slice_gates:
                    state.apply_2q(CX_CT, index_of[("data", control)], index_of[("data", target)])
            for q in range(7):
                self._maybe_apply(("data", q))  # X frame bit
                self._maybe_apply(("data", q))  # Z frame bit

        # (b)
        self._init_qubit(("anc",), KET_PLUS)
        self._init_qubit(("flag",), KET_0)
        for slice_gates in GADGET_SLICES:
            gate = slice_gates[0]
            if gate[0] == "CH":
                pair = [("anc",), ("data", gate[1])]
                state.apply_2q(CH_CT, index_of[pair[0]], index_of[pair[1]])
            else:
                pair = [("anc",), ("flag",)]
                state.apply_2q(CX_CT, index_of[pair[0]], index_of[pair[1]])
            self._maybe_apply(*pair)
            all_tags = [("data", q) for q in range(7)] + [("anc",), ("flag",)]
            for tag in all_tags:
                if tag not in pair:
                    self._maybe_apply(tag)
        accepted = True
        self._maybe_apply(("anc",))
        if self._measure(("anc",), "X") != 0:
            accepted = False
        self._maybe_apply(("flag",))
        if self._measure(("flag",), "Z") != 0:
            accepted = False

        # (c) — must mirror build_location_table's slice/idle enumeration
        for name in STAB_ANCILLA_ORDER:
            self._init_qubit((name,), kets[STAB_ANCILLA_INITS[name]])
        slices = _stab_slices()
        windows = _idle_windows(slices)
        all_tags_c = [("data", q) for q in range(7)] + [(name,) for name in STAB_ANCILLA_ORDER]
        for slice_index, gate_ids in enumerate(slices):
            busy: set[tuple] = set()
            for gate_id in gate_ids:
                control, target = STAB_ROUND_GATES[gate_id]
                pair = [_tag(control), _tag(target)]
                busy.update(pair)
                state.apply_2q(CX_CT, index_of[pair[0]], index_of[pair[1]])
                self._maybe_apply(*pair)
            for tag in all_tags_c:
                lo, hi = windows[tag]
                if tag not in busy and lo <= slice_index <= hi:
                    self._maybe_apply(tag)
        for name in STAB_ANCILLA_ORDER:
            self._maybe_apply((name,))
            if self._measure((name,), STAB_ANCILLA_BASES[name]) != 0:
                accepted = False

        return accepted, state.psi

    def _measure(self, tag: tuple, basis: str) -> int:
        qubit = self.index_of[tag]
        outcome = self.state.measure_and_remove(qubit, basis, self.rng)
        removed_index = self.index_of.pop(tag)
        for other, idx in list(self.index_of.items()):
            if idx > removed_index:
                self.index_of[other] = idx - 1
        return outcome


# --- Ideal decoder -------------------------------------------------------
# The six measured supports form a Hamming parity check: every qubit has a
# distinct nonzero membership vector, so each nonzero syndrome points to a
# unique single-qubit correction (CSS decoding, X and Z independently).
STABILIZER_SUPPORTS = [(2, 3, 4, 7), (1, 2, 6, 7), (4, 5, 6, 7)]
_SYNDROME_TO_QUBIT = {}
for _q in range(1, 8):
    _vec = tuple(1 if _q in sup else 0 for sup in STABILIZER_SUPPORTS)
    _SYNDROME_TO_QUBIT[_vec] = _q - 1


def _apply_pauli_string(psi: np.ndarray, gate: np.ndarray, qubits: tuple[int, ...]) -> np.ndarray:
    state = psi.reshape((2,) * 7)
    for q in qubits:
        state = np.moveaxis(np.tensordot(gate, np.moveaxis(state, q, 0), axes=1), 0, q)
    return state.reshape(-1)


def ideal_decode(psi: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Project onto a syndrome sector (Born-sampled) and correct it.

    This is the ideal end-of-circuit decoder that defines the logical
    channel E_L in the paper's fidelity formula: measure both syndrome
    types noiselessly, apply the unique Hamming correction, return the
    corrected (codespace) state.
    """

    for gate, correction_gate in ((Z_GATE, X_GATE), (X_GATE, Z_GATE)):
        syndrome = []
        for support in STABILIZER_SUPPORTS:
            qubits = tuple(q - 1 for q in support)
            s_psi = _apply_pauli_string(psi, gate, qubits)
            p_plus = float(np.real(np.vdot(psi, psi + s_psi))) / 2.0
            if rng.random() < p_plus:
                psi = (psi + s_psi) / (2.0 * np.sqrt(max(p_plus, 1e-300)))
                syndrome.append(0)
            else:
                psi = (psi - s_psi) / (2.0 * np.sqrt(max(1.0 - p_plus, 1e-300)))
                syndrome.append(1)
        if any(syndrome):
            flip = _SYNDROME_TO_QUBIT[tuple(syndrome)]
            psi = _apply_pauli_string(psi, correction_gate, (flip,))
    return psi


_TARGET_CACHE: np.ndarray | None = None


def noiseless_target_state() -> np.ndarray:
    """The 7-qubit data state produced by the noiseless protocol."""

    global _TARGET_CACHE
    if _TARGET_CACHE is None:
        sim = ProtocolSimulator({}, np.random.default_rng(0))
        accepted, psi = sim.run()
        assert accepted, "noiseless protocol must accept"
        _TARGET_CACHE = psi
    return _TARGET_CACHE


def run_shot(p: float, rng: np.random.Generator) -> ShotResult:
    errors = sample_errors(p, rng)
    if not errors:
        return ShotResult(accepted=True, fidelity=1.0, had_error=False)
    sim = ProtocolSimulator(errors, rng)
    accepted, psi = sim.run()
    if not accepted:
        return ShotResult(accepted=False, fidelity=None, had_error=True)
    target = noiseless_target_state()
    fidelity = float(np.abs(np.vdot(target, psi)) ** 2)
    return ShotResult(accepted=True, fidelity=fidelity, had_error=True)


def run_point(p: float, shots: int, seed: int) -> dict[str, float | int]:
    """Monte Carlo estimate of acceptance rate and infidelity at one p."""

    rng = np.random.default_rng(seed)
    trigger_prob = 1.0 - (1.0 - p) ** len(LOCATIONS)
    n_error_shots = int(np.random.default_rng(seed + 1).binomial(shots, trigger_prob))
    accepted = shots - n_error_shots  # error-free shots always accept with F=1
    fidelity_sum = float(shots - n_error_shots)
    fidelity_sq_sum = float(shots - n_error_shots)
    for _ in range(n_error_shots):
        result = _run_error_shot(p, rng)
        if result.accepted:
            accepted += 1
            fidelity_sum += result.fidelity
            fidelity_sq_sum += result.fidelity**2
    acceptance = accepted / shots
    acceptance_se = float(np.sqrt(acceptance * (1.0 - acceptance) / shots))
    if accepted:
        fidelity = fidelity_sum / accepted
        variance = max(fidelity_sq_sum / accepted - fidelity**2, 0.0)
        fidelity_se = float(np.sqrt(variance / accepted))
    else:
        fidelity = float("nan")
        fidelity_se = float("nan")
    return {
        "p": p,
        "shots": shots,
        "error_shots": n_error_shots,
        "accepted": accepted,
        "acceptance_rate": acceptance,
        "acceptance_se": acceptance_se,
        "fidelity": fidelity,
        "infidelity": 1.0 - fidelity,
        "infidelity_se": fidelity_se,
        "locations": len(LOCATIONS),
    }


def _run_error_shot(p: float, rng: np.random.Generator) -> ShotResult:
    """A shot conditioned on having at least one triggered location."""

    while True:
        errors = sample_errors(p, rng)
        if errors:
            break
    sim = ProtocolSimulator(errors, rng)
    accepted, psi = sim.run()
    if not accepted:
        return ShotResult(accepted=False, fidelity=None, had_error=True)
    decoded = ideal_decode(psi, rng)
    target = noiseless_target_state()
    return ShotResult(True, float(np.abs(np.vdot(target, decoded)) ** 2), True)
