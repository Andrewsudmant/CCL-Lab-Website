# Gate 5D baseline

Captured: 27 August 2026  
Branch: `codex/gate-5c-thematic-consistency`  
HEAD: `bcf168ef52b5855566116597dcc3b457da50a18c`

## Repository and pull request

- Working tree: clean; local branch matched `origin/codex/gate-5c-thematic-consistency`.
- Remote: `origin` → `https://github.com/Andrewsudmant/CCL-Lab-Website.git` for fetch and push.
- Base: local and remote `main` at `8be464c482c292513188101472dea8ec05692259`.
- Difference from `main`: Gate 5C was seven commits ahead and zero behind.
- PR #1: open, draft, mergeable; head `codex/gate-5c-thematic-consistency`; base `main`.
- PR title: “Reframe the lab website around the urban climate learning cycle”.
- PR URL: https://github.com/Andrewsudmant/CCL-Lab-Website/pull/1
- Commits following the final Gate 5C QA/owner-package commit `9805fb6`: `113ed95` (remote-transfer and handoff documentation) and `bcf168e` (post-handoff integrity scan). Both are retained.

## Baseline commands

| Command | Result |
|---|---|
| `make validate` | Passed: 70 records and 15 schemas |
| `make test` | Passed: 99 tests; one known legacy `research_watch` import deprecation warning |
| `make build` | Passed: 103 Quarto pages rendered |
| `make check` | Passed: validation, build, 99 tests, internal links and static accessibility for 103 pages |

The normal build made no discovery or paid/model call. No repository file was changed before this baseline was captured.

## Starting model limitation

The active model required all six heterogeneous research records to validate as “projects”, used project-only public routes and headings, and retained theme-level `portfolio_maturity`. Theme pages used generic project sections and database-style empty messages. Gate 5D replaces those active assumptions while preserving the source records, canonical publications, Current Conversations controls, routes as transitions, and Git history.
