# Gate 5G bounded external-link audit

Checked: 28 August 2026  
Method: bounded HTTP GET with redirects, 18-second timeout and an identifying release-audit user agent. No paywall or access control was bypassed.

## Summary

- Working or authoritatively redirected: 19
- Temporarily unavailable: 2
- Access restricted to the automated audit client: 5
- Permanently broken: 0
- Ambiguous: 0

## Working or redirected

SFU faculty profile; ORCID; University of Edinburgh person and project/publication records; Bluesky profile; Nature delivery-modes article; Research Square DOI; Elsevier DOI records for producer/consumer cities, integrated planning, and transport consequences; Springer records for Data Scaling, urban carbon blind spots, climate policy as social policy, and affordability; RePEc; Cogitatio; White Rose repository; and the LSE just-transition finance report all returned HTTP 200 after any normal redirect.

## Temporarily unavailable

| URL | Observation | Treatment |
|---|---|---|
| `https://ukcobenefitsatlas.net/` | HTTP 503 | Retained as the official tool URL; temporary service failure is not evidence of a broken canonical record. |
| `https://ukcobenefitsatlas.net/about` | HTTP 503 | Retained as the official methods/team page; recheck before publication. |

## Access restricted

| Source | Observation | Treatment |
|---|---|---|
| Taylor & Francis page for *Replicate and generalize* | HTTP 403 | Retain DOI/publisher link; automated access restriction. |
| Taylor & Francis page for Shanghai retrofit governance | HTTP 403 | Retain DOI; automated access restriction. |
| SSRN record for *Missing the target* | HTTP 403 | Retain stable repository URL; automated access restriction. |
| SAGE page for pro-poor Kolkata | HTTP 403 after DOI redirect | Retain DOI; automated access restriction. |
| LinkedIn profile | HTTP 999 | Retain optional profile link; LinkedIn blocks automated verification. |

No link was classified as permanently broken. The Atlas availability is the only owner-facing recheck recommended immediately before Draft 0.1 publication.
