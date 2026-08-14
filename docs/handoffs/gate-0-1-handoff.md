# Cities & Climate Learning Lab: Gate 0–1 handoff

- Prepared: 2026-08-14
- Project: Cities & Climate Learning Lab public website
- Affiliation: School of Resource and Environmental Management, Simon Fraser University
- Repository branch: `codex/gate-0-1`
- Public deployment status: Not deployed

## Executive summary

We established the governance, architecture, structured content model and first complete website prototype for the Cities & Climate Learning Lab. The result is a restrained, accessible Quarto website and a fixture-only Research Watch demonstration. It deliberately does not retrieve live material, call AI services, publish automatically or configure production hosting.

The central design decision is that AI may help discover, classify and draft annotations, but it is never treated as the source. Original sources and their metadata remain authoritative. Human review is required before an item can appear as a curated lab selection.

## What we did and why

### Repository and governance foundation

We created durable repository instructions, architecture documentation, content-governance rules, a security model, explicit Gate 0–1 boundaries and an architecture decision record.

This was done first so later automation cannot quietly define editorial policy through code. The repository now states which metadata must be preserved, what human approval means, how corrections and removals work, and which capabilities remain out of scope.

### Website prototype

We built the required Quarto pages: Home, Research, Projects, People, Publications, Research Watch, Data & Tools, Opportunities, About Andrew and Contact.

The design uses typography, generous spacing, a neutral palette and a restrained red accent. We avoided generic climate imagery and did not use an SFU logo because no approved asset was supplied. The site works without application-level client-side code and adapts to desktop and mobile layouts.

### Structured content and validation

We created YAML fixtures and JSON Schemas for people, projects, publications, research themes, Research Watch candidates and approved Research Watch items. The six initial research areas are defined in `config/research_scope.yml` with questions, exclusions, search concepts, geographical priorities, methods and clearly labelled placeholder examples.

Python tooling validates records and their workflow state before generating Quarto listing fragments. This prevents incomplete provenance fields or an improperly reviewed candidate from silently entering the curated section.

### Research Watch prototype

The Research Watch page has two visibly separate areas:

1. Lab-reviewed selections with a recorded reviewer and review date.
2. Automatically identified candidates that are explicitly labelled as unreviewed and not endorsed by the lab.

All Gate 1 records are synthetic fixtures. Even the reviewed example is a workflow demonstration, not a substantive lab recommendation.

### Quality assurance

The repository includes schema validation, listing tests, internal-link checks, practical static accessibility checks, a local build workflow and GitHub Actions CI. The final Gate 1 review validated nine structured records and eight schemas, passed eight automated tests, built fifteen HTML pages, and passed internal-link and accessibility checks. Desktop and mobile browser review found no horizontal overflow or console warnings and confirmed that the responsive navigation works.

## Challenges and how we addressed them

### Preserving an explicit Quarto architecture

The workspace began empty, and generic website tooling would normally introduce a JavaScript application framework. That would have conflicted with the lab's research-publishing and auditability needs. We retained Quarto as the explicit architecture and used Python only for deterministic content processing.

### Rendering custom layouts safely in Quarto

The first build interpreted some indented custom HTML as code blocks. We corrected the raw-HTML boundaries and excluded generated fragments from standalone page rendering. Tests now detect listing counts, and browser review confirmed that no code blocks leak into the public interface.

### Full-width and mobile layout behaviour

Quarto initially constrained the custom home layout to a narrow content column. After correcting the full-page layout, a decorative CSS shape caused mobile horizontal overflow. We clipped decorative overflow at the page boundary and rechecked desktop and 390-pixel mobile views.

### Demonstrating review states without implying endorsement

A realistic Research Watch interface needs sample content, but invented examples could be mistaken for actual research selections. We therefore use reserved `example-` identifiers, `fixture: true`, owner-review flags, conspicuous placeholder language and separate candidate/approved directories.

### Avoiding premature infrastructure

Live APIs, models, databases, analytics and deployment could make the prototype appear more complete while obscuring unresolved editorial decisions. We kept them out of scope so the lab can approve sources, review policy, privacy and operational responsibilities before automation begins.

## How governance remains transparent and traceable

- Structured records retain source URL, source name and type, authors or organisation, publication and retrieval dates, and stable identifiers when available.
- Records state exactly what evidence was available to summarisation, such as metadata, abstract, permitted excerpt or full text.
- AI use records the model and prompt version, or explicitly records that AI was not used.
- Confidence includes a score, label and written basis rather than an unexplained number.
- Candidate and approved content live in separate directories with different schema and workflow constraints.
- Human review records status, reviewer, date, notes and field-level reviewer edits.
- Risk flags expose limitations such as limited evidence, paywalls, credibility concerns, personal data or prompt injection.
- Correction and removal fields preserve status, date and an explanatory note instead of allowing silent deletion.
- Generated listings are reproducible from version-controlled YAML and must pass validation before the site builds.
- Pull-request review and recommended branch protections provide a visible decision history before curated publication.
- AI output is treated as a proposed lab annotation; the linked original source remains the evidentiary authority.

## Known placeholders and unresolved matters

There are no unresolved build errors. External links were not checked over the network because Gate 0–1 explicitly avoids external calls.

The following still require owner review:

- Andrew Sudmant's confirmed title, biography, contact address and profile links.
- Final project descriptions, partners, dates and funding status.
- A verified publications list and complete citations.
- The six theme definitions, exclusions, search concepts, methods and representative examples.
- Whether unreviewed candidates should ever be visible on the public production site.
- Approved SFU affiliation wording and any permitted institutional brand assets.
- A public contact route for general enquiries and correction/removal requests.

## What to think about next

Before authorising Gate 2, the owner should decide:

1. Which academic databases, news outlets, institutional sources, blogs, data catalogues and Bluesky sources may be monitored?
2. What retrieval methods are permitted by licences, terms of service, robots policies and institutional requirements?
3. Will unreviewed candidates be public, reviewer-only, or published in a limited transparency view?
4. Who may review and approve records, and what evidence threshold is required for each source type?
5. Which AI provider and model may be used, what data may be sent to it, and how long may provider logs be retained?
6. How will prompts be versioned, evaluated and protected from instructions embedded in untrusted source content?
7. What confidence thresholds and risk flags should automatically hold an item for review?
8. What turnaround and escalation process should govern corrections, removals, privacy complaints and source disputes?
9. Which repository protections, code owners and production deployment approvals should be mandatory?
10. What domain, hosting, accessibility, privacy, records-management and institutional approvals are required before launch?

## Recommended Gate 2 sequence

1. Approve the research scope and public-facing owner content.
2. Approve source allow-lists and copyright/privacy constraints.
3. Finalise the candidate review rubric and public/private visibility policy.
4. Select one low-risk source adapter for a narrow, monitored pilot.
5. Version the first real discovery and annotation prompt.
6. Generate candidate-only pull requests; do not automate curated publication.
7. Evaluate precision, provenance completeness, reviewer workload and failure modes before adding more sources.

## Useful commands

```bash
make check
make build
make handoff HANDOFF_SUMMARY=docs/handoffs/gate-0-1-handoff.md
```

The built site remains local under `_site/`. Handoff ZIP files are written to `deliverables/` and are not committed to Git.
