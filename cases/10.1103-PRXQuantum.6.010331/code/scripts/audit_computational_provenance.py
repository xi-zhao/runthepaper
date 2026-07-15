#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CODE_ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = CODE_ROOT.parent if CODE_ROOT.name == "code" else CODE_ROOT
sys.path.insert(0, str(CODE_ROOT))

from src.provenance_audit import audit_computational_provenance  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify that paper-figure pixels never enter numerical calculations."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=CASE_ROOT / "outputs" / "checks" / "computational_provenance_audit.json",
    )
    args = parser.parse_args()

    result = audit_computational_provenance(CASE_ROOT)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
