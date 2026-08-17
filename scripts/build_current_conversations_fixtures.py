#!/usr/bin/env python3
"""Expand the compact mixed-source fixture into schema-valid source/cluster records."""

from __future__ import annotations

import hashlib
import json
import shutil
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

import yaml

try:
    from scripts.content import ROOT
except ModuleNotFoundError:
    from content import ROOT

FIXTURE = ROOT / "tests/fixtures/current-conversations/mixed-source-gate-4b-5a.yml"
OUTPUT = ROOT / "data/current-conversations/generated"


def source_record(item: dict, fixture: dict) -> dict:
    url = item["url"]
    evidence = item["evidence"]
    identifier = {"type": "doi", "value": item["doi"]} if item.get("doi") else None
    return {
        "source_id": "ccs-" + item["id"], "title": item["title"], "original_url": url,
        "canonical_url": url, "stable_identifier": identifier,
        "authors_or_organisation": [item["organisation"]], "publication_date": item["date"],
        "retrieval_timestamp": fixture["retrieved_at"], "source_environment": item["environment"],
        "source_type": item["type"], "source_role": item["role"],
        "publisher_or_platform": item["organisation"], "source_domain": urlsplit(url).netloc.lower(),
        "language": "en", "geographies": item.get("geography", ["global"]),
        "evidence_basis": [evidence], "evidence_limitations": item["limitations"],
        "content_access_status": "substantive", "content_hash": hashlib.sha256((item["title"] + item["summary"]).encode()).hexdigest(),
        "discovery": {"adapter": "openalex" if not item["fixture"] else "captured-web-fixture", "query_id": "cc-fixture-" + item["theme"], "query_version": "current-conversations-v1.0.0", "run_id": "gate-4b-5a-mixed-source-captured"},
        "ai_annotation": {"model": "captured-deterministic-annotation", "prompt_version": "current-conversations-classification-v1-fixture", "summary": item["summary"], "reason_for_relevance": item["relevance"]},
        "risk_flags": [], "correction_status": "none", "availability_status": "available",
        "review": {"status": "not-reviewed", "reviewer": None, "reviewed_date": None, "edits": []},
        "lab_affiliated": False, "mdpi_excluded": False, "captured_fixture": bool(item["fixture"]),
    }


def build() -> tuple[list[dict], list[dict]]:
    fixture = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))
    source_items = fixture["sources"]
    sources = [source_record(item, fixture) for item in source_items]
    grouped: dict[str, list[tuple[dict, dict]]] = defaultdict(list)
    for item, source in zip(source_items, sources):
        grouped[item["cluster"]].append((item, source))
    clusters = []
    for key, members in grouped.items():
        principal = next((member for member in members if member[0].get("principal")), members[0])
        item, source = principal
        linked = [member[1]["source_id"] for member in members if member[1]["source_id"] != source["source_id"]]
        environments = list(dict.fromkeys(member[1]["source_environment"] for member in members))
        clusters.append({
            "cluster_id": "ccc-" + key, "slug": key, "public_title": item["title"],
            "discussion_statement": item["summary"], "date_first_observed": min(member[0]["date"] for member in members),
            "date_most_recently_observed": max(member[0]["date"] for member in members),
            "principal_source_id": source["source_id"], "linked_source_ids": linked,
            "primary_theme": item["theme"], "secondary_themes": item.get("secondary", []),
            "geographies": item.get("geography", ["global"]), "source_environments": environments,
            "principal_source_role": source["source_role"], "summary": item["summary"],
            "reason_for_relevance": item["relevance"], "limitations": item["limitations"],
            "agreement_disagreement_uncertainty": "No source disagreement was established by the captured evidence." if len(members) == 1 else "The official announcement states the commitment; reporting adds context without independently verifying implementation.",
            "clustering": {"confidence": 1.0 if len(members) == 1 else 0.98, "rationale": "Single-source cluster." if len(members) == 1 else "The reporting links directly to the named official pact.", "method": "stable-link-and-event-identity", "version": "1.0.0", "supporting_identifiers": [member[1]["canonical_url"] for member in members], "principal_source_rationale": "The original evidence or official source is principal; reporting, analysis and commentary remain separately attributed."},
            "ai_provenance": {"used": False, "model": None, "prompt_version": "current-conversations-classification-v1-fixture", "run_id": "gate-4b-5a-mixed-source-captured"},
            "publication_decision": "published", "correction_status": "none", "availability_status": "available",
            "history": [{"date": "2026-08-17", "action": "created", "note": "Created for private mixed-source calibration; identifiers remain stable."}],
            "homepage_eligible": True, "archive_date": None,
            "captured_fixture": any(member[1]["captured_fixture"] for member in members),
        })
    for directory in (OUTPUT / "sources", OUTPUT / "clusters"):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True)
    for record in sources:
        (OUTPUT / "sources" / f"{record['source_id']}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for record in clusters:
        (OUTPUT / "clusters" / f"{record['cluster_id']}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return sources, clusters


if __name__ == "__main__":
    sources, clusters = build()
    print(f"Generated {len(sources)} source records and {len(clusters)} conversation clusters.")
