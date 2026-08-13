"""Shared content loading helpers for CCLL tooling."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def normalize(value: Any) -> Any:
    """Convert YAML-native date objects to JSON-Schema-friendly strings."""
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in {path.relative_to(ROOT)}")
    return normalize(data)


def load_records(relative_directory: str) -> list[dict[str, Any]]:
    directory = ROOT / relative_directory
    return [load_yaml(path) for path in sorted(directory.glob("*.yml"))]


def research_scope() -> dict[str, Any]:
    return load_yaml(ROOT / "config/research_scope.yml")


def theme_index() -> dict[str, dict[str, Any]]:
    return {theme["id"]: theme for theme in research_scope()["themes"]}
