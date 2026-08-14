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


def test_published_withheld_and_quarantine_states_are_separate() -> None:
    states = [{path.name for path in (ROOT / "data/research-watch" / state).glob("*.yml")} for state in ("published", "withheld", "quarantine")]
    assert states[0]
    assert states[1]
    assert not (states[0] & states[1] or states[0] & states[2] or states[1] & states[2])


def test_retired_theme_id_is_absent() -> None:
    for base in (ROOT / "config", ROOT / "data", ROOT / "schemas"):
        for path in base.rglob("*"):
            if path.is_file():
                assert "canadian-comparative-policy" not in path.read_text(encoding="utf-8", errors="ignore")
