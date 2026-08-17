#!/usr/bin/env python3
"""Create the owner Current Conversations calibration ZIP."""
from __future__ import annotations
import datetime as dt
import hashlib
import zipfile
from pathlib import Path
try:
    from .content import ROOT
except ImportError:
    from content import ROOT

REQUIRED = ["owner-labelling.html", "candidates.json", "candidates.csv", "empty-labels.json", "README.txt"]

def package(output: Path | None = None) -> Path:
    source = ROOT / "calibration/current-conversations"
    missing = [name for name in REQUIRED if not (source / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing calibration files: {missing}; run make current-conversations-pilot")
    destination = output or ROOT / "deliverables" / f"CCLL-current-conversations-calibration-{dt.date.today()}.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)
    manifest = ["CCLL Current Conversations calibration", f"Created: {dt.date.today()}", "Labels evaluate discovery and grouping; they are not publication approvals.", "", "SHA-256  File"]
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in REQUIRED:
            data = (source / name).read_bytes()
            archive.writestr(name, data)
            manifest.append(f"{hashlib.sha256(data).hexdigest()}  {name}")
        archive.writestr("MANIFEST.txt", "\n".join(manifest) + "\n")
    return destination

if __name__ == "__main__":
    print(package().resolve())
