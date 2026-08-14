#!/usr/bin/env python3
"""Reconcile Andrew Sudmant's public ORCID works with Crossref/DataCite metadata."""

from __future__ import annotations
import argparse
import datetime as dt
import difflib
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from scripts.content import ROOT, load_records, load_yaml

ORCID = "0000-0001-8650-8419"
ORCID_URL = f"https://pub.orcid.org/v3.0/{ORCID}/works"
USER_AGENT = "CCLL-Publication-Reconciliation/1.0"


def get_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def canonical_doi(value: str) -> str:
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value.strip(), flags=re.I).lower()


def date_parts(value: dict[str, Any] | None) -> tuple[str | None, str | None]:
    parts = ((value or {}).get("date-parts") or [[]])[0]
    if not parts:
        return None, None
    text = "-".join(str(v).zfill(2) for v in parts)
    return text, ("exact" if len(parts) >= 3 else "month" if len(parts) == 2 else "year")


def authors_crossref(message: dict[str, Any]) -> list[str]:
    return [" ".join(filter(None, (item.get("given"), item.get("family")))) for item in message.get("author", [])]


def authors_datacite(attributes: dict[str, Any]) -> list[str]:
    return [" ".join(filter(None, (item.get("givenName"), item.get("familyName")))) or item.get("name", "") for item in attributes.get("creators", [])]


def orcid_candidates() -> list[dict[str, Any]]:
    payload = get_json(ORCID_URL)
    candidates = []
    for group in payload.get("group", []):
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        summary = summaries[0]
        title = html.unescape((((summary.get("title") or {}).get("title") or {}).get("value") or "").strip())
        year = (((summary.get("publication-date") or {}).get("year") or {}).get("value"))
        ids = [(item.get("external-id-type", "").lower(), item.get("external-id-value", "")) for item in (summary.get("external-ids") or {}).get("external-id", [])]
        dois = []
        for id_type, value in ids:
            if id_type == "doi":
                doi = canonical_doi(value)
                if doi and doi not in dois:
                    dois.append(doi)
        candidates.append({"put_code": summary.get("put-code"), "orcid_title": title, "orcid_year": year, "dois": dois, "external_identifiers": [f"{k}:{v}" for k, v in ids if v]})
    return candidates


def enrich(candidate: dict[str, Any]) -> dict[str, Any]:
    enriched = {**candidate, "provider": "orcid", "retrieval_status": "orcid-only", "conflicts": []}
    if not candidate["dois"]:
        return enriched
    doi = candidate["dois"][0]
    try:
        message = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""))["message"]
        publication_date, precision = date_parts(message.get("published-online") or message.get("published-print") or message.get("published"))
        provider_title = html.unescape((message.get("title") or [""])[0])
        enriched.update({
            "provider": "crossref", "retrieval_status": "enriched", "doi": doi,
            "title": provider_title, "authors": authors_crossref(message),
            "publication_date": publication_date, "date_precision": precision,
            "venue": (message.get("container-title") or [""])[0], "volume": message.get("volume"),
            "issue": message.get("issue"), "pages": message.get("page"),
            "article_number": message.get("article-number"), "type": message.get("type"),
            "url": message.get("URL") or f"https://doi.org/{doi}",
        })
    except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError):
        try:
            attributes = get_json("https://api.datacite.org/dois/" + urllib.parse.quote(doi, safe=""))["data"]["attributes"]
            dates = attributes.get("dates", [])
            source_date = next((item.get("date") for item in dates if item.get("dateType") in {"Issued", "Submitted", "Available"}), str(attributes.get("publicationYear") or ""))
            publication_date = source_date[:10] if len(source_date) >= 10 else source_date[:7] if len(source_date) >= 7 else source_date[:4]
            enriched.update({"provider": "datacite", "retrieval_status": "enriched", "doi": doi,
                "title": html.unescape((attributes.get("titles") or [{}])[0].get("title", "")),
                "authors": authors_datacite(attributes), "publication_date": publication_date,
                "date_precision": "exact" if len(publication_date) == 10 else "month" if len(publication_date) == 7 else "year",
                "venue": attributes.get("publisher", ""), "volume": None, "issue": None,
                "pages": None, "article_number": None, "type": (attributes.get("types") or {}).get("resourceTypeGeneral"),
                "url": attributes.get("url") or f"https://doi.org/{doi}"})
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError):
            return enriched
    if enriched.get("title") and enriched["title"].casefold() != candidate["orcid_title"].casefold():
        enriched["conflicts"].append({"field": "title", "orcid": candidate["orcid_title"], "provider": enriched["title"]})
    if enriched.get("publication_date") and candidate.get("orcid_year") and not enriched["publication_date"].startswith(candidate["orcid_year"]):
        enriched["conflicts"].append({"field": "year", "orcid": candidate["orcid_year"], "provider": enriched["publication_date"]})
    return enriched


