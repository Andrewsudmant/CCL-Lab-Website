# Cities & Climate Learning Lab — Gate 5D handoff

Status: `GATE_5D_PASS_WITH_SOURCE_VERIFICATION_LIMITATIONS`

## What changed and why

Gate 5D replaced the project-only public model because the lab's research is not composed only of bounded projects. The active model now separates four current research themes from research work, publications/outputs and possible research ideas. Work may be a programme, research line, project, study, paper, report, tool or dataset. A paper may stand alone when no genuine parent is evidenced; the system no longer invents a project to make a listing look complete.

Work carries its own ongoing/completed status and relationship to the lab. This keeps intellectual themes equal while allowing the site to distinguish current CCLL work, work begun before CCLL and continuing, foundational prior work and associated collaboration. The canonical route is `/work/`; `/projects/` remains as a transition for existing links.

## Migration outcome

- Geography of urban climate evidence became an ongoing standalone paper whose title derives from its canonical preprint; it has no parent.
- Data Methodologies remains a completed foundational project.
- Climate delivery modes became an ongoing CCLL research programme linked to the verified August 2026 paper.
- CoBen became an ongoing CCLL programme with conditional-scenario and valuation boundaries.
- Occupational transitions became an ongoing research line because no bounded project dates, funder or deliverables were evidenced.
- UK Co-Benefits Atlas remains a completed foundational project; its still-available public interface is a separate linked tool.

There are seven Work records: five ongoing and two completed. Forty-two of 46 canonical publications have no Work parent, which is valid; one is also represented as the standalone ongoing Geography paper. Connected publication cards are deduplicated where Work already represents the same object.

## Prior work and source limitations

Selected completed/foundational examples are justified from publisher abstracts, institutional records, repository descriptions or lawful full text—not titles alone. The four theme pages display 6, 4, 8 and 12 completed/foundational examples respectively. MDPI work remains in the complete verified bibliography but is not promoted as a theme example.

The verified public inventory contains 46 records. Nine earlier ORCID-only groups were resolved through authoritative sources and one was excluded after an authorship check. Ten ORCID-only groups still lack enough authoritative metadata and remain withheld rather than guessed. This is why the gate uses the source-verification-limitations status.

## Research ideas governance

Thirteen ideas are stored under a schema separate from Work: 3 Geographies, 3 New Evidence, 3 Delivery and 4 Consequences. Every card says exactly `Research idea · not currently an active or funded project`. Ideas contain no funder, partner, date, finding, recruitment claim or publication/Current Conversations link. They are draft owner-review questions with suggested methods, not commitments or open opportunities.

## Transparent and traceable governance

Canonical records preserve stable IDs, source URLs/identifiers, publication and retrieval dates, verification state, relationship rationales, claim boundaries and corrections. Theme-example selection has a separate audit recording evidence reviewed, relationship reason, uncertainty and exclusion decisions. Historical themes, project migrations and old routes remain available as decision evidence.

Current Conversations remains a separate external horizon-scanning layer and appears last on theme pages. Inclusion is not endorsement or evidence evaluation. Fixtures with `ai_provenance.used=false` explicitly say that no AI generation was recorded and do not masquerade as live discovery. No external item or idea can become lab-authored Work through generation.

The repository/history scan found zero credential-pattern findings across 1,210 reachable Git blobs and 610 present files. No paid/model call, deployment, merge, API-key access, history rewrite or force-push occurred.

## Challenges and controls

- Converting generated pages exposed a delete-before-regenerate weakness. Cleanup now runs only after all current pages are written, preserving the last complete source tree if generation fails.
- Source scarcity required restraint. Unresolved ORCID-only groups and weak theme relationships were withheld instead of inferred.
- The in-app browser could not expose a numeric zoom percentage or reliable synthetic sequential-Tab traversal. Desktop/mobile checks passed; the enlarged check used a conservative 720-CSS-pixel equivalent, and visible focus styling was verified directly.
- One deprecation warning remains from the intentional `research_watch` compatibility import.

## Quality and Git state

- 84 records and 17 schemas validated
- 118 tests passed; one known compatibility deprecation warning
- 112 pages rendered
- Internal links passed
- Static accessibility passed for all 112 pages
- Desktop, mobile and enlarged-width QA passed with no horizontal overflow or captured console errors
- Branch: `codex/gate-5c-thematic-consistency`
- Draft pull request: https://github.com/Andrewsudmant/CCL-Lab-Website/pull/1
- No merge or deployment

## What to think about next

1. Confirm that the expanded themes are useful and equally current.
2. Confirm the distinctions among programme, research line, project, standalone paper, tool and idea.
3. Review whether every previous-work example is convincing and appropriately qualified.
4. Review each possible research direction and suggested method; approval does not by itself make it active work.
5. Decide whether to resolve any of the ten withheld ORCID-only groups with new authoritative evidence.
6. Only after owner approval, decide whether to merge PR #1. Paid benchmarking, staging writes, deployment, Pages and DNS remain separate future decisions.

## Exact next owner action

Review the Gate 5D owner package, focusing on the expanded theme descriptions, the distinction among programmes, projects, standalone papers and ideas, the selected examples of previous work, and whether the research ideas are clearly presented as possibilities rather than active commitments.
