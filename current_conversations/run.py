#!/usr/bin/env python3
"""Run one explicit bounded adapter or the network-free mixed-source fixture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from current_conversations.adapters.base import AdapterError
from current_conversations.adapters.bluesky import BlueskyAdapter
from current_conversations.adapters.crossref import CrossrefAdapter
from current_conversations.adapters.openai_web import OpenAIWebSearchAdapter
from current_conversations.adapters.openalex import OpenAlexAdapter
from current_conversations.normalize import deduplicate

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = {"openalex": OpenAlexAdapter, "crossref": CrossrefAdapter, "bluesky": BlueskyAdapter, "openai_web_search": OpenAIWebSearchAdapter}


def query_for(adapter: str, query_id: str | None) -> dict:
    pack = yaml.safe_load((ROOT / "config/query_packs/current-conversations-v1.yml").read_text())
    group = "academic" if adapter in {"openalex", "crossref"} else "bluesky" if adapter == "bluesky" else "web"
    queries = pack["queries"][group]
    if query_id:
        match = next((query for query in queries if query["id"] == query_id), None)
        if not match:
            raise AdapterError(f"query ID {query_id} is not configured for {adapter}")
        return match
    return queries[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", choices=[*ADAPTERS, "fixture"], default="fixture")
    parser.add_argument("--query-id")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.adapter == "fixture":
        source_dir = ROOT / "data/current-conversations/generated/sources"
        records = [json.loads(path.read_text()) for path in sorted(source_dir.glob("*.json"))]
        result = {"mode": "captured-mixed-source-fixture", "items": records, "network_calls": 0, "fixtures_explicit": True}
    else:
        try:
            query = query_for(args.adapter, args.query_id)
            items, duplicates = deduplicate(ADAPTERS[args.adapter]().search(query["query"], query["id"], min(args.limit, query["result_limit"])))
        except AdapterError as exc:
            print(f"Adapter unavailable: {exc}")
            return 2
        result = {"mode": "live-bounded", "adapter": args.adapter, "query_id": query["id"], "items": [item.public_dict() for item in items], "duplicates": duplicates}
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
