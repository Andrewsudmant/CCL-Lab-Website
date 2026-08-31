# ADR 0004: Distinguish themes, research work, publications and research ideas

- Status: Accepted
- Date: 2026-08-27
- Decision owner: Project owner

## Context

The former model required every substantial research record to behave like a conventional project. That made an ongoing paper look like a project, blurred a completed project with its still-live public tool, and encouraged synthetic programme wrappers solely to support website navigation. It also placed activity status too close to the themes, even though all four themes are current and equally important parts of the lab's intellectual programme.

## Decision

The active model has four separate concepts.

1. **Themes** are enduring analytical questions and have no maturity or activity status.
2. **Research work** records actual ongoing or completed programmes, research lines, projects, studies, papers, reports, tools and datasets.
3. **Publications and outputs** remain canonical bibliographic records. A paper may connect to genuine work or directly to themes, and no parent work is required.
4. **Research ideas** are possible future questions with suggested methods and a mandatory statement that they are not active or funded projects.

Earlier work may illustrate a current theme when an abstract, publisher or institutional description, lawful full text, or owner-approved information supports the relationship. That thematic relationship does not change authorship, dates, institutional provenance or the relationship to CCLL.

When work represents a paper or report, the work record links to the canonical publication and derives bibliographic title, authors, year, identifier and publication status. It stores only research relationship, status, description, themes, facets, claim boundaries and work links. The publication remains one canonical record even when it appears under several themes.

## Consequences

The public navigation uses **Work**, with `/work/` as the canonical listing. Static `/projects/` transition pages preserve older links. Theme pages can present ongoing work, selected completed/foundational examples and research ideas without inventing empty projects. An active tool can be linked to a completed project without changing the project's completion status.

Validation and tests must prevent ideas from entering work/output counts, feeds or Current Conversations; reject unsupported work links; allow `parent_work_id: null`; and require evidence-backed rationales for selected publication examples. Historical migrations may retain former status fields as decision evidence, but active theme data cannot depend on them.

## Alternatives considered

- Extending the project schema while continuing to call every record a project was rejected because it preserved the semantic error in public copy.
- Creating a synthetic programme for every standalone paper was rejected because it would invent organisational structure.
- Treating ideas as `planned` work was rejected because it could imply commitment, funding or recruitment.
- Duplicating publications into theme-specific records was rejected because metadata and correction history would diverge.

## Revisit triggers

Revisit this decision if the lab adopts a research-information system with a stronger canonical work graph; if programmes require hierarchical funding and partner records; if research ideas become a governed proposal pipeline; or if static route transitions become inadequate for a production hosting platform. Any replacement must preserve canonical publication identity, provenance, corrections and the separation between actual work and possible future ideas.
