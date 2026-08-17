"""Atomic multi-artefact private staging with last-known-good preservation."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


def publish_current_state(target: Path, snapshot: dict[str, object], validator: Callable[[Path], None], run_id: str) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=f".{target.name}-{run_id}-", dir=target.parent))
    backup = target.with_name(target.name + ".last-known-good")
    try:
        for directory in ("sources", "clusters", "feeds", "site"):
            (work / directory).mkdir()
        for kind in ("sources", "clusters"):
            for record in snapshot.get(kind, []):
                path = work / kind / f"{record[kind[:-1] + '_id']}.json"
                path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        for name, content in snapshot.get("feeds", {}).items():
            (work / "feeds" / name).write_text(content, encoding="utf-8")
        for name, content in snapshot.get("site", {}).items():
            (work / "site" / name).write_text(content, encoding="utf-8")
        (work / "budget-ledger.json").write_text(json.dumps(snapshot.get("budget_ledger", {}), indent=2) + "\n", encoding="utf-8")
        manifest = dict(snapshot.get("manifest", {}))
        manifest.update({"run_id": run_id, "created_at": datetime.now(timezone.utc).isoformat(), "status": "validated", "source_count": len(snapshot.get("sources", [])), "cluster_count": len(snapshot.get("clusters", [])), "transaction_version": "2.0"})
        (work / "run-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        validator(work)
        if backup.exists():
            shutil.rmtree(backup)
        if target.exists():
            os.replace(target, backup)
        os.replace(work, target)
        return target
    except Exception as exc:
        shutil.rmtree(work, ignore_errors=True)
        failure = {"run_id": run_id, "failed_at": datetime.now(timezone.utc).isoformat(), "status": "failed", "error_type": type(exc).__name__, "last_known_good_preserved": target.exists(), "staging_site_preserved": (target / "site").exists()}
        (target.parent / f"failure-{run_id}.json").write_text(json.dumps(failure, indent=2) + "\n", encoding="utf-8")
        raise


def publish_transaction(target: Path, records: list[dict], validator: Callable[[Path], None], run_id: str) -> Path:
    """One-gate compatibility wrapper for the former source-centred transaction."""
    target.parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=f".{target.name}-{run_id}-", dir=target.parent))
    backup = target.with_name(target.name + ".last-known-good")
    try:
        (work / "published").mkdir()
        for index, record in enumerate(records, 1):
            (work / "published" / f"{index:03d}-{record['record_id']}.json").write_text(json.dumps(record, indent=2, default=str) + "\n")
        (work / "run-manifest.json").write_text(json.dumps({"run_id": run_id, "created_at": datetime.now(timezone.utc).isoformat(), "record_count": len(records), "status": "validated", "transaction_version": "1.0"}, indent=2) + "\n")
        validator(work)
        if backup.exists():
            shutil.rmtree(backup)
        if target.exists():
            os.replace(target, backup)
        os.replace(work, target)
        return target
    except Exception as exc:
        shutil.rmtree(work, ignore_errors=True)
        (target.parent / f"failure-{run_id}.json").write_text(json.dumps({"run_id": run_id, "status": "failed", "error_type": type(exc).__name__, "last_known_good_preserved": target.exists()}, indent=2) + "\n")
        raise


def recheck_status(http_status: int | None, redirected: bool = False) -> str:
    if http_status in {404, 410}:
        return "unavailable"
    if http_status is None or http_status >= 500:
        return "under-review"
    if redirected:
        return "redirected"
    return "available"
