#!/usr/bin/env python3
from pathlib import Path

try:
    from .content import ROOT
except ImportError:
    from content import ROOT

required = [
    ROOT / "reports/screenshots/gate-5b/desktop/home.png",
    ROOT / "reports/screenshots/gate-5b/desktop/current-conversations.png",
    ROOT / "reports/screenshots/gate-5b/desktop/verified-publications.png",
    ROOT / "reports/screenshots/gate-5b/desktop/delivery-modes-publication.png",
    ROOT / "reports/screenshots/gate-5b/desktop/multi-source-detail.png",
    ROOT / "reports/screenshots/gate-5b/mobile/home.png",
    ROOT / "reports/screenshots/gate-5b/mobile/current-conversations.png",
    ROOT / "reports/screenshots/gate-5b/mobile/verified-publications.png",
    ROOT / "reports/screenshots/gate-5b/zoom/current-conversations-200-percent-equivalent.png",
    ROOT / "reports/browser-qa-gate-5b.md",
]
missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
if missing:
    raise SystemExit("Missing Gate 5B browser QA artefacts: " + ", ".join(missing))
print("Gate 5B browser QA artefact set is present.")
