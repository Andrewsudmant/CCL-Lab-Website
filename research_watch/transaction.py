"""Atomic private staging publication with a durable last-known-good state."""

from __future__ import annotations
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


def publish_transaction(target: Path, records: list[dict], validator: Callable[[Path], None], run_id: str) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=f".{target.name}-{run_id}-", dir=target.parent))
    backup = target.with_name(target.name + ".last-known-good")
    try:
        (work / "published").mkdir()
        for index, record in enumerate(records, 1):
            (work / "published" / f"{index:03d}-{record['record_id']}.json").write_text(json.dumps(record, indent=2, default=str) + "\n")
        manifest = {"run_id": run_id, "created_at": datetime.now(timezone.utc).isoformat(), "record_count": len(records), "status": "validated", "transaction_version": "1.0"}
        (work / "run-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        validator(work)
        if backup.exists():
            shutil.rmtree(backup)
        if target.exists():
            os.replace(target, backup)
        os.replace(work, target)
        return target
    except Exception as exc:
        shutil.rmtree(work, ignore_errors=True)
        failure = {"run_id": run_id, "failed_at": datetime.now(timezone.utc).isoformat(), "status": "failed", "error_type": type(exc).__name__, "last_known_good_preserved": target.exists()}
        (target.parent / f"failure-{run_id}.json").write_text(json.dumps(failure, indent=2) + "\n")
        raise


def recheck_status(http_status: int | None, redirected: bool = False) -> str:
    if http_status in {404, 410}:
        return "link-unavailable"
    if http_status is None or http_status >= 500:
        return "under-review"
    if redirected:
        return "corrected"
    return "available"
