#!/usr/bin/env python3
"""Fail closed unless staged changes are on the private automation allowlist."""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = (
    "data/current-conversations/generated/",
    "staging/current-conversations/",
    "reports/current-conversations/runs/",
    "state/current-conversations/budget/",
    "current-conversations/feed.json",
    "current-conversations/feed.xml",
)
TARGET_BRANCH = "automation/current-conversations-staging"

def changed_paths() -> list[str]:
    result = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, check=True, capture_output=True, text=True)
    return [line[3:].split(" -> ")[-1] for line in result.stdout.splitlines() if line]

def verify(paths: list[str], branch: str | None = None) -> None:
    if branch is not None and branch != TARGET_BRANCH:
        raise SystemExit(f"Refusing write: branch must be {TARGET_BRANCH}")
    denied = [path for path in paths if not any(path == prefix or path.startswith(prefix) for prefix in ALLOWED)]
    if denied:
        raise SystemExit("Refusing write outside Current Conversations allowlist: " + ", ".join(denied))

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--paths", nargs="*")
    parser.add_argument("--branch")
    args = parser.parse_args()
    verify(args.paths if args.paths is not None else changed_paths(), args.branch)
    print("Current Conversations staging allowlist passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
