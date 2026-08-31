# Owner runbook: publish Draft 0.1 with GitHub Pages

Gate 5I prepares this procedure; it does not execute it. The owner controls each step. GitHub interface wording was checked against official documentation on 31 August 2026. Repository: `Andrewsudmant/CCL-Lab-Website`; PR #1: **Prepare the Draft 0.1 release candidate**.

## Exact inputs

| Setting | Required value |
|---|---|
| Workflow | **Publish Draft 0.1 to GitHub Pages** |
| Workflow file | `.github/workflows/public-draft-pages.yml` |
| Branch | `main`, containing the reviewed merge |
| Boolean input | `confirm_draft_0_1=true` |
| Repository Actions variable | `PUBLIC_DRAFT_DEPLOY_ENABLED=true` only during an approved publication window |
| Environment | `public-draft`, required owner review, only branch `main` |
| Pages source | GitHub Actions |
| Artifact directory | `_site-project-path/CCL-Lab-Website` |

No secret or API key is required. Do not add Current Conversations or OpenAI credentials. Keep `site_status: draft`, `site_version: "0.1"` and Current Conversations in development with its public feed disabled.

## Phase 1 — review and merge

1. Complete the Gate 5I owner review and any manual keyboard checklist named in the final readiness report.
2. In PR #1 → **Checks**, confirm **Site checks / build-and-test** succeeds on the exact final head SHA, not an earlier commit.
3. Review **Files changed**, the owner-decision record and `docs/reviews/gate-5i/draft-0-1-final-readiness.md`. Obtain any required independent approval; marking a PR ready is not an approval.
4. In the merge-button dropdown choose **Create a merge commit**, then **Merge pull request** and confirm. Do not squash, rebase-merge or enable auto-merge.
5. Open **Code**, select `main`, confirm it includes the reviewed Gate 5I head and record the merge SHA.

## Phase 2 — protect main

Open **Settings → Branches → Add classic branch protection rule** (edit an existing exact-match rule if present). Set branch-name pattern `main`.

1. Enable **Require a pull request before merging**. Require approving review when an independent reviewer is available; authors cannot approve their own PRs. Do not invent an approval or expand collaborator access as a workaround.
2. Enable **Require status checks to pass before merging** and **Require branches to be up to date before merging**. Select **build-and-test** from GitHub Actions, displayed under **Site checks**. The workflow name alone is not the required check context.
3. Require conversation resolution. Leave **Allow force pushes** and **Allow deletions** unchecked.
4. Leave **Require linear history** off: the project retains merge commits. Do not require deployment before merge.
5. Prefer **Do not allow bypassing the above settings**. If a sole maintainer needs emergency administrator override, record that deliberate exception and every use; it is not routine direct-push permission.
6. Save and inspect the protection summary. Do not change visibility or collaborators.

See GitHub's [branch-protection controls](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule).

## Phase 3 — configure public-draft deployment

1. **Settings → Pages → Build and deployment → Source:** select **GitHub Actions**. Keep the custom domain empty. Skip suggested templates; this repository already has its guarded workflow.
2. **Settings → Environments → New environment:** enter `public-draft`, then **Configure environment**.
3. Enable **Required reviewers**, select the owner and save. If the owner will both dispatch and approve, leave **Prevent self-review** off. Enable it only when a separate authorized reviewer will approve; otherwise it blocks the intended approval. Do not bypass environment review.
4. Under deployment branches and tags choose **Selected branches and tags**; add a **Branch** rule for exact pattern `main`, with no tags or other branches. Save and recheck.
5. **Settings → Secrets and variables → Actions → Variables → New repository variable:** name `PUBLIC_DRAFT_DEPLOY_ENABLED`, value `true`. This is a non-secret switch. Set it only when ready to publish.

See [Pages source configuration](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) and [environment approval rules](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).

## Phase 4 — publish

1. Open **Actions → Publish Draft 0.1 to GitHub Pages → Run workflow**. Manual dispatch is available after the workflow is on default branch `main`.
2. Select `main`, check Draft 0.1 confirmation (`confirm_draft_0_1=true`) and click **Run workflow** once.
3. Inspect the run's source SHA. Guard/build jobs have `contents: read`. They validate records, build before tests, run tests and link/accessibility checks, build the project path, confirm draft/disabled-feed configuration and reject fixture leakage before uploading.
4. After build passes, choose **Review deployments**, select `public-draft`, verify the expected SHA and approve. Only the deployment job receives `pages: write` and `id-token: write`. Stop on any failed check.
5. Open the successful run's published URL. Expected project route: `https://andrewsudmant.github.io/CCL-Lab-Website/`; treat the run's actual URL as authoritative.

See GitHub's [manual dispatch](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow) and [deployment review](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/review-deployments) instructions.

## Phase 5 — post-publication safety

1. Immediately edit repository variable `PUBLIC_DRAFT_DEPLOY_ENABLED` back to `false`.
2. Inspect desktop, mobile and 200% zoom: homepage, all four themes and five selected Delivery examples, Work, publications and metadata page, Current Conversations, contact and footer. Test keyboard navigation, search, filters and correction links.
3. Retain the Draft 0.1 banner. Confirm Current Conversations has no entries, fixtures, counts or feeds and leave it disabled.
4. Through the next PR, record the live URL, deployment run URL, source/merge SHA, date, reviewer and any issues in a dated release record. Keep private correspondence out of the public repository.

## Rollback without rewriting history

1. Set `PUBLIC_DRAFT_DEPLOY_ENABLED=false`. Cancel any queued/running publication workflow and reject waiting deployment approvals: changing the variable does not cancel a run whose guard already passed.
2. For urgent withdrawal, use **Settings → Pages → Unpublish site** (or the available disable-source control). Record why and when. Disabling the variable alone does not remove the live site.
3. Identify the last-known-good source SHA from a successful deployment. Open a new branch and reviewed PR restoring affected sources using ordinary revert commits. Preserve correction/provenance records; never reset or force-push `main`.
4. Run both profiles and Site checks, merge the rollback PR with a merge commit, temporarily enable the deployment variable and manually dispatch the guarded workflow on `main`. Approve after checks. Do not dispatch an old feature branch: environment protection permits only `main`.
5. Inspect the restored site, set the variable back to `false` and record the rollback run and SHA.

Draft 0.1 has no analytics, newsletter collection or public form. Custom domain, live API calibration and automated Current Conversations publication remain separate later decisions.
