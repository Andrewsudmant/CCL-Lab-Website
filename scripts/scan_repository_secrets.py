#!/usr/bin/env python3
"""Non-disclosing secret scan of reachable Git blobs and present repository files."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from scripts.content import ROOT

PATTERNS = {
    "private-key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "openai-key": re.compile(rb"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    "github-token": re.compile(rb"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}"),
    "aws-access-key": re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "slack-token": re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{20,}"),
    "stripe-live-key": re.compile(rb"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}"),
    "google-api-key": re.compile(rb"\bAIza[0-9A-Za-z_-]{30,}"),
}
EXCLUDED_PARTS = {".git", ".venv", "_site", ".quarto", "deliverables", "__pycache__"}


def git_blobs() -> dict[str, str]:
    listing = subprocess.run(["git", "rev-list", "--objects", "--all"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()
    blobs: dict[str, str] = {}
    for row in listing:
        object_id, _, path = row.partition(" ")
        object_type = subprocess.run(["git", "cat-file", "-t", object_id], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
        if object_type == "blob":
            blobs.setdefault(object_id, path or "<historical-blob>")
    return blobs


def scan(data: bytes, label: str, findings: list[dict[str, str]]) -> None:
    for pattern_name, pattern in PATTERNS.items():
        if pattern.search(data):
            findings.append({"location": label, "pattern": pattern_name})


def main() -> int:
    findings: list[dict[str, str]] = []
    blobs = git_blobs()
    for object_id, path in blobs.items():
        data = subprocess.run(["git", "cat-file", "blob", object_id], cwd=ROOT, check=True, capture_output=True).stdout
        scan(data, f"history:{path}", findings)
    present = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or EXCLUDED_PARTS & set(path.relative_to(ROOT).parts):
            continue
        present += 1
        scan(path.read_bytes(), f"present:{path.relative_to(ROOT)}", findings)
    result = {"reachable_git_blobs": len(blobs), "present_files": present, "patterns": sorted(PATTERNS), "findings": findings}
    print(json.dumps(result, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
