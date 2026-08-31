# Gate 5I baseline — 31 August 2026

Repository: `Andrewsudmant/CCL-Lab-Website`

Branch: `codex/gate-5c-thematic-consistency`
Starting HEAD: `125f48db6bd1168e7eb235298ddd5482231c9cee`

The working tree was clean before baseline logs and review screenshots were created. `origin` remains `https://github.com/Andrewsudmant/CCL-Lab-Website.git`. Fetching origin found no later work: zero commits since Gate 5H; the branch is 33 commits ahead of `origin/main` and zero behind. All prior gate branches and commits remain intact.

PR #1, **Prepare the Draft 0.1 release candidate**, is open, draft and mergeable (`CLEAN`). Both Site checks runs on the exact starting HEAD succeeded. The repository remains public, `main` is the default branch, Pages is disabled, homepage is unset, auto-merge is disabled and the environment list is empty. No settings were changed. Historical ZIPs are present only under ignored `deliverables/`; no untracked source change was present.

## Baseline checks

`make validate test build check release-check` ran all requested targets in dependency order (Make reused the just-completed builds).

- 95 records and 20 schemas validated.
- 162 tests passed on each of the test and check invocations.
- Root and `/CCL-Lab-Website/` builds: 87 HTML pages each.
- Internal links and static accessibility: pass in both profiles.
- One existing `research_watch` compatibility-import DeprecationWarning; no errors.

Full output: `reports/qa/gate-5i-baseline/release-checks.log`.

## Observations and preservation boundary

All 46 complete canonical records, the schemas, generator, selected relationships and deployment controls were inspected. All 46 publication pages repeat the date-precision and no-AI-metadata rules. Generic relationship notes and generic original-source instructions add repetition. The individual template does not explicitly display peer-review status, although the complete listing does. One venue retains an encoded ampersand in the source record; a presentation-only decode is appropriate without changing canonical bytes. Quarto also displays the description twice when both title-block description and page deck are supplied.

The only selected-example change authorized is removal of `low-carbon-cities-affordable` from prominent Delivery display. The record, bibliography, search and underlying relationship remain. No refresh, reclassification, metadata rewrite, API/model call, deployment or settings change is authorized.
