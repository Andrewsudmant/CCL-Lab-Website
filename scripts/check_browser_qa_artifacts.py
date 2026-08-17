#!/usr/bin/env python3
from pathlib import Path
try:
    from .content import ROOT
except ImportError:
    from content import ROOT

required = [
    ROOT / "reports/screenshots/gate-4b-5a-current-conversations-desktop.png",
    ROOT / "reports/screenshots/gate-4b-5a-current-conversations-mobile.png",
    ROOT / "reports/screenshots/gate-4b-5a-current-conversations-200-percent.png",
    ROOT / "reports/screenshots/gate-4b-5a-publications-complete-desktop.png",
    ROOT / "reports/screenshots/gate-4b-5a-publications-complete-mobile.png",
    ROOT / "reports/screenshots/gate-4b-5a-multi-source-detail-desktop.png",
    ROOT / "reports/browser-qa-gate-4b-5a.md",
]
missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
if missing:
    raise SystemExit("Missing browser QA artefacts: " + ", ".join(missing))
print("Gate 4B–5A browser QA artefact set is present.")
