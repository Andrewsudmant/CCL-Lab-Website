#!/usr/bin/env python3
"""Exercise the private branch target against a temporary local bare remote."""
from __future__ import annotations
import datetime as dt
import subprocess
import tempfile
from pathlib import Path

from stage_current_conversations import TARGET_BRANCH, verify

ROOT = Path(__file__).resolve().parents[1]

def run(*args: str, cwd: Path) -> str:
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()

def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ccll-staging-remote-") as raw:
        base = Path(raw)
        remote, work = base / "remote.git", base / "work"
        run("git", "init", "--bare", str(remote), cwd=base)
        run("git", "init", "-b", "main", str(work), cwd=base)
        run("git", "config", "user.email", "local-test@example.invalid", cwd=work)
        run("git", "config", "user.name", "CCLL local staging test", cwd=work)
        allowed = "staging/current-conversations/current/run-manifest.json"
        verify([allowed], TARGET_BRANCH)
        path = work / allowed
        path.parent.mkdir(parents=True)
        path.write_text('{"status":"validated"}\n', encoding="utf-8")
        run("git", "add", allowed, cwd=work)
        run("git", "commit", "-m", "Local staging exercise", cwd=work)
        run("git", "branch", "-M", TARGET_BRANCH, cwd=work)
        run("git", "remote", "add", "origin", str(remote), cwd=work)
        run("git", "push", "origin", f"HEAD:{TARGET_BRANCH}", cwd=work)
        refs = run("git", "for-each-ref", "--format=%(refname:short)", "refs/heads", cwd=remote)
        assert refs.splitlines() == [TARGET_BRANCH]
    report = ROOT / "reports/current-conversations/staging/local-bare-remote-exercise.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(f"# Local bare-remote staging exercise\n\nDate: {dt.date.today()}\n\nA temporary repository committed one allow-listed private staging manifest and pushed it only to `{TARGET_BRANCH}` on a temporary local bare remote. The remote contained no `main` reference. The temporary repositories were deleted automatically. No external remote or network was used.\n", encoding="utf-8")
    print(report)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
