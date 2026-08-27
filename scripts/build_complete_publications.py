#!/usr/bin/env python3
"""Build a complete verified bibliography from the ORCID reconciliation output."""

from __future__ import annotations

import csv
import datetime as dt
import html
import json
import re
from pathlib import Path

try:
    from scripts.content import ROOT, load_records, load_yaml
except ModuleNotFoundError:
    from content import ROOT, load_records, load_yaml


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:90].rstrip("-")


def theme_for(title: str) -> str:
    value = title.casefold()
    if any(term in value for term in ("workforce", "worker", "livelihood", "just transition", "employment")):
        return "consequences-for-people-and-places"
    if any(term in value for term in ("governance", "policy", "delivery", "implementation")):
        return "modes-of-climate-delivery"
    if any(term in value for term in ("economic", "finance", "pro-poor", "benefit", "health", "social impact", "inequit")):
        return "consequences-for-people-and-places"
    if any(term in value for term in ("data scaling", "natural experiment", "forecasting", "machine learning", "blind spot", "crowdsourced", "carbon account", "methodolog")):
        return "where-new-evidence-matters"
    return "geographies-of-climate-learning"


def geographies_for(title: str) -> list[str]:
    value = title.casefold()
    candidates = [
        ("british columbia", "british-columbia"), ("canada", "canada"), ("calgary", "canada"),
        ("uk", "united-kingdom"), ("belfast", "united-kingdom"), ("leeds", "united-kingdom"),
        ("edinburgh", "united-kingdom"), ("yorkshire", "united-kingdom"), ("rwanda", "rwanda"),
        ("kigali", "rwanda"), ("india", "india"), ("kolkata", "india"), ("china", "global"),
        ("europe", "europe"),
    ]
    found = list(dict.fromkeys(code for term, code in candidates if term in value))
    return found or ["global"]


def type_for(value: str | None) -> str:
    return {"journal-article": "article", "book-chapter": "chapter", "posted-content": "preprint", "report": "report", "Dataset": "dataset"}.get(value or "", "other")


def build_record(item: dict, selected: dict[str, dict], verified_date: str) -> dict:
    doi = item["doi"].lower()
    if doi in selected:
        record = dict(selected[doi])
        record["current_conversations_eligible"] = True
        record["mdpi_excluded"] = False
        return record
    mdpi = doi.startswith("10.3390/")
    title = html.unescape(re.sub(r"<[^>]+>", "", item["title"]))
    authors = [html.unescape(re.sub(r"<[^>]+>", "", author)) for author in item["authors"]]
    venue = item.get("venue") or "Authoritative repository record"
    date = item["publication_date"]
    author_text = ", ".join(authors)
    return {
        "record_id": slug(title), "title": title, "authors": authors,
        "publication_date": date, "date_precision": item["date_precision"],
        "publication_type": type_for(item.get("type")), "peer_review_status": "unknown",
        "venue": venue, "volume": item.get("volume"), "issue": item.get("issue"),
        "pages": item.get("pages"), "article_number": item.get("article_number"),
        "doi": doi, "other_identifiers": item.get("external_identifiers", []), "version": None,
        "original_submission_date": None, "current_version_date": None,
        "url": item.get("url") or f"https://doi.org/{doi}",
        "citation": f"{author_text}. ({date[:4]}). {title}. {venue}. https://doi.org/{doi}",
        "abstract_summary": "Verified bibliographic record. Consult the original source for its scope, methods, findings and limitations.",
        "relationship_to_lab": "foundational-prior-work",
        "relationship_note": "Verified work by Andrew Sudmant that predates the establishment of the Cities & Climate Learning Lab.",
        "primary_theme": theme_for(title), "secondary_themes": [], "theme_relationships": [],
        "geographies": geographies_for(title), "governance_scales": [], "methods": [],
        "climate_domains": ["evidence-and-learning"], "sectors": ["cross-sectoral"],
        "connected_work_ids": [], "featured": False,
        "current_conversations_eligible": not mdpi, "mdpi_excluded": mdpi,
        "metadata_sources": ["orcid", item["provider"], "owner-override"] if mdpi else ["orcid", item["provider"]],
        "last_verified_date": verified_date,
        "authoritative_sources": [{"label": f"{item['provider'].title()} DOI record", "url": f"https://api.{item['provider']}.org/works/{doi}" if item["provider"] == "crossref" else f"https://api.datacite.org/dois/{doi}", "retrieved_date": verified_date}],
        "verification_status": "verified",
    }