def apply_overrides(record: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    key = record.get("doi") or str(record.get("put_code"))
    override = overrides.get(key, {})
    if override:
        record = {**record, **override, "override_applied": True}
    return record


def current_inventory() -> dict[str, dict[str, Any]]:
    return {item["doi"].lower(): item for item in load_records("data/publications") if item.get("doi")}


def render_report(records: list[dict[str, Any]], current: dict[str, dict[str, Any]], retrieved: str) -> str:
    rows = ["# Publication reconciliation", "", f"Retrieved: {retrieved}", f"Identity source: ORCID `{ORCID}`", "", "## Summary", "", f"- ORCID work groups: {len(records)}", f"- Identifier-enriched records: {sum(r.get('retrieval_status') == 'enriched' for r in records)}", f"- ORCID-only records: {sum(r.get('retrieval_status') != 'enriched' for r in records)}", f"- Provider conflicts retained: {sum(len(r.get('conflicts', [])) for r in records)}", f"- Current canonical DOI records: {len(current)}", "", "## ORCID candidates", "", "| Title | Year | DOI | Provider | Current inventory |", "|---|---:|---|---|---|"]
    for item in records:
        doi = item.get("doi") or (item.get("dois") or [""])[0]
        inventory_state = "excluded by owner override" if item.get("exclude_from_public_inventory") else "included" if doi in current else "candidate"
        rows.append(f"| {item.get('title') or item['orcid_title']} | {item.get('publication_date') or item.get('orcid_year') or '—'} | {doi or '—'} | {item['provider']} | {inventory_state} |")
    rows.extend(["", "## Included canonical records", ""])
    rows.extend(f"- **{item['title']}** — `{doi}` — relationship: `{item['relationship_to_lab']}` — featured: `{str(item['featured']).lower()}`" for doi, item in sorted(current.items()))
    rows.extend(["", "## Exclusions and unresolved metadata", "", "- The Nature Cities global stocktake is excluded from Andrew Sudmant's inventory because authoritative metadata does not list him as an author.", "- `10.3390/land13050641` is explicitly excluded by the owner override applied after provider enrichment; it remains in this reconciliation trail and cannot become featured.", "- ORCID records without a DOI remain candidates for repository/publisher verification; they are not silently discarded.", "- MDPI records may remain visible in the reconciliation report but are not eligible for featured status under the owner decision.", "- Conflicting titles and years are retained below rather than silently overwritten.", "", "## Conflicts", ""])
    conflicts = [(item, conflict) for item in records for conflict in item.get("conflicts", [])]
    if not conflicts:
        rows.append("No title or year conflicts were found in this run.")
    for item, conflict in conflicts:
        rows.append(f"- `{item.get('doi') or item.get('put_code')}` {conflict['field']}: ORCID = “{conflict['orcid']}”; {item['provider']} = “{conflict['provider']}”.")
    rows.extend(["", "## Editorial proposal", "", "The ten records currently marked `featured: true` are a private staging proposal spanning learning, delivery, valuation and evidence infrastructure. They are predominantly foundational prior work because the lab is newly established. Theme 4 is represented by a current project rather than a fabricated publication; Theme 6 remains a developing programme without an invented project or output.", ""])
    return "\n".join(rows)


def render_diff(records: list[dict[str, Any]], current: dict[str, dict[str, Any]]) -> str:
    proposed = {item.get("doi"): item for item in records if item.get("doi")}
    lines = ["# Publication inventory diff", "", "This readable diff compares current canonical DOI records with the normalized provider proposal.", ""]
    for doi, canonical in sorted(current.items()):
        candidate = proposed.get(doi)
        if not candidate:
            lines.append(f"- `{doi}`: current record not returned as a normalized DOI candidate; retain pending verification.")
            continue
        changes = []
        for field in ("title", "authors", "publication_date", "venue", "volume", "issue", "pages", "article_number"):
            if canonical.get(field) != candidate.get(field):
                changes.append(field)
        lines.append(f"- `{doi}`: {'provider differences in ' + ', '.join(changes) if changes else 'canonical bibliographic fields match provider proposal'}.")
    new = sorted(set(proposed) - set(current))
    lines.extend(f"- `{doi}`: ORCID candidate not in the selected public inventory." for doi in new)
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports/content")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    overrides = load_yaml(ROOT / "config/publication_overrides.yml").get("overrides", {})
    retrieved = dt.datetime.now(dt.timezone.utc).isoformat()
    try:
        candidates = orcid_candidates()[: args.limit]
        records = [apply_overrides(enrich(item), overrides) for item in candidates]
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        print(f"Publication reconciliation failed safely: {exc}", file=sys.stderr)
        return 2
    current = current_inventory()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    normalized = {"retrieved_at": retrieved, "orcid": ORCID, "records": records, "raw_provider_payloads_retained": False}
    (args.output_dir / "publication-proposed-inventory.json").write_text(json.dumps(normalized, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (args.output_dir / "publication-reconciliation.md").write_text(render_report(records, current, retrieved), encoding="utf-8")
    (args.output_dir / "publication-diff.md").write_text(render_diff(records, current), encoding="utf-8")
    print(f"Reconciled {len(records)} ORCID work groups; normalized outputs written to {args.output_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
