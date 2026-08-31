# Gate 5F baseline

Recorded on 2026-08-28 before Gate 5F source changes.

- Repository: `Andrewsudmant/CCL-Lab-Website`
- Branch: `codex/gate-5c-thematic-consistency`
- HEAD: `070bbfedfc4ce3437c7b5919eb220254fa478e9a`
- Working tree: clean before baseline logs were created
- Remote: `origin` → `https://github.com/Andrewsudmant/CCL-Lab-Website.git`
- Pull request: #1, open, mergeable and draft; head branch correct; both existing Site checks successful
- Divergence from `main`: 14 commits ahead, 0 behind
- Commits after the expected Gate 5E head: none
- Existing ignored deliverables: Gate 2–5E owner-review, calibration and handoff ZIPs were present and left unchanged

## Baseline commands

| Command | Result |
|---|---|
| `make validate` | Passed: 95 records, 18 schemas |
| `make test` | Passed: 131 tests; one legacy `research_watch` import deprecation warning |
| `make build` | Passed: 87 pages rendered |
| `make check` | Passed: validation, build, 131 tests, internal links and static accessibility for 87 HTML pages |

The warning is pre-existing compatibility debt, not a Gate 5F regression. The baseline used no discovery, API, paid-model, staging-write, deployment or network workflow.

Machine-readable command logs are retained under `reports/qa/gate-5f-baseline/`.
