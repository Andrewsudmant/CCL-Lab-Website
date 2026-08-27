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

CANONICAL_THEME_ORDER = [
    ("geographies-of-climate-learning", "Geographies of Climate Learning"),
    ("where-new-evidence-matters", "Where New Evidence Matters"),
    ("modes-of-climate-delivery", "Modes of Climate Delivery"),
    ("consequences-for-people-and-places", "Consequences for People and Places"),
]
CANONICAL_THEMES = {item[0] for item in CANONICAL_THEME_ORDER}
RETIRED_THEMES = {
    "urban-climate-learning", "climate-governance-delivery",
    "co-benefits-place-based-valuation", "just-transitions-workforce",
    "evidence-infrastructure-tools", "canadian-climate-policy",
    "canadian-comparative-policy",
}
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
    observed_themes = [(item.get("id"), item.get("name")) for item in scope.get("themes", [])]
    if observed_themes != CANONICAL_THEME_ORDER:
        errors.append("config/research_scope.yml: theme IDs and titles must match the four canonical themes in order")

    vocab = load_yaml(ROOT / "config/vocabularies.yml")
    errors.extend(schema_errors(vocab, load_schema("vocabularies.schema.json"), "config/vocabularies.yml"))
    query_pack = load_yaml(ROOT / "config/query_packs/current-conversations-v2.yml")
    errors.extend(schema_errors(query_pack, load_schema("current-conversations-query-pack.schema.json"), "config/query_packs/current-conversations-v2.yml"))
    for query_group in query_pack.get("queries", {}).values():
        for query in query_group:
            label = f"query pack {query.get('id')}"
            errors.extend(theme_reference_errors([query.get("theme_intent"), *query.get("candidate_themes", [])], label, CANONICAL_THEMES, allow_unclassified=True))
            if query.get("query_type") == "theme" and not query.get("theme_intent"):
                errors.append(f"{label}: theme queries require theme_intent")
            if query.get("query_type") != "theme" and query.get("theme_intent") is not None:
                errors.append(f"{label}: facet and exploratory queries cannot force theme_intent")
            if query.get("classification_required") is not True:
                errors.append(f"{label}: every retrieved item requires content-based classification")
            facets = query.get("facets", {})
            for field, vocabulary in (("geographies", "geographies"), ("sectors", "sectors"), ("methods", "methods"), ("climate_domains", "climate_domains")):
                invalid = sorted(set(facets.get(field, [])) - set(vocab[vocabulary]))
                if invalid:
                    errors.append(f"{label}: invalid facet {field}: {', '.join(invalid)}")
            if query.get("theme_intent") == "where-new-evidence-matters":
                lowered = query.get("query", "").casefold()
                consequential = ("consequential", "value of", "could change", "evaluation priorit", "research priorit")
                if not any(term in lowered for term in consequential):
                    errors.append(f"{label}: Theme 2 query lacks a consequential evidence or uncertainty concept")

    publication_examples = load_yaml(ROOT / "config/publication_theme_examples.yml")
    errors.extend(schema_errors(publication_examples, load_schema("publication-theme-examples.schema.json"), "config/publication_theme_examples.yml"))
    for example in publication_examples.get("records", []):
        label = f"publication theme example {example.get('record_id')}"
        relationship_themes = [item.get("theme_id") for item in example.get("theme_relationships", [])]
        errors.extend(theme_reference_errors([example.get("primary_theme"), *example.get("secondary_themes", []), *relationship_themes], label, CANONICAL_THEMES))
        assigned = {example.get("primary_theme"), *example.get("secondary_themes", [])}
        if assigned != set(relationship_themes):
            errors.append(f"{label}: every assigned theme requires exactly one rationale")

    records: dict[str, list[dict[str, Any]]] = {}
    for kind, schema_name in (
        ("people", "person.schema.json"),
        ("work", "research-work.schema.json"),
        ("research-ideas", "research-idea.schema.json"),
        ("publications", "publication.schema.json"),
    ):
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

    complete_path = ROOT / "reports/content/publication-complete-inventory.json"
    if complete_path.exists():
        complete = json.loads(complete_path.read_text(encoding="utf-8")).get("records", [])
        publication_schema = load_schema("publication.schema.json")
        complete_dois: list[str] = []
        for index, record in enumerate(complete):
            label = f"reports/content/publication-complete-inventory.json[{index}]"
            errors.extend(schema_errors(record, publication_schema, label))
            if record.get("doi"):
                complete_dois.append(record["doi"].lower())
            if record.get("mdpi_excluded") and (record.get("featured") or record.get("current_conversations_eligible")):
                errors.append(f"{label}: MDPI records cannot be featured or Current Conversations eligible")
        if len(complete_dois) != len(set(complete_dois)):
            errors.append("complete publication inventory: duplicate DOI")
        if sum(bool(record.get("featured")) for record in complete) > 12:
            errors.append("complete publication inventory: selected set exceeds 12")

    source_schema = load_schema("current-conversation-source.schema.json")
    cluster_schema = load_schema("current-conversation-cluster.schema.json")
    sources: dict[str, dict[str, Any]] = {}
    for path in sorted((ROOT / "data/current-conversations/generated/sources").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        label = str(path.relative_to(ROOT))
        errors.extend(schema_errors(record, source_schema, label))
        source_id = record.get("source_id")
        if source_id in sources:
            errors.append(f"{label}: duplicate source_id {source_id}")
        sources[source_id] = record
        if record.get("mdpi_excluded") and record.get("source_environment") == "academic-research":
            errors.append(f"{label}: MDPI academic source cannot enter Current Conversations")

    cluster_ids: set[str] = set()
    for path in sorted((ROOT / "data/current-conversations/generated/clusters").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        label = str(path.relative_to(ROOT))
        errors.extend(schema_errors(record, cluster_schema, label))
        cluster_id = record.get("cluster_id")
        if cluster_id in cluster_ids:
            errors.append(f"{label}: duplicate cluster_id {cluster_id}")
        cluster_ids.add(cluster_id)
        principal = record.get("principal_source_id")
        linked = record.get("linked_source_ids", [])
        if principal not in sources:
            errors.append(f"{label}: principal source does not exist: {principal}")
        missing = set(linked) - set(sources)
        if missing:
            errors.append(f"{label}: missing linked sources: {', '.join(sorted(missing))}")
        if principal in linked or len(linked) != len(set(linked)):
            errors.append(f"{label}: principal/linked source IDs must be unique")
        errors.extend(theme_reference_errors([record.get("primary_theme"), *record.get("secondary_themes", [])], label, CANONICAL_THEMES, allow_unclassified=True))

    # Retired IDs must not survive in controlled content. Generated transition
    # routes retain old slugs only so shared URLs resolve to an explanatory page.
    for base in (ROOT / "config", ROOT / "data", ROOT / "schemas"):
        for path in base.rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8", errors="ignore")
                for retired in RETIRED_THEMES:
                    if retired in text:
                        errors.append(f"{path.relative_to(ROOT)}: contains retired theme ID {retired}")
    return errors


def theme_reference_errors(values: list[str | None], label: str, theme_ids: set[str], *, allow_unclassified: bool = False) -> list[str]:
    if allow_unclassified:
        values = [value for value in values if value is not None]
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
    elif "theme_id" in record:
        errors.extend(theme_reference_errors([record.get("theme_id")], label, CANONICAL_THEMES))
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
    work_ids = {r.get("work_id") for r in records["work"]}
    publication_ids = {r.get("record_id") for r in records["publications"]}
    complete_path = ROOT / "reports/content/publication-complete-inventory.json"
    if complete_path.is_file():
        publication_ids |= {
            item.get("record_id")
            for item in json.loads(complete_path.read_text(encoding="utf-8")).get("records", [])
        }
    for kind, id_field in (("work", "work_id"), ("research-ideas", "idea_id"), ("publications", "record_id")):
        ids = [r.get(id_field) for r in records[kind]]
        if len(ids) != len(set(ids)):
            errors.append(f"data/{kind}: {id_field} values must be unique")
    dois = [r.get("doi", "").lower() for r in records["publications"] if r.get("doi")]
    urls = [r.get("url") for r in records["publications"]]
    if len(dois) != len(set(dois)):
        errors.append("data/publications: DOI values must be unique")
    if len(urls) != len(set(urls)):
        errors.append("data/publications: canonical URLs must be unique")
    for publication in records["publications"]:
        if publication.get("doi", "").lower() == "10.1038/s44284-025-00260-8":
            errors.append("data/publications: Nature Cities global stocktake is not an Andrew Sudmant publication")
    for work in records["work"]:
        work_id = work.get("work_id")
        missing = set(work.get("connected_publication_ids", [])) - publication_ids
        if missing:
            errors.append(f"work {work_id}: missing publication links: {', '.join(sorted(missing))}")
        missing_work = set(work.get("connected_work_ids", [])) - work_ids
        if missing_work:
            errors.append(f"work {work_id}: missing work links: {', '.join(sorted(missing_work))}")
        missing_tools = set(work.get("connected_tool_ids", [])) - work_ids
        if missing_tools:
            errors.append(f"work {work_id}: missing tool links: {', '.join(sorted(missing_tools))}")
        parent = work.get("parent_work_id")
        if parent is not None and parent not in work_ids:
            errors.append(f"work {work_id}: missing parent work: {parent}")
        if parent == work_id or work_id in work.get("connected_work_ids", []):
            errors.append(f"work {work_id}: cannot link to itself")
        if work.get("work_type") in {"paper", "report"} and work.get("title") is None and len(work.get("connected_publication_ids", [])) != 1:
            errors.append(f"work {work_id}: publication-derived title requires exactly one connected publication")
        if work.get("work_type") not in {"paper", "report"} and work.get("title") is None:
            errors.append(f"work {work_id}: only paper/report records may derive a title from a publication")
        for tool_id in work.get("connected_tool_ids", []):
            tool = next((item for item in records["work"] if item.get("work_id") == tool_id), None)
            if tool and tool.get("work_type") not in {"tool", "dataset"}:
                errors.append(f"work {work_id}: connected_tool_ids must reference tool or dataset work")
    for publication in records["publications"]:
        missing = set(publication.get("connected_work_ids", [])) - work_ids
        if missing:
            errors.append(f"publication {publication.get('record_id')}: missing work links: {', '.join(sorted(missing))}")
        relationship_themes = [item.get("theme_id") for item in publication.get("theme_relationships", [])]
        errors.extend(theme_reference_errors(relationship_themes, f"publication {publication.get('record_id')} relationships", CANONICAL_THEMES))
        if len(relationship_themes) != len(set(relationship_themes)):
            errors.append(f"publication {publication.get('record_id')}: theme relationships must be unique")
        assigned = {publication.get("primary_theme"), *publication.get("secondary_themes", [])}
        if publication.get("theme_relationships") and assigned != set(relationship_themes):
            errors.append(f"publication {publication.get('record_id')}: every assigned selected-example theme requires a rationale")
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
    count = sum(1 for _ in (ROOT / "data").rglob("*.yml")) + sum(1 for _ in (ROOT / "data/current-conversations/generated").rglob("*.json"))
    print(f"Validated {count} records and {len(list((ROOT / 'schemas').glob('*.json')))} schemas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
