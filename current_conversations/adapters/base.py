"""Discovery adapter contract and safe HTTP helper."""

from __future__ import annotations
import json
import urllib.parse
import urllib.request
import urllib.error
import time
from abc import ABC, abstractmethod
from typing import Any
from current_conversations.models import DiscoveredItem


class AdapterError(RuntimeError):
    pass


def get_json(url: str, params: dict[str, Any], headers: dict[str, str] | None = None) -> dict[str, Any]:
    target = url + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(target, headers={"User-Agent": "CCLL-Research-Watch/1.0 (research use)", **(headers or {})})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code in {429, 500, 502, 503, 504} and attempt < 2:
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                delay = min(float(retry_after), 5.0) if retry_after and retry_after.isdigit() else float(attempt + 1)
                time.sleep(delay)
                continue
            raise AdapterError(f"request failed for {urllib.parse.urlsplit(url).netloc}: {exc}") from exc
        except Exception as exc:
            raise AdapterError(f"request failed for {urllib.parse.urlsplit(url).netloc}: {exc}") from exc
    raise AdapterError(f"request retries exhausted for {urllib.parse.urlsplit(url).netloc}")


class DiscoveryAdapter(ABC):
    name: str

    @abstractmethod
    def search(self, query: str, query_id: str, limit: int = 10) -> list[DiscoveredItem]:
        """Return normalized candidates without publishing them."""
