# Gate 4B–5A baseline

Date: 2026-08-17  
Starting branch: `codex/gate-3b-4a-content-truth-private-pilot`  
Starting commit: `4df2e2bd8c1d225294f9243bf88969ea10b18472`

## Repository integrity

- The starting working tree was clean and had no untracked files.
- Recent history matched the reported Gate 3B–4A workstreams and final commit.
- No Git remote was configured. GitHub repository variables, secrets, branch
  protections and remote workflow runs therefore could not be inspected or changed
  from this checkout.
- Environment-variable names were inspected without printing values. No OpenAI,
  Current Conversations, Research Watch, GitHub token, Bluesky, DataCite or Crossref
  credential/configuration variables were present. `GH_PAGER` was the only matching
  non-secret variable.
- Existing workflow permissions were read-only. The Research Watch schedule could
  create private artefacts but could not write a staging branch.
- Current private state existed under `staging/research-watch/current/`, the active
  owner exercise under `calibration/research-watch/`, and Gate 3B–4A owner/handoff
  packages under `deliverables/`.
- No `.openai/hosting.json` existed and no production deployment was configured.

## Material inspected

The repository instructions, README, Makefile, Quarto configuration, architecture,
content-governance and security documents, both historical ADRs, Gate 3B–4A baseline
and handoff, publication reconciliation and diff, pilot evaluation, query pack,
research scope, controlled vocabularies, all Research Watch Python modules and
adapters, schemas, prompts, workflows, packaging scripts and related tests were read
before implementation.

## Baseline checks

- `make check`: passed.
- Content: 19 YAML records and 10 JSON Schemas validated.
- Tests: 54 passed in 2.01 seconds.
- Quarto: 34 HTML pages built.
- Internal links: passed.
- Static accessibility: passed on all 34 pages.
- Separate `make build`: passed and rebuilt the same 34 pages.
- `make browser-qa`: passed using the retained Gate 3B–4A desktop, mobile and 200%
  zoom artefact inventory.
- `make publications-refresh`: passed in an isolated worktree and reconciled all 54
  ORCID work groups. This command intentionally did not overwrite the prior gate's
  tracked reconciliation evidence.
- `make research-watch-fixture`: passed in an isolated worktree with zero network
  calls.

## Existing private pilot rerun

The existing Gate 3B–4A pilot was rerun in an isolated worktree with no paid calls.
It completed successfully and did not replace the repository's prior calibration or
last-known-good staging state.

- OpenAlex live retrievals: 46.
- Normalized unique records: 42.
- Duplicates: 4.
- Event clusters: 40.
- Evidence-sufficient records: 34.
- Private-staged records: 4.
- Withheld records: 36.
- Quarantined records: 0.
- Source environment: academic research only.
- Crossref: live success for the sampled enrichment.
- DataCite: live attempt returned HTTP 404 for the sampled Crossref DOI.
- Bluesky: official public search endpoint returned HTTP 403; no bypass was used.
- OpenAI: not called because credentials and the new approved cost configuration were
  absent.
- Paid API cost: CAD 0.00.

## Baseline gaps confirmed

- Public and internal naming still use Research Watch.
- Public records are source-centred rather than conversation-cluster-centred.
- The complete bibliography is not yet public; only ten selected records are
  canonical site records.
- The active calibration exercise is a 35-item academic-heavy set.
- Mixed-source discovery, strict Current Conversations AI output, CAD budget ledger,
  feeds and a controlled private-staging write workflow are not implemented.
- No remote is available for a real automation-branch write test.
- OpenAI model benchmarking cannot run without credentials; a captured-response
  harness is required instead.

These are Gate 4B–5A implementation targets, not repository-integrity failures.
