# Cities & Climate Learning Lab — Gate 4B–5A handoff

## What changed and why

The active public feature is now **Current Conversations**. The former “Research Watch” name implied a literature-only feed; the new model can show a discussion supported by academic research, official policy, news, institutional analysis, commentary and data tools without pretending those sources have equal evidentiary roles. Accessible former-route pages remain, while historical reports retain their original terminology.

The repository now separates canonical source records from conversation clusters, validates both with JSON Schema, records the principal-source rationale and grouping history, renders source roles and limitations, and emits JSON Feed and RSS. A 26-source/25-cluster captured fixture exercises all six themes and five source environments; one cluster groups an official announcement with independent reporting. Fixtures are clearly labelled and are not evidence of live provider coverage.

Publications now have a complete 36-record verified inventory and a smaller 10-record selected view. Twenty ORCID-only candidates remain unresolved rather than being guessed. One verified MDPI item is retained in the complete inventory but is explicitly ineligible for Current Conversations and not featured.

## Challenges and decisions

No OpenAI credentials, approved model selection or current-conversations remote was available. The paid adapter was therefore not called. A captured structured-output benchmark documents the schema behavior but cannot establish live model performance. Web/news/tool examples are captured fixtures, and Bluesky/DataCite coverage remains provider-limited. This honest limitation is safer than manufacturing a “live” result.

The migration had to retain traceability while changing the public unit from an item to a cluster. Source IDs are never collapsed into cluster IDs; linked sources remain individually inspectable. Historical Gate 3B–4A calibration files moved to regression fixtures unchanged.

## Transparent and traceable governance

- AI is discovery/annotation infrastructure, never a cited authority.
- Every source retains identity, URL, dates, stable identifier where available, evidence basis, adapter/query/run provenance, review and correction state.
- Every cluster records principal/linked sources, grouping confidence/rationale, themes, limitations, uncertainty, decision and change history.
- Unreviewed entries say **“Identified and summarized using AI · not reviewed by the lab”** and the landing page says inclusion does not imply endorsement.
- Paid search fails closed unless credentials, model, fresh currency rate, call/item caps and the CAD 2/run and CAD 20/month ceilings all validate.
- A complete snapshot validates before atomic private-staging replacement; failure preserves last-known-good state.
- The scheduled workflow is read-only by default. Its disabled write job can target only `automation/current-conversations-staging` after an exact path allowlist check. It cannot deploy or write to `main`.
- Corrections/removals cannot be silent, and control-plane changes require pull-request review.

## Known limitations and placeholders

- Live OpenAI/model choice and real cost remain unverified; recorded cost for this gate is CAD 0.00.
- There is no repository remote, staging branch on a host, branch protection or production deployment.
- Captured fixture dates outside the nominal lookback are retained only to test display/calibration and say so in their limitations.
- Bluesky access returned a provider limitation in the prior bounded diagnostic; no bypass was attempted.
- Twenty publication candidates need authoritative identifier reconciliation.
- All representative research-scope examples remain owner-review placeholders by design.

## Owner decisions before Gate 5B/production

1. Approve the Current Conversations name, disclosure, source-role hierarchy and whether fixtures should appear only in private previews.
2. Choose an OpenAI model only after a small live benchmark is authorized; confirm CAD ceilings, exchange-rate source and alert thresholds.
3. Decide which repository/remote will host the private automation branch and configure branch protections and environment secrets.
4. Label the 25-entry calibration pack for relevance and grouping quality; set acceptable precision, duplicate and diversity thresholds.
5. Resolve or explicitly omit the 20 publication candidates and confirm the selected 10.
6. Approve a correction/removal contact workflow, feed base URL and production hosting plan before deployment.

Gate status: `GATE_4B_5A_PASS_WITH_PROVIDER_OR_REMOTE_LIMITATIONS`. No merge, push, deployment or DNS change was made.
