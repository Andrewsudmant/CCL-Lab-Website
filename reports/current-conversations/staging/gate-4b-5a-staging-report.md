# Gate 4B–5A staging report

- **Real hosted staging branch written:** No; the repository has no configured remote.
- **Approved branch:** `automation/current-conversations-staging`.
- **Hosted commit:** Not applicable.
- **Local bare-remote exercise:** Passed; the ephemeral commit hash is recorded in `local-bare-remote-exercise.md`.
- **Allowed-path validation:** Passed for the staged manifest; prompts/control-plane paths were separately rejected by tests.
- **Fixture run ID:** Recorded in `staging/current-conversations/current/run-manifest.json`.
- **Live providers in this fixture execution:** None; network calls were zero.
- **Live-captured source provenance retained:** Eight academic sources captured from the prior bounded OpenAlex run; they remain marked as fixtures here.
- **Fixture providers/environments:** academic research, policy/institutions, news/analysis, blogs/commentary and data/tools. Bluesky has no active fixture entry.
- **Entries:** 26 sources, 25 clusters: 24 standalone and one multi-source cluster.
- **Cost:** CAD 0.00; monthly owner ceiling remaining CAD 20.00.
- **Last-known-good:** Complete source, cluster, feed, ledger and site snapshot retained.
- **Rollback:** Passed automated deliberate-failure exercise; no partial or empty replacement.

The local fixture pilot wrote sources, clusters, JSON Feed, RSS, generated site fragment, run manifest and zero-cost budget ledger through the multi-artefact atomic transaction. Validation completed before replacement.

The GitHub workflow is repository-read-only by default. Its write job requires `CURRENT_CONVERSATIONS_STAGING_WRITE_ENABLED == true`, has isolated `contents: write`, verifies the changed-path allowlist and pushes only the approved branch. `main` is never a target and no deploy step exists.

Status: `GATE_4B_5A_PASS_WITH_PROVIDER_OR_REMOTE_LIMITATIONS`.
