# Gate 3B–4A baseline

Date: 2026-08-14  
Starting branch: `codex/gate-2-3a-automated-research-watch`  
Starting commit: `dc6a2826e640ee4de850f8fe2f62f0e5fd2cd2cb`

## Repository integrity

- Working tree was clean before baseline outputs were generated.
- No Git remotes are configured. Remote branch protections and GitHub workflow
  execution therefore cannot be inspected or changed locally.
- Recent history matches the Gate 2–3A workstream and contains four substantive
  commits plus the final QA-log commit.
- No `.openai/hosting.json` exists and no production deployment is configured.
- Existing repository instructions, architecture, governance, security, both ADRs,
  handoff, audit, metadata workflow, pilot reports, relevant schemas and all person,
  project and publication records were inspected.

## Credential availability

Only variable presence was inspected; values were not printed.

| Variable | Baseline state |
|---|---|
| `OPENAI_API_KEY` | absent |
| `OPENAI_MODEL` | absent |
| `OPENAI_MAX_COST_PER_RUN` | absent |
| `OPENAI_MAX_ITEMS_PER_RUN` | absent |
| `GITHUB_TOKEN` | absent |
| `GH_TOKEN` | absent |

Missing credentials constrain paid/model and remote workflow testing, but do not
block independent Gate 3B–4A work.

## Baseline checks

- `make check`: passed.
- Content: 11 YAML records and 9 JSON Schemas validated.
- Tests: 15 passed in 1.21 seconds.
- Quarto: 35 HTML pages built.
- Internal links: passed.
- Static accessibility checks: passed on 35 pages.
- Separate `make build`: passed and rebuilt the same 35 pages.
- Fixture Research Watch run: passed with zero network calls and wrote a normalized
  captured-fixture report.
- Existing screenshot inventory: 20 files at desktop and mobile sizes.

## Baseline weaknesses confirmed

- Internal maintainer documents are rendered publicly and included in public search.
- Basic personal information still uses the former email and an owner-review notice.
- Theme 4 is incorrectly marked established; Theme 5 is incorrectly marked developing.
- Current, prior and associated work are not represented as separate dimensions.
- Publication metadata contains synthetic dates, incomplete author text and known
  title/attribution errors.
- The publication refresh script is a non-networking plan rather than a reconciliation.
- Research Watch does not yet implement evidence acquisition, clustering, structured AI
  output, ranking/diversity, transactional staging, availability rechecks or run manifests.
- The query pack still permits 24 new items rather than the approved maximum of 12.
- Existing screenshot files use `.png` names but contain JPEG data. They decode in the
  operating-system image tools, but their content type and extension are inconsistent.
- Pillow is not installed, so an attempted Pillow-based decode check was unavailable;
  the operating-system `file` utility exposed the content-type mismatch instead.

These weaknesses are implementation targets for Gate 3B–4A and are not repository
integrity failures.
