"""Crossref discovery and DOI metadata enrichment."""

from __future__ import annotations
from research_watch.adapters.base import DiscoveryAdapter, get_json
from research_watch.models import DiscoveredItem


class CrossrefAdapter(DiscoveryAdapter):
    name = "crossref"
    endpoint = "https://api.crossref.org/works"

    def search(self, query: str, query_id: str, limit: int = 10) -> list[DiscoveredItem]:
        payload = get_json(self.endpoint, {"query.bibliographic": query, "rows": min(limit, 25), "select": "DOI,title,author,published-online,published-print,URL,publisher,container-title,abstract"})
        items = []
        for work in payload.get("message", {}).get("items", []):
            date_parts = ((work.get("published-online") or work.get("published-print") or {}).get("date-parts") or [[]])[0]
            date = "-".join(str(v).zfill(2) for v in (date_parts + [1, 1])[:3]) if date_parts else ""
            title = (work.get("title") or ["Untitled"])[0]
            authors = [" ".join(filter(None, (a.get("given"), a.get("family")))) for a in work.get("author", [])]
            abstract = work.get("abstract")
            doi = work.get("DOI")
            items.append(DiscoveredItem(title=title, url=work.get("URL") or f"https://doi.org/{doi}",
                source_name=(work.get("container-title") or [work.get("publisher") or "Crossref"])[0],
                source_type="academic-paper", publication_date=date, authors=authors, doi=doi,
                abstract=abstract, evidence_types=["abstract"] if abstract else ["metadata-only"],
                adapter=self.name, query_id=query_id, raw_metadata=work))
        return items
