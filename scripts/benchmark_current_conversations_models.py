#!/usr/bin/env python3
"""Small benchmark harness; never invents results when paid credentials are absent."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path

from jsonschema import Draft202012Validator

from current_conversations.adapters.openai_web import OpenAIWebSearchAdapter
from scripts.content import ROOT


def evaluate_captured(path: Path) -> dict:
    schema = json.loads((ROOT / "schemas/current-conversations-ai-output-v1.schema.json").read_text())
    payload = json.loads(path.read_text())
    rows = []
    for case in payload["cases"]:
        errors = list(Draft202012Validator(schema).iter_errors(case["output"]))
        rows.append({"case_id": case["case_id"], "schema_valid": not errors, "source_links_retained": case["source_url"] in case["retained_urls"], "captured_fixture": True})
    return {"cases": rows, "all_schema_valid": all(row["schema_valid"] for row in rows)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--captured", type=Path, default=ROOT / "tests/fixtures/openai-web/model-benchmark-captured.json")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/current-conversations/model-benchmark.md")
    parser.add_argument("--mock-response", type=Path, default=ROOT / "tests/fixtures/openai-web/responses-api-mock.json")
    args = parser.parse_args()
    result = evaluate_captured(args.captured)
    mock = json.loads(args.mock_response.read_text(encoding="utf-8"))
    mock_items = OpenAIWebSearchAdapter.parse_result(mock, limit=2)
    request = OpenAIWebSearchAdapter.request_body("urban climate delivery", "mock-model", 2)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    credential_state = "available" if os.environ.get("OPENAI_API_KEY") else "absent"
    report = f"""# Current Conversations model benchmark

Date: {dt.date.today()}  
Credential state: {credential_state}

The harness checks schema adherence and source-link retention using captured test
responses. It is not a live model comparison and does not establish latency, current
quality or actual cost.

- Captured cases: {len(result['cases'])}
- All captured outputs schema-valid: {result['all_schema_valid']}
- Mocked Responses payloads parsed: {len(mock_items)}
- Mocked source URLs retained: {mock_items[0]['original_url'] == 'https://example.org/original'}
- Responses tool type: {request['tools'][0]['type']}
- Strict structured output enabled: {request['text']['format']['strict']}
- Live models tested: 0
- Selected model: operationally unverified
- Paid cost: CAD 0.00

A live benchmark must compare relevance, source-link retention, grouping, summary
fidelity, latency and estimated cost under the CAD 2 run ceiling. The lowest-cost model
that passes every schema and fidelity criterion should then be written to the repository
variable `CURRENT_CONVERSATIONS_OPENAI_MODEL`.
"""
    args.output.write_text(report, encoding="utf-8")
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
