#!/usr/bin/env python3
"""Create the bounded thematic-architecture owner-review bundle."""

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

BASE_COMMIT = "8be464c482c292513188101472dea8ec05692259"
REVIEW_ROOT = Path("docs/reviews/thematic-architecture-reframe-v1")
README = REVIEW_ROOT / "README_OWNER_REVIEW.md"
OUTPUT = ROOT / "deliverables/CCLL_thematic_architecture_reframe_v1_OWNER_REVIEW_REQUIRED.zip"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def changed_paths() -> list[Path]:
    lines = git("diff", "--name-status", f"{BASE_COMMIT}..HEAD").splitlines()
    paths: list[Path] = []
    for line in lines:
        parts = line.split("\t")
        candidate = parts[-1]
        path = Path(candidate)
        if (ROOT / path).is_file() and not candidate.startswith(("deliverables/", "_site/")):
            paths.append(path)
    return sorted(set(paths))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def package() -> Path:
    branch = git("branch", "--show-current")
    commit = git("rev-parse", "HEAD")
    status = git("status", "--short")
    changed = changed_paths()
    ending = "\n".join(
        [
            "# Ending Git state",
            "",
            f"- Repository: `{ROOT}`",
            f"- Branch: `{branch}`",
            f"- Commit: `{commit}`",
            f"- Status at packaging: {'clean' if not status else 'local package-related changes present'}",
            f"- Base commit retained: `{BASE_COMMIT}`",
            "- No merge, deployment, force-push or history rewrite performed.",
            "",
        ]
    )
    changes = "# Changed-file manifest\n\n" + "\n".join(
        f"- `{path.as_posix()}`" for path in changed
    ) + "\n"
    manifest = [
        "Cities and Climate Learning Lab thematic architecture reframe v1",
        f"Branch: {branch}",
        f"Commit: {commit}",
        f"Base: {BASE_COMMIT}",
        f"Files: {len(changed)}",
        "",
        "SHA-256  Archive path",
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(ROOT / README, "README_OWNER_REVIEW.md")
        archive.writestr("review/STARTING_GIT_STATE.md", (ROOT / REVIEW_ROOT / "starting-git-state.md").read_text(encoding="utf-8"))
        archive.writestr("review/ENDING_GIT_STATE.md", ending)
        archive.writestr("review/CHANGED_FILES.md", changes)
        for path in changed:
            target = Path("changed-source") / path
            archive.write(ROOT / path, target)
            manifest.append(f"{digest(ROOT / path)}  {target.as_posix()}")
        archive.writestr("MANIFEST.txt", "\n".join(manifest) + "\n")
    return OUTPUT


def main() -> int:
    try:
        print(package().resolve())
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Unable to create thematic owner-review package: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
