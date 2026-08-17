# Rollback demonstration

The automated test `test_atomic_rollback_preserves_last_known_good` first publishes a valid multi-artefact snapshot, then deliberately fails validation on a replacement. The transaction returns non-zero through the raised exception, writes a failure manifest, removes the temporary directory and leaves the original `run-manifest.json` byte-for-byte unchanged. The same transaction boundary covers sources, clusters, feeds, budget ledger and generated site artefact.

Result on 2026-08-17: **passed** as part of the 64-test suite. No partial replacement or empty staging state was created.
