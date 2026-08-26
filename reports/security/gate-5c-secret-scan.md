# Gate 5C repository and history secret scan

Pre-first-push run: 26 August 2026

- Reachable Git blobs scanned: 1,045
- Present repository files scanned: 515
- Findings: zero
- Pattern classes: private keys, OpenAI keys, GitHub tokens, AWS access keys, Slack tokens, Stripe live keys and Google API keys
- Exclusions: `.git` internals, virtual environments, `_site`, Quarto caches, `deliverables` and Python caches

The scan reports only locations and suspected types if a match occurs; it never prints a matched value. A later post-handoff scan covered 1,050 reachable blobs and 518 present files, also with zero findings. No API key was requested, accessed or stored.

This pattern scan supplements—not replaces—review of fixture/source policy. The Gate 5C owner package and compact handoff exclude raw provider responses, private calibration labels, environment files, build caches and credentials.
