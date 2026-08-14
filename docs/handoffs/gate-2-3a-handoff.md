# Cities & Climate Learning Lab — Gate 2–3A handoff

Date: 2026-08-14  
Branch: `codex/gate-2-3a-automated-research-watch`  
Status: development complete for review; not merged and not deployed

## What we did and why

This phase turns the Gate 1 fixture website into a governed development prototype
with canonical content and an inspectable Research Watch pipeline.

- Replaced the former Canadian/comparative theme with the owner-directed canonical
  theme `canadian-climate-policy` / **Canadian climate policy**.
- Modelled themes as overlapping research relationships: every project and publication
  is stored once, has one primary theme and limited secondary themes, while geography,
  governance scale, method, climate domain and sector remain separate.
- Replaced invented example projects, publications and biography text with records
  supported by SFU, University of Edinburgh, DOI/publisher and named project sites.
- Added canonical project and publication detail pages plus theme pages with core,
  related and recent-evidence sections.
- Adopted the owner's automated-publication decision. Unreviewed Research Watch items
  may publish only after deterministic controls pass, with the complete site-level
  disclosure and a compact label on every item.
- Added modular adapters for OpenAlex, Crossref, OpenAI Responses API web search and
  Bluesky; normalization, DOI/URL deduplication and deterministic publication decisions
  are tested independently of provider networks.
- Added a captured-fixture public record and a title-only withheld record so successful
  and failed publication paths are reproducible without network calls.
- Added scheduled GitHub workflow scaffolding, CI, schemas, cross-record validation,
  static accessibility and link checks, responsive browser QA and review packaging.

## Key challenges and what we learned

The first bounded live pilot was deliberately small. OpenAlex and Crossref connections
worked, but all six returned records were out of scope: OpenAlex treated the initial
Boolean-looking text too broadly, while Crossref's placeholder enrichment query was not
a meaningful discovery query. The public Bluesky endpoint returned a CDN-level 403 from
this environment. The OpenAI adapter found no API key and correctly exited before making
a request. These results are retained in `reports/pilot/` and no poor-quality live result
was promoted to public content.

Public metadata was incomplete in places. Rather than guess, records use explicit
“and collaborators” author text and year-first placeholder dates where only a year was
confirmed. Both are owner-review items. Searches also did not establish a clear
Andrew-specific body of workforce-transition work, so no workforce project was invented.

Full-page screenshots from the in-app browser initially showed a stitching artefact.
The artifact was detected during visual QA and the package uses stable desktop and
mobile viewport screenshots instead.

## Transparent and traceable governance

Research Watch preserves original and canonical URLs, stable/platform identifiers,
authors or organisation, source type/name, publication and retrieval dates, adapter,
query and run versions, theme scores and rationales, evidence types and limitations,
model and prompt versions, confidence, human-review state, edits, risk flags and
correction/availability status.

Automation is explicitly not endorsement. The public disclosure states:

> Research Watch uses automated searches and AI-generated classification and summaries.
> Items have not normally been reviewed by a member of the Cities & Climate Learning
> Lab, and inclusion does not imply endorsement. Summaries may contain errors or omit
> important context. Please consult the original source.

Deterministic gates—not the model—decide whether a record is published, withheld or
quarantined. Insufficient evidence, title-only evidence, suspicious URLs, prompt-injection
signals, unsupported claims and low theme scores cannot be bypassed by AI output.
Control-plane changes (scope, queries, schemas, prompts, workflows and policy) remain
pull-request reviewed. Secrets are environment/GitHub secrets only; live calls never run
as a side effect of building the site. Corrections and removals preserve a dated trail.

## Verification completed

- 11 YAML content records and 9 JSON Schemas validated.
- 14 automated tests passed.
- 35 HTML pages built with Quarto.
- Internal-link checks passed.
- Static accessibility checks passed on all 35 pages.
- Ten principal pages inspected at desktop and mobile sizes; no mobile horizontal
  overflow or console warnings were observed.
- Research Watch search/reset/theme-filter interaction passed.

## Unresolved items and placeholders

- All newly verified biographical, project and publication wording remains owner-review
  material until approved for production.
- Some publication author lists are incomplete and some dates are year-only normalized
  to 1 January; run an owner-approved ORCID/Crossref reconciliation.
- Theme 4 lacks enough public evidence to support a claimed project; its “established”
  status should be reconsidered if the owner has no additional material.
- Theme 5 has substantial public evidence but remains “developing” according to the
  current owner direction; consider changing it to “established.”
- The scheduled Research Watch workflow produces private candidate artifacts only in
  Gate 3A. Record assembly, event clustering and safe staged automatic publication are
  Gate 3B work.
- Bluesky needs testing from an approved GitHub Actions network path. OpenAI needs an
  owner-approved model/budget/retention decision and a GitHub secret.
- Cross-browser, high-zoom and assistive-technology user testing remain outstanding.
- Branch protection and required-check settings must be configured on the remote host.

## Owner decisions before Gate 3B / production

1. Approve or edit Andrew's biography, role, public email, profile links and photo choice.
2. Confirm which historical projects should be described as lab work versus prior work
   by the lab lead, including status, dates, collaborators and funders.
3. Provide a trusted publication export or approve ORCID reconciliation; resolve partial
   author lists, exact dates and the selected/featured publication set.
4. Provide evidence for the workforce theme or decide whether to mark it “developing.”
5. Decide whether the evidence-infrastructure/tools theme is now “established.”
6. Approve provider usage, OpenAI model, monthly budget, retention settings, workflow
   frequency, publication thresholds, per-domain caps and archive period.
7. Decide whether lab-authored items may appear in Research Watch and how prominently
   the conflict-of-interest flag should be shown.
8. Approve the correction/removal contact route and response expectations.
9. Approve the visual design and wording after reviewing desktop/mobile screenshots.
10. Configure remote branch protections and select the eventual hosting environment;
    neither merge nor deployment is part of this package.

## Suggested next work

Gate 3B should begin with a labelled evaluation set and provider-native query revision,
not an unattended publish. Add record assembly, source/event clustering, diversity health
checks, staging/rollback behavior, availability rechecks and audit-log retention. Then run
the complete pipeline in a private staging branch, compare results against owner labels,
and only enable production publication after thresholds and failure procedures are agreed.

## File map

- `config/`: theme scope, controlled vocabularies, query pack and owner overrides.
- `data/`: canonical people, project, publication and Research Watch records.
- `schemas/`: JSON Schemas for all controlled records.
- `research_watch/`: adapters, provider-neutral model, normalization and publication gate.
- `scripts/`: validation, generation, checks, publication-refresh plan and packaging.
- `docs/`: architecture, governance, security, ADRs, audit and metadata workflow.
- `reports/pilot/`: bounded provider outputs and evaluation.
- `reports/screenshots/`: desktop and mobile captures for all principal pages.
- `_site/`: complete local rendered site included only in the owner review ZIP.

This handoff contains no secrets, no raw private provider payloads and no production
deployment configuration.
