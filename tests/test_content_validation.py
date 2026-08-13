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


def test_candidate_and_approved_directories_are_separate() -> None:
    candidates = {path.name for path in (ROOT / "data/research-watch/candidates").glob("*.yml")}
    approved = {path.name for path in (ROOT / "data/research-watch/approved").glob("*.yml")}
    assert candidates
    assert approved
    assert candidates.isdisjoint(approved)
