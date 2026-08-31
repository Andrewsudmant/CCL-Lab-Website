# Gate 5D owner review — read this first

Status: `OWNER_REVIEW_REQUIRED`  
Deployment: none  
Paid/model calls: none

Open `rendered-site/index.html` to inspect the complete private static site. A local server is optional; `python3 -m http.server 8000 --directory rendered-site` provides the most faithful link behaviour, then open `http://127.0.0.1:8000/`.

## What changed and why

The former project-only model made heterogeneous research look like conventional projects. Gate 5D separates four current intellectual themes from actual ongoing/completed work, canonical publications/outputs and possible future research ideas. Papers may remain standalone; previous work can illustrate a theme without being called a current CCLL output; and a completed project can connect to a still-live tool.

The principal navigation now says **Work**. `/work/` is canonical, while former `/projects/` URLs remain accessible transition pages. Every theme page now follows the same sequence: purpose and boundary, ongoing work, selected completed/foundational work, visibly separate research ideas, learning-cycle connections and Current Conversations last.

## What to assess

1. Do the expanded theme descriptions add useful depth?
2. Do all four themes clearly appear as current lab research?
3. Are programmes, projects, papers and tools distinguishable?
4. Can standalone papers appear naturally without artificial projects?
5. Does previous work provide convincing, source-supported examples under each theme?
6. Are ongoing, completed and possible future work clearly differentiated?
7. Are research ideas unmistakably ideas rather than commitments?
8. Are the suggested methods plausible and appropriately qualified?
9. Is the Work page more intelligible than the former Projects page?
10. Does Current Conversations remain secondary and clearly external?

## Governance and limitations

Original sources remain authoritative. Each selected publication example has a rationale and evidence-source URL; title-only assignments were withheld. Relationship labels preserve whether work is current CCLL work, began before CCLL and continues, is foundational prior work, or is an associated collaboration. Ideas contain no invented funders, partners, dates, findings or recruitment claims and use the exact non-active/non-funded disclaimer.

Ten ORCID-only publication groups remain withheld because authoritative metadata is insufficient. This is a source-verification limitation, not a schema failure. The known legacy `research_watch` compatibility import still emits one deprecation warning. Browser automation limitations are recorded in `review/browser-qa.md`.

No paid call, secret access, merge, deployment, Pages/DNS/permission change, force-push or history rewrite occurred.

## Included evidence

- `rendered-site/`: complete private site.
- `review/screenshots/gate-5d/`: screenshots produced from the packaged commit.
- `review/gate-5d/`: architecture, theme-copy and research-idea audits.
- `review/content/`: thematic-example and standalone-publication audits.
- `review/migration.md`: exact project-to-work migration.
- `source/schemas/` and `source/data/`: relevant contracts and records.
- `review/full-test.log`, `review/browser-qa.md`, `review/file-by-file-summary.md`.

## Exact next owner action

Review the Gate 5D owner package, focusing on the expanded theme descriptions, the distinction among programmes, projects, standalone papers and ideas, the selected examples of previous work, and whether the research ideas are clearly presented as possibilities rather than active commitments.
