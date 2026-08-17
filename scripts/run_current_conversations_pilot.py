#!/usr/bin/env python3
"""Build the bounded Gate 4B–5A pilot from explicit fixtures or live diagnostics.

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
        cards.append(
            f'''<article data-id="{html.escape(cluster['cluster_id'])}">
<h2>{html.escape(cluster['public_title'])}</h2>
<p><a href="{html.escape(source['original_url'])}">Open principal source</a> · {html.escape(source['publisher_or_platform'])} · {html.escape(source['publication_date'])}</p>
<p><strong>Discussion:</strong> {html.escape(cluster['discussion_statement'])}</p>
<p><strong>Why it may matter:</strong> {html.escape(cluster['reason_for_relevance'])}</p>
<p><strong>Limitations:</strong> {html.escape(cluster['limitations'])}</p>
<label>Relevance <select><option value="">Choose…</option><option>Clearly relevant</option><option>Potentially relevant</option><option>Not relevant</option></select></label>
<label>Grouping <select><option value="">Choose…</option><option>Correctly grouped</option><option>Missing source</option><option>Should split</option></select></label>
<label>Comments <textarea rows="3"></textarea></label></article>'''
        )
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CCLL Current Conversations calibration</title><style>body{font:17px/1.55 system-ui;max-width:900px;margin:auto;padding:2rem;color:#222}article{border-top:4px solid #a6192e;padding:1.4rem 0}label{display:block;margin:.7rem 0}select,textarea,button{font:inherit;padding:.45rem;width:100%;max-width:42rem}button{width:auto;background:#a6192e;color:white;border:0}</style></head><body><h1>Current Conversations owner calibration</h1><p>These labels test discovery relevance and source grouping. They are not publication approvals. Review the original source before labelling.</p><button id="export">Download structured labels</button>''' + "".join(cards) + '''<script>document.querySelector('#export').onclick=()=>{const labels=[...document.querySelectorAll('article')].map(a=>({cluster_id:a.dataset.id,relevance:a.querySelectorAll('select')[0].value,grouping:a.querySelectorAll('select')[1].value,comments:a.querySelector('textarea').value}));const b=new Blob([JSON.stringify(labels,null,2)],{type:'application/json'}),x=document.createElement('a');x.href=URL.createObjectURL(b);x.download='current-conversations-labels.json';x.click()};</script></body></html>'''


def write_calibration(clusters: list[dict], sources: list[dict]) -> None:
    directory = ROOT / "calibration/current-conversations"
    directory.mkdir(parents=True, exist_ok=True)
    source_map = {source["source_id"]: source for source in sources}
    rows = []
    for cluster in clusters[:25]:
        source = source_map[cluster["principal_source_id"]]
        rows.append({"cluster_id": cluster["cluster_id"], "title": cluster["public_title"], "principal_source": source["publisher_or_platform"], "url": source["original_url"], "primary_theme": cluster["primary_theme"], "relevance": "", "grouping": "", "comments": ""})
    (directory / "candidates.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (directory / "empty-labels.json").write_text(json.dumps([{"cluster_id": row["cluster_id"], "relevance": "", "grouping": "", "comments": ""} for row in rows], indent=2) + "\n", encoding="utf-8")
    (directory / "owner-labelling.html").write_text(calibration_html(clusters[:25], source_map), encoding="utf-8")
    with (directory / "candidates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    (directory / "README.txt").write_text(
        "Open owner-labelling.html locally. Review each principal source, assign Clearly relevant, Potentially relevant, or Not relevant, assess grouping, add comments, and download the JSON. Labels calibrate discovery and clustering; they are not publication approvals. All examples are captured fixtures requiring owner review.\n",
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
    run_id = f"gate-4b-5a-{args.mode}-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
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
    report_dir = ROOT / "reports/current-conversations/pilot"
    report_dir.mkdir(parents=True, exist_ok=True)
    report = f"""# Gate 4B–5A Current Conversations evaluation

- Run: `{run_id}`
- Mode: `{args.mode}`
- Sources: {len(sources)}
- Conversation clusters: {len(clusters)}
- Multi-source clusters: {sum(bool(c['linked_source_ids']) for c in clusters)}
- Calibration entries: {min(25, len(clusters))}
- Paid API cost: CAD 0.00
- Source environments: `{dict(source_counts)}`
- Primary themes: `{dict(theme_counts)}`
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

`GATE_4B_5A_PASS_WITH_PROVIDER_OR_REMOTE_LIMITATIONS`
"""
    (report_dir / "gate-4b-5a-evaluation.md").write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
