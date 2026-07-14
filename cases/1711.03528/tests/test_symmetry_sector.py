from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

import numpy as np


CASE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_ROOT / "code/src"))

from pxp_scars import (  # noqa: E402
    build_basis,
    build_hamiltonian,
    build_symmetric_hamiltonian,
    build_symmetric_sector,
    mean_level_spacing_ratio,
    pattern_state,
    symmetrized_state_vector,
)


class SymmetrySectorTests(unittest.TestCase):
    def test_sector_spectrum_is_contained_in_full_spectrum(self) -> None:
        for system_size in (8, 10, 12):
            sector = build_symmetric_sector(system_size)
            sector_energies = np.linalg.eigvalsh(build_symmetric_hamiltonian(sector).toarray())
            full_energies = np.linalg.eigvalsh(build_hamiltonian(build_basis(system_size)).toarray())
            for energy in sector_energies:
                self.assertLess(float(np.min(np.abs(full_energies - energy))), 1e-9)

    def test_sector_hamiltonian_is_symmetric(self) -> None:
        sector = build_symmetric_sector(12)
        matrix = build_symmetric_hamiltonian(sector).toarray()
        self.assertTrue(np.allclose(matrix, matrix.T))

    def test_z2_state_projects_to_a_single_sector_basis_state(self) -> None:
        sector = build_symmetric_sector(12)
        vector = symmetrized_state_vector(sector, pattern_state(12, "z2"))
        self.assertAlmostEqual(1.0, float(np.sum(vector**2)))
        self.assertEqual(1, int(np.count_nonzero(vector)))

    def test_gap_ratio_reference_behaviour(self) -> None:
        rng = np.random.default_rng(3)
        poisson_levels = np.cumsum(rng.exponential(size=20000))
        self.assertAlmostEqual(0.386, mean_level_spacing_ratio(poisson_levels), delta=0.01)

    def test_published_sector_check_passes(self) -> None:
        checks = json.loads(
            (CASE_ROOT / "outputs/checks/symmetry_resolved_sector.json").read_text()
        )
        self.assertEqual("physically_consistent", checks["status"])
        self.assertTrue(all(checks["gate_flags"].values()))
        self.assertEqual(
            {"L": 28, "momentum": 0, "inversion": "+1", "dimension": 13201},
            checks["sector"],
        )
        self.assertEqual(15, checks["scar_tower"]["expected_states"])
        self.assertEqual("external_required", checks["remote_rerun"]["constraint_class"])


if __name__ == "__main__":
    unittest.main()
