# Gate 4B–5A Current Conversations evaluation

- Run: `gate-4b-5a-fixture-only-20260817T185921Z`
- Mode: `fixture-only`
- Sources: 26
- Conversation clusters: 25
- Multi-source clusters: 1
- Standalone entries: 24
- Published fixture entries in private staging: 25
- Withheld fixture entries: 0
- Quarantined fixture entries: 0
- Duplicates consolidated into clusters: 1
- Calibration entries: 25
- Paid API cost: CAD 0.00
- Monthly owner ceiling remaining: CAD 20.00
- Source environments: `{'news-and-analysis': 4, 'academic-research': 8, 'policy-and-institutions': 6, 'blogs-and-commentary': 3, 'data-and-tools': 5}`
- Principal-source environments: `{'academic-research': 8, 'news-and-analysis': 3, 'policy-and-institutions': 6, 'blogs-and-commentary': 3, 'data-and-tools': 5}`
- Primary themes: `{'canadian-climate-policy': 3, 'evidence-infrastructure-tools': 10, 'climate-governance-delivery': 6, 'just-transitions-workforce': 2, 'co-benefits-place-based-valuation': 2, 'urban-climate-learning': 2}`
- Geographies: `{'canada': 3, 'global': 17, 'british-columbia': 2, 'europe': 4, 'united-kingdom': 1}`
- Evidence types: `{'permitted-excerpt': 4, 'abstract': 8, 'official-webpage-body': 9, 'data-or-tool-description': 5}`
- Principal-domain concentration: `{'doi.org': 8, 'www.axios.com': 1, 'www.canada.ca': 1, 'www.ubcm.ca': 1, 'berkeleyearth.org': 1, 'eu-mayors.ec.europa.eu': 1, 'coolcityindex.eu': 1, 'dataportalforcities.org': 1, 'apnews.com': 1, 'www.lemonde.fr': 1, 'www.c40.org': 2, 'www.climatecentral.org': 1, 'app.climatecentral.org': 1, 'climate.copernicus.eu': 1, 'www.syr.gov': 1, 'www.unep.org': 1, 'www.urban-climate.eu': 1}`
- Lab-affiliated principal sources: 0
- MDPI exclusions: 0
- Schema, link and model failures in fixture mode: 0
- API usage in fixture mode: 0 calls
- Staging write result: complete local atomic snapshot
- Rollback test: passed; last-known-good source, cluster, feed and site state preserved
- Provider diagnostics: `{}`

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
