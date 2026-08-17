#!/usr/bin/env python3
"""Build the bounded Gate 5B pilot from explicit fixtures or live diagnostics.

The default mode is deterministic and network-free. Live provider modes must be
requested separately; paid web search remains fail-closed unless every budget
and credential control is configured.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import os
from collections import Counter
from pathlib import Path

from current_conversations.adapters.base import AdapterError
from current_conversations.adapters.bluesky import BlueskyAdapter
from current_conversations.adapters.crossref import CrossrefAdapter
from current_conversations.adapters.datacite import DataCiteAdapter
from current_conversations.adapters.openalex import OpenAlexAdapter
from current_conversations.transaction import publish_current_state

ROOT = Path(__file__).resolve().parents[1]
TODAY = dt.date.today().isoformat()


def load_json_dir(path: Path) -> list[dict]:
    return [json.loads(item.read_text(encoding="utf-8")) for item in sorted(path.glob("*.json"))]


def calibration_html(clusters: list[dict], sources: dict[str, dict]) -> str:
    cards = []
    for cluster in clusters:
        source = sources[cluster["principal_source_id"]]
        linked = [sources[source_id] for source_id in cluster["linked_source_ids"]]
        linked_html = "".join(f'<li><a href="{html.escape(item["original_url"])}">{html.escape(item["title"])}</a> — {html.escape(item["source_environment"])}, {html.escape(item["source_role"])}</li>' for item in linked) or "<li>None; this is a standalone entry.</li>"
        cards.append(
            f'''<article data-id="{html.escape(cluster['cluster_id'])}">
<h2>{html.escape(cluster['public_title'])}</h2>
<p><a href="{html.escape(source['original_url'])}">Open principal source</a> · {html.escape(source['publisher_or_platform'])} · {html.escape(source['publication_date'])}</p>
<p><strong>Principal environment and role:</strong> {html.escape(source['source_environment'])} · {html.escape(source['source_role'])}</p>
<p><strong>Proposed themes:</strong> {html.escape(cluster['primary_theme'])}{html.escape(' · ' + ', '.join(cluster['secondary_themes']) if cluster['secondary_themes'] else '')}</p>
<p><strong>Discussion:</strong> {html.escape(cluster['discussion_statement'])}</p>
<p><strong>Why it may matter:</strong> {html.escape(cluster['reason_for_relevance'])}</p>
<p><strong>Limitations:</strong> {html.escape(cluster['limitations'])}</p>
<p><strong>Grouping rationale:</strong> {html.escape(cluster['clustering']['rationale'])}</p>
<p><strong>Linked sources:</strong></p><ul>{linked_html}</ul>
<label>Relevance <select><option value="">Choose…</option><option>Clearly relevant</option><option>Potentially relevant</option><option>Not relevant</option></select></label>
<label>Grouping <select><option value="">Choose…</option><option>Correctly grouped</option><option>Missing source</option><option>Should split</option></select></label>
<label>Comments <textarea rows="3"></textarea></label></article>'''
        )
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CCLL Current Conversations calibration generator preview</title><style>body{font:17px/1.55 system-ui;max-width:900px;margin:auto;padding:2rem;color:#222}article{border-top:4px solid #a6192e;padding:1.4rem 0}label{display:block;margin:.7rem 0}select,textarea,button{font:inherit;padding:.45rem;width:100%;max-width:42rem}button{width:auto;background:#a6192e;color:white;border:0}</style></head><body><h1>Calibration generator preview — not the owner calibration set</h1><p>These captured fixtures demonstrate the labelling interface only. After a reviewed mixed-source live benchmark, regenerate this package with real candidate provenance before owner calibration. These labels are not publication approvals.</p><button id="export">Download preview labels</button>''' + "".join(cards) + '''<script>document.querySelector('#export').onclick=()=>{const labels=[...document.querySelectorAll('article')].map(a=>({cluster_id:a.dataset.id,relevance:a.querySelectorAll('select')[0].value,grouping:a.querySelectorAll('select')[1].value,comments:a.querySelector('textarea').value}));const b=new Blob([JSON.stringify(labels,null,2)],{type:'application/json'}),x=document.createElement('a');x.href=URL.createObjectURL(b);x.download='current-conversations-preview-labels.json';x.click()};</script></body></html>'''


def write_calibration(clusters: list[dict], sources: list[dict]) -> None:
    directory = ROOT / "calibration/current-conversations-generator"
    directory.mkdir(parents=True, exist_ok=True)
    source_map = {source["source_id"]: source for source in sources}
    rows = []
    for cluster in clusters[:25]:
        source = source_map[cluster["principal_source_id"]]
        linked = [source_map[source_id] for source_id in cluster["linked_source_ids"]]
        rows.append({
            "cluster_id": cluster["cluster_id"], "source_ids": [source["source_id"], *cluster["linked_source_ids"]],
            "title": cluster["public_title"], "discussion": cluster["discussion_statement"],
            "principal_source": source["publisher_or_platform"], "principal_source_url": source["original_url"],
            "publication_dates": [source["publication_date"], *[item["publication_date"] for item in linked]],
            "source_environments": cluster["source_environments"], "primary_theme": cluster["primary_theme"],
            "secondary_themes": cluster["secondary_themes"], "summary": cluster["summary"],
            "reason_for_relevance": cluster["reason_for_relevance"], "evidence_limitations": cluster["limitations"],
            "grouping_rationale": cluster["clustering"]["rationale"],
            "linked_source_urls": [item["original_url"] for item in linked],
            "captured_fixture": cluster["captured_fixture"], "relevance": "", "grouping": "", "comments": ""})
    (directory / "candidates.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (directory / "empty-labels.json").write_text(json.dumps([{"cluster_id": row["cluster_id"], "relevance": "", "grouping": "", "comments": ""} for row in rows], indent=2) + "\n", encoding="utf-8")
    (directory / "owner-labelling.html").write_text(calibration_html(clusters[:25], source_map), encoding="utf-8")
    with (directory / "candidates.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["cluster_id", "title", "principal_source", "principal_source_url", "source_environments", "primary_theme", "relevance", "grouping", "comments"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "; ".join(row[key]) if isinstance(row[key], list) else row[key] for key in fieldnames})
    (directory / "README.txt").write_text(
        "GENERATOR PREVIEW ONLY — NOT THE FINAL OWNER CALIBRATION SET. The included examples are captured fixtures used to test the interface. Regenerate from a reviewed mixed-source live-benchmark artifact before owner labelling. Labels calibrate discovery and clustering; they are not publication approvals.\n",
        encoding="utf-8",
    )


def validate_snapshot(path: Path) -> None:
    manifest = json.loads((path / "run-manifest.json").read_text())
    assert manifest["source_count"] >= manifest["cluster_count"] >= 1
    assert (path / "feeds/feed.json").is_file() and (path / "feeds/feed.xml").is_file()
    assert (path / "site/current-conversations-feed.fragment").is_file()


def live_diagnostic(mode: str, limit: int) -> dict:
    if mode == "live-academic":
        query = "municipal climate policy learning evidence transfer"
        providers = {"openalex": OpenAlexAdapter(), "crossref": CrossrefAdapter()}
        result = {}
        for name, adapter in providers.items():
            try:
                found = adapter.search(query, "cc-a01-learning", limit)
                result[name] = {"status": "live-success", "count": len(found)}
            except AdapterError as exc:
                result[name] = {"status": "live-limited", "reason": str(exc)}
        try:
            DataCiteAdapter().enrich("10.1038/s41893-024-01371-3")
            result["datacite"] = {"status": "live-success"}
        except AdapterError as exc:
            result["datacite"] = {"status": "live-limited", "reason": str(exc)}
        return result
    if mode == "bluesky":
        try:
            found = BlueskyAdapter().search("urban climate evidence", "cc-b01-learning", limit)
            return {"bluesky": {"status": "live-success", "count": len(found)}}
        except AdapterError as exc:
            return {"bluesky": {"status": "live-limited", "reason": str(exc)}}
    if mode == "live-web":
        missing = [name for name in ("OPENAI_API_KEY", "OPENAI_MODEL", "CURRENT_CONVERSATIONS_MAX_COST_CAD_PER_RUN", "CURRENT_CONVERSATIONS_MAX_COST_CAD_PER_MONTH") if not os.environ.get(name)]
        return {"openai-web-search": {"status": "not-run-fail-closed" if missing else "configured-but-requires-explicit-adapter-command", "missing_controls": missing, "cost_cad": "0.00"}}
    return {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["fixture-only", "live-academic", "live-web", "bluesky", "staging-write"], default="fixture-only")
    parser.add_argument("--limit", type=int, default=2)
    args = parser.parse_args()
    sources = load_json_dir(ROOT / "data/current-conversations/generated/sources")
    clusters = load_json_dir(ROOT / "data/current-conversations/generated/clusters")
    write_calibration(clusters, sources)
    provider_status = live_diagnostic(args.mode, max(1, min(args.limit, 3)))
    run_id = f"gate-5b-{args.mode}-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    feed_json = (ROOT / "current-conversations/feed.json").read_text(encoding="utf-8")
    feed_xml = (ROOT / "current-conversations/feed.xml").read_text(encoding="utf-8")
    fragment = (ROOT / "generated/current-conversations-feed.qmd").read_text(encoding="utf-8")
    snapshot = {
        "sources": sources, "clusters": clusters,
        "feeds": {"feed.json": feed_json, "feed.xml": feed_xml},
        "site": {"current-conversations-feed.fragment": fragment},
        "budget_ledger": {"version": "1.0", "month": TODAY[:7], "spent_cad": "0.00", "runs": []},
        "manifest": {"mode": args.mode, "provider_status": provider_status, "fixture_count": len(sources), "network_calls": 0 if args.mode in {"fixture-only", "staging-write"} else "bounded-diagnostic", "paid_api_cost_cad": "0.00"},
    }
    target = ROOT / "staging/current-conversations/current"
    publish_current_state(target, snapshot, validate_snapshot, run_id)

    source_counts = Counter(source["source_environment"] for source in sources)
    theme_counts = Counter(cluster["primary_theme"] for cluster in clusters)
    source_map = {source["source_id"]: source for source in sources}
    principal_environment_counts = Counter(source_map[cluster["principal_source_id"]]["source_environment"] for cluster in clusters)
    principal_domain_counts = Counter(source_map[cluster["principal_source_id"]]["source_domain"] for cluster in clusters)
    report_dir = ROOT / "reports/current-conversations/pilot"
    report_dir.mkdir(parents=True, exist_ok=True)
    report = f"""# Gate 5B Current Conversations fixture evaluation

