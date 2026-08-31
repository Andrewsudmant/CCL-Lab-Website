# Gate 5I bounded external-link diagnostic

## Interpretation and bounded follow-up

53 of 57 HEAD endpoints were reachable (2xx) or returned redirects. Redirect destinations were deliberately not followed, so this is not a full downstream availability certification. Three GET follow-ups on the same approved hosts used an eight-second timeout and read at most 1 KiB without persisting bodies: Bluesky returned 200; `ukcobenefitsatlas.net/` and `/about` both returned 503. LinkedIn's HEAD 405 is an automated-method restriction, not proof of a dead link.

These four initial exceptions do not alter canonical identity or prove a source has disappeared. The two Atlas URLs are an external-service availability warning for owner inspection before/after publication; do not silently remove the associated Work or publication. No paid API, model, ingestion run or metadata refresh was made. This explicitly bounded availability diagnostic is acceptable for a labelled public draft, with the limits retained in the readiness report.

## HEAD evidence

UTC: 2026-08-31T16:10:12.628354+00:00
57 distinct public-source URLs; 15 approved hosts; maximum 60 requests; 8-second timeout; 240-second total limit; 0.2-second minimum interval.
HEAD only. No redirects followed, response bodies read or persisted, API requests, model calls, credentials or provider refreshes. A redirect verifies only the starting endpoint. Non-2xx responses are diagnostics, not proof that the underlying source is absent.

| URL | Result |
|---|---|
| https://arxiv.org/abs/2604.20781v2 | Reachable; HTTP 200 |
| https://bsky.app/profile/andrewsudmant.bsky.social | Unverified: requires owner/source review; HTTP 404 |
| https://coalitionforurbantransitions.org/wp-content/uploads/2020/03/Building-climate-resilience-and-water-security-in-cities-lessons-from-the-Sponge-City-of-Wuhan-China-final.pdf | Redirect (not followed); HTTP 301 |
| https://doi.org/10.1002/sd.1906 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1002/sd.2221 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1007/978-3-319-74983-9_28 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1007/s00267-024-01991-5 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1007/s10113-017-1112-x | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1007/s10584-016-1751-9 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1007/s13412-024-00955-9 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/b978-0-12-818122-5.00019-3 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/j.adapen.2022.100111 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/j.apenergy.2016.07.112 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/j.cities.2015.10.010 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/j.eneco.2022.105872 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/j.enpol.2015.01.020 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/j.gloenvcha.2015.07.009 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/j.jclepro.2017.12.139 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/j.jenvman.2015.08.001 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/j.rser.2019.109623 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/j.sciaf.2025.e02959 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1016/j.uclim.2017.02.011 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1038/s41598-025-12210-4 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1038/s42949-024-00168-7 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1038/s44168-026-00408-9 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1080/12265934.2024.2382706 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1080/14693062.2015.1104498 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1080/14693062.2021.1948383 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1080/17565529.2015.1040367 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1080/23748834.2025.2468017 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1177/0956247816677775 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1177/09562478231190475 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.1177/2455747117708929 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.17645/up.8302 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.20935/acadenvsci6141 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.21203/rs.3.rs-1676382/v1 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.21203/rs.3.rs-9268986/v1 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.3390/land13050641 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.48550/arXiv.2604.20781 | Redirect (not followed); HTTP 302 |
| https://doi.org/10.5281/zenodo.8075492 | Redirect (not followed); HTTP 302 |
| https://edemocracy.northyorks.gov.uk/documents/s10308/Yorkshire%20and%20Humber%20Climate%20Action%20Plan.pdf | Reachable; HTTP 200 |
| https://eprints.whiterose.ac.uk/183447/ | Redirect (not followed); HTTP 301 |
| https://orcid.org/0000-0001-8650-8419 | Reachable; HTTP 200 |
| https://uk.linkedin.com/in/andrew-sudmant-89393a32 | Unverified: automated access refused; HTTP 405 |
| https://ukcobenefitsatlas.net/ | Unverified: requires owner/source review; HTTP 503 |
| https://ukcobenefitsatlas.net/about | Unverified: requires owner/source review; HTTP 503 |
| https://www.lse.ac.uk/granthaminstitute/publication/financing-climate-action-with-positive-social-impact-how-banking-can-support-a-just-transition-in-the-uk/ | Reachable; HTTP 200 |
| https://www.lse.ac.uk/granthaminstitute/publication/investing-in-a-just-transition-in-the-uk/ | Reachable; HTTP 200 |
| https://www.nature.com/articles/s44168-026-00408-9 | Redirect (not followed); HTTP 303 |
| https://www.research.ed.ac.uk/en/persons/andrew-sudmant/ | Reachable; HTTP 200 |
| https://www.research.ed.ac.uk/en/projects/data-methodologies-for-climate-impact-assessment/ | Reachable; HTTP 200 |
| https://www.research.ed.ac.uk/en/publications/a-net-zero-carbon-roadmap-for-belfast | Redirect (not followed); HTTP 301 |
| https://www.research.ed.ac.uk/en/publications/a-net-zero-carbon-roadmap-for-edinburgh | Redirect (not followed); HTTP 301 |
| https://www.research.ed.ac.uk/en/publications/a-net-zero-carbon-roadmap-for-leeds | Redirect (not followed); HTTP 301 |
| https://www.sfu.ca/rem/about/people/sudmant.html | Reachable; HTTP 200 |
| https://www.theigc.org/publications/car-free-days-pollution-free-cities-reflections-clean-urban-transport-rwanda | Reachable; HTTP 200 |
| https://zenodo.org/record/8075492 | Redirect (not followed); HTTP 301 |
