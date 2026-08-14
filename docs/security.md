# Security model

## Secrets and least privilege

Local tests and fixture mode require no secrets. API keys, tokens, credentials, `.env` files, raw authorization headers and private provider payloads must never enter Git or public artefacts. Networked workflows use protected secrets, least-privilege tokens, short-lived credentials where available and read-only repository permissions unless an audited content update requires more.

Discovery, annotation and publication packaging are separate stages. Adapters and models do not receive repository write credentials or deployment authority.

## Untrusted content and prompt injection

All retrieved metadata, pages, documents, snippets, feeds and posts are untrusted data. Processing must:

- parse content as data and never execute embedded scripts, macros, shell commands or templates;
- strip active HTML and render only escaped, allow-listed fields;
- isolate evidence from system/developer instructions;
- state that source instructions cannot authorize actions or alter policy;
- bound input size, redirects, nesting and file types;
- record the exact evidence shown to the model;
- flag suspected prompt injection and quarantine contaminated output; and
- avoid exposing secrets, network tools, repository writes or publication credentials to the model.

## Bounded network access

Networked adapters use identifiable user agents, allow-listed schemes, timeouts, retry caps, caching and rate limits. They block private, loopback, link-local and cloud-metadata address ranges. Redirects and canonical URLs are revalidated. Retrieval respects source terms, robots rules and licences; paywalls are never circumvented.

Tests remain network-independent. Live discovery is an explicit mode with a run manifest and bounded lookback/result limits.

## Safe failure and publication transactions

Runs stage output outside the public store. A failed or partial run never deletes prior records or publishes incomplete data. Only a fully validated staging set and successful static build can replace the publishable artefact. Operational reports expose adapter errors, withheld/quarantined counts and whether the previous public state was retained.

## Branch protections

Before production authorization:

- protect `main` against direct/force pushes;
- require review for workflows, schemas, prompts, source/search policy, security, governance and disclosure wording;
- require validation, tests, build, internal-link and accessibility checks;
- restrict workflow permissions and third-party actions;
- separate an automation content branch from the reviewed control plane; and
- protect deployment environments independently.

Automatically generated records need not receive item-level approval, but their run manifest and resulting commit/artefact remain auditable.

## Incident handling

Revoke exposed secrets before history cleanup. For unsafe or incorrect published material, mark unavailable, correct or remove the listing, preserve the audit record, assess scope and document remediation. Repeated quality or safety incidents trigger reconsideration under ADR 0002.
