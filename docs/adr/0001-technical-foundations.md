# ADR 0001: Technical foundations for the website and Research Watch

- Status: Accepted for Gate 0–1
- Date: 2026-08-13
- Decision owners: Project owner and future lab maintainers

## Context

The lab needs an academically credible public website and an auditable path toward an AI-assisted Research Watch. The team must be able to review changes as text, preserve provenance, keep hosting simple, and prevent automatically generated annotations from becoming curated content without review.

## Decision

1. **Quarto will render the website.** Quarto supports research-oriented publishing, citations, accessible semantic HTML, Markdown-based authoring, static output, and reproducible local builds without a runtime application server.
2. **Python will handle discovery and processing.** Python has mature libraries for scholarly metadata, text processing, validation, testing, and later model integrations. One processing language reduces operational complexity.
3. **Structured records will use YAML or JSON and validate against JSON Schema.** YAML is readable in editorial pull requests; JSON is suitable for interchange. Schemas make required provenance and workflow states enforceable.
4. **Scheduled GitHub workflows will run future discovery jobs.** Versioned workflows provide repeatable execution, logs, reviewable changes, and a natural path to opening candidate pull requests without operating a separate scheduler in the early stages.
5. **Curated items require pull-request review before publication.** A reviewed diff creates an audit trail, separates automatic suggestions from lab decisions, and allows validation and branch protection to block incomplete records.

## Consequences

The public site can be hosted as static files and has a small attack surface. Editorial changes remain legible and traceable. Contributors need Quarto, Python, and basic Git familiarity. YAML does not provide a rich editorial UI, and pull-request review may not suit every future contributor; a dedicated review interface may be considered later without changing the record contract.

Scheduled workflows are not a guarantee of reliable ingestion. Jobs must fail safely, avoid publishing partial output, and respect source policies. Model and source-provider changes must be versioned and observable.

## Alternatives considered

- A JavaScript application framework was not selected because Gate 1 requires no runtime interactivity or server state and the lab benefits more from research-publishing features.
- A database-first CMS was deferred because it would add operations, migrations, permissions, and export concerns before the editorial workflow is proven.
- Direct automated publishing was rejected because classification errors, provenance gaps, copyright risks, and prompt injection require human judgment.
- Provider-native scheduled tasks were deferred to avoid coupling the workflow to a discovery or model vendor.

## Revisit triggers

Revisit this ADR if the lab needs authenticated editorial workflows, high-volume ingestion, full-text search beyond static-site capabilities, non-technical review at scale, or service-level reliability that GitHub scheduling cannot provide.
