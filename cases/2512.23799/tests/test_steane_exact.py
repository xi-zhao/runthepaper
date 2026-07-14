from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_ROOT / "code/src"))

import steane_h_prep as sim  # noqa: E402


def pauli_string(psi: np.ndarray, gate: np.ndarray, qubits: tuple[int, ...]) -> float:
    state = psi.reshape((2,) * 7)
    for qubit in qubits:
        state = np.moveaxis(
            np.tensordot(gate, np.moveaxis(state, qubit, 0), axes=1), 0, qubit
        )
    return float(np.real(np.vdot(psi, state.reshape(-1))))


class SteaneExactProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sim.set_protocol_config("asap", "active_window", "explicit_no_idle")
        cls.target = sim.noiseless_target_state()

    def test_noiseless_protocol_accepts(self) -> None:
        accepted, state = sim.ProtocolSimulator({}, np.random.default_rng(5)).run()
        self.assertTrue(accepted)
        self.assertAlmostEqual(1.0, abs(np.vdot(self.target, state)) ** 2, places=10)

    def test_encoded_state_is_logical_h_eigenstate(self) -> None:
        state = self.target.reshape((2,) * 7)
        for qubit in range(7):
            state = np.moveaxis(
                np.tensordot(sim.H_GATE, np.moveaxis(state, qubit, 0), axes=1),
                0,
                qubit,
            )
        overlap = float(np.real(np.vdot(self.target, state.reshape(-1))))
        self.assertAlmostEqual(1.0, overlap, places=9)

    def test_encoded_state_passes_all_six_stabilizers(self) -> None:
        for gate in (sim.X_GATE, sim.Z_GATE):
            for support in sim.STABILIZER_SUPPORTS:
                qubits = tuple(qubit - 1 for qubit in support)
                self.assertAlmostEqual(
                    1.0, pauli_string(self.target, gate, qubits), places=9
                )

    def test_stabilizer_supports_form_hamming_check(self) -> None:
        vectors = {
            tuple(1 if qubit in support else 0 for support in sim.STABILIZER_SUPPORTS)
            for qubit in range(1, 8)
        }
        self.assertEqual(7, len(vectors))
        self.assertNotIn((0, 0, 0), vectors)

    def test_ideal_decoder_corrects_each_single_qubit_pauli(self) -> None:
        rng = np.random.default_rng(11)
        for gate in (sim.X_GATE, sim.Y_GATE, sim.Z_GATE):
            for qubit in range(7):
                state = self.target.reshape((2,) * 7)
                state = np.moveaxis(
                    np.tensordot(gate, np.moveaxis(state, qubit, 0), axes=1),
                    0,
                    qubit,
                ).reshape(-1)
                decoded = sim.ideal_decode(state, rng)
                fidelity = float(abs(np.vdot(self.target, decoded)) ** 2)
                self.assertAlmostEqual(1.0, fidelity, places=9)

    def test_location_table_matches_published_artifact(self) -> None:
        counts: dict[str, int] = {}
        for location in sim.LOCATIONS:
            counts[location[0]] = counts.get(location[0], 0) + 1
        self.assertEqual(15, counts["init"])
        self.assertEqual(8, counts["meas"])
        self.assertEqual(48, counts["dep2"])
        self.assertEqual(200, len(sim.LOCATIONS))

    def test_public_benchmark_declares_residual(self) -> None:
        checks = json.loads(
            (CASE_ROOT / "outputs/checks/steane_exact_benchmark.json").read_text()
        )
        self.assertEqual(12, checks["validation_summary"]["acceptance_points_passed"])
        self.assertTrue(checks["validation_summary"]["infidelity_edges_match"])
        self.assertEqual(
            "not_claimed_as_reproduced", checks["known_residual"]["status"]
        )


if __name__ == "__main__":
    unittest.main()
