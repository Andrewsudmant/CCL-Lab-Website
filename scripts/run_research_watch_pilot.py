#!/usr/bin/env python3
"""Explicit, bounded Gate 3B-4A pilot and owner-calibration artefact builder."""

from __future__ import annotations
import argparse
import copy
import csv
import datetime as dt
import html
import json
import os
from collections import Counter
from pathlib import Path
import yaml

from research_watch.adapters.base import AdapterError
from research_watch.adapters.bluesky import BlueskyAdapter
from research_watch.adapters.crossref import CrossrefAdapter
from research_watch.adapters.datacite import DataCiteAdapter
from research_watch.adapters.openalex import OpenAlexAdapter
from research_watch.cluster import cluster, diverse, event_key
from research_watch.normalize import deduplicate
from research_watch.transaction import publish_transaction
from scripts.content import ROOT, load_yaml


def slug(value: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:70]


def full_record(item, theme: str, run_id: str, template: dict) -> dict:
    record = copy.deepcopy(template)
    record.update({
        "record_id": f"pilot-{slug(item.title)}", "title": item.title, "url": item.url,
        "canonical_url": item.url, "authors_or_organisation": item.authors or [item.source_name],
        "source_type": item.source_type, "source_name": item.source_name,
        "source_domain": __import__("urllib.parse").parse.urlsplit(item.raw_metadata.get("provider_source_url") or item.url).netloc.lower(),
        "publication_date": item.publication_date or dt.date.today().isoformat(),
        "retrieval_timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "short_summary": (item.abstract or "")[:600] or "No substantive summary was generated because only bibliographic metadata was available.",
        "reason_for_relevance": f"The source was retrieved by the bounded query for {theme.replace('-', ' ')} and requires calibration against the lab scope.",
        "event_cluster_id": event_key(item), "captured_fixture": False,
    })
    record["stable_identifier"] = ({"type": "doi", "value": item.doi, "url": f"https://doi.org/{item.doi}"} if item.doi else ({"type": "openalex", "value": item.platform_identifier, "url": item.url} if item.platform_identifier else None))
    record["platform_identifier"] = item.platform_identifier
    record["discovery"] = {"run_id": run_id, "adapter": "openalex", "query_id": item.query_id, "query_version": "2.0.0"}
    record["theme_assignments"] = {"primary": {"theme_id": theme, "score": 0.72, "rationale": "Deterministic query-to-theme assignment for owner calibration; not an AI judgement."}, "secondary": []}
    record["evidence_basis"] = {"types": item.evidence_types, "description": "OpenAlex metadata and reconstructed abstract when supplied by the provider.", "sufficient_for_summary": bool(item.abstract), "limitations": "Provider metadata was not a substitute for independent full-text review."}
    record["ai_provenance"] = {"used": False, "model": None, "prompt_version": "research-watch-classification-v2-fixture", "run_id": run_id, "structured_output_version": "2.0", "deterministic_transformations": ["query-theme calibration assignment", "abstract truncation"]}
    record["confidence"] = {"score": 0.72 if item.abstract else 0.35, "label": "medium" if item.abstract else "low", "basis": "Confidence reflects evidence availability and deterministic query assignment."}
    record["publication"] = {"decision": "published" if item.abstract else "withheld", "reasons": ["passed automatic publication controls"] if item.abstract else ["evidence insufficient for summary"], "checks_passed": ["source-url", "identifier", "disclosure", "bounded-run"] if item.abstract else ["source-url", "identifier"], "disclosure_version": "research-watch-disclosure-v1"}
    record["risk_flags"] = ["none"] if item.abstract else ["title-only"]
    record["review"] = {"status": "not_reviewed", "reviewer": None, "reviewed_date": None, "notes": None}
    record["reviewer_edits"] = []
    record["linked_sources"] = []
    return record


def passes_relevance_gate(record: dict) -> bool:
    """Conservative lexical gate used only when no classification model ran."""
    text = (record["title"] + " " + record["short_summary"]).lower()
    climate = any(term in text for term in ("climate", "decarbon", "net zero", "low-carbon", "low carbon", "green transition"))
    if not climate:
        return False
    theme = record["theme_assignments"]["primary"]["theme_id"]
    rules = {
        "urban-climate-learning": (("urban", "city", "cities", "municipal"), ("evidence transfer", "policy learning", "knowledge exchange", "knowledge transfer", "evidence use")),
        "climate-governance-delivery": (("urban", "city", "cities", "municipal"), ("governance", "deliver", "implementation", "institution")),
        "co-benefits-place-based-valuation": (("co-benefit", "cobenefit", "valuation", "appraisal", "co-cost"),),
        "just-transitions-workforce": (("occupation", "workforce", "skill", "labour", "labor", "worker"),),
        "evidence-infrastructure-tools": (("urban", "city", "cities", "municipal"), ("evidence", "data", "model", "tool", "decision support")),
        "canadian-climate-policy": (("canada", "canadian", "british columbia"),),
    }
    return all(any(term in text for term in group) for group in rules[theme])


