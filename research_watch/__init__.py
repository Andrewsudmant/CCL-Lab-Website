"""One-gate compatibility shim for the former ``research_watch`` package."""

from __future__ import annotations

import importlib
import sys
import warnings

warnings.warn(
    "research_watch is deprecated; import current_conversations instead",
    DeprecationWarning,
    stacklevel=2,
)

_MODULES = ("models", "normalize", "cluster", "publication", "transaction", "run")
for _name in _MODULES:
    sys.modules[f"{__name__}.{_name}"] = importlib.import_module(f"current_conversations.{_name}")

for _name in ("base", "openalex", "crossref", "datacite", "bluesky", "openai_web"):
    sys.modules[f"{__name__}.adapters.{_name}"] = importlib.import_module(f"current_conversations.adapters.{_name}")

from current_conversations import PIPELINE_VERSION

__all__ = ["PIPELINE_VERSION"]
