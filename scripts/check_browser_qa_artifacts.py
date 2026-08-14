#!/usr/bin/env python3
from pathlib import Path
try:
    from .content import ROOT
except ImportError:
    from content import ROOT

root = ROOT / "reports/screenshots/gate-3b-4a"
required = [root / "desktop/home.jpg", root / "mobile/home.jpg", root / "zoom/home-200-percent.jpg", ROOT / "reports/browser-qa-gate-3b-4a.md"]
missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
if missing: raise SystemExit("Missing browser QA artefacts: " + ", ".join(missing))
print("Browser QA artefact set is present.")
