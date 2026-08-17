# Gate 5B repository and history secret scan

Date: 2026-08-17

Command: `PYTHONPATH=. .venv/bin/python scripts/scan_repository_secrets.py`

- Reachable Git blobs scanned: 665
- Present repository files scanned: 473
- Credential pattern classes: private keys, OpenAI keys, GitHub tokens, AWS access keys, Slack tokens, Stripe live keys and Google API keys
- Findings: 0

The scanner reports only the location and pattern class if it detects a match; it never prints a matched value. Build output, virtual environments, Git internals, deliverable ZIPs and caches are excluded from the present-file pass. Reachable historical blobs are scanned independently, so removing a file from the working tree cannot hide a historical match.

This pattern scan is one control, not proof that no sensitive information exists. Pull-request review, GitHub secret scanning, least-privilege environments and credential rotation remain required.
