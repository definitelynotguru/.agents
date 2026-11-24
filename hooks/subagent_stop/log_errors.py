#!/usr/bin/env python3
"""SubagentStop hook: log subagent failures to a lightweight JSONL file.

Silent on successful subagent completions. Appends one compact JSON line when
``task_error`` is non-empty so silent model/auth/tool flakes stay visible.
Always fails open.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import (  # type: ignore
    HookInputError,
    SubagentStopInput,
    exit,
    get_toml_section,
    load_toml,
    read_input_as,
)

HOOK_EVENT_NAME = "SubagentStop"
DEFAULT_LOG_PATH = "~/.local/state/droid-sessions/subagent-errors.jsonl"


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
    return get_toml_section(data, "hooks", "subagent_stop", "error_log")


def record_error(
    hook_input: SubagentStopInput, config: dict[str, object]
) -> Path | None:
    if config.get("enabled") is False:
        return None
    if not hook_input.task_error:
        return None

    log_path = Path(str(config.get("log_path") or DEFAULT_LOG_PATH)).expanduser()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": hook_input.session_id,
        "cwd": hook_input.cwd,
        "task_name": hook_input.task_name or "",
        "task_error": str(hook_input.task_error)[:2000],
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
    return log_path


def main() -> None:
    args = _parse_args(sys.argv[1:])
    config = _load_config(args.config_file)
    try:
        hook_input = read_input_as(SubagentStopInput)
    except HookInputError as exc:
        print(f"[subagent_stop] input error: {exc}", file=sys.stderr)
        sys.exit(0)

    try:
        record_error(hook_input, config)
    except Exception as exc:
        print(f"[subagent_stop] warning: {exc}", file=sys.stderr)

    exit(hook_event_name=HOOK_EVENT_NAME)


if __name__ == "__main__":
    raise SystemExit(main())
