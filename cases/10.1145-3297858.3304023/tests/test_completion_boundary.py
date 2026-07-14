from __future__ import annotations

import csv
import json
from pathlib import Path
import unittest


CASE_ROOT = Path(__file__).resolve().parents[1]


class CompletionBoundaryTests(unittest.TestCase):
    def load_json(self, relative_path: str) -> dict:
        return json.loads((CASE_ROOT / relative_path).read_text(encoding="utf-8"))

    def test_full_table2_corpus_is_present_and_compliant(self) -> None:
        reproduction = self.load_json("outputs/checks/table2_reproduction.json")
        with (CASE_ROOT / "outputs/data/table2_reproduction.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = list(csv.DictReader(handle))

        self.assertEqual(26, len(rows))
        self.assertEqual(26, reproduction["rows_ran"])
        self.assertEqual(26, reproduction["qasm_g_ori_matches"])
        self.assertEqual(26, reproduction["hardware_compliant_rows"])
        self.assertTrue(all(row["status"] == "ran" for row in rows))
        self.assertTrue(all(row["all_compliant"] == "True" for row in rows))

    def test_residual_is_metadata_not_compute_boundary(self) -> None:
        sensitivity = self.load_json("outputs/checks/table2_seed_sensitivity.json")
        assessment = self.load_json("outputs/checks/completion_assessment.json")

        self.assertEqual(
            {"exact": 7, "seed_explainable": 13, "ours_better": 6},
            sensitivity["verdict_counts"],
        )
        self.assertEqual("missing_benchmark_metadata", sensitivity["boundary"]["kind"])
        self.assertEqual("stop_without_row_exact_metadata", assessment["decision"])
        self.assertFalse(assessment["compute_assessment"]["additional_large_campaign_needed"])

    def test_completion_evidence_exists(self) -> None:
        assessment = self.load_json("outputs/checks/completion_assessment.json")
        for relative_path in assessment["evidence"]:
            self.assertTrue((CASE_ROOT / relative_path).exists(), relative_path)


if __name__ == "__main__":
    unittest.main()
