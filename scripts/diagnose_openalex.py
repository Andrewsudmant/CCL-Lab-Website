#!/usr/bin/env python3
"""Run bounded, no-key OpenAlex provider diagnostics and write an auditable report."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from current_conversations.adapters.base import AdapterError
from current_conversations.adapters.openalex import OpenAlexAdapter
from scripts.content import ROOT, load_yaml


def main() -> int:
    scope = load_yaml(ROOT / "config/research_scope.yml")
    rows: list[str] = []
    failures = 0
    adapter = OpenAlexAdapter()
    for theme in scope["themes"]:
        concepts = theme["initial_search_concepts"][:3]
        query = " OR ".join(f'"{concept}"' if " " in concept else concept for concept in concepts)
        try:
            items = adapter.search(query, f"diagnostic-{theme['id']}", limit=2, lookback_days=365)
            identifiers = ", ".join(item.platform_identifier or item.doi or "no identifier" for item in items) or "no results"
            rows.append(f"| {theme['name']} | `{query}` | {len(items)} | {identifiers} | pass |")
        except AdapterError as exc:
            failures += 1
            rows.append(f"| {theme['name']} | `{query}` | 0 | none | fail: {type(exc).__name__} |")
    report = ROOT / "reports/current-conversations/openalex-no-key-diagnostics.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "# OpenAlex no-key diagnostics\n\n"
        f"Run date: {dt.date.today().isoformat()}\n\n"
        "Credential use: none\n\n"
        "Scope: two provider-native results per research theme, 365-day lookback.\n\n"
        "| Theme | Provider-native query | Results | OpenAlex/DOI identifiers | Status |\n"
        "|---|---|---:|---|---|\n" + "\n".join(rows) + "\n\n"
        "This is a connectivity and query-shape diagnostic, not a relevance benchmark or final calibration set.\n",
        encoding="utf-8",
    )
    print(report.resolve())
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
