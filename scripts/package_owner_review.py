#!/usr/bin/env python3
"""Package the complete Gate 4B–5A private review candidate with checksums."""

from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

try:
    from .content import ROOT
except ImportError:
    from content import ROOT


def tracked_files() -> list[Path]:
    result = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, check=True, capture_output=True, text=True)
    return [Path(line) for line in result.stdout.splitlines() if line and not line.startswith("deliverables/")]


def included_files() -> list[tuple[Path, Path]]:
    files = [(ROOT / path, Path("source") / path) for path in tracked_files() if (ROOT / path).is_file()]
    for relative_root, archive_root in ((Path("_site"), Path("rendered-site")), (Path("reports/screenshots"), Path("review/screenshots")), (Path("reports/qa"), Path("review/qa")), (Path("reports/content"), Path("review/content")), (Path("reports/current-conversations"), Path("review/current-conversations")), (Path("staging/current-conversations"), Path("review/private-staging")), (Path("calibration/current-conversations"), Path("review/calibration"))):
        root = ROOT / relative_root
        if root.exists():
            files.extend((path, archive_root / path.relative_to(root)) for path in sorted(root.rglob("*")) if path.is_file())
    unique: dict[str, tuple[Path, Path]] = {}
    for source, archive in files:
        unique[archive.as_posix()] = (source, archive)
    return [unique[key] for key in sorted(unique)]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package(output: Path | None = None) -> Path:
    destination = output or ROOT / "deliverables" / f"CCLL-owner-review-gate-4b-5a-{dt.date.today().isoformat()}.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    files = included_files()
    manifest = ["Cities & Climate Learning Lab — Gate 4B–5A private review candidate", f"Created: {dt.date.today().isoformat()}", f"Branch: {branch}", f"Commit: {commit}", f"Files: {len(files)}", "", "SHA-256  Archive path"]
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for source, target in files:
            archive.write(source, target)
            manifest.append(f"{sha256(source)}  {target.as_posix()}")
        archive.writestr("00_READ_ME_FIRST.md", (ROOT / "docs/handoffs/gate-4b-5a-handoff.md").read_text(encoding="utf-8"))
        archive.writestr("MANIFEST.txt", "\n".join(manifest) + "\n")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        print(package(args.output).resolve())
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Unable to create owner review package: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