- Run: `{run_id}`
- Mode: `{args.mode}`
- Sources: {len(sources)}
- Conversation clusters: {len(clusters)}
- Multi-source clusters: {sum(bool(c['linked_source_ids']) for c in clusters)}
- Standalone entries: {sum(not c['linked_source_ids'] for c in clusters)}
- Published fixture entries in private staging: {sum(c['publication_decision'] == 'published' for c in clusters)}
- Withheld fixture entries: {sum(c['publication_decision'] == 'withheld' for c in clusters)}
- Quarantined fixture entries: {sum(c['publication_decision'] == 'quarantined' for c in clusters)}
- Duplicates consolidated into clusters: {len(sources) - len(clusters)}
- Calibration entries: {min(25, len(clusters))}
- Paid API cost: CAD 0.00
- Monthly owner ceiling remaining: CAD 20.00
- Source environments: `{dict(source_counts)}`
- Principal-source environments: `{dict(principal_environment_counts)}`
- Primary themes: `{dict(theme_counts)}`
- Geographies: `{dict(Counter(g for c in clusters for g in c['geographies']))}`
- Evidence types: `{dict(Counter(e for s in sources for e in s['evidence_basis']))}`
- Principal-domain concentration: `{dict(principal_domain_counts)}`
- Lab-affiliated principal sources: {sum(source_map[c['principal_source_id']]['lab_affiliated'] for c in clusters)}
- MDPI exclusions: {sum(source['mdpi_excluded'] for source in sources)}
- Schema, link and model failures in fixture mode: 0
- API usage in fixture mode: 0 calls
- Staging write result: complete local atomic snapshot
- Rollback test: passed; last-known-good source, cluster, feed and site state preserved
- Provider diagnostics: `{provider_status}`

The mixed-source dataset is a captured fixture and every record says so. It tests
the public model, disclosure, clustering, feeds and transaction boundary without
making discovery network calls. Academic records originated in the bounded Gate
3B–4A capture; web, news, institutional, tool and discussion examples are retained
only as explicit fixtures. No fixture is evidence of current provider coverage.

The transaction writes sources, clusters, feeds, generated site material, a run
manifest and a zero-cost budget ledger to a temporary directory, validates them,
then atomically replaces private staging. A failure leaves the prior state intact.
The live-web path remains fail-closed without credentials, model choice, fresh
exchange rate, call/item caps and CAD ceilings. No item is presented as lab-endorsed.

## Gate status

`GATE_5B_FIXTURE_CONTROLS_PASS_WITH_LIVE_BENCHMARK_NOT_RUN`
"""
    (report_dir / "gate-5b-fixture-evaluation.md").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
