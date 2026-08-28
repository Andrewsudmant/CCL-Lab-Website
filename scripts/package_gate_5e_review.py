#!/usr/bin/env python3
"""Create the bounded Gate 5E Draft 0.1 owner-review package."""

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

OUTPUT = ROOT / "deliverables/CCLL-draft-0-1-content-candidate-gate-5e-OWNER_REVIEW_REQUIRED.zip"
README = ROOT / "docs/reviews/gate-5e/README_OWNER_REVIEW.md"
BOUNDED_FILES = {
    Path("docs/reviews/gate-5e/theme-reader-value-audit.md"): Path("review/theme-reader-value-audit.md"),
    Path("docs/reviews/gate-5e/research-ideas-reader-value-audit.md"): Path("review/research-ideas-reader-value-audit.md"),
    Path("docs/reviews/gate-5e/current-conversations-development-state-audit.md"): Path("review/current-conversations-development-state-audit.md"),
    Path("docs/reviews/gate-5e/previous-work-examples-freeze-audit.md"): Path("review/previous-work-examples-freeze-audit.md"),
    Path("docs/reviews/gate-5e/draft-0-1-readiness.md"): Path("review/draft-0-1-readiness.md"),
    Path("docs/migrations/research-ideas-gate-5d-to-gate-5e.md"): Path("review/research-idea-migration.md"),
    Path("reports/qa/gate-5e-final/full-test.log"): Path("review/full-test.log"),
    Path("reports/browser-qa-gate-5e.md"): Path("review/browser-qa.md"),
    Path("reports/file-by-file-summary-gate-5e.md"): Path("review/file-by-file-summary.md"),
    Path("docs/baseline-gate-5e.md"): Path("review/baseline.md"),
    Path("schemas/research-theme.schema.json"): Path("source/schemas/research-theme.schema.json"),
    Path("schemas/research-idea.schema.json"): Path("source/schemas/research-idea.schema.json"),
    Path("schemas/site-config.schema.json"): Path("source/schemas/site-config.schema.json"),
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
    for path in sorted((ROOT / "reports/screenshots/gate-5e").rglob("*")):
        if path.is_file():
            files.append((path, Path("review/screenshots/gate-5e") / path.relative_to(ROOT / "reports/screenshots/gate-5e")))
    for source, target in BOUNDED_FILES.items():
        if (ROOT / source).is_file():
            files.append((ROOT / source, target))
    for path in sorted((ROOT / "data/research-ideas").glob("*.yml")):
        files.append((path, Path("source") / path.relative_to(ROOT)))
    return files


def package(output: Path = OUTPUT) -> Path:
    if not README.is_file() or not (ROOT / "_site/index.html").is_file():
        raise FileNotFoundError("Gate 5E README and rendered site are required")
    files = included_files()
    manifest = [
        "Cities & Climate Learning Lab — Gate 5E Draft 0.1 owner review",
        f"Branch: {git('branch', '--show-current')}", f"Commit: {git('rev-parse', 'HEAD')}",
        f"Files: {len(files)}", "Deployment: none", "Paid/model calls: none", "", "SHA-256  Archive path",
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
        print(f"Unable to create Gate 5E owner-review package: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
