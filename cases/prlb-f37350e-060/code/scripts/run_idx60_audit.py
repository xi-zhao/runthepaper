from __future__ import annotations

import json
import sys
from pathlib import Path


CASE_ROOT = Path(__file__).resolve().parents[2]
CODE_ROOT = CASE_ROOT / "code"
sys.path.insert(0, str(CODE_ROOT / "src"))

from fermionic_reference_audit import task_summary  # noqa: E402


def main() -> None:
    output = CASE_ROOT / "outputs" / "data" / "idx60_gold_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(task_summary(), indent=2, default=_json_default) + "\n")
    print(output)


def _json_default(value: object) -> object:
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    raise TypeError(f"cannot encode {type(value)!r}")


if __name__ == "__main__":
    main()
