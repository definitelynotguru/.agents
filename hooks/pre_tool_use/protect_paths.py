#!/usr/bin/env python3
"""PreToolUse hook: block edits to sensitive files across Create, Edit, and ApplyPatch.

Inspects ``file_path`` / ``path`` for Create and Edit, and parses ``*** (Update|Add|Delete|Move to) File:``
headers inside ``ApplyPatch`` payloads. Configurable under ``[hooks.pre_tool_use.protect_paths]``
in ``droid.toml``. Pair with ``"onFailure": "block"`` in ``~/.factory/hooks.json`` to fail closed.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import (  # type: ignore
    HookInputError,
    PreToolUseInput,
    exit,
    get_toml_section,
    load_toml,
    read_input_as,
)

HOOK_EVENT_NAME = "PreToolUse"
SUPPORTED_TOOLS = frozenset({"Create", "Edit", "ApplyPatch", "Write"})

DEFAULT_PROTECTED_BASENAMES = (
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "id_rsa",
    "id_ed25519",
    "auth.v2.*",
    "mcp-oauth.v2.*",
)
DEFAULT_ALLOWED_BASENAMES = (
    ".env.example",
    ".env.sample",
    ".env.template",
    ".env.dist",
)
DEFAULT_PROTECTED_SEGMENTS = (
    ".git",
    ".ssh",
)

_PATCH_FILE_RE = re.compile(
    r"^\*\*\*\s+(?:Update|Add|Delete|Move to)\s+File:\s*(.+?)\s*$",
    re.MULTILINE,
)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config-file", default="")
    return parser.parse_args(argv)


def _load_config(config_path: str) -> dict[str, object]:
    if not config_path:
        return {}
    data = load_toml(config_path)
    return get_toml_section(data, "hooks", "pre_tool_use", "protect_paths")


def _str_tuple(value: object, default: tuple[str, ...]) -> tuple[str, ...]:
    if isinstance(value, list):
        return tuple(item for item in value if isinstance(item, str) and item)
    return default


def extract_target_paths(tool_name: str, tool_input: dict[str, object]) -> list[str]:
    paths: list[str] = []
    for key in ("file_path", "path", "target_file"):
        val = tool_input.get(key)
        if isinstance(val, str) and val.strip():
            paths.append(val.strip())

    if tool_name == "ApplyPatch":
        for key in ("patch", "input", "content"):
            blob = tool_input.get(key)
            if isinstance(blob, str) and blob:
                for match in _PATCH_FILE_RE.finditer(blob):
                    candidate = match.group(1).strip()
                    if candidate:
                        paths.append(candidate)

    # Preserve order, deduplicate
    return list(dict.fromkeys(paths))


def match_protected_path(
    raw_path: str,
    *,
    protected_basenames: tuple[str, ...],
    allowed_basenames: tuple[str, ...],
    protected_segments: tuple[str, ...],
) -> str | None:
    expanded = Path(raw_path).expanduser()
    parts = expanded.parts
    basename = expanded.name

    for segment in protected_segments:
        if segment in parts:
            return f"protected directory segment '{segment}'"

    if any(fnmatch.fnmatch(basename, pat) for pat in allowed_basenames):
        return None

    for pat in protected_basenames:
        if fnmatch.fnmatch(basename, pat):
            return f"protected filename pattern '{pat}'"

    return None


def main() -> None:
    args = _parse_args(sys.argv[1:])
    try:
        config = _load_config(args.config_file)
    except Exception as exc:
        exit(
            2,
            text=f"[protect_paths] config error: {exc}",
            to_stderr=True,
            hook_event_name=HOOK_EVENT_NAME,
        )

    if config.get("enabled") is False:
        exit(hook_event_name=HOOK_EVENT_NAME)

    try:
        hook_input = read_input_as(PreToolUseInput)
    except HookInputError as exc:
        exit(
            2,
            text=f"[protect_paths] input error: {exc}",
            to_stderr=True,
            hook_event_name=HOOK_EVENT_NAME,
        )

    if hook_input.tool_name not in SUPPORTED_TOOLS:
        exit(hook_event_name=HOOK_EVENT_NAME)

    protected_basenames = _str_tuple(
        config.get("protected_basenames"), DEFAULT_PROTECTED_BASENAMES
    )
    allowed_basenames = _str_tuple(
        config.get("allowed_basenames"), DEFAULT_ALLOWED_BASENAMES
    )
    protected_segments = _str_tuple(
        config.get("protected_segments"), DEFAULT_PROTECTED_SEGMENTS
    )

    for target in extract_target_paths(hook_input.tool_name, hook_input.tool_input):
        violation = match_protected_path(
            target,
            protected_basenames=protected_basenames,
            allowed_basenames=allowed_basenames,
            protected_segments=protected_segments,
        )
        if violation:
            exit(
                decision="deny",
                reason=(
                    f"[protect_paths] Blocked {hook_input.tool_name} on '{target}' "
                    f"({violation}). Edit sensitive files manually if intended."
                ),
                hook_event_name=HOOK_EVENT_NAME,
            )

    exit(hook_event_name=HOOK_EVENT_NAME)


if __name__ == "__main__":
    raise SystemExit(main())
