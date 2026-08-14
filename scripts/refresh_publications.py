#!/usr/bin/env python3
"""Produce a non-mutating publication metadata refresh plan."""

from __future__ import annotations
import argparse
import json
from pathlib import Path
from scripts.content import ROOT, load_records, load_yaml


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    overrides = load_yaml(ROOT / "config/publication_overrides.yml")
    records = load_records("data/publications")
    report = {
        "mode": "dry-run-plan",
        "person_orcid": overrides["person_orcid"],
        "record_count": len(records),
        "doi_records": sum(bool(item["doi"]) for item in records),
        "owner_overrides": len(overrides["overrides"]),
        "next_action": "Fetch ORCID works, enrich known DOIs through Crossref, preserve conflicts, and open a reviewed pull request.",
        "network_calls": 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
