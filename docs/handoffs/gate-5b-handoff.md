# Cities & Climate Learning Lab — Gate 5B handoff

## What we completed and why

Gate 5B turns the Gate 4B–5A prototype into a credential-ready, reviewable live-benchmark candidate without making a paid call or deploying anything. The existing Gate 0–5A Git history was preserved on `codex/gate-5b-live-current-conversations`; the target GitHub remote was added only after a repository- and history-wide secret scan found no credential patterns.

The verified publication inventory now has 46 records. It includes the Nature paper **“From urban climate ambition to delivery: a framework of climate delivery modes”**, published 3 August 2026 with DOI `10.1038/s44168-026-00408-9`. Nine ORCID-only outputs were resolved through university repositories, public institutions or commissioning organisations. One ORCID entry was excluded because the authoritative LSE record does not list Andrew Sudmant as an author. Ten records remain withheld because authoritative metadata is still insufficient. The former “Complete publication record” page is now **“Verified publications and outputs.”**

Current Conversations now groups cross-source evidence using DOI, canonical URL, underlying-source and explicit citation links, platform identifiers, and corroborated organisation-plus-title evidence. A bounded model can suggest a pair but cannot make the merge; deterministic evidence must accept it. Fixture pages with `ai_provenance.used=false` now explicitly say that no AI generation was recorded, so the public prototype no longer attributes fixture summaries to AI.

The OpenAI Responses adapter uses the current `web_search` tool and a strict JSON schema, retains original/underlying links, treats retrieved instructions as untrusted, flags common prompt-injection language and validates output again locally. Missing secret, stale/missing controls, a corrupt ledger or an over-budget estimate all fail before publication. The mocked benchmark ran with CAD 0.00; no OpenAI request was made.

The new GitHub Actions workflow is named **Current Conversations live benchmark**. It is manual, uses protected environment `live-benchmark`, expects `OPENAI_API_KEY` only from that environment, has `contents: read`, and writes artifacts only. Repository writes remain in a different job with `contents: write`, an explicit opt-in variable, validation, a changed-path allowlist and the private `automation/current-conversations-staging` target. Neither workflow deploys.

## Challenges and how they were handled

- The target GitHub repository was empty, while the valuable history was local. A local `main` reference was created at the exact Gate 4B–5A tip so no gate commit would be flattened or reconstructed. HTTPS publication is still blocked because this machine has neither an authenticated Git credential nor the `gh` CLI; no credential was requested or inspected.
- The August paper had not yet appeared in Andrew’s ORCID feed. The Nature publisher page supplied the title, authors, exact date, DOI, version notice and licence, so it was added through a visible authoritative override instead of waiting silently or fabricating an ORCID link.
- Many historic reports have no DOI. Only records with institutional, publisher or commissioning evidence were promoted; unresolved records remain in CSV rather than disappearing.
- Narrow OpenAlex provider-native queries returned zero results for two themes. The diagnostic records those gaps and does not quietly broaden scope. The other four themes returned bounded results, confirming the no-key path operates.
- A true numeric 200% zoom control was not exposed by the in-app browser. The review used a 720 × 450 CSS viewport as the equivalent reflow pressure, labelled it accurately, and separately inspected 1440 × 900 and 390 × 844 layouts.

## Transparent and traceable governance

Every publication override names its authoritative source and retrieval date. Provider conflicts and unresolved ORCID entries remain visible. Current Conversations source and cluster IDs, original/canonical links, dates, evidence limitations, adapter/query provenance, model/prompt provenance when actually used, review status, risk flags and correction history remain schema-controlled.

Public disclosure is computed from record provenance. Model-assisted clustering is proposal-only and every accepted cluster retains deterministic evidence and principal-source rationale. The budget ledger records conservative CAD cost and aggregate provider usage, while secret values and raw provider responses are excluded from the repository and handoff. Transactional staging validates a complete snapshot before replacement; failures preserve last-known-good state. Control-plane changes still require a pull request.

## Verification status

- Content validation: passed for 70 canonical source records and 15 schemas.
- Automated tests: 80 passed; one historical deprecation warning remains for the compatibility `research_watch` import.
- Full Quarto build: passed for 98 HTML pages.
- Internal links: passed.
- Static accessibility checks: passed for 98 pages.
- Browser QA: no horizontal overflow, one H1 per inspected page and no browser console warning/error at desktop, mobile or zoom-equivalent widths.
- Paid API calls: 0. Public deployments: 0.
- Repository/history secret scan: 665 reachable blobs and 473 present files scanned; zero credential-pattern findings.

## Known limitations and placeholders

- The live benchmark remains operationally unverified until the owner merges, configures and approves the protected environment, then manually dispatches it.
- Ten historic ORCID records remain withheld pending authoritative verification.
- Two OpenAlex theme diagnostics returned no results under the current narrow phrase set.
- The 25 visible Current Conversations entries are captured fixtures, not current provider coverage, not lab endorsements and not the owner’s final calibration set.
- GitHub push and pull-request creation remain dependent on owner-controlled GitHub authentication on this machine.

## Owner decisions before the next gate

1. Decide whether the August 2026 paper should join or replace an item in the ten selected publications; this gate adds it to the verified inventory but does not silently change the curated selection.
2. Review the ten unresolved ORCID rows and supply institutional/publisher links only where useful.
3. Configure `live-benchmark` reviewers, secret and variables exactly as listed in `docs/current-conversations-live-runbook.md`; choose and approve the model and conservative per-call estimate.
4. Merge the reviewed workflow before approving one artifact-only live benchmark. Do not enable staging writes for the first run.
5. Review live artifacts, then generate a genuinely mixed-source owner calibration set; do not label the fixture preview as final calibration.
6. Decide whether later private-staging automation should be enabled for one approved run, then return `CURRENT_CONVERSATIONS_STAGING_WRITE_ENABLED` to `false`.
7. Configure branch protections for `main` and the automation branch before any production gate.
8. Separately decide hosting, DNS, public schedule and publication policy; none is authorized here.
