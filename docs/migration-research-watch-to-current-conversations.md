# Research Watch → Current Conversations migration map

| Former path or name | Replacement | Identifier treatment | Compatibility and history |
|---|---|---|---|
| `/research-watch/` | `/current-conversations/` | Public cluster IDs are new; source identifiers are retained where a legacy record maps cleanly. | Former route is an accessible static redirect/link page with canonical metadata and no duplicated feed. |
| `/research-watch/methods.html` | `/current-conversations/how-it-works.html` | Not applicable. | The former methods URL links to the new method. |
| `research_watch` | `current_conversations` | Record/run IDs are never rewritten solely for naming. | A one-gate Python import shim emits `DeprecationWarning`. |
| `data/research-watch/` | `data/current-conversations/` | Legacy record IDs remain historical evidence; new source and cluster IDs use `ccs-` and `ccc-`. | Legacy source-centred YAML is retained as migration evidence and is not the new public canonical model. |
| `staging/research-watch/` | `staging/current-conversations/` | Existing run IDs are retained. | Last-known-good material remains available during transition. |
| `calibration/research-watch/` | `tests/fixtures/regression/gate-3b-4a-academic-calibration/` | All 35 IDs are unchanged. | Former exercise is a regression fixture, not the active owner exercise. |
| `research-watch-v1.yml` | `current-conversations-v1.yml` | Former query IDs/version remain in historical manifests. | Old query pack remains in Git history; compatibility loader warns if explicitly selected. |
| `RESEARCH_WATCH_AUTOPUBLISH_ENABLED` | `CURRENT_CONVERSATIONS_STAGING_WRITE_ENABLED` | Not applicable. | Legacy environment variable is read for one gate only, warns, and cannot broaden the allowed write paths. |
| old Make targets | `current-conversations-*` | Not applicable. | Former targets call the new targets with a deprecation warning. |

Historical ADRs, baselines, reports and handoffs continue to use “Research Watch” when
they describe the former system. They are evidence, not current product copy.
