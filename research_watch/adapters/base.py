"""Discovery adapter contract and safe HTTP helper."""

from __future__ import annotations
import json
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from typing import Any
from research_watch.models import DiscoveredItem


class AdapterError(RuntimeError):
    pass


def get_json(url: str, params: dict[str, Any], headers: dict[str, str] | None = None) -> dict[str, Any]:
    target = url + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(target, headers={"User-Agent": "CCLL-Research-Watch/1.0 (research use)", **(headers or {})})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return json.load(response)
    except Exception as exc:
        raise AdapterError(f"request failed for {urllib.parse.urlsplit(url).netloc}: {exc}") from exc


class DiscoveryAdapter(ABC):
    name: str

    @abstractmethod
    def search(self, query: str, query_id: str, limit: int = 10) -> list[DiscoveredItem]:
        """Return normalized candidates without publishing them."""
