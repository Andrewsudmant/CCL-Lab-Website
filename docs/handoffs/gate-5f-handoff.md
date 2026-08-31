# Cities & Climate Learning Lab — Gate 5F handoff

## What changed and why

Gate 5F completes the final site-level reader-value pass before previous-work curation and public Draft 0.1 hardening. The homepage now makes one claim unavoidable: **urban climate evidence does not become useful merely because it exists.** It explains the risk of separating judgements about relevance, new evidence, delivery and consequences, then gives researchers, policy and practice readers, and prospective students or collaborators a clear route into the site.

Homepage theme cards now create intellectual tension rather than repeat definitions. Theme pages retain their complete approved argument but expose one proposition, one restrained boundary and a later connection to the cycle. The structured fields remain in YAML so revisions, review and corrections stay traceable.

The 24 possible research ideas remain six per theme. Two per theme provide a reading hierarchy and four appear as additional directions. This is not a ranking, priority list, funding signal or pipeline. Full method lists remain stored; at most three separately governed tags appear publicly. Reader/decision fields describe only audiences already supported by approved text.

Work pages now read as mini-arguments: problem, question, approach, possible reader value, evidence status and boundaries, outputs, metadata and authoritative sources. Ongoing work uses prospective language. Completed work remains source-backed. Unsupported output sections are omitted rather than padded.

Our Approach now identifies six places where the four-theme learning cycle can break down. A static active-travel example shows how the questions connect and is clearly labelled hypothetical—not evidence, a score or policy advice. Current Conversations now begins with the difficulty of tracing dispersed discussion and its underlying sources; it remains **In development**, with no public feed or fixture content.

## Challenges and resolutions

- Quarto initially placed the semantic Work `<aside>` in a margin column, producing 61–77 pixels of desktop overflow. It was changed to a labelled content `<section>`; all seven Work pages then passed desktop, mobile and reflow checks with zero overflow.
- Gate 5E froze entire Work files by hash, which conflicted with the explicitly required Gate 5F argument fields. The freeze now protects what the owner decision actually fixes: selection, order, theme relationships and public rationales.
- Full structured editorial fields were valuable for governance but visually repetitive. Templates now combine them into coherent public arguments while audits retain field-level provenance.
- Full-page browser screenshots are very tall on idea-heavy theme pages, so the package includes both complete captures and readable `*-opening.png` viewport captures.

## Transparent and traceable governance

Canonical theme text remains in `config/research_scope.yml`; ideas and Work remain human-readable YAML validated by JSON Schema. Deterministic generation preserves a single source of truth. Audits show every public method-tag selection, narrative tier, Work claim and evidence basis. The previous-work proposal is private and marked not implemented; public selections and rationales did not change.

AI remains a discovery and annotation layer, never a source. Current Conversations public disclosure still depends on actual provenance, fixtures remain non-public, and builds/tests make no network or model calls. Correction, removal, human-review and source-provenance rules remain in the governance documents. The final repository/history scan records no credential-pattern findings. ZIPs remain ignored outside Git.

## Quality result and remaining limitations

- 95 records validated against 18 schemas.
- 142 tests passed; one pre-existing `research_watch` compatibility import deprecation warning remains.
- 87 pages rendered.
- Internal links and static accessibility passed for all 87 pages.
- Desktop, mobile and 200%-equivalent reflow passed with one `main`, one `h1`, no horizontal overflow and no captured console warnings/errors.
- Explicit focus CSS remains present; automated browser key dispatch did not move focus from the body, so the focus indicator was verified through the rendered stylesheet rather than a captured focus screenshot.
- Representative examples in `config/research_scope.yml` remain clearly marked placeholders requiring owner review.
- Previous-work curation, final public-release hardening and any live Current Conversations work remain out of scope.

## What to think about next

1. Is the homepage’s central claim accurate and memorable?
2. Are the three reader communities and destinations right?
3. Do signature questions improve navigation without suggesting priority?
4. Does each Work page strike the right balance between intellectual contribution and evidence boundary?
5. Does the hypothetical example clarify the cycle without sounding prescriptive?
6. Which previous-work examples should be retained, regrouped, rewritten or removed in the separate academic curation gate?
7. Are all remaining placeholder examples needed before Draft 0.1 publication?
8. After curation, what owner approval sequence should govern public Draft 0.1 publication?

## Branch and pull request

Work remains on `codex/gate-5c-thematic-consistency` in draft PR #1. The branch is not merged. GitHub Pages, deployment, DNS, Current Conversations live feeds and staging writes remain disabled. No paid/API call was made.

## Exact next owner action

Review the Gate 5F owner package, focusing on the homepage’s central claim, audience pathways, simplified theme and idea presentation, argument-led Work pages, the worked illustration and Current Conversations. Previous-work examples remain unchanged and will receive the final separate academic curation before Draft 0.1 publication.
