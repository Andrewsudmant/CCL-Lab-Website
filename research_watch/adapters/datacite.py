"""DataCite identifier enrichment for repository, preprint, data and software DOIs."""

from __future__ import annotations
from urllib.parse import quote
from research_watch.adapters.base import AdapterError, get_json
from research_watch.models import DiscoveredItem


class DataCiteAdapter:
    name = "datacite"
    endpoint = "https://api.datacite.org/dois"

    def enrich(self, doi: str, query_id: str = "datacite-doi-enrichment") -> DiscoveredItem:
        payload = get_json(f"{self.endpoint}/{quote(doi, safe='')}", {})
        attrs = (payload.get("data") or {}).get("attributes") or {}
        titles = attrs.get("titles") or []
        creators = attrs.get("creators") or []
        dates = attrs.get("dates") or []
        published = next((d.get("date") for d in dates if d.get("dateType") in {"Issued", "Available", "Submitted"}), None)
        published = published or str(attrs.get("publicationYear") or "")
        if not attrs:
            raise AdapterError(f"DataCite returned no metadata for DOI {doi}")
        return DiscoveredItem(
            title=(titles[0].get("title") if titles else "Untitled"),
            url=attrs.get("url") or f"https://doi.org/{doi}",
            source_name=attrs.get("publisher") or "DataCite",
            source_type="academic-paper",
            publication_date=published,
            authors=[c.get("name", "") for c in creators if c.get("name")],
            doi=doi,
            platform_identifier=(payload.get("data") or {}).get("id"),
            abstract=next((d.get("description") for d in attrs.get("descriptions", []) if d.get("descriptionType") == "Abstract"), None),
            evidence_types=["metadata-only"], adapter=self.name, query_id=query_id,
            raw_metadata={"provider": "DataCite", "retrieved": True},
        )
