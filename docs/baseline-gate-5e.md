# Gate 5E baseline

- Date: 2026-08-27
- Branch: `codex/gate-5c-thematic-consistency`
- Starting commit: `6ce901ac43f2e3a51e9e915f43c65034708ac6fe`
- Remote: `https://github.com/Andrewsudmant/CCL-Lab-Website.git`
- Pull request: #1, open and draft, branch into `main`
- History: the branch was 11 commits ahead of and 0 behind `main`; no Gate 5E commits existed.

The required pre-change sequence passed: `make validate && make test && make build && make check`. It validated 84 records against 17 schemas, passed 118 tests with one known legacy `research_watch` deprecation warning, rendered 112 pages, passed internal-link checks and passed static accessibility checks on all 112 pages.

The only untracked baseline path was an owner-extracted copy of the prior deliverable under `deliverables/`. It was preserved and subsequently excluded through the repository's deliverable-directory ignore rule. No owner-review ZIP or extracted owner package is a source of record.
