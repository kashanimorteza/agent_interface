#!/usr/bin/env python3
"""Enforce Agent Interface source boundaries for Claude Code."""

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


def overlaps(path: Path, protected: Path) -> bool:
    """Return whether either resolved path contains the other."""
    return within(path, protected) or within(protected, path)


def grant_path(payload: dict[str, object]) -> Path | None:
    scratchpad = payload.get("scratchpad_dir")
    prompt_id = payload.get("prompt_id")
    if not isinstance(scratchpad, str) or not scratchpad or not isinstance(prompt_id, str) or not prompt_id:
        return None
    return Path(scratchpad).resolve() / f"agent-sync-read-{prompt_id}.grant"


def has_agent_sync_grant(payload: dict[str, object]) -> bool:
    marker = grant_path(payload)
    return marker is not None and marker.is_file()


payload = json.load(sys.stdin)
event = payload.get("hook_event_name", "")
tool = payload.get("tool_name", "")
tool_input = payload.get("tool_input") or {}
project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()).resolve()
interface = (project / ".interface").resolve()
agent_module = (interface / "agent").resolve()
config = (interface / "foundation" / "config").resolve()

if event == "UserPromptExpansion":
    if payload.get("expansion_type") != "slash_command" or payload.get("command_name") != "my-interface-agent-sync":
        block("Agent Module access can be granted only by explicit /my-interface-agent-sync expansion.")
    marker = grant_path(payload)
    if marker is None:
        block("Cannot bind Agent Module access to this Agent Sync prompt.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("explicit-human-agent-sync\n", encoding="utf-8")
    marker.chmod(0o600)
    raise SystemExit(0)

agent_sync_granted = has_agent_sync_grant(payload)

if tool == "Read":
    raw = tool_input.get("file_path")
    if raw:
        target = Path(raw).expanduser()
        if not target.is_absolute():
            target = project / target
        if within(target.resolve(), agent_module) and not agent_sync_granted:
            block("Agent Module reads are reserved for an explicit /my-interface-agent-sync prompt.")
    raise SystemExit(0)

if tool in {"Glob", "Grep"}:
    raw = tool_input.get("path") or str(project)
    target = Path(raw).expanduser()
    if not target.is_absolute():
        target = project / target
    if overlaps(target.resolve(), agent_module) and not agent_sync_granted:
        block("This search scope includes the Agent Module. Scope it outside .interface/agent/ or explicitly run /my-interface-agent-sync.")
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
    agent_path_reference = re.search(r"(?:^|[\s'\"=])(?:\./)?\.interface/agent(?:/|\b)", command)
    absolute_agent_reference = str(agent_module) in command
    if (agent_path_reference or absolute_agent_reference) and not agent_sync_granted:
        block("Shell access to the Agent Module is reserved for an explicit /my-interface-agent-sync prompt.")
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
