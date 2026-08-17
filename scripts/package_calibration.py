#!/usr/bin/env python3
"""Create a clearly labelled calibration-generator preview ZIP."""
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
    source = ROOT / "calibration/current-conversations-generator"
    missing = [name for name in REQUIRED if not (source / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing calibration generator files: {missing}; run make current-conversations-pilot")
    destination = output or ROOT / "deliverables" / f"CCLL-current-conversations-calibration-generator-preview-{dt.date.today()}.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)
    manifest = ["CCLL Current Conversations calibration generator preview — NOT FINAL", f"Created: {dt.date.today()}", "Fixtures demonstrate the labelling interface and are not the owner calibration set.", "Regenerate from reviewed live-benchmark artifacts before calibration.", "", "SHA-256  File"]
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in REQUIRED:
            data = (source / name).read_bytes()
            archive_name = f"calibration-generator-preview-NOT-FINAL/{name}"
            archive.writestr(archive_name, data)
            manifest.append(f"{hashlib.sha256(data).hexdigest()}  {archive_name}")
        for kind in ("sources", "clusters"):
            for path in sorted((ROOT / f"data/current-conversations/generated/{kind}").glob("*.json")):
                data = path.read_bytes()
                name = f"metadata/{kind}/{path.name}"
                archive.writestr(name, data)
                manifest.append(f"{hashlib.sha256(data).hexdigest()}  {name}")
        archive.writestr("MANIFEST.txt", "\n".join(manifest) + "\n")
    return destination

if __name__ == "__main__":
    print(package().resolve())
