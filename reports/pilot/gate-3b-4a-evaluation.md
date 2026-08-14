# Gate 3B–4A bounded pilot evaluation

Run: `gate-3b-4a-20260814T121957`  
Date: 2026-08-14  
Mode: OpenAlex live; Crossref/DataCite enrichment live-attempted; OpenAI and unavailable Bluesky paths use no paid or bypass access.

## Counts

- Retrieved: 48
- Normalized unique records: 35
- Duplicates consolidated: 13
- Event clusters: 35
- Evidence-sufficient: 34
- Published to private staging: 1
- Withheld: 34
- Quarantined: 0
- Calibration candidates: 35

## Distribution

- Themes: `{'urban-climate-learning': 7, 'climate-governance-delivery': 5, 'co-benefits-place-based-valuation': 8, 'just-transitions-workforce': 8, 'evidence-infrastructure-tools': 1, 'canadian-climate-policy': 6}`
- Evidence types: `{'abstract': 34, 'metadata-only': 1}`
- Source types: academic papers only from the live OpenAlex portion; web, reports, news, tools and Bluesky remain provider-limited.
- Estimated paid API cost: CAD/USD 0.00 for this pilot; no paid adapter ran. Future cost is not calculable until the owner selects `OPENAI_MODEL` and an explicit cap.

## Provider status

- Enrichment: `{'crossref': 'live-success', 'datacite': 'live-attempted: request failed for api.datacite.org: HTTP Error 404: Not Found'}`
- Missing or limited paths: `{'bluesky': 'fixture-required: request failed for public.api.bsky.app: HTTP Error 403: Forbidden', 'openai-web-search': 'fixture-required: credentials/cost cap absent'}`

## Controls and weaknesses

The run used a 30-day OpenAlex publication filter, English article/preprint filter, twelve bounded theme queries, DOI/URL deduplication, conservative event clustering, abstract sufficiency, a conservative lexical relevance gate, a 12-record maximum, and domain caps. Deterministic query-theme assignments are calibration proposals, not model judgements. No raw provider payload, full article text, secret, or private label was retained. The private transaction wrote to a temporary directory and atomically replaced staging only after its manifest and records validated; rollback is separately tested. Source-type and geographic diversity cannot be evaluated well until web and Bluesky access are configured.
