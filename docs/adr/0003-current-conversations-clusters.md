# ADR 0003: Current Conversations and conversation-centred records

- Status: Accepted
- Date: 2026-08-17
- Decision owner: Project owner
- Supersedes: Research Watch public naming and its source-centred presentation

## Context

The former Research Watch name and item model suggested a research-literature feed.
The intended public feature is broader: it should show where the lab's themes are being
discussed across research, policy, institutions, news, commentary, tools and public
discussion without implying endorsement or equal evidentiary weight.

## Decision

The public feature is **Current Conversations**, with the navigation label
**Conversations**. The canonical content model separates individual sources from public
conversation clusters. A cluster may have one source and later gain related sources
without changing public identity. Source environment describes where material appears;
source role describes what it contributes. These dimensions remain separate because a
newsroom, journal, government site, blog or social platform does not by itself establish
the source's evidentiary role.

Principal sources follow an explicit originality hierarchy, with recorded exceptions
when the highest-ranked type does not contain the central claim. Identifier and URL
relationships precede conservative model-assisted clustering, and deterministic controls
accept or reject proposals. Merge, split and principal-source changes are retained in
history.

The former route remains as an accessible compatibility page. Python imports, Make
targets and one environment variable may retain one-gate warning shims. Historical
records and decisions are not renamed retrospectively.

## Consequences

Public entries can reveal how an original paper, policy or tool is reported, analysed or
contested without collapsing authorship into a synthetic citation. Rendering and feeds
must resolve cluster-to-source links, and transaction validation is more demanding. The
system must state disagreement and source inequality rather than average claims.

## Revisit triggers

Reconsider the model if clustering obscures attribution, correction volume becomes
unmanageable, the feature cannot represent important single-source discussions, source
access changes materially, or owner calibration shows that readers consistently
misinterpret inclusion as endorsement.
