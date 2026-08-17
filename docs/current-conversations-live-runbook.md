# Current Conversations live benchmark owner runbook

This is an owner-controlled, artifact-only benchmark. Do not paste or send the API key to Codex, ChatGPT, a prompt, a repository file, a log or a test fixture.

## One-time GitHub setup

1. Merge the reviewed Gate 5B pull request.
2. In repository settings, create the GitHub environment `live-benchmark`.
3. Add environment secret `OPENAI_API_KEY` directly in GitHub. Configure required reviewers so a named owner must approve each job.
4. Add these environment variables:

| Variable | Required rule |
|---|---|
| `CURRENT_CONVERSATIONS_OPENAI_MODEL` | Owner-reviewed Responses API model identifier |
| `CURRENT_CONVERSATIONS_MAX_COST_CAD_PER_RUN` | Positive, no more than `2.00` |
| `CURRENT_CONVERSATIONS_MAX_COST_CAD_PER_MONTH` | Positive, no more than `20.00` |
| `CURRENT_CONVERSATIONS_USD_PER_CAD` | Positive USD value of one CAD |
| `CURRENT_CONVERSATIONS_USD_PER_CAD_DATE` | ISO date, not future and no more than 31 days old |
| `CURRENT_CONVERSATIONS_MAX_WEB_SEARCH_CALLS` | `1` for the first benchmark |
| `CURRENT_CONVERSATIONS_MAX_WEB_ITEMS` | `1`, `2` or `3`; use `2` initially |
| `CURRENT_CONVERSATIONS_ESTIMATED_USD_PER_WEB_CALL` | Reviewed conservative maximum used for pre-authorization |

Do not create `CURRENT_CONVERSATIONS_STAGING_WRITE_ENABLED` yet. The benchmark workflow cannot write repository contents even if that variable exists.

## Exact first-run inputs

Open Actions → **Current Conversations live benchmark** → **Run workflow**, select the merged `main` branch, and use:

- `query_id`: `cc-w02-governance`
- `result_limit`: `2`
- `artifacts_only`: checked / `true`

The environment reviewer should confirm the branch/commit, variables, CAD ceilings and artifact-only input before approving access to the environment secret. Approval authorizes one bounded paid request; it does not authorize staging or publication.

## Review sequence

1. Download `current-conversations-live-benchmark-<run-id>` after the job completes.
2. Confirm the mocked preflight passed, the budget ledger stayed within both CAD ceilings, original and underlying URLs are present, and no staging/site path changed.
3. Review every candidate against its original source for relevance, evidence sufficiency, identity, date, copyright/privacy and injection risk.
4. Record model quality, link retention, false positives, clustering proposals, latency and the conservative recorded cost. Do not call fixtures a live calibration set.
5. If the run fails because a secret is missing, the ledger is corrupt/stale or the maximum cost is over budget, correct the GitHub environment configuration and dispatch a new run; never bypass the fail-closed check.

## Later private-staging approval

Only after benchmark artifacts and an owner-generated mixed-source calibration set pass review may the owner set repository variable `CURRENT_CONVERSATIONS_STAGING_WRITE_ENABLED=true` and manually choose `staging-write` in **Current Conversations bounded discovery**. That separate job has `contents: write`, validates the site and records, checks the exact changed-path allowlist, and may write only `automation/current-conversations-staging`. Set the variable back to `false` immediately after the approved run. It never writes `main` and never deploys.

## Rollback and incident response

- A failed replacement preserves `staging/current-conversations/current` and its last-known-good snapshot.
- Do not delete or hand-edit the cost ledger to force a request. Archive the corrupt artifact, document the incident and begin a newly reviewed monthly ledger only through a pull request or workflow change.
- If a credential could have appeared in output, cancel the run, revoke/rotate it in the OpenAI project, delete affected artifacts through GitHub, inspect audit logs and run the repository/history secret scan before resuming.
