#!/usr/bin/env python3
"""Validate CCLL structured content against schemas and editorial rules."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

try:
    from .content import ROOT, load_yaml, research_scope
except ImportError:  # Direct script execution.
    from content import ROOT, load_yaml, research_scope


def load_schema(name: str) -> dict[str, Any]:
    with (ROOT / "schemas" / name).open(encoding="utf-8") as handle:
        return json.load(handle)


def schema_errors(instance: Any, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    messages: list[str] = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        messages.append(f"{label}: {location}: {error.message}")
    return messages


def validate_all() -> list[str]:
    errors: list[str] = []

    # Ensure every schema is itself valid.
    for path in sorted((ROOT / "schemas").glob("*.schema.json")):
        schema = load_schema(path.name)
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # pragma: no cover - exact library exception varies
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON Schema: {exc}")

    theme_schema = load_schema("research-theme.schema.json")
    scope_schema = copy.deepcopy(load_schema("research-scope.schema.json"))
    scope_schema["properties"]["themes"]["items"] = theme_schema
    scope = research_scope()
    errors.extend(schema_errors(scope, scope_schema, "config/research_scope.yml"))

    expected_themes = {
        "urban-climate-learning",
        "climate-governance-delivery",
        "co-benefits-place-based-valuation",
        "just-transitions-workforce",
        "evidence-infrastructure-tools",
        "canadian-comparative-policy",
    }
    theme_ids = [theme.get("id") for theme in scope.get("themes", [])]
    if set(theme_ids) != expected_themes or len(theme_ids) != len(set(theme_ids)):
        errors.append("config/research_scope.yml: theme IDs must be the six canonical, unique IDs")

    collections = [
        ("data/people", "person.schema.json"),
        ("data/projects", "project.schema.json"),
        ("data/publications", "publication.schema.json"),
        ("data/research-themes", "research-theme.schema.json"),
    ]
    for directory, schema_name in collections:
        schema = load_schema(schema_name)
        for path in sorted((ROOT / directory).glob("*.yml")):
            record = load_yaml(path)
            errors.extend(schema_errors(record, schema, str(path.relative_to(ROOT))))
            errors.extend(cross_record_errors(record, path, expected_themes))

    watch_schema = load_schema("research-watch.schema.json")
    for state in ("candidates", "approved"):
        state_schema_name = f"research-watch-{'candidate' if state == 'candidates' else 'approved'}.schema.json"
        state_schema = copy.deepcopy(load_schema(state_schema_name))
        state_schema["allOf"][0] = watch_schema
        for path in sorted((ROOT / "data/research-watch" / state).glob("*.yml")):
            record = load_yaml(path)
            label = str(path.relative_to(ROOT))
            errors.extend(schema_errors(record, state_schema, label))
            errors.extend(cross_record_errors(record, path, expected_themes))
            errors.extend(watch_policy_errors(record, path, state))

    return errors


def cross_record_errors(record: dict[str, Any], path: Path, theme_ids: set[str]) -> list[str]:
    errors: list[str] = []
    label = str(path.relative_to(ROOT))
    referenced = record.get("lab_themes", record.get("themes", []))
    unknown = sorted(set(referenced) - theme_ids)
    if unknown:
        errors.append(f"{label}: unknown theme IDs: {', '.join(unknown)}")
    if record.get("placeholder") or record.get("fixture"):
        if not record.get("owner_review_required"):
            errors.append(f"{label}: fixtures/placeholders must require owner review")
        record_id = record.get("record_id", record.get("id", ""))
        if not str(record_id).startswith("example-"):
            errors.append(f"{label}: fixture/placeholder ID must start with example-")
    return errors


def watch_policy_errors(record: dict[str, Any], path: Path, state: str) -> list[str]:
    errors: list[str] = []
    label = str(path.relative_to(ROOT))
    review = record.get("human_review", {})
    if state == "approved":
        if review.get("status") != "approved":
            errors.append(f"{label}: records in approved/ must have approved review status")
        if not review.get("reviewer") or not review.get("reviewed_date"):
            errors.append(f"{label}: approved records require reviewer and reviewed date")
    elif review.get("status") not in {"unreviewed", "in-review", "held"}:
        errors.append(f"{label}: candidates cannot have approved or rejected status")

    published = record.get("publication_date")
    retrieved = record.get("retrieval_date")
    if published and retrieved and retrieved < published:
        errors.append(f"{label}: retrieval_date cannot precede publication_date")

    ai = record.get("ai_provenance", {})
    if ai.get("used") and (not ai.get("model") or not ai.get("prompt_version")):
        errors.append(f"{label}: AI-assisted records require model and prompt version")
    if not ai.get("used") and (ai.get("model") is not None or ai.get("prompt_version") is not None):
        errors.append(f"{label}: non-AI records must use null model and prompt version")

    risks = record.get("risk_flags", [])
    if "none" in risks and len(risks) > 1:
        errors.append(f"{label}: risk flag 'none' cannot be combined with other flags")
    return errors


def main() -> int:
    errors = validate_all()
    if errors:
        print("Content validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    record_count = sum(1 for _ in (ROOT / "data").rglob("*.yml"))
    print(f"Validated {record_count} records and {len(list((ROOT / 'schemas').glob('*.json')))} schemas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
