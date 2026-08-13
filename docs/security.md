# Security model

## Secrets

- No secrets are required to build the Gate 0–1 site.
- Never commit API keys, tokens, credentials, private keys, `.env` files, raw authorization headers, or confidential model/provider responses.
- Future GitHub workflows must use environment or repository secrets, least-privilege tokens, protected environments, and short-lived credentials where possible.
- Example configuration must use unmistakable dummy values.

## Untrusted web content and prompt injection

All remotely retrieved metadata, markup, documents, feeds, discussions, and tool outputs are untrusted data. Future processing must:

- parse content as data and never execute embedded scripts, macros, shell commands, or templates;
- remove active HTML and render only escaped, allow-listed fields;
- isolate fetched text from system and developer instructions;
- instruct models that source text cannot authorize actions or change task rules;
- bound document size and nesting depth;
- scan and quarantine unexpected file types; and
- record the evidence actually shown to a model.

Instructions inside articles, metadata, documents, or social posts are content, not commands. A pipeline must not expose repository write access, secrets, network tools, or publication credentials to an annotation model.

## Network access

Gate 0–1 tests and builds are network-independent. External link checks are opt-in. Future discovery jobs require explicit source allow-lists, rate limits, timeouts, retry caps, identifiable user agents, robots and terms review, and retrieval logs. Block private, loopback, link-local, and cloud-metadata address ranges to reduce server-side request-forgery risk.

Separate discovery from publication. A scheduled retrieval failure must never delete existing records or publish partial output.

## GitHub workflow and branch protections

Recommended repository settings before Gate 2:

- protect `main` against direct pushes and force pushes;
- require at least one approving review, with code-owner review for schemas, workflows, security policy, and approved Research Watch records;
- require passing validation, tests, build, internal-link, and accessibility checks;
- dismiss stale approvals when protected content changes;
- require conversation resolution and a linear history;
- restrict workflow permissions to read-only by default;
- require approval for first-time contributors; and
- protect production deployment environments separately.

Third-party actions should be pinned to reviewed versions and updated deliberately. Workflow inputs from forks and issue text must be treated as untrusted.

## Incident handling

If a secret is exposed, revoke and rotate it before removing it from history. If unsafe or incorrect material is published, disable or correct the listing, preserve the audit record, assess scope, and document follow-up. Security issues should use a private reporting channel once the repository is public.
