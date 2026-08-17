from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.validate_content import ROOT, validate_all


def test_all_content_is_valid() -> None:
    assert validate_all() == []


def test_all_schema_documents_are_valid() -> None:
    for path in sorted((ROOT / "schemas").glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_current_conversation_source_and_cluster_ids_are_separate() -> None:
    sources = {json.loads(path.read_text())["source_id"] for path in (ROOT / "data/current-conversations/generated/sources").glob("*.json")}
    clusters = {json.loads(path.read_text())["cluster_id"] for path in (ROOT / "data/current-conversations/generated/clusters").glob("*.json")}
    assert sources and clusters and not (sources & clusters)


def test_retired_theme_id_is_absent() -> None:
    for base in (ROOT / "config", ROOT / "data", ROOT / "schemas"):
        for path in base.rglob("*"):
            if path.is_file():
                assert "canadian-comparative-policy" not in path.read_text(encoding="utf-8", errors="ignore")
