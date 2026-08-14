#!/usr/bin/env python3
"""Validate CCLL content, taxonomy, cross-links, and publication controls."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

try:
    from .content import ROOT, load_yaml, research_scope
except ImportError:
    from content import ROOT, load_yaml, research_scope

CANONICAL_THEMES = {
    "urban-climate-learning", "climate-governance-delivery",
    "co-benefits-place-based-valuation", "just-transitions-workforce",
    "evidence-infrastructure-tools", "canadian-climate-policy",
}
RETIRED_THEME = "canadian-comparative-policy"
WATCH_STATES = ("published", "withheld", "quarantine")
CRITICAL_FLAGS = {"title-only", "prompt-injection", "suspicious-url", "unsupported-claim"}


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


def schema_errors(instance: Any, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    messages = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        messages.append(f"{label}: {location}: {error.message}")
    return messages


def validate_all() -> list[str]:
    errors: list[str] = []
    for path in sorted((ROOT / "schemas").glob("*.schema.json")):
        try:
            Draft202012Validator.check_schema(load_schema(path.name))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON Schema: {exc}")

    theme_schema = load_schema("research-theme.schema.json")
    scope_schema = copy.deepcopy(load_schema("research-scope.schema.json"))
    scope_schema["properties"]["themes"]["items"] = theme_schema
    scope = research_scope()
    errors.extend(schema_errors(scope, scope_schema, "config/research_scope.yml"))
    theme_ids = [item.get("id") for item in scope.get("themes", [])]
    if set(theme_ids) != CANONICAL_THEMES or len(theme_ids) != len(set(theme_ids)):
        errors.append("config/research_scope.yml: theme IDs must be the six canonical unique IDs")

    vocab = load_yaml(ROOT / "config/vocabularies.yml")
    errors.extend(schema_errors(vocab, load_schema("vocabularies.schema.json"), "config/vocabularies.yml"))
    query_pack = load_yaml(ROOT / "config/query_packs/research-watch-v1.yml")
    errors.extend(schema_errors(query_pack, load_schema("query-pack.schema.json"), "config/query_packs/research-watch-v1.yml"))
    for adapter_queries in query_pack.get("source_queries", {}).values():
        for query in adapter_queries:
            errors.extend(theme_reference_errors(query.get("themes", []), "query pack", CANONICAL_THEMES))

    records: dict[str, list[dict[str, Any]]] = {}
    for kind, schema_name in (("people", "person.schema.json"), ("projects", "project.schema.json"), ("publications", "publication.schema.json")):
        records[kind] = []
        schema = load_schema(schema_name)
        for path in sorted((ROOT / "data" / kind).glob("*.yml")):
            record = load_yaml(path)
            records[kind].append(record)
            label = str(path.relative_to(ROOT))
            errors.extend(schema_errors(record, schema, label))
            errors.extend(content_policy_errors(record, label, vocab))

    people = records["people"]
    if not people or people[0].get("email") != "andrew_sudmant@sfu.ca":
        errors.append("data/people: public email must be andrew_sudmant@sfu.ca")

    errors.extend(unique_and_crosslink_errors(records))

    watch_schema = load_schema("research-watch.schema.json")
    seen_watch_ids: set[str] = set()
    for state in WATCH_STATES:
        for path in sorted((ROOT / "data/research-watch" / state).glob("*.yml")):
            record = load_yaml(path)
            label = str(path.relative_to(ROOT))
            errors.extend(schema_errors(record, watch_schema, label))
            errors.extend(watch_policy_errors(record, label, state, vocab))
            record_id = record.get("record_id")
            if record_id in seen_watch_ids:
                errors.append(f"{label}: duplicate Research Watch record_id {record_id}")
            seen_watch_ids.add(record_id)

    # Retired IDs must not survive in controlled content or site source.
    for base in (ROOT / "config", ROOT / "data", ROOT / "schemas"):
        for path in base.rglob("*"):
            if path.is_file() and RETIRED_THEME in path.read_text(encoding="utf-8", errors="ignore"):
                errors.append(f"{path.relative_to(ROOT)}: contains retired theme ID {RETIRED_THEME}")
    return errors


def theme_reference_errors(values: list[str], label: str, theme_ids: set[str]) -> list[str]:
    unknown = sorted(set(values) - theme_ids)
    return [f"{label}: unknown theme IDs: {', '.join(unknown)}"] if unknown else []


def content_policy_errors(record: dict[str, Any], label: str, vocab: dict[str, Any]) -> list[str]:
    errors = []
    if "primary_theme" in record:
        primary = record.get("primary_theme")
        secondary = record.get("secondary_themes", [])
        errors.extend(theme_reference_errors([primary, *secondary], label, CANONICAL_THEMES))
        if primary in secondary:
            errors.append(f"{label}: primary theme cannot also be secondary")
        for field, vocabulary in (("geographies", "geographies"), ("governance_scales", "governance_scales"), ("methods", "methods"), ("climate_domains", "climate_domains"), ("sectors", "sectors")):
            invalid = sorted(set(record.get(field, [])) - set(vocab[vocabulary]))
            if invalid:
                errors.append(f"{label}: invalid {field}: {', '.join(invalid)}")
    else:
        errors.extend(theme_reference_errors(record.get("themes", []), label, CANONICAL_THEMES))
    if "authors" in record:
        authors = record.get("authors", [])
        if any("collaborator" in author.casefold() for author in authors):
            errors.append(f"{label}: canonical author lists cannot use 'and collaborators'")
        date = record.get("publication_date", "")
        precision = record.get("date_precision")
        expected_length = {"exact": 10, "month": 7, "year": 4}.get(precision)
        if expected_length and len(date) != expected_length:
            errors.append(f"{label}: publication_date does not match date_precision {precision}")
        if precision == "year" and date.endswith("-01-01"):
            errors.append(f"{label}: year-only evidence cannot use a synthetic January 1 date")
    return errors


def unique_and_crosslink_errors(records: dict[str, list[dict[str, Any]]]) -> list[str]:
    errors = []
    project_ids = {r.get("record_id") for r in records["projects"]}
    publication_ids = {r.get("record_id") for r in records["publications"]}
    for kind in ("projects", "publications"):
        ids = [r.get("record_id") for r in records[kind]]
        if len(ids) != len(set(ids)):
            errors.append(f"data/{kind}: record_id values must be unique")
    dois = [r.get("doi", "").lower() for r in records["publications"] if r.get("doi")]
    urls = [r.get("url") for r in records["publications"]]
    if len(dois) != len(set(dois)):
        errors.append("data/publications: DOI values must be unique")
    if len(urls) != len(set(urls)):
        errors.append("data/publications: canonical URLs must be unique")
    for publication in records["publications"]:
        if publication.get("doi", "").lower() == "10.1038/s44284-025-00260-8":
            errors.append("data/publications: Nature Cities global stocktake is not an Andrew Sudmant publication")
    for project in records["projects"]:
        missing = set(project.get("connected_publications", [])) - publication_ids
        if missing:
            errors.append(f"project {project.get('record_id')}: missing publication links: {', '.join(sorted(missing))}")
    for publication in records["publications"]:
        missing = set(publication.get("connected_projects", [])) - project_ids
        if missing:
            errors.append(f"publication {publication.get('record_id')}: missing project links: {', '.join(sorted(missing))}")
    return errors


def watch_policy_errors(record: dict[str, Any], label: str, state: str, vocab: dict[str, Any]) -> list[str]:
    errors = []
    assignments = record.get("theme_assignments", {})
    primary = assignments.get("primary", {}).get("theme_id")
    secondary = [item.get("theme_id") for item in assignments.get("secondary", [])]
    errors.extend(theme_reference_errors([primary, *secondary], label, CANONICAL_THEMES))
    if primary in secondary or len(secondary) != len(set(secondary)):
        errors.append(f"{label}: theme assignments must be unique")
    invalid_geo = set(record.get("geographies", [])) - set(vocab["geographies"])
    if invalid_geo:
        errors.append(f"{label}: invalid geographies: {', '.join(sorted(invalid_geo))}")
    expected = "quarantined" if state == "quarantine" else state
    if record.get("publication", {}).get("decision") != expected:
        errors.append(f"{label}: directory state and publication decision must match")
    if state == "published":
        evidence = record.get("evidence_basis", {})
        flags = set(record.get("risk_flags", []))
        checks = set(record.get("publication", {}).get("checks_passed", []))
        if not evidence.get("sufficient_for_summary"):
            errors.append(f"{label}: published records require sufficient evidence")
        if flags & CRITICAL_FLAGS:
            errors.append(f"{label}: critical risk flags require withholding or quarantine")
        if not {"schema-valid", "url-safe", "deduplicated", "evidence-sufficient", "disclosure-present"} <= checks:
            errors.append(f"{label}: published records are missing mandatory checks")
        if record.get("source_type") == "academic-paper" and ("mdpi" in record.get("source_domain", "").casefold() or "mdpi" in record.get("source_name", "").casefold()):
            errors.append(f"{label}: MDPI academic records are excluded from public Research Watch")
    review = record.get("review", {})
    if review.get("status") == "reviewed" and (not review.get("reviewer") or not review.get("reviewed_date")):
        errors.append(f"{label}: reviewed records require reviewer and date")
    if review.get("status") == "not_reviewed" and (review.get("reviewer") or review.get("reviewed_date")):
        errors.append(f"{label}: not-reviewed records cannot name a reviewer or date")
    ai = record.get("ai_provenance", {})
    if ai.get("used") and (not ai.get("model") or not ai.get("prompt_version")):
        errors.append(f"{label}: AI records require model and prompt version")
    if "none" in record.get("risk_flags", []) and len(record.get("risk_flags", [])) > 1:
        errors.append(f"{label}: risk flag none cannot be combined")
    return errors


def main() -> int:
    errors = validate_all()
    if errors:
        print("Content validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    count = sum(1 for _ in (ROOT / "data").rglob("*.yml"))
    print(f"Validated {count} records and {len(list((ROOT / 'schemas').glob('*.json')))} schemas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
