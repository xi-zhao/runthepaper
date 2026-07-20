#!/usr/bin/env python3
"""Run public-safe reduced-scale checks for the case's two core mechanisms."""

from __future__ import annotations

from pathlib import Path
import sys


CODE_ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = CODE_ROOT.parent
sys.path.insert(0, str(CODE_ROOT))

from scripts import run_fig2_geometry, run_fig4_boundary_ratio  # noqa: E402


def _run(module: object, arguments: list[str]) -> int:
    previous_argv = sys.argv
    previous_root = module.WORKSPACE
    try:
        module.WORKSPACE = CASE_ROOT
        sys.argv = [str(Path(module.__file__).name), *arguments]
        return int(module.main())
    finally:
        sys.argv = previous_argv
        module.WORKSPACE = previous_root


def main() -> int:
    fig2_status = _run(run_fig2_geometry, ["--scale", "smoke"])
    fig4_status = _run(run_fig4_boundary_ratio, ["--scale", "smoke"])
    return 0 if fig2_status == 0 and fig4_status == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