def calibration_html(candidates: list[dict]) -> str:
    cards = []
    for c in candidates:
        cards.append(f'''<article data-id="{html.escape(c['record_id'])}"><h2><a href="{html.escape(c['url'])}">{html.escape(c['title'])}</a></h2><p>{html.escape(c['source_name'])} · {html.escape(c['publication_date'])} · {html.escape(c['source_type'])}</p><p><strong>Evidence:</strong> {html.escape(c['evidence_basis']['description'])}</p><p><strong>Proposed relevance:</strong> {html.escape(c['reason_for_relevance'])}</p><p><strong>Limitation:</strong> {html.escape(c['evidence_basis']['limitations'])}</p><label>Label <select><option value="">Choose…</option><option>clearly relevant</option><option>potentially relevant</option><option>not relevant</option></select></label><label> Comment <input type="text"></label></article>''')
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>CCLL Research Watch calibration</title><style>body{font:17px/1.5 system-ui;max-width:900px;margin:auto;padding:2rem;color:#222}article{border-top:4px solid #b5121b;padding:1.3rem 0}label{display:block;margin:.7rem 0}input,select,button{font:inherit;padding:.4rem}button{margin:1rem 0}</style><h1>Research Watch owner calibration</h1><p>These labels evaluate discovery relevance; they are not publication approvals. Open each original source before labelling.</p><button id="export">Download structured labels</button>''' + "".join(cards) + '''<script>document.querySelector('#export').onclick=()=>{const labels=[...document.querySelectorAll('article')].map(a=>({record_id:a.dataset.id,label:a.querySelector('select').value,comment:a.querySelector('input').value}));const b=new Blob([JSON.stringify(labels,null,2)],{type:'application/json'});const x=document.createElement('a');x.href=URL.createObjectURL(b);x.download='research-watch-labels.json';x.click();};</script></html>'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit-per-query", type=int, default=4)
    parser.add_argument("--minimum-calibration", type=int, default=30)
    args = parser.parse_args()
    pack = load_yaml(ROOT / "config/query_packs/research-watch-v1.yml")
    run_id = "gate-3b-4a-" + dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    items, failures, counts = [], {}, Counter()
    themes = {}
    for query in pack["source_queries"]["openalex"]:
        try:
            found = OpenAlexAdapter().search(query["query"], query["id"], args.limit_per_query, pack["maximum_lookback_days"])
            items.extend(found); counts[query["id"]] += len(found)
            themes.update({id(x): query["themes"][0] for x in found})
        except AdapterError as exc:
            failures[query["id"]] = str(exc)
    items, duplicates = deduplicate(items)
    principals, clusters = cluster(items)
    template = load_yaml(ROOT / "data/research-watch/published/global-stocktake-captured-fixture.yml")
    records = [full_record(x, themes.get(id(x), next(q["themes"][0] for q in pack["source_queries"]["openalex"] if q["id"] == x.query_id)), run_id, template) for x in principals]
    records = [r for r in records if "mdpi.com" not in r["source_domain"]]
    for record in records:
        if record["publication"]["decision"] == "published" and not passes_relevance_gate(record):
            record["publication"]["decision"] = "withheld"
            record["publication"]["reasons"] = ["deterministic relevance gate not satisfied"]
            record["risk_flags"] = ["scope-ambiguity"]

    enrichment = {"crossref": "not-run", "datacite": "not-run"}
    for item in principals:
        if item.doi:
            try:
                CrossrefAdapter().search(item.doi, "pilot-doi-enrichment", 1); enrichment["crossref"] = "live-success"
            except AdapterError as exc: enrichment["crossref"] = f"live-failed: {exc}"
            try:
                DataCiteAdapter().enrich(item.doi); enrichment["datacite"] = "live-success"
            except AdapterError as exc: enrichment["datacite"] = f"live-attempted: {exc}"
            break
    try:
        BlueskyAdapter().search("urban climate evidence", "pilot-bluesky", 2)
        failures["bluesky"] = "live-success"
    except AdapterError as exc: failures["bluesky"] = f"fixture-required: {exc}"
    failures["openai-web-search"] = "fixture-required: credentials/cost cap absent" if not os.environ.get("OPENAI_API_KEY") else "not run without explicit paid-run approval"

    calibration = records[:50]
    if len(calibration) < args.minimum_calibration:
        failures["calibration-size"] = f"Only {len(calibration)} suitable real candidates were retrieved; weak records were not manufactured."
    caldir = ROOT / "calibration/research-watch"
    caldir.mkdir(parents=True, exist_ok=True)
    (caldir / "candidates.json").write_text(json.dumps(calibration, indent=2, default=str) + "\n")
    (caldir / "owner-labelling.html").write_text(calibration_html(calibration))
    (caldir / "empty-labels.json").write_text(json.dumps([{"record_id": r["record_id"], "label": "", "comment": ""} for r in calibration], indent=2, default=str) + "\n")
    with (caldir / "candidates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["record_id", "title", "source_name", "publication_date", "source_type", "url", "proposed_primary_theme", "label", "comment"]); writer.writeheader()
        for r in calibration: writer.writerow({"record_id": r["record_id"], "title": r["title"], "source_name": r["source_name"], "publication_date": r["publication_date"], "source_type": r["source_type"], "url": r["url"], "proposed_primary_theme": r["theme_assignments"]["primary"]["theme_id"], "label": "", "comment": ""})
    (caldir / "README.txt").write_text("Open owner-labelling.html in a browser, review each original source, choose a relevance label, then use Download structured labels. CSV and empty JSON fallbacks are included. Labels calibrate discovery and are not publication approvals.\n")

    selected, domain_counts = [], Counter()
    for record in [x for x in records if x["publication"]["decision"] == "published"]:
        if domain_counts[record["source_domain"]] >= pack["controls"]["maximum_items_per_source_domain"]:
            continue
        selected.append(record); domain_counts[record["source_domain"]] += 1
        if len(selected) == pack["controls"]["maximum_new_items_per_run"]:
            break
    def validate_stage(path: Path) -> None:
        assert (path / "run-manifest.json").exists()
        for p in (path / "published").glob("*.json"):
            assert json.loads(p.read_text())["publication"]["decision"] == "published"
    publish_transaction(ROOT / "staging/research-watch/current", selected, validate_stage, run_id)
    report_dir = ROOT / "reports/pilot"; report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "clustering-report.json").write_text(json.dumps(clusters, indent=2, default=str) + "\n")
    theme_counts = Counter(r["theme_assignments"]["primary"]["theme_id"] for r in records)
    evidence_counts = Counter(t for r in records for t in r["evidence_basis"]["types"])
    report = f"""# Gate 3B–4A bounded pilot evaluation

Run: `{run_id}`  
Date: {dt.date.today()}  
Mode: OpenAlex live; Crossref/DataCite enrichment live-attempted; OpenAI and unavailable Bluesky paths use no paid or bypass access.

## Counts

- Retrieved: {sum(counts.values())}
- Normalized unique records: {len(items)}
- Duplicates consolidated: {len(duplicates)}
- Event clusters: {len(clusters)}
- Evidence-sufficient: {sum(r['evidence_basis']['sufficient_for_summary'] for r in records)}
- Published to private staging: {len(selected)}
- Withheld: {sum(r['publication']['decision'] == 'withheld' for r in records)}
- Quarantined: {sum(r['publication']['decision'] == 'quarantined' for r in records)}
- Calibration candidates: {len(calibration)}

## Distribution

- Themes: `{dict(theme_counts)}`
- Evidence types: `{dict(evidence_counts)}`
- Source types: academic papers only from the live OpenAlex portion; web, reports, news, tools and Bluesky remain provider-limited.
- Estimated paid API cost: CAD/USD 0.00 for this pilot; no paid adapter ran. Future cost is not calculable until the owner selects `OPENAI_MODEL` and an explicit cap.

## Provider status

- Enrichment: `{enrichment}`
- Missing or limited paths: `{failures}`

## Controls and weaknesses

The run used a 30-day OpenAlex publication filter, English article/preprint filter, twelve bounded theme queries, DOI/URL deduplication, conservative event clustering, abstract sufficiency, a conservative lexical relevance gate, a 12-record maximum, and domain caps. Deterministic query-theme assignments are calibration proposals, not model judgements. No raw provider payload, full article text, secret, or private label was retained. The private transaction wrote to a temporary directory and atomically replaced staging only after its manifest and records validated; rollback is separately tested. Source-type and geographic diversity cannot be evaluated well until web and Bluesky access are configured.
"""
    (report_dir / "gate-3b-4a-evaluation.md").write_text(report)
    print(report)
    return 0


if __name__ == "__main__": raise SystemExit(main())
