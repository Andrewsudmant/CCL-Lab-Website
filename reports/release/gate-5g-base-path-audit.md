# Gate 5G root and project-path audit

Audit date: 28 August 2026

## Strategy

- Default Quarto profile: domain-root build in `_site/`.
- `project-path` profile: `website.site-path: /CCL-Lab-Website/`, output in `_site-project-path/CCL-Lab-Website/`.
- Generated links use Quarto project-root paths; Quarto rewrites navigation, cards, scripts, assets, search and transition routes for the active profile.
- No custom domain or future production URL is hardcoded.

## Results

The full 87-page project-path build completed and `scripts/check_links.py --site-dir _site-project-path/CCL-Lab-Website --base-path /CCL-Lab-Website` passed. The root build also completed without unresolved-link warnings. The release workflow uploads only the contents of the project-path site directory so GitHub Pages mounts the artifact at the repository path.

Checked surfaces include navigation, theme/Work/publication cards, footer, `assets/site.js`, search assets, former-theme routes, former-project routes, Current Conversations method and correction links. Current Conversations exposes no JSON/RSS link in either profile.

Canonical metadata remains path-based because no public domain is approved. Quarto applies the active site path; the publication runbook requires live canonical/social metadata inspection after the owner configures Pages.