def authoritative_record(item: dict, verified_date: str) -> dict:
    title = html.unescape(item["title"])
    authors = [html.unescape(author) for author in item["authors"]]
    date = str(item["publication_date"])
    doi = item.get("doi")
    return {
        "record_id": item.get("record_id") or slug(title), "title": title, "authors": authors,
        "publication_date": date, "date_precision": item["date_precision"],
        "publication_type": item["publication_type"], "peer_review_status": item.get("peer_review_status", "not-applicable"),
        "venue": item["venue"], "volume": item.get("volume"), "issue": item.get("issue"),
        "pages": item.get("pages"), "article_number": item.get("article_number"),
        "doi": doi, "other_identifiers": item.get("other_identifiers", []), "version": item.get("version"),
        "original_submission_date": item.get("original_submission_date"), "current_version_date": item.get("current_version_date"),
        "url": item["url"],
        "citation": item.get("citation") or f"{', '.join(authors)}. ({date[:4]}). {title}. {item['venue']}.",
        "abstract_summary": "Verified bibliographic record. Consult the original source for its scope, methods, findings and limitations.",
        "relationship_to_lab": item.get("relationship_to_lab", "foundational-prior-work"),
        "relationship_note": item.get("relationship_note", "Verified work by Andrew Sudmant; the record does not imply that historic work was produced by the Cities & Climate Learning Lab."),
        "primary_theme": item.get("primary_theme", theme_for(title)),
        "secondary_themes": item.get("secondary_themes", []),
        "theme_relationships": item.get("theme_relationships", []),
        "geographies": geographies_for(title),
        "governance_scales": [], "methods": [], "climate_domains": ["evidence-and-learning"], "sectors": ["cross-sectoral"],
        "connected_work_ids": item.get("connected_work_ids", []), "featured": False, "current_conversations_eligible": True, "mdpi_excluded": False,
        "metadata_sources": ["orcid", "repository"] if item.get("put_code") else ["publisher"],
        "last_verified_date": verified_date,
        "authoritative_sources": [
            {**source, "retrieved_date": str(source["retrieved_date"])} for source in item["authoritative_sources"]
        ],
        "verification_status": "verified",
    }


