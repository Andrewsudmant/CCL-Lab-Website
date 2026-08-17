#!/usr/bin/env python3
"""Bounded availability recheck; writes a report and never deletes records."""
from __future__ import annotations
import argparse, datetime as dt, json, urllib.error, urllib.request
from pathlib import Path
from research_watch.transaction import recheck_status
from scripts.content import ROOT


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--network", action="store_true"); parser.add_argument("--limit", type=int, default=12); args = parser.parse_args()
    rows = []
    for path in sorted((ROOT / "staging/research-watch/current/published").glob("*.json"))[:args.limit]:
        record = json.loads(path.read_text()); status = None; final = record["url"]
        if args.network:
            try:
                request = urllib.request.Request(record["url"], method="HEAD", headers={"User-Agent": "CCLL-Research-Watch/1.0"})
                with urllib.request.urlopen(request, timeout=15) as response: status, final = response.status, response.url
            except urllib.error.HTTPError as exc: status = exc.code
            except Exception: status = None
        rows.append({"record_id": record["record_id"], "url": record["url"], "http_status": status, "final_url": final, "availability": recheck_status(status, final != record["url"]) if args.network else "not-checked-offline"})
    output = ROOT / "reports/pilot/availability-recheck.json"; output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"checked_at": dt.datetime.now(dt.timezone.utc).isoformat(), "network": args.network, "records": rows}, indent=2) + "\n")
    print(output.resolve()); return 0
if __name__ == "__main__": raise SystemExit(main())
