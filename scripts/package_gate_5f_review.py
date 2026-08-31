#!/usr/bin/env python3
"""Create the bounded Gate 5F owner-review package."""

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

OUTPUT = ROOT / "deliverables/CCLL-mcenerney-reader-value-gate-5f-OWNER_REVIEW_REQUIRED.zip"
README = ROOT / "docs/reviews/gate-5f/README_OWNER_REVIEW.md"
BOUNDED_FILES = {
    Path("docs/baseline-gate-5f.md"): Path("review/baseline.md"),
    Path("docs/editorial/site-level-reader-value.md"): Path("review/site-level-reader-value.md"),
    Path("docs/adr/0006-site-level-reader-value-and-public-scaffolding.md"): Path("review/adr-0006.md"),
    Path("docs/reviews/gate-5f/homepage-reader-value-audit.md"): Path("review/homepage-reader-value-audit.md"),
    Path("docs/reviews/gate-5f/theme-public-scaffolding-audit.md"): Path("review/theme-public-scaffolding-audit.md"),
    Path("docs/reviews/gate-5f/research-idea-display-audit.md"): Path("review/research-idea-display-audit.md"),
    Path("docs/reviews/gate-5f/work-page-reader-value-audit.md"): Path("review/work-page-reader-value-audit.md"),
    Path("docs/reviews/gate-5f/our-approach-and-illustration-audit.md"): Path("review/our-approach-and-illustration-audit.md"),
    Path("docs/reviews/gate-5f/current-conversations-reader-problem-audit.md"): Path("review/current-conversations-reader-problem-audit.md"),
    Path("docs/reviews/gate-5f/previous-work-reader-value-proposal.md"): Path("review/PRIVATE_NOT_IMPLEMENTED-previous-work-reader-value-proposal.md"),
    Path("reports/browser-qa-gate-5f.md"): Path("review/browser-qa.md"),
    Path("reports/security/gate-5f-secret-scan.md"): Path("review/security/secret-scan.md"),
    Path("reports/file-by-file-summary-gate-5f.md"): Path("review/file-by-file-summary.md"),
    Path("reports/qa/gate-5f-final/validate.log"): Path("review/tests/validate.log"),
    Path("reports/qa/gate-5f-final/test.log"): Path("review/tests/test.log"),
    Path("reports/qa/gate-5f-final/build.log"): Path("review/tests/build.log"),
    Path("reports/qa/gate-5f-final/check.log"): Path("review/tests/check.log"),
    Path("reports/qa/gate-5f-final/accessibility.log"): Path("review/tests/accessibility.log"),
    Path("schemas/research-idea.schema.json"): Path("source/schemas/research-idea.schema.json"),
    Path("schemas/research-work.schema.json"): Path("source/schemas/research-work.schema.json"),
    Path("config/research_scope.yml"): Path("source/config/research_scope.yml"),
    Path("config/site.yml"): Path("source/config/site.yml"),
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
    for path in sorted((ROOT / "reports/screenshots/gate-5f").rglob("*")):
        if path.is_file():
            files.append((path, Path("review/screenshots/gate-5f") / path.relative_to(ROOT / "reports/screenshots/gate-5f")))
    for source, target in BOUNDED_FILES.items():
        if (ROOT / source).is_file():
            files.append((ROOT / source, target))
    for folder in ("data/research-ideas", "data/work"):
        for path in sorted((ROOT / folder).glob("*.yml")):
            files.append((path, Path("source") / path.relative_to(ROOT)))
    return files


def package(output: Path = OUTPUT) -> Path:
    if not README.is_file() or not (ROOT / "_site/index.html").is_file():
        raise FileNotFoundError("Gate 5F README and rendered site are required")
    files = included_files()
    manifest = [
        "Cities & Climate Learning Lab — Gate 5F owner review",
        f"Branch: {git('branch', '--show-current')}",
        f"Commit: {git('rev-parse', 'HEAD')}",
        f"Files: {len(files)}",
        "Deployment: none",
        "API/paid/model calls: none",
        "Previous-work proposal: private and not implemented",
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
        print(f"Unable to create Gate 5F owner-review package: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