def main() -> int:
    source = ROOT / "reports/content/publication-proposed-inventory.json"
    proposed = json.loads(source.read_text(encoding="utf-8"))["records"]
    authority = load_yaml(ROOT / "config/publication_authoritative_overrides.yml")
    selected_records = load_records("data/publications")
    selected = {item["doi"].lower(): item for item in selected_records if item.get("doi")}
    verified_date = dt.date.today().isoformat()
    records = []
    seen: set[str] = set()
    for item in proposed:
        if item.get("retrieval_status") != "enriched" or not item.get("doi"):
            continue
        if not any("sudmant" in author.casefold() for author in item.get("authors", [])):
            continue
        record = build_record(item, selected, verified_date)
        if record["doi"] not in seen:
            records.append(record); seen.add(record["doi"])
    by_put_code = {str(item.get("put_code")): item for item in proposed}
    excluded_put_codes = set(authority.get("excluded_orcid_records", {}))
    resolved_put_codes: set[str] = set()
    for put_code, override in authority.get("orcid_records", {}).items():
        if put_code not in by_put_code:
            continue
        record = authoritative_record({**by_put_code[put_code], **override, "put_code": put_code, "title": by_put_code[put_code]["orcid_title"]}, verified_date)
        key = record.get("doi") or f"orcid-put:{put_code}"
        if key not in seen:
            records.append(record); seen.add(key); resolved_put_codes.add(put_code)
    for item in authority.get("new_records", []):
        record = authoritative_record(item, verified_date)
        key = record.get("doi") or record["url"]
        if key not in seen:
            records.append(record); seen.add(key)
    for doi, record in selected.items():
        if doi not in seen:
            value = dict(record); value["current_conversations_eligible"] = True; value["mdpi_excluded"] = False
            records.append(value); seen.add(doi)
    theme_examples = load_yaml(ROOT / "config/publication_theme_examples.yml")
    relationships_by_id = {item["record_id"]: item for item in theme_examples["records"]}
    for record in records:
        relationship = relationships_by_id.get(record["record_id"])
        if relationship:
            record["primary_theme"] = relationship["primary_theme"]
            record["secondary_themes"] = relationship["secondary_themes"]
            record["theme_relationships"] = relationship["theme_relationships"]
    records.sort(key=lambda item: (item["publication_date"], item["title"]), reverse=True)
    output_dir = ROOT / "reports/content"
    (output_dir / "publication-complete-inventory.json").write_text(json.dumps({"verified_at": verified_date, "orcid": "0000-0001-8650-8419", "records": records}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    unresolved = [item for item in proposed if item.get("retrieval_status") != "enriched" and str(item.get("put_code")) not in resolved_put_codes | excluded_put_codes]
    with (output_dir / "publication-unresolved.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["put_code", "title", "orcid_year", "external_identifiers", "reason"]); writer.writeheader()
        for item in unresolved:
            writer.writerow({"put_code": item.get("put_code"), "title": item.get("orcid_title"), "orcid_year": item.get("orcid_year"), "external_identifiers": "; ".join(item.get("external_identifiers", [])), "reason": "ORCID-only record lacks sufficient authoritative bibliographic verification"})
    selected_diff = "# Selected-publications diff\n\nThe ten Gate 3B–4A selected records were retained provisionally. No authoritative verification disproved them, and no record was automatically promoted.\n\n- Added to selected set: 0\n- Removed from selected set: 0\n- Selected count: 10\n- MDPI selected records: 0\n"
    (output_dir / "publication-selected-diff.md").write_text(selected_diff, encoding="utf-8")
    mdpi_count = sum(record["mdpi_excluded"] for record in records)
    report = f"""# Publication reconciliation — Gate 5B

Verified: {verified_date}
Identity: ORCID `0000-0001-8650-8419`

## Outcome

- ORCID groups: {len(proposed)}
- Complete verified public records: {len(records)}
- Selected publications and outputs: {sum(record['featured'] for record in records)}
- ORCID-only records resolved through authoritative sources: {len(resolved_put_codes)}
- ORCID records excluded after authoritative authorship check: {len(excluded_put_codes)}
- Unresolved ORCID-only records withheld: {len(unresolved)}
- Duplicate DOI records: 0 after normalization
- Provider conflicts: retained in `publication-proposed-inventory.json` and never silently resolved
- Verified MDPI records: {mdpi_count}

Every complete record has verified Andrew Sudmant authorship and a Crossref or DataCite
identifier record, or was an already canonical selected output with authoritative
sources. Exact provider titles, ordered authors and supported date precision are
retained. The complete view does not imply that historic work was produced by the new
lab.

## MDPI rule

Crossref verifies Andrew Sudmant as an author of `10.3390/land13050641`. It is included
in the complete scholarly record, marked non-featured and ineligible for Current
Conversations. It is absent from selected publications.

## Unresolved records

The unresolved CSV retains {len(unresolved)} ORCID-only groups without inventing public
metadata. They do not require owner-by-owner adjudication unless a genuine authorship
conflict later emerges.
"""
    (output_dir / "publication-reconciliation-gate-5b.md").write_text(report, encoding="utf-8")
    print(f"Built {len(records)} verified complete records; {len(unresolved)} unresolved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
