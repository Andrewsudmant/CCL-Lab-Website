# Gate 4B–5A staging exercise

The local fixture pilot wrote 26 sources, 25 clusters, JSON Feed, RSS, a generated site fragment, run manifest and zero-cost budget ledger to `staging/current-conversations/current` through the multi-artefact atomic transaction. Validation completed before replacement.

The GitHub workflow is repository-read-only by default. Its write job requires `CURRENT_CONVERSATIONS_STAGING_WRITE_ENABLED == true`, has its own `contents: write` permission, verifies the changed-path allowlist and pushes only `automation/current-conversations-staging`. `main` is never a target and no deploy step exists.

A local bare-remote exercise successfully pushed one allow-listed manifest only to `automation/current-conversations-staging`; the temporary remote contained no `main` reference and was deleted afterward. A hosted staging-branch exercise was not possible because this repository has no configured remote. Production branch protection remains an owner action.

Status: `GATE_4B_5A_PASS_WITH_PROVIDER_OR_REMOTE_LIMITATIONS`.
