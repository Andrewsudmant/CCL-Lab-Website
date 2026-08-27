#!/usr/bin/env python3
"""Create the bounded Gate 5D owner-review package."""

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

OUTPUT = ROOT / "deliverables/CCLL-research-work-architecture-gate-5d-OWNER_REVIEW_REQUIRED.zip"
README = ROOT / "docs/reviews/gate-5d/README_OWNER_REVIEW.md"
BOUNDED_FILES = {
    Path("docs/reviews/gate-5d/research-work-architecture-audit.md"): Path("review/gate-5d/research-work-architecture-audit.md"),
    Path("docs/reviews/gate-5d/theme-description-audit.md"): Path("review/gate-5d/theme-description-audit.md"),
    Path("docs/reviews/gate-5d/research-ideas-audit.md"): Path("review/gate-5d/research-ideas-audit.md"),
    Path("reports/content/theme-examples-audit-gate-5d.md"): Path("review/content/theme-examples-audit-gate-5d.md"),
    Path("reports/content/standalone-publications-audit-gate-5d.md"): Path("review/content/standalone-publications-audit-gate-5d.md"),
    Path("docs/migrations/project-to-research-work-gate-5d.md"): Path("review/migration.md"),
    Path("reports/qa/gate-5d-final/full-test.log"): Path("review/full-test.log"),
    Path("reports/browser-qa-gate-5d.md"): Path("review/browser-qa.md"),
    Path("reports/file-by-file-summary-gate-5d.md"): Path("review/file-by-file-summary.md"),
    Path("docs/baseline-gate-5d.md"): Path("review/baseline.md"),
    Path("schemas/research-theme.schema.json"): Path("source/schemas/research-theme.schema.json"),
    Path("schemas/research-work.schema.json"): Path("source/schemas/research-work.schema.json"),
    Path("schemas/research-idea.schema.json"): Path("source/schemas/research-idea.schema.json"),
    Path("schemas/publication.schema.json"): Path("source/schemas/publication.schema.json"),
    Path("config/research_scope.yml"): Path("source/config/research_scope.yml"),
    Path("config/publication_theme_examples.yml"): Path("source/config/publication_theme_examples.yml"),
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
    for path in sorted((ROOT / "reports/screenshots/gate-5d").rglob("*")):
        if path.is_file():
            files.append((path, Path("review/screenshots/gate-5d") / path.relative_to(ROOT / "reports/screenshots/gate-5d")))
    for source, target in BOUNDED_FILES.items():
        if (ROOT / source).is_file():
            files.append((ROOT / source, target))
    for directory in ("data/work", "data/research-ideas"):
        for path in sorted((ROOT / directory).glob("*.yml")):
            files.append((path, Path("source") / path.relative_to(ROOT)))
    return files


def package(output: Path = OUTPUT) -> Path:
    if not README.is_file() or not (ROOT / "_site/index.html").is_file():
        raise FileNotFoundError("Gate 5D README and rendered site are required")
    files = included_files()
    manifest = [
        "Cities & Climate Learning Lab — Gate 5D owner review",
        f"Branch: {git('branch', '--show-current')}",
        f"Commit: {git('rev-parse', 'HEAD')}",
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
        print(f"Unable to create Gate 5D owner-review package: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
