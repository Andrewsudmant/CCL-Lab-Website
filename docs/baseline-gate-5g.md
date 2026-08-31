# Gate 5G baseline

Baseline date: 28 August 2026 (America/Vancouver)

## Repository state

- Branch: `codex/gate-5c-thematic-consistency`
- HEAD: `80aa1cae809f52c656d4336e43eb9405e16f0626`
- Working tree: clean before the baseline
- Remote: `origin` → `https://github.com/Andrewsudmant/CCL-Lab-Website.git`
- Draft pull request: #1, open, draft, mergeable, targeting `main`
- Branch divergence from `main`: 22 commits ahead, 0 behind
- Commits after the expected Gate 5F head: none
- CI: both reported `Site checks / build-and-test` runs passed
- Repository: public, default branch `main`, merge methods unchanged
- GitHub Pages: not configured (`has_pages: false`; Pages API returned 404)
- Existing ZIP deliverables remain ignored and outside Git; none were treated as source material.

## Required command baseline

The four Gate 5G baseline commands were run in the requested order from the untouched Gate 5F tree:

| Command | Result |
|---|---|
| `make validate` | Passed: 95 records and 18 schemas |
| `make test` | Passed: 142 tests; 1 pre-existing deprecation warning |
| `make build` | Passed: 87 pages rendered |
| `make check` | Passed: 142 tests, internal links and static accessibility across 87 HTML pages |

The sole warning is the existing compatibility import in `tests/test_gate_3b_4a_controls.py`: `research_watch` is deprecated in favour of `current_conversations`. No network discovery, paid model call, staging write or deployment occurred during the baseline.

## Gate 5G interpretation

The owner has approved the Gate 5F homepage, four-theme, research-idea, Work, Our Approach, Current Conversations and Draft 0.1 decisions. Gate 5G may curate the previous-work display and harden public presentation and release mechanics without reopening those settled decisions.
