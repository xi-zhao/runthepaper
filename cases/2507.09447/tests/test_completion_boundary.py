from __future__ import annotations

import json
from pathlib import Path
import unittest


CASE_ROOT = Path(__file__).resolve().parents[1]


class CompletionBoundaryTests(unittest.TestCase):
    def load_json(self, relative_path: str) -> dict:
        return json.loads((CASE_ROOT / relative_path).read_text(encoding="utf-8"))

    def test_paper_scale_campaign_is_complete(self) -> None:
        config = self.load_json("code/config/paper_exact_run.json")
        ed = self.load_json("outputs/checks/paper_ed_generation.json")
        scientific = self.load_json("outputs/checks/paper_scientific_similarity.json")

        self.assertEqual(1000, config["fig3_fig4"]["diagonalization_length"])
        self.assertEqual(3200, config["fig3_fig4"]["disorder_realizations"])
        self.assertEqual(3200, ed["completed_realizations"])
        self.assertEqual(3200, ed["target_realizations"])
        self.assertTrue(all(scientific["gate_flags"].values()))
        self.assertEqual(2.1, scientific["fig5_metrics"]["estimated_Wc_alpha_ge_0_98"])

    def test_remaining_gap_is_not_compute_limited(self) -> None:
        assessment = self.load_json("outputs/checks/completion_assessment.json")
        self.assertEqual("stop_without_author_protocol_metadata", assessment["decision"])
        self.assertFalse(assessment["compute_assessment"]["additional_large_campaign_needed"])
        self.assertEqual(
            {"missing_author_protocol_metadata", "missing_author_artwork"},
            {item["classification"] for item in assessment["remaining_scope"]},
        )

    def test_completion_evidence_and_figure_reasons_exist(self) -> None:
        assessment = self.load_json("outputs/checks/completion_assessment.json")
        self.assertEqual({"fig3", "fig4", "fig5"}, set(assessment["difference_reasons_for_figures"]))
        for relative_path in assessment["evidence"]:
            self.assertTrue((CASE_ROOT / relative_path).exists(), relative_path)


if __name__ == "__main__":
    unittest.main()
