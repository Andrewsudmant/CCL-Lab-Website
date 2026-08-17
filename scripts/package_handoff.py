#!/usr/bin/env python3
"""Create a shareable, governance-focused project handoff ZIP."""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
import zipfile
from pathlib import Path

try:
    from .content import ROOT
except ImportError:  # Direct script execution.
    from content import ROOT

CONTEXT_FILES = [
    Path(".github/workflows/current-conversations-scheduled.yml"),
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/architecture.md"),
    Path("docs/content-governance.md"),
    Path("docs/security.md"),
    Path("docs/gate-0-1-scope.md"),
    Path("docs/gate-2-3a-scope.md"),
    Path("docs/gate-4b-5a-scope.md"),
    Path("docs/baseline-gate-4b-5a.md"),
    Path("docs/baseline-gate-3b-4a.md"),
    Path("docs/adr/0001-technical-foundations.md"),
    Path("docs/adr/0002-automated-research-watch-publication.md"),
    Path("docs/adr/0003-current-conversations-clusters.md"),
    Path("docs/migration-research-watch-to-current-conversations.md"),
    Path("docs/theme-content-audit.md"),
    Path("docs/theme-and-project-content-audit-gate-3b-4a.md"),
    Path("docs/publication-metadata-workflow.md"),
    Path("reports/content/publication-reconciliation.md"),
    Path("reports/pilot/gate-3b-4a-evaluation.md"),
    Path("reports/current-conversations/pilot/gate-4b-5a-evaluation.md"),
    Path("reports/current-conversations/cost-controls.md"),
    Path("reports/current-conversations/staging/gate-4b-5a-staging-report.md"),
    Path("reports/current-conversations/staging/rollback-demonstration.md"),
    Path("reports/file-by-file-summary-gate-4b-5a.md"),
    Path("config/research_scope.yml"),
    Path("config/vocabularies.yml"),
    Path("config/query_packs/current-conversations-v1.yml"),
    Path("config/source_registry.yml"),
    Path("current_conversations/budget.py"),
    Path("scripts/stage_current_conversations.py"),
]


def git_value(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def manifest(summary: Path, included: list[Path]) -> str:
    branch = git_value("branch", "--show-current")
    commit = git_value("rev-parse", "HEAD")
    status = git_value("status", "--short")
    lines = [
        "Cities & Climate Learning Lab handoff package",
        f"Created: {dt.date.today().isoformat()}",
        f"Branch: {branch}",
        f"Commit: {commit}",
        f"Summary source: {summary.as_posix()}",
        f"Working tree at packaging: {'clean' if not status else 'contains local handoff-related changes'}",
        "",
        "Included files:",
        "- 00_READ_ME_FIRST.md (the selected handoff summary)",
    ]
    lines.extend(f"- project-context/{path.as_posix()}" for path in included)
    lines.extend(
        [
            "- MANIFEST.txt",
            "",
            "Excluded by design:",
            "- secrets and environment files",
            "- build caches and the rendered _site directory",
            "- raw API, model or provider responses",
            "- private contact information",
            "",
        ]
    )
    return "\n".join(lines)


def package(summary_relative: Path, output: Path | None = None) -> Path:
    summary = (ROOT / summary_relative).resolve()
    try:
        summary.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError("Summary must be inside the repository") from exc
    if not summary.is_file():
        raise FileNotFoundError(f"Handoff summary not found: {summary_relative}")

    included = [path for path in CONTEXT_FILES if (ROOT / path).is_file()]
    destination = output or (
        ROOT
        / "deliverables"
        / f"CCLL-project-handoff-{dt.date.today().isoformat()}.zip"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(summary, "00_READ_ME_FIRST.md")
        for path in included:
            archive.write(ROOT / path, Path("project-context") / path)
        archive.writestr("MANIFEST.txt", manifest(summary_relative, included))
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        output = package(args.summary, args.output)
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Unable to create handoff package: {exc}", file=sys.stderr)
        return 1
    print(output.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
