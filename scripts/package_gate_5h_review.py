#!/usr/bin/env python3
"""Create the bounded Gate 5H voice/accessibility owner-review package."""

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

OUTPUT = ROOT / "deliverables/CCLL-human-cadence-plain-language-gate-5h-OWNER_REVIEW_REQUIRED.zip"
README = ROOT / "docs/reviews/gate-5h/README_OWNER_REVIEW.md"
ROOT_SITE = ROOT / "_site"
PROJECT_SITE = ROOT / "_site-project-path/CCL-Lab-Website"

BOUNDED = [
    "docs/baseline-gate-5h.md",
    "docs/decisions/gate-5h-human-cadence-and-accessibility.md",
    "docs/editorial/public-voice-and-plain-language.md",
    "docs/reviews/gate-5h/README.md",
    "docs/reviews/gate-5h/non-academic-reader-comprehension-audit.md",
    "docs/reviews/gate-5h/public-copy-before-and-after.md",
    "docs/reviews/gate-5h/work-page-type-mapping.md",
    "reports/editorial/gate-5h-public-voice-diagnostic.md",
    "reports/browser-qa-gate-5h.md",
    "reports/accessibility/gate-5h-accessibility.md",
    "reports/security/gate-5h-secret-scan.md",
    "reports/file-by-file-summary-gate-5h.md",
    "config/plain_language_terms.yml",
    "config/public_voice_allowlist.yml",
    "schemas/plain-language-terms.schema.json",
    "tests/test_gate_5h_public_voice.py",
]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def digest(path: Path) -> str:
    value = hashlib.sha256(); value.update(path.read_bytes()); return value.hexdigest()


def add_tree(files: list[tuple[Path, Path]], source: Path, target: Path) -> None:
    for path in sorted(source.rglob("*")):
        if path.is_file(): files.append((path, target / path.relative_to(source)))


def package(output: Path = OUTPUT) -> Path:
    required = [README, ROOT_SITE / "index.html", PROJECT_SITE / "index.html"]
    required += [ROOT / item for item in BOUNDED]
    missing = [p for p in required if not p.is_file()]
    if missing: raise FileNotFoundError("missing Gate 5H review files: " + ", ".join(str(p.relative_to(ROOT)) for p in missing))
    files: list[tuple[Path, Path]] = []
    add_tree(files, ROOT_SITE, Path("rendered-root"))
    add_tree(files, PROJECT_SITE, Path("rendered-project-path/CCL-Lab-Website"))
    add_tree(files, ROOT / "reports/screenshots/gate-5h", Path("review/screenshots/gate-5h"))
    files += [(ROOT / p, Path("review") / p) for p in map(Path, BOUNDED)]
    manifest = [
        "Cities & Climate Learning Lab — Gate 5H owner review",
        f"Branch: {git('branch', '--show-current')}", f"Commit: {git('rev-parse', 'HEAD')}",
        "Deployment: none", "Current Conversations: in development; no public feed", "Owner review required: yes", "", "SHA-256  Archive path",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(README, "00_READ_ME_FIRST.md")
        for source, target in files:
            archive.write(source, target); manifest.append(f"{digest(source)}  {target.as_posix()}")
        archive.writestr("MANIFEST.txt", "\n".join(manifest) + "\n")
    return output


def main() -> int:
    try: print(package().resolve())
    except (FileNotFoundError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Unable to create Gate 5H package: {exc}", file=sys.stderr); return 1
    return 0


if __name__ == "__main__": raise SystemExit(main())
