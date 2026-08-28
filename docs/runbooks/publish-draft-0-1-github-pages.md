# Owner runbook: publish Draft 0.1 with GitHub Pages

This runbook describes a later owner-controlled action. Gate 5G does not run the workflow, enable Pages or deploy anything.

## Required workflow input

Workflow: **Publish Draft 0.1 to GitHub Pages** (`.github/workflows/public-draft-pages.yml`)

| Input | Required value |
|---|---|
| `confirm_draft_0_1` | `true`, only after content and CI approval |

## Required repository configuration

| Kind | Exact name | Required value or rule |
|---|---|---|
| Repository variable | `PUBLIC_DRAFT_DEPLOY_ENABLED` | `true` only during an approved publication window; absent/false fails closed |
| Environment | `public-draft` | Required reviewers; prevent self-review where available; restrict to `main` |
| Pages source | GitHub Actions | Configure only after merge and branch protection |

No secret or API key is required. Do not add `OPENAI_API_KEY` or any Current Conversations credential to this environment.

## Approval sequence

1. Review the Gate 5G owner package, especially the four curated sets and contribution statements.
2. If approved, mark draft PR #1 ready for review; obtain the required review and confirm all checks on the exact head commit.
3. Protect `main`: require pull-request review and checks; block force pushes and deletion; avoid direct pushes.
4. Merge PR #1 with a merge commit so the gate history remains visible. Do not squash the governance history.
5. In Settings → Pages, choose **GitHub Actions** as the publishing source.
6. Create the protected environment `public-draft`, add required reviewers and restrict deployment to `main`.
7. Add repository variable `PUBLIC_DRAFT_DEPLOY_ENABLED=true`.
8. Manually dispatch **Publish Draft 0.1 to GitHub Pages** from `main` with `confirm_draft_0_1=true`.
9. Approve the `public-draft` environment only after the build job passes and identifies the expected commit.
10. Inspect the published Draft 0.1 at desktop, mobile and 200% reflow. Verify navigation, search, correction route, affiliation, banner, and the absence of Current Conversations entries/feeds.
11. Set `PUBLIC_DRAFT_DEPLOY_ENABLED=false` after the approved deployment window.

## What the workflow checks

The build job has `contents: read`, validates content, deterministically builds before tests, runs all tests, checks root links/accessibility, builds and checks `/CCL-Lab-Website/`, confirms Draft 0.1 status, confirms Current Conversations remains disabled and checks for fixture leakage. Only the separate deployment job has `pages: write` and `id-token: write`.

## Rollback

Immediately set `PUBLIC_DRAFT_DEPLOY_ENABLED=false` to prevent another dispatch. For a content rollback, create a reviewed pull request that restores the last-known-good source commit, rerun checks, merge with a merge commit and manually dispatch again. Do not rewrite Git history, delete provenance or silently alter a published record.

## Privacy and tracking

Draft 0.1 adds no analytics, cookies, newsletter collection or public form. Contact and correction requests use the published SFU email address.
