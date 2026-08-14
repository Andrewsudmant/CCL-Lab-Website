# Cities & Climate Learning Lab — Gate 3B–4A handoff

## What we did and why

This work turns the Gate 2–3A prototype into a private launch candidate without deploying it. The public site now separates current lab research from foundational prior work and associated collaborations. Andrew Sudmant’s approved profile and contact details are canonical structured data. Publication metadata was rebuilt through ORCID discovery and identifier enrichment, with exact titles, complete ordered authors, supported date precision and explicit provenance.

Research Watch now has a bounded private staging path: provider-specific discovery, normalization, DOI/URL deduplication, conservative event clustering, evidence sufficiency, deterministic publication controls, diversity caps, a run manifest and atomic last-known-good replacement. A failed validation leaves the prior staging set intact. The public disclosure continues to make clear that AI is a discovery and annotation mechanism, never the source or an endorsement.

## Challenges and limitations

- OpenAlex and Crossref were reachable in the private pilot.
- DataCite was attempted as an identifier-specific fallback; the sampled Crossref DOI was not in DataCite.
- Bluesky returned HTTP 403 from this environment. It was not bypassed.
- No OpenAI key, model or explicit cost cap was configured, so no paid call was made.
- The 35-item calibration set is real but academic-heavy and intentionally includes plausible negatives to measure precision. Reports, news, tools, commentary and Bluesky need a later provider-enabled calibration supplement.
- No profile photograph was used because reusable rights were not supplied.

## Transparent and traceable governance

Structured records preserve stable identifiers, original URLs, publication and retrieval dates, evidence types, model/prompt versions, confidence, risk flags, review status and correction state. Bibliographic identity is never AI-rewritten. Owner overrides apply after providers and are reported. Public Research Watch records carry the full landing-page disclosure and compact item disclosure. Internal security, architecture, pilot and governance documents remain in the repository but are excluded from the public site and search index. External content is treated as untrusted and cannot change prompts, thresholds, governance or publication rules.

## What to consider next

Before Gate 4B or production deployment, the owner should:

1. label the calibration set and decide whether an additional non-academic calibration supplement is required;
2. select an OpenAI model and hard per-run item and cost caps, or decide to omit paid web search;
3. configure and verify a supported Bluesky network path;
4. approve publication featured status and review any unresolved ORCID reconciliation items;
5. decide hosting, privacy/accessibility statements, branch protection and repository variables;
6. confirm whether an owner-supplied, rights-cleared portrait should be added;
7. approve automatic staging-branch writes separately—the repository variable remains disabled by default.

## Local review

Open `rendered-site/index.html` from the owner-review ZIP. If browser security blocks local navigation, run `python3 -m http.server 8000 --directory rendered-site` from the unzipped directory and open `http://localhost:8000/`. The calibration ZIP is separate; open `owner-labelling.html` and use its download button after reviewing original sources.

## Boundary

No merge to `main`, public deployment, DNS change, analytics, authentication, subscriber collection or unattended production write was performed.
