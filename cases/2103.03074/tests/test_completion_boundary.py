from __future__ import annotations

import csv
import json
from pathlib import Path
import unittest


CASE_ROOT = Path(__file__).resolve().parents[1]


class CompletionBoundaryTests(unittest.TestCase):
    def test_reported_a100_boundary_matches_table(self) -> None:
        with (CASE_ROOT / "outputs/data/table2_method_comparison_arxiv.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = {row["method"]: row for row in csv.DictReader(handle)}
        assessment = json.loads(
            (CASE_ROOT / "outputs/checks/completion_assessment.json").read_text()
        )
        self.assertEqual("149 days", rows["Ours"]["computational_time"])
        self.assertEqual("One A100 GPU", rows["Ours"]["hardware"])
        self.assertEqual(
            149,
            assessment["completed_scope"]["reported_table_checks"]["reported_single_a100_time_days"],
        )
        self.assertFalse(
            assessment["resource_assessment"]["single_a100_run_acceptable_under_current_policy"]
        )

    def test_direct_statevector_boundary_is_128_pib(self) -> None:
        assessment = json.loads(
            (CASE_ROOT / "outputs/checks/completion_assessment.json").read_text()
        )
        expected_bytes = 2**53 * 16
        self.assertEqual(
            expected_bytes,
            assessment["resource_assessment"]["direct_statevector_complex128_bytes"],
        )
        self.assertEqual(128, expected_bytes / 2**50)

    def test_missing_scope_is_not_counted_as_complete(self) -> None:
        assessment = json.loads(
            (CASE_ROOT / "outputs/checks/completion_assessment.json").read_text()
        )
        self.assertEqual("stop_without_53_qubit_contraction", assessment["decision"])
        self.assertFalse(assessment["proxy_substitution_used_for_missing_scope"])
        for relative_path in assessment["evidence"]:
            self.assertTrue((CASE_ROOT / relative_path).exists(), relative_path)


if __name__ == "__main__":
    unittest.main()
