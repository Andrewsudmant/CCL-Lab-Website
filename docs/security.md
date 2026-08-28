# Security model

## Secrets and paid access

Fixture tests/builds require no secrets. Never commit API keys, tokens, `.env` files, authorization headers, provider payloads, browser profiles or model reasoning traces. Paid web discovery fails closed unless the API key, model, fresh USD/CAD rate and date, maximum calls/items, estimated per-call cost, CAD 2/run ceiling and CAD 20/month ceiling are all valid. A corrupt or inconsistent ledger disables paid access.

The `OPENAI_API_KEY` is expected only as an environment secret in the protected GitHub environment `live-benchmark`. It must not be requested in a task, placed in a prompt, copied to a repository/environment file, printed, uploaded as an artifact or shared with staging jobs. The manually dispatched live benchmark has `contents: read`; its first run produces artifacts only.

## Untrusted web content and prompt injection

All fetched metadata, HTML, documents, snippets and posts are untrusted data. Parse rather than execute; strip active content; escape output; limit schemes, redirects, size and file types; block private/link-local/cloud-metadata networks; and never let source instructions alter prompts, policy, tools, budgets or publication decisions. The Responses request explicitly treats retrieved instructions as evidence rather than commands, local tests flag common injection language, and strict structured output rejects unknown fields. Record the exact evidence class shown to a model. Suspected injection, unexpected personal data or invalid structured output is quarantined.

## Network and role separation

Tests and normal builds are offline. Live modes are explicit, bounded, timed and logged. Discovery/annotation components receive no deploy credentials. Repository writing is a separate workflow job with a specific opt-in variable, least-privilege token, exact private branch and changed-path allowlist. No workflow in this gate deploys publicly.

## Safe failure

Staging is transactional and complete: sources, clusters, feeds, site fragment, run manifest and budget ledger validate before replacement. Failure preserves the last-known-good snapshot and records a failure manifest without leaking fetched content or secrets.

Research-work and research-idea records are editorial content, not a place for private planning data. Do not add confidential partner discussions, unannounced funding, private review labels, prospective personal data or unpublished findings. Owner-review ZIPs stay in ignored `deliverables/` and may contain only bounded public or governance material.

## Required branch protection before production

- prohibit direct and force pushes to `main`;
- require review of control-plane and security changes;
- require schema, test, build, link and accessibility checks;
- restrict workflow/action permissions and deployment environments;
- protect and monitor the automation branch independently; and
- require incident response for credential exposure or repeated quality failures.

Gate 5B does not configure hosting, production secrets, deployment credentials or public scheduled writes. Repository write permission exists only in the separately guarded private-staging job, after validation and an allowed-path diff check, and remains disabled unless `CURRENT_CONVERSATIONS_STAGING_WRITE_ENABLED` is exactly `true`.

## Gate 5F integrity boundary

Gate 5F is an offline editorial and presentation pass. Builds, tests, screenshots and packages must not call discovery providers or models, read secrets, enable staging writes, change environments, alter Pages or deploy. The Current Conversations problem statement is public copy only and does not activate the system. Owner-review archives stay ignored outside Git, and the private previous-work proposal must not enter generated public routes. Hypothetical examples are tested for explicit status so they cannot be mistaken for empirical evidence, rankings or advice.

## Draft 0.1 Pages boundary

`.github/workflows/public-draft-pages.yml` is inert until the owner later merges it, configures Pages, creates the protected `public-draft` environment and sets `PUBLIC_DRAFT_DEPLOY_ENABLED=true`. It has only `workflow_dispatch`; no push, pull-request or scheduled event can invoke it. The build job has `contents: read`. Only the environment-gated deployment job has `pages: write` and `id-token: write`. The workflow requires a boolean publication confirmation and fails closed when the repository variable is absent or false. It requires no secret and must never receive an OpenAI or discovery credential.

Gate 5G does not run this workflow or alter Pages settings. Owner-review archives and rendered sites remain ignored. A repository/history scan is required before the final push, and a credible credential finding blocks the release candidate.
