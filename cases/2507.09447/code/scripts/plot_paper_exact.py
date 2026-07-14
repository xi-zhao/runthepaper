#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


CASE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CASE_ROOT / "code" / "src"))

from paper_exact_plot import plot_paper_exact  # noqa: E402


def main() -> None:
    print(json.dumps(plot_paper_exact(CASE_ROOT), indent=2))


if __name__ == "__main__":
    main()
