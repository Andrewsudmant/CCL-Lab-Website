#!/usr/bin/env python3
"""Run bounded discovery or an offline captured-fixture smoke test."""

from __future__ import annotations
import argparse
import json
from pathlib import Path
import yaml
from scripts.content import load_yaml
from research_watch.adapters.base import AdapterError
from research_watch.adapters.bluesky import BlueskyAdapter
from research_watch.adapters.crossref import CrossrefAdapter
from research_watch.adapters.openalex import OpenAlexAdapter
from research_watch.adapters.openai_web import OpenAIWebSearchAdapter
from research_watch.normalize import deduplicate

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = {"openalex": OpenAlexAdapter, "crossref": CrossrefAdapter, "bluesky": BlueskyAdapter, "openai_web_search": OpenAIWebSearchAdapter}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", choices=[*ADAPTERS, "fixture"], default="fixture")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.adapter == "fixture":
        records = [load_yaml(path) for path in sorted((ROOT / "data/research-watch/published").glob("*.yml"))]
        result = {"mode": "captured-fixture", "items": records, "network_calls": 0}
    else:
        pack = yaml.safe_load((ROOT / "config/query_packs/research-watch-v1.yml").read_text())
        query = pack["source_queries"][args.adapter][0]
        try:
            items, duplicates = deduplicate(ADAPTERS[args.adapter]().search(query["query"], query["id"], args.limit))
        except AdapterError as exc:
            print(f"Adapter unavailable: {exc}")
            return 2
        result = {"mode": "live-bounded", "adapter": args.adapter, "items": [i.public_dict() for i in items], "duplicates": duplicates}
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
