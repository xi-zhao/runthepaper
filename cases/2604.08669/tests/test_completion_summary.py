from __future__ import annotations

import csv
import json
from pathlib import Path
import unittest


CASE_ROOT = Path(__file__).resolve().parents[1]


class CompletionSummaryTests(unittest.TestCase):
    def test_a100_csv_matches_campaign_summary(self) -> None:
        with (CASE_ROOT / "outputs/data/fig3_a100_paper_geometry_summary.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = {row["metric"]: row for row in csv.DictReader(handle)}
        campaign = json.loads(
            (CASE_ROOT / "outputs/checks/a100_paper_geometry_campaign.json").read_text()
        )
        probe = campaign["best_validation_probe"]
        self.assertEqual("NVIDIA A100-SXM4-80GB", campaign["platform"]["gpu"])
        self.assertEqual(64, probe["validation_instances"])
        self.assertAlmostEqual(
            probe["mean_predicted_average_distance"],
            float(rows["mean_average_distance"]["reproduced_value"]),
        )
        self.assertAlmostEqual(
            probe["mean_predicted_max_distance"],
            float(rows["mean_max_distance"]["reproduced_value"]),
        )
        self.assertFalse(probe["strict_paper_metric_gate_passed"])

    def test_p2wgs_boundary_is_honest(self) -> None:
        checks = json.loads(
            (CASE_ROOT / "outputs/checks/p2wgs_paper_scale.json").read_text()
        )
        self.assertEqual(10201, checks["parameters"]["N"])
        self.assertEqual(1024, checks["parameters"]["grid"])
        self.assertTrue(checks["gate_flags"]["phase_tightly_constrained_all_iterations"])
        self.assertFalse(checks["gate_flags"]["intensity_3_to_5_improvement_resolved"])

    def test_missing_targets_are_not_counted_as_complete(self) -> None:
        assessment = json.loads(
            (CASE_ROOT / "outputs/checks/completion_assessment.json").read_text()
        )
        self.assertEqual(
            "stop_without_long_training_or_gpu_decoder_reimplementation",
            assessment["decision"],
        )
        classifications = {
            item["classification"] for item in assessment["remaining_scope"]
        }
        self.assertIn("compute_limited_and_metric_gate_blocked", classifications)
        self.assertIn("implementation_unavailable_and_hardware_specific", classifications)
        self.assertFalse(assessment["proxy_substitution_used_for_missing_scope"])
        for relative_path in assessment["evidence"]:
            self.assertTrue((CASE_ROOT / relative_path).exists(), relative_path)


if __name__ == "__main__":
    unittest.main()
