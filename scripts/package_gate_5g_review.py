#!/usr/bin/env python3
"""Create the bounded Gate 5G Draft 0.1 owner-review package."""

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

OUTPUT = ROOT / "deliverables/CCLL-draft-0-1-release-candidate-gate-5g-OWNER_REVIEW_REQUIRED.zip"
README = ROOT / "docs/reviews/gate-5g/README_OWNER_REVIEW.md"
ROOT_SITE = ROOT / "_site"
PROJECT_SITE = ROOT / "_site-project-path/CCL-Lab-Website"

BOUNDED_FILES = {
    Path("docs/baseline-gate-5g.md"): Path("review/baseline.md"),
    Path("docs/decisions/gate-5f-owner-approval.md"): Path("review/owner-decisions.md"),
    Path("docs/adr/0007-previous-work-curation-and-draft-release-boundary.md"): Path("review/adr-0007.md"),
    Path("docs/reviews/gate-5g/previous-work-owner-decision-table.md"): Path("review/previous-work-owner-decision-table.md"),
    Path("docs/reviews/gate-5g/previous-work-curation-audit.md"): Path("review/previous-work-curation-audit.md"),
    Path("docs/reviews/gate-5g/public-metadata-display-audit.md"): Path("review/public-metadata-display-audit.md"),
    Path("docs/reviews/gate-5g/placeholder-and-public-copy-audit.md"): Path("review/placeholder-and-public-copy-audit.md"),
    Path("docs/reviews/gate-5g/public-internal-language-audit.md"): Path("review/public-internal-language-audit.md"),
    Path("docs/runbooks/publish-draft-0-1-github-pages.md"): Path("review/runbook.md"),
    Path("reports/release/gate-5g-external-link-audit.md"): Path("review/release/external-link-audit.md"),
    Path("reports/release/gate-5g-base-path-audit.md"): Path("review/release/base-path-audit.md"),
    Path("reports/release/gate-5g-draft-0-1-hardening.md"): Path("review/release/draft-hardening.md"),
    Path("reports/browser-qa-gate-5g.md"): Path("review/browser-qa.md"),
    Path("reports/security/gate-5g-secret-scan.md"): Path("review/security/secret-scan.md"),
    Path("reports/file-by-file-summary-gate-5g.md"): Path("review/file-by-file-summary.md"),
    Path("reports/qa/gate-5g-final/validate.log"): Path("review/tests/validate.log"),
    Path("reports/qa/gate-5g-final/test.log"): Path("review/tests/test.log"),
    Path("reports/qa/gate-5g-final/build.log"): Path("review/tests/build.log"),
    Path("reports/qa/gate-5g-final/check.log"): Path("review/tests/check.log"),
    Path("reports/qa/gate-5g-final/release-check.log"): Path("review/tests/release-check.log"),
    Path(".github/workflows/public-draft-pages.yml"): Path("source/workflows/public-draft-pages.yml"),
    Path("_quarto-project-path.yml"): Path("source/_quarto-project-path.yml"),
    Path("config/site.yml"): Path("source/config/site.yml"),
    Path("config/theme_featured_examples.yml"): Path("source/config/theme_featured_examples.yml"),
    Path("config/publication_theme_examples.yml"): Path("source/config/publication_theme_examples.yml"),
    Path("config/vocabularies.yml"): Path("source/config/vocabularies.yml"),
    Path("schemas/theme-featured-examples.schema.json"): Path("source/schemas/theme-featured-examples.schema.json"),
}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def add_tree(files: list[tuple[Path, Path]], source_root: Path, archive_root: Path) -> None:
    for path in sorted(source_root.rglob("*")):
        if path.is_file():
            files.append((path, archive_root / path.relative_to(source_root)))


def included_files() -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = []
    add_tree(files, ROOT_SITE, Path("rendered-root"))
    add_tree(files, PROJECT_SITE, Path("rendered-project-path/CCL-Lab-Website"))
    add_tree(files, ROOT / "reports/screenshots/gate-5g", Path("review/screenshots/gate-5g"))
    for source, target in BOUNDED_FILES.items():
        if (ROOT / source).is_file():
            files.append((ROOT / source, target))
    return files


def package(output: Path = OUTPUT) -> Path:
    required = (README, ROOT_SITE / "index.html", PROJECT_SITE / "index.html")
    if not all(path.is_file() for path in required):
        raise FileNotFoundError("Gate 5G README and both rendered sites are required")
    files = included_files()
    manifest = [
        "Cities & Climate Learning Lab — Gate 5G Draft 0.1 owner review",
        f"Branch: {git('branch', '--show-current')}",
        f"Commit: {git('rev-parse', 'HEAD')}",
        f"Files: {len(files)}",
        "Deployment: none",
        "Pages/repository settings changed: none",
        "API/paid/model calls: none",
        "Current Conversations public feed: disabled",
        "Owner review required: yes",
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
        print(f"Unable to create Gate 5G owner-review package: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

