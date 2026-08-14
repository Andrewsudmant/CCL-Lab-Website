# Research Watch bounded pilot evaluation

Run date: 2026-08-14  
Query pack: `research-watch-v1` version 1.0.0  
Public feed input: captured fixture only

## Outcome

| Adapter | Requested | Returned | Clearly in scope | Outcome |
|---|---:|---:|---:|---|
| OpenAlex | 3 | 3 | 0 | Network and normalization worked; query interpretation was too broad. |
| Crossref | 3 | 3 | 0 | Network and normalization worked; the placeholder enrichment query is not suitable for discovery. |
| Bluesky | 3 | 0 | 0 | Public AppView request received CDN-level HTTP 403 from this environment. |
| OpenAI web search | 3 | 0 | 0 | `OPENAI_API_KEY` was absent; adapter exited before making a request. |
| Captured fixture | 1 | 1 | 1 | Deterministic validation and publication controls passed. |

The six live academic results were manually labelled for this small diagnostic only.
Precision at three was 0.00 for both OpenAlex and Crossref; recall cannot be estimated
without a defined reference corpus. This is a query-design failure, not evidence that
either provider is unsuitable.

## Quality and diversity observations

- The raw source mix was academic-only because the web and social adapters were
  unavailable. It does not satisfy the configured diversity target.
- OpenAlex returned older, high-citation climate papers unrelated to cities or policy
  learning. Query tokens must be translated into provider-native filters rather than
  sent as a Boolean-looking free-text string.
- Crossref should primarily enrich known DOIs. If used for discovery, it needs separate,
  topical query strings and date filters.
- The captured record has adequate abstract and webpage evidence, but it is authored
  by the lab lead. The visible `conflict-of-interest` flag is therefore retained.
- No live result was promoted to the public fixture. Raw pilot outputs are reports,
  not public records.

## Required changes before an unattended run

1. Add provider-specific query syntax and explicit `from_publication_date` filters.
2. Establish a 30–50 item owner-labelled evaluation set spanning all six themes.
3. Test Bluesky from GitHub Actions or another approved network path; do not bypass
   the CDN control.
4. Configure an OpenAI project secret in GitHub only after the owner approves budget,
   model and retention settings.
5. Require the source-type diversity threshold before any batch is considered healthy.
6. Add event clustering and a full record-assembly stage before unattended publishing.

## Reproducibility

Provider-neutral outputs are stored beside this report. They omit raw provider payloads.
The public fixture is generated with:

```sh
PYTHONPATH=. .venv/bin/python -m research_watch.run --adapter fixture \
  --output reports/pilot/captured-fixture-run.json
```

Live calls are opt-in through `--adapter`; no adapter runs merely because the site builds.
