# Gate 4B–5A Current Conversations evaluation

- Run: `gate-4b-5a-fixture-only-20260817T183040Z`
- Mode: `fixture-only`
- Sources: 26
- Conversation clusters: 25
- Multi-source clusters: 1
- Calibration entries: 25
- Paid API cost: CAD 0.00
- Source environments: `{'news-and-analysis': 4, 'academic-research': 8, 'policy-and-institutions': 6, 'blogs-and-commentary': 3, 'data-and-tools': 5}`
- Primary themes: `{'canadian-climate-policy': 3, 'evidence-infrastructure-tools': 10, 'climate-governance-delivery': 6, 'just-transitions-workforce': 2, 'co-benefits-place-based-valuation': 2, 'urban-climate-learning': 2}`
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
