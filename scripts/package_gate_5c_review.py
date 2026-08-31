#!/usr/bin/env python3
"""Create the bounded Gate 5C owner-review package."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

try:
    from .content import ROOT
except ImportError:
    from content import ROOT

OUTPUT = ROOT / "deliverables/CCLL-thematic-consistency-gate-5c-OWNER_REVIEW_REQUIRED.zip"
README = ROOT / "docs/reviews/gate-5c/README_OWNER_REVIEW.md"
REVIEW_FILES = {
    Path("docs/reviews/gate-5c/thematic-consistency-audit.md"): Path("review/gate-5c/thematic-consistency-audit.md"),
    Path("docs/reviews/gate-5c/project-learning-fields-audit.md"): Path("review/gate-5c/project-learning-fields-audit.md"),
    Path("docs/reviews/gate-5c/project-mapping-table.md"): Path("review/gate-5c/project-mapping-table.md"),
    Path("docs/migrations/current-conversations-four-theme-query-alignment.md"): Path("review/query-migration.md"),
    Path("reports/current-conversations/openalex-four-theme-diagnostics-gate-5c.md"): Path("review/openalex-diagnostics.md"),
    Path("reports/qa/gate-5c-final/full-test.log"): Path("review/full-test.log"),
    Path("reports/browser-qa-gate-5c.md"): Path("review/browser-qa.md"),
    Path("reports/stale-string-audit-gate-5c.md"): Path("review/stale-string-audit.md"),
    Path("reports/file-by-file-summary-gate-5c.md"): Path("review/file-by-file-summary.md"),
    Path("reports/git/gate-5c-remote-transfer.md"): Path("review/git-state-and-remote-transfer.md"),
}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def included_files() -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = []
    for path in sorted((ROOT / "_site").rglob("*")):
        if path.is_file():
            files.append((path, Path("rendered-site") / path.relative_to(ROOT / "_site")))
    for path in sorted((ROOT / "reports/screenshots/gate-5c").rglob("*")):
        if path.is_file():
            files.append((path, Path("review/screenshots/gate-5c") / path.relative_to(ROOT / "reports/screenshots/gate-5c")))
    for source, target in REVIEW_FILES.items():
        path = ROOT / source
        if path.is_file():
            files.append((path, target))
    return files


def package(output: Path = OUTPUT) -> Path:
    if not README.is_file() or not (ROOT / "_site/index.html").is_file():
        raise FileNotFoundError("Gate 5C README and rendered site are required")
    files = included_files()
    branch = git("branch", "--show-current")
    commit = git("rev-parse", "HEAD")
    manifest = [
        "Cities & Climate Learning Lab — Gate 5C owner review",
        f"Branch: {branch}",
        f"Commit: {commit}",
        f"Files: {len(files)}",
        "Deployment: none",
        "Paid/model calls: none",
        "",
        "SHA-256  Archive path",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(README, "00_READ_ME_FIRST.md")
        for source, target in files:
            archive.write(source, target)
            manifest.append(f"{digest(source)}  {target.as_posix()}")
        archive.writestr("MANIFEST.txt", "\n".join(manifest) + "\n")
    return output


def main() -> int:
    try:
        print(package().resolve())
    except (FileNotFoundError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Unable to create Gate 5C owner-review package: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
