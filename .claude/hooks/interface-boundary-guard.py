#!/usr/bin/env python3
"""Block Root README reads and direct writes outside Interface Config."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys


def within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def block(reason: str) -> None:
    print(reason, file=sys.stderr)
    raise SystemExit(2)


payload = json.load(sys.stdin)
tool = payload.get("tool_name", "")
tool_input = payload.get("tool_input") or {}
project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()).resolve()
interface = (project / ".interface").resolve()
config = (interface / "foundation" / "config").resolve()
root_readme = (project / "README.md").resolve()

if tool == "Read":
    raw = tool_input.get("file_path") or tool_input.get("path")
    if raw and Path(raw).expanduser().resolve() == root_readme:
        block("Root README.md is not an Agent Understanding or Context source.")
    raise SystemExit(0)

if tool in {"Edit", "Write", "NotebookEdit"}:
    raw = tool_input.get("file_path") or tool_input.get("notebook_path") or tool_input.get("path")
    if not raw:
        block("Cannot verify the Interface boundary because the target path is missing.")
    target = Path(raw).expanduser()
    if not target.is_absolute():
        target = project / target
    target = target.resolve()
    if within(target, interface) and not within(target, config):
        block("Agent writes are forbidden throughout .interface/ except authorized records under .interface/foundation/config/.")
    raise SystemExit(0)

if tool == "Bash":
    command = str(tool_input.get("command") or "")
    root_readme_reference = re.search(
        rf"(?:^|[\s'\"])(?:\./)?README\.md(?:$|[\s'\"])|{re.escape(str(root_readme))}",
        command,
    )
    if root_readme_reference:
        block("Root README.md cannot be read through shell execution.")
    mutation = re.search(
        r"(?:^|[;&|]\s*)(?:rm|mv|cp|install|mkdir|rmdir|touch|truncate|chmod|chown|ln|tee|patch|rsync)\b"
        r"|\bsed\s+-i\b|\bperl\s+-pi\b|\bgit\s+(?:checkout|restore|clean|reset)\b|(?:^|[^<])>{1,2}",
        command,
    )
    if mutation and ".interface" in command:
        paths = re.findall(r"(?:^|[\s'\"])(\.interface(?:/[^\s;'\"|&<>]*)?)", command)
        for raw in paths or [".interface"]:
            target = (project / raw).resolve()
            if within(target, interface) and not within(target, config):
                block("Shell mutation of .interface/ is forbidden outside .interface/foundation/config/.")

raise SystemExit(0)
