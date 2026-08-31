#!/usr/bin/env python3
"""Run bounded, no-key OpenAlex provider diagnostics and write an auditable report."""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

from current_conversations.adapters.base import AdapterError
from current_conversations.adapters.openalex import OpenAlexAdapter
from scripts.content import ROOT, load_yaml

STOPWORDS = {
    "a", "an", "and", "city", "climate", "for", "in", "municipal", "of",
    "or", "the", "to", "urban", "with",
}


def obvious_false_positive(query: str, title: str, abstract: str | None) -> bool:
    query_terms = {term for term in re.findall(r"[a-z]{4,}", query.casefold()) if term not in STOPWORDS}
    evidence_terms = set(re.findall(r"[a-z]{4,}", f"{title} {abstract or ''}".casefold()))
    return bool(query_terms) and not (query_terms & evidence_terms)


def main() -> int:
    pack = load_yaml(ROOT / "config/query_packs/current-conversations-v2.yml")
    rows: list[str] = []
    details: list[str] = []
    failures = 0
    adapter = OpenAlexAdapter()
    for configured in pack["queries"]["academic"]:
        query = configured["query"]
        query_id = configured["id"]
        lookback = 365
        limit = 2
        parameters = adapter.provider_parameters(query, limit=limit, lookback_days=lookback)
        try:
            items = adapter.search(query, f"diagnostic-{query_id}", limit=limit, lookback_days=lookback)
            false_positives = [item.title for item in items if obvious_false_positive(query, item.title, item.abstract)]
            reason = "none" if items else "No results in the bounded 365-day, English article/preprint window; the multi-concept query may be too narrow or indexed wording may differ."
            narrow = "yes—review before live use" if not items else "possible" if len(items) == 1 else "not obvious from count"
            old_assumption = "no"
            if configured["query_type"] == "facet" and configured["theme_intent"] is not None:
                old_assumption = "yes—facet forces a theme"
            rows.append(
                f"| `{query_id}` | {configured['query_type']} | `{configured['theme_intent']}` | {len(items)} | "
                f"{len(false_positives)} | {narrow} | {old_assumption} | pass |"
            )
            item_rows = "\n".join(
                f"- `{item.platform_identifier or item.doi or 'no identifier'}` — {item.title}"
                for item in items
            ) or "- No results."
            details.extend([
                f"## `{query_id}`",
                "",
                f"- Query: `{query}`",
                f"- Actual provider parameters: `{json.dumps(parameters, sort_keys=True)}`",
                f"- Result count: {len(items)}",
                f"- Query errors: none",
                f"- Obvious false positives by conservative token-overlap check: {len(false_positives)}" + (f" — {'; '.join(false_positives)}" if false_positives else ""),
                f"- Obvious reason for zero results: {reason}",
                f"- Appears too narrow: {narrow}",
                f"- Appears to reproduce an old-theme assumption: {old_assumption}",
                "- Returned records:",
                item_rows,
                "",
            ])
        except AdapterError as exc:
            failures += 1
            rows.append(f"| `{query_id}` | {configured['query_type']} | `{configured['theme_intent']}` | 0 | n/a | unknown | no | fail: {type(exc).__name__} |")
            details.extend([
                f"## `{query_id}`", "",
                f"- Query: `{query}`",
                f"- Actual provider parameters: `{json.dumps(parameters, sort_keys=True)}`",
                f"- Query errors: {type(exc).__name__}; provider message deliberately not copied into public diagnostics.",
                "- Result interpretation: unavailable because the request failed.", "",
            ])
    report = ROOT / "reports/current-conversations/openalex-four-theme-diagnostics-gate-5c.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "# OpenAlex four-theme no-key diagnostics — Gate 5C\n\n"
        f"Run date: {dt.date.today().isoformat()}\n\n"
        "Credential use: none\n\n"
        "Scope: up to two provider-native results for every active academic query, using a 365-day diagnostic lookback. The production query pack retains its 30-day bound.\n\n"
        "| Query | Type | Theme intent | Results | Obvious false positives | Too narrow? | Old-theme assumption? | Status |\n"
        "|---|---|---|---:|---:|---|---|---|\n" + "\n".join(rows) + "\n\n"
        "This is a connectivity and query-shape diagnostic, not a measure of scientific relevance, completeness or a final calibration set. False-positive notes are conservative heuristics and require human calibration.\n\n"
        + "\n".join(details),
        encoding="utf-8",
    )
    print(report.resolve())
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
