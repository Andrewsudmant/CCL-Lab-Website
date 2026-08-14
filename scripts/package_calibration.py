#!/usr/bin/env python3
"""Create the one-time owner Research Watch calibration ZIP."""
from __future__ import annotations
import datetime as dt
import hashlib
import zipfile
from pathlib import Path
try:
    from .content import ROOT
except ImportError:
    from content import ROOT


def package(output: Path | None = None) -> Path:
    source = ROOT / "calibration/research-watch"
    required = ["owner-labelling.html", "candidates.json", "candidates.csv", "empty-labels.json", "README.txt"]
    missing = [x for x in required if not (source / x).is_file()]
    if missing: raise FileNotFoundError(f"Missing calibration files: {missing}; run make research-watch-pilot")
    destination = output or ROOT / "deliverables" / f"CCLL-research-watch-calibration-{dt.date.today()}.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)
    manifest = ["CCLL one-time Research Watch calibration", f"Created: {dt.date.today()}", "Labels evaluate discovery relevance and are not publication approvals.", ""]
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in required:
            data = (source / name).read_bytes(); archive.writestr(name, data)
            manifest.append(f"{hashlib.sha256(data).hexdigest()}  {name}")
        archive.writestr("MANIFEST.txt", "\n".join(manifest) + "\n")
    return destination


if __name__ == "__main__": print(package().resolve())
