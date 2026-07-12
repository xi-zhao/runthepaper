from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "cases" / "catalog.json"


def load_catalog() -> list[dict[str, Any]]:
    payload = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported catalog schema")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("catalog must contain cases")
    return [item for item in cases if isinstance(item, dict)]


def render_cases_index(cases: list[dict[str, Any]]) -> str:
    lines = [
        "# Published Cases",
        "",
        "Every case provides a public overview, Chinese and English getting-started notes, runnable code, generated data and figures, and an explicit reproduction boundary.",
        "",
        "| Paper ID | Topic | Public status | Audit score |",
        "| --- | --- | --- | ---: |",
    ]
    for case in cases:
        paper_id = str(case["paper_id"])
        lines.append(
            f"| [`{paper_id}`](cases/{paper_id}/README.md) | {case['topic']} | "
            f"{case['status']} | {float(case['audit_score']):.2f} |"
        )
    lines.extend(
        [
            "",
            "The audit score records evidence strength at export time. It is not a visual-style rating, and it does not erase the limitation stated by each case.",
            "It is also not a cross-paper ranking or a publishing threshold: publication readiness comes from satisfying the public case contract and stating the remaining boundary honestly.",
            "",
        ]
    )
    return "\n".join(lines)


def render_case_readme(case: dict[str, Any], case_dir: Path) -> str:
    paper_id = str(case["paper_id"])
    figures = sorted((case_dir / "outputs" / "figures").glob("*.png"))
    lines = [
        f"# {paper_id}: {case['title']}",
        "",
        f"Paper: [{case['title']}]({case['paper_url']})",
        "",
        f"Public status: **{case['status']}**",
        "",
        f"Audit score at export: **{float(case['audit_score']):.2f}/100**",
        "",
        f"Similarity level: `{case['similarity_level']}`",
        "",
        str(case["summary"]),
        "",
        "## Start Here / 上手讲义",
        "",
        "- [中文上手讲义](note/reproduction-note.zh-CN.md)",
        "- [English getting-started note](note/reproduction-note.en.md)",
        "- [Bilingual note index](note/reproduction-note.md)",
        "- [Code and run commands](code/README.md)",
        "- [Machine-readable scorecard](outputs/checks/similarity_scorecard.json)",
        "- [Numerical methods](docs/NUMERICAL_METHODS.md)",
        "- [Lessons learned](docs/LESSONS_LEARNED.md)",
        "",
        "## Public Boundary",
        "",
        "This public case includes paper-derived code, generated data, generated figures, public validation checks, and explanatory notes. It does not redistribute the paper PDF, arXiv source archive, original figures, EPS paths, digitized source curves, source-derived point sets, or source-vs-generated composite panels.",
        "",
        f"Remaining limitation: {case['limitation']}",
        "",
        "Final-parameter rule: final public figures use the paper parameters when feasible. Any reduced-scale, subset, proxy, or blocked target must be labeled explicitly and cannot be presented as a complete reproduction.",
        "",
        "## Quick Run",
        "",
        "```bash",
        "python -m venv .venv",
        "source .venv/bin/activate",
        "pip install -r requirements.txt",
    ]
    extras = [str(item) for item in case.get("extra_dependencies", [])]
    if extras:
        lines.append("pip install " + " ".join(extras))
    lines.append(f"cd cases/{paper_id}/code")
    for script in case.get("run_scripts", []):
        lines.append(f"python scripts/{script}")
    lines.extend(["```", "", "## Generated Figures", ""])
    for figure in figures:
        label = figure.stem.replace("_", " ")
        lines.extend([f"![{label}](outputs/figures/{figure.name})", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_code_readme(case: dict[str, Any]) -> str:
    paper_id = str(case["paper_id"])
    extras = [str(item) for item in case.get("extra_dependencies", [])]
    lines = [
        f"# Runnable code for {paper_id}",
        "",
        "Run commands from the repository root unless a command below changes directory.",
        "",
        "```bash",
        "python -m venv .venv",
        "source .venv/bin/activate",
        "pip install -r requirements.txt",
    ]
    if extras:
        lines.append("pip install " + " ".join(extras))
    lines.extend([f"cd cases/{paper_id}/code"])
    for script in case.get("run_scripts", []):
        lines.append(f"python scripts/{script}")
    lines.extend(
        [
            "```",
            "",
            "Generated CSV files are written to `../outputs/data/`, figures to `../outputs/figures/`, and machine-readable checks to `../outputs/checks/`.",
            "",
            f"Boundary: {case['limitation']}",
            "",
        ]
    )
    return "\n".join(lines)


def render_note_index(case: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# {case['paper_id']} reproduction notes / 复现讲义",
            "",
            "请选择语言 / Choose a language:",
            "",
            "- [中文上手讲义](reproduction-note.zh-CN.md)",
            "- [English getting-started note](reproduction-note.en.md)",
            "",
            f"Case overview: [../README.md](../README.md)",
            "",
        ]
    )


def expected_files(cases: list[dict[str, Any]]) -> dict[Path, str]:
    rendered = {ROOT / "CASES.md": render_cases_index(cases)}
    for case in cases:
        case_dir = ROOT / "cases" / str(case["paper_id"])
        if not case_dir.exists():
            raise FileNotFoundError(case_dir)
        rendered[case_dir / "README.md"] = render_case_readme(case, case_dir)
        rendered[case_dir / "code" / "README.md"] = render_code_readme(case)
        rendered[case_dir / "note" / "reproduction-note.md"] = render_note_index(case)
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render public case navigation from the catalog.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if generated navigation is stale instead of rewriting it",
    )
    args = parser.parse_args()
    cases = load_catalog()
    stale: list[Path] = []
    for path, content in expected_files(cases).items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(path.relative_to(ROOT))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        for path in stale:
            print(f"stale generated file: {path}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
