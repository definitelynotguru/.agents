#!/usr/bin/env python3
"""PreCompact + SessionEnd hook: capture durable session/workspace state snapshots.

Writes one JSON snapshot per session under ``state_dir`` (default:
``~/.local/state/droid-sessions/<session_id>.json``), updates ``latest.json``,
and appends a compact event record to ``history.jsonl``.

Always fails open so it never blocks compaction or session exit.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import (  # type: ignore
    HookInputError,
    PreCompactInput,
    SessionEndInput,
    exit,
    get_toml_section,
    load_toml,
    read_input,
)

DEFAULT_STATE_DIR = "~/.local/state/droid-sessions"
DEFAULT_MAX_FILES = 200
MAX_DIRTY_FILES = 50
MAX_LEDGERS = 20
GIT_TIMEOUT_SEC = 2


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config-file", default="")
    return parser.parse_args(argv)


def _load_config(config_path: str) -> dict[str, object]:
    if not config_path:
        return {}
    try:
        data = load_toml(config_path)
    except Exception:
        return {}
    return get_toml_section(data, "hooks", "state_capture")


def _run_git(cwd: Path, args: list[str]) -> str | None:
    try:
        res = subprocess.run(
            ["git", "-C", str(cwd), *args],
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SEC,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if res.returncode != 0:
        return None
    return res.stdout.strip()


def _collect_git_state(cwd: Path) -> dict[str, object] | None:
    if not cwd.exists():
        return None
    repo_root = _run_git(cwd, ["rev-parse", "--show-toplevel"])
    if not repo_root:
        return None
    branch = _run_git(cwd, ["rev-parse", "--abbrev-ref", "HEAD"])
    head = _run_git(cwd, ["rev-parse", "--short", "HEAD"])
    status_raw = _run_git(cwd, ["status", "--porcelain"])
    dirty_lines = [line for line in (status_raw or "").splitlines() if line.strip()]
    return {
        "repo_root": repo_root,
        "branch": branch or "",
        "head": head or "",
        "dirty_count": len(dirty_lines),
        "dirty_files": dirty_lines[:MAX_DIRTY_FILES],
    }


def _collect_ledgers(cwd: Path, repo_root: str | None) -> list[str]:
    roots: list[Path] = []
    if cwd.exists():
        roots.append(cwd.resolve())
    if repo_root:
        rr = Path(repo_root).resolve()
        if rr not in roots:
            roots.append(rr)

    found: list[str] = []
    seen: set[str] = set()
    for root in roots:
        ledger_dir = root / ".agents" / "ledgers"
        if not ledger_dir.is_dir():
            continue
        try:
            entries = sorted(
                p for p in ledger_dir.iterdir() if p.is_file() and p.suffix == ".md"
            )
        except OSError:
            continue
        for entry in entries:
            resolved = str(entry)
            if resolved not in seen:
                seen.add(resolved)
                found.append(resolved)
                if len(found) >= MAX_LEDGERS:
                    return found
    return found


def _safe_session_filename(session_id: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in "-_" else "_" for c in session_id)
    return cleaned[:128] or "unknown"


def _atomic_write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".tmp-", suffix=".json", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _prune_old_snapshots(state_dir: Path, max_files: int) -> None:
    if max_files <= 0:
        return
    try:
        snapshots = [
            p
            for p in state_dir.iterdir()
            if p.is_file() and p.suffix == ".json" and p.name != "latest.json"
        ]
    except OSError:
        return
    if len(snapshots) <= max_files:
        return
    snapshots.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    for stale in snapshots[max_files:]:
        try:
            stale.unlink()
        except OSError:
            pass


def capture(hook_input: PreCompactInput | SessionEndInput, config: dict[str, object]) -> Path | None:
    if config.get("enabled") is False:
        return None

    state_dir = Path(
        str(config.get("state_dir") or DEFAULT_STATE_DIR)
    ).expanduser()
    try:
        max_files = int(config.get("max_files", DEFAULT_MAX_FILES))
    except (TypeError, ValueError):
        max_files = DEFAULT_MAX_FILES

    now = datetime.now(timezone.utc).isoformat()
    cwd = Path(hook_input.cwd) if hook_input.cwd else Path.cwd()
    git_state = _collect_git_state(cwd)
    repo_root = str(git_state["repo_root"]) if git_state else None
    ledgers = _collect_ledgers(cwd, repo_root)

    event_meta: dict[str, object] = {
        "timestamp": now,
        "event": hook_input.hook_event_name,
        "permission_mode": hook_input.permission_mode,
    }
    if isinstance(hook_input, PreCompactInput):
        event_meta.update(
            {
                "trigger": hook_input.trigger,
                "message_count": hook_input.message_count,
                "estimated_tokens": hook_input.estimated_tokens,
            }
        )
    elif isinstance(hook_input, SessionEndInput):
        event_meta.update(
            {
                "reason": hook_input.reason,
                "session_duration_ms": hook_input.session_duration_ms,
                "message_count": hook_input.message_count,
            }
        )

    session_key = _safe_session_filename(hook_input.session_id)
    snapshot_path = state_dir / f"{session_key}.json"

    existing_events: list[object] = []
    if snapshot_path.is_file():
        try:
            prev = json.loads(snapshot_path.read_text(encoding="utf-8"))
            if isinstance(prev, dict) and isinstance(prev.get("events"), list):
                existing_events = prev["events"][-19:]
        except Exception:
            existing_events = []

    snapshot: dict[str, object] = {
        "session_id": hook_input.session_id,
        "transcript_path": hook_input.transcript_path,
        "cwd": str(cwd),
        "updated_at": now,
        "last_event": hook_input.hook_event_name,
        "git": git_state,
        "ledgers": ledgers,
        "events": [*existing_events, event_meta],
    }

    _atomic_write_json(snapshot_path, snapshot)
    _atomic_write_json(state_dir / "latest.json", snapshot)

    history_entry = {
        "timestamp": now,
        "event": hook_input.hook_event_name,
        "session_id": hook_input.session_id,
        "cwd": str(cwd),
        "branch": git_state["branch"] if git_state else "",
        "dirty_count": git_state["dirty_count"] if git_state else 0,
        "ledgers": ledgers,
    }
    try:
        with (state_dir / "history.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(history_entry) + "\n")
    except OSError:
        pass

    _prune_old_snapshots(state_dir, max_files)
    return snapshot_path


def main() -> None:
    args = _parse_args(sys.argv[1:])
    config = _load_config(args.config_file)
    try:
        hook_input = read_input()
    except HookInputError as exc:
        print(f"[state_capture] input error: {exc}", file=sys.stderr)
        sys.exit(0)

    event_name = hook_input.hook_event_name
    if not isinstance(hook_input, (PreCompactInput, SessionEndInput)):
        exit(hook_event_name=event_name)

    try:
        capture(hook_input, config)
    except Exception as exc:
        print(f"[state_capture] warning: {exc}", file=sys.stderr)

    exit(hook_event_name=event_name)


if __name__ == "__main__":
    raise SystemExit(main())
