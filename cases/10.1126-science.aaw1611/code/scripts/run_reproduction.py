#!/usr/bin/env python3
"""Run the public Science aaw1611 reproduction into the case output tree."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


CODE_ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = CODE_ROOT.parent
IMPLEMENTATION = Path(__file__).with_name("_run_paper_exact.py")


def main() -> int:
    arguments = list(sys.argv[1:])
    has_output_dir = any(
        argument == "--output-dir" or argument.startswith("--output-dir=")
        for argument in arguments
    )
    if not has_output_dir:
        arguments.extend(["--output-dir", str(CASE_ROOT / "outputs")])
    command = [sys.executable, str(IMPLEMENTATION), *arguments]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
