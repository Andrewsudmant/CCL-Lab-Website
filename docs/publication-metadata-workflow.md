# Publication metadata workflow

## Source priority

1. Owner overrides in `config/publication_overrides.yml` resolve deliberate editorial
   choices and must link to evidence in the pull request.
2. ORCID `0000-0001-8650-8419` supplies the principal identity and work identifiers.
3. Crossref enriches DOI records with title, author, date, venue and type metadata.
4. Publisher records resolve remaining conflicts where possible.

No source silently overwrites an owner override. A refresh produces a diff for review;
it does not publish directly to `main`.

## Conflict and deduplication rules

- Normalize DOI case and remove resolver prefixes before comparing records.
- Prefer DOI identity; otherwise compare a normalized title plus year and first author.
- Preserve all source values in the refresh report when sources disagree.
- Prefer a complete date over a year-only date only when the source is authoritative.
- Never merge two records solely because their titles are similar.
- Reject duplicate canonical DOIs, URLs and record IDs in validation.

## Owner override format

Each key is a canonical publication record ID. A value may replace a field, suppress a
candidate or state that two provider records are the same work. Overrides record a
reason and review date. The initial file is intentionally empty pending owner review.

## Scheduled maintenance

The scheduled publication refresh creates a branch, runs the bounded metadata job,
validates the result and opens a pull request. Publication listings change only after
the pull request is reviewed and merged. Credentials, raw provider payloads and
private metadata are never committed.
