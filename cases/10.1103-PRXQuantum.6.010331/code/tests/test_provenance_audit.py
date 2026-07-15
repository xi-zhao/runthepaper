from __future__ import annotations

import sys
from pathlib import Path


CODE_ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = CODE_ROOT.parent if CODE_ROOT.name == "code" else CODE_ROOT
sys.path.insert(0, str(CODE_ROOT))

from src.provenance_audit import audit_computational_provenance  # noqa: E402


def test_source_figure_pixels_are_comparison_only() -> None:
    result = audit_computational_provenance(CASE_ROOT)
    assert result["status"] == "passed"
    assert result["source_figure_data_used_as_computational_input"] is False
    assert result["forbidden_findings"] == []
    assert result["comparison_only_image_reads"] == []
