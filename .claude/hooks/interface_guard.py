#!/usr/bin/env python3
"""Interface boundary guard for Claude Code (synchronized Runtime realization).

Realizes two Human-declared Enforced Guarantees (Permission Component):

* ``agent-native-read-grant`` -- UserPromptExpansion hook: only the prompt created by the
  Human's direct ``/my-interface-agent-native`` invocation receives a read grant for the
  Agent Module. The grant is bound to the session's main thread, never to subagents, and is
  revoked by the next user prompt that is not that invocation.
* ``interface-boundary-guard`` -- PreToolUse hook: blocks Agent Module reads without the
  grant, blocks every non-Human attempt to invoke Agent Native Sync, and blocks Interface
  mutations outside the ``.interface/config/`` boundary.

Failure policy: fail closed. Any unexpected error denies the tool call.
Usage: interface_guard.py expansion|submit|session|pretool   (hook JSON on stdin)

Do not edit by hand: re-run /my-interface-agent-native to regenerate it.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path

SYNC_SKILL = "my-interface-agent-native"
INTERFACE = ".interface"
AGENT_MODULE = ".interface/agent"
CONFIG = ".interface/config"

READ_TOOLS = {"Read"}
WRITE_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}
SEARCH_TOOLS = {"Glob", "Grep"}

BOUNDARY_MSG = (
    "Interface boundary: the Agent Module (.interface/agent/) is readable only within the "
    "prompt created by the Human's direct /my-interface-agent-native invocation (main thread, "
    "non-transferable). Use the synchronized Runtime artifacts (.claude/rules, .claude/skills); "
    "if one is missing, report Runtime drift and ask the Human to run Agent Native Sync."
)
MUTATION_MSG = (
    "Interface boundary: .interface/ is read-only. Only exact Config records under "
    ".interface/config/ may be changed, by the Skill that owns them. Report the needed change "
    "for direct Human authorship instead."
)
GUARD_MSG = (
    "Interface boundary: the guard's grant state and script cannot be created or changed by a "
    "tool call. Only the Human's /my-interface-agent-native invocation issues the grant."
)
SYNC_INVOKE_MSG = (
    "Interface boundary: Agent Native Sync (/my-interface-agent-native) may only be invoked "
    "directly by the Human. No Agent, Skill, Hook, or automation may invoke it."
)

WRITE_CMD = re.compile(
    r"(>|\btee\b|\brm\b|\bmv\b|\bcp\b|\bsed\s+-i|\bperl\s+-p?i|\btouch\b|\bmkdir\b|\brmdir\b|"
    r"\bchmod\b|\bchown\b|\bln\b|\btruncate\b|\binstall\b|\brsync\b|\bdd\b|\bunlink\b|"
    r"\bgit\s+(checkout|restore|reset|clean|rm|mv|stash|apply|am)\b|\bpatch\b|"
    r"\.write_text|\.write_bytes|open\([^)]*['\"][wa+])"
)
RECURSIVE_CMD = re.compile(
    r"\b(grep|egrep|fgrep)\s+[^|;&]*-[a-zA-Z]*[rR]|\b(rg|ag|ack|find|fd|tree|du|tar|zip|rsync)\b|"
    r"\bls\s+[^|;&]*-[a-zA-Z]*R|\bcp\s+[^|;&]*-[a-zA-Z]*[rR]|\bcat\b|\bhead\b|\btail\b|\bless\b"
)


# --------------------------------------------------------------------------- helpers
def project_dir(data: dict) -> Path:
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    return Path(root).resolve()


def grant_file(data: dict) -> Path:
    session = re.sub(r"[^A-Za-z0-9_.-]", "_", str(data.get("session_id") or "unknown"))
    base = Path(tempfile.gettempdir()) / "claude-interface-guard"
    base.mkdir(mode=0o700, parents=True, exist_ok=True)
    return base / f"{session}.grant"


def is_subagent(data: dict) -> bool:
    return bool(data.get("agent_id") or data.get("agent_type") or data.get("subagent_id"))


def has_grant(data: dict) -> bool:
    if is_subagent(data):
        return False
    path = grant_file(data)
    if not path.is_file():
        return False
    try:
        grant = json.loads(path.read_text())
    except (OSError, ValueError):
        return False
    return grant.get("session_id") == data.get("session_id")


def resolve(data: dict, raw: str | None) -> Path | None:
    if not raw:
        return None
    base = Path(data.get("cwd") or project_dir(data))
    p = Path(os.path.expanduser(raw))
    if not p.is_absolute():
        p = base / p
    return Path(os.path.realpath(p))


def within(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _unlink(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def glob_to_regex(pattern: str) -> "re.Pattern[str]":
    out, i = "", 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
            continue
        if pattern.startswith("**", i):
            out, i = out + ".*", i + 2
            continue
        if c == "*":
            out += "[^/]*"
        elif c == "?":
            out += "[^/]"
        elif c == "{":
            end = pattern.find("}", i)
            if end < 0:
                out += re.escape(c)
            else:
                alts = pattern[i + 1:end].split(",")
                out += "(?:" + "|".join(glob_to_regex(a).pattern[:-2] for a in alts) + ")"
                i = end
        elif c == "[":
            end = pattern.find("]", i + 1)
            out += pattern[i:end + 1] if end > 0 else re.escape(c)
            i = end if end > 0 else i
        else:
            out += re.escape(c)
        i += 1
    return re.compile(out + r"\Z")


def glob_reaches(pattern: str, search_root: Path, agent_root: Path) -> bool:
    """True when the Glob pattern, applied under search_root, matches any Agent Module path."""
    if os.path.isabs(pattern):
        rx, base = glob_to_regex(pattern.lstrip("/")), Path("/")
    else:
        rx, base = glob_to_regex(pattern), search_root
    candidates = [agent_root] + [Path(d) / n for d, ds, fs in os.walk(str(agent_root)) for n in ds + fs]
    return any(rx.match(os.path.relpath(str(c), str(base))) for c in candidates)


def is_sync_invocation(text: str) -> bool:
    return bool(re.match(rf"^\s*/(?:[\w-]+:)?{re.escape(SYNC_SKILL)}(\s|$)", text or ""))


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def allow_with_input(updated: dict) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "updatedInput": updated,
        }
    }))
    sys.exit(0)


# --------------------------------------------------------------------------- events
def on_expansion(data: dict) -> None:
    """UserPromptExpansion: the Human's typed sync command issues the main-thread, per-prompt
    grant; every other expanded command revokes it (UserPromptSubmit may not fire for commands)."""
    name = str(data.get("command_name") or "").split(":")[-1]
    typed = data.get("expansion_type") in (None, "slash_command")
    if name == SYNC_SKILL and typed and not is_subagent(data):
        grant_file(data).write_text(json.dumps({
            "session_id": data.get("session_id"),
            "issued_at": time.time(),
            "skill": SYNC_SKILL,
        }))
    else:
        _unlink(grant_file(data))


def on_submit(data: dict) -> None:
    """UserPromptSubmit: any prompt other than the direct sync invocation revokes the grant."""
    if not is_sync_invocation(str(data.get("prompt") or "")):
        _unlink(grant_file(data))


def on_session(data: dict) -> None:
    """SessionStart (startup, resume, clear, compact): a new or resumed session holds no grant."""
    _unlink(grant_file(data))


def on_pretool(data: dict) -> None:
    tool = str(data.get("tool_name") or "")
    ti = data.get("tool_input") or {}
    root = project_dir(data)
    agent_root = root / AGENT_MODULE
    iface_root = root / INTERFACE
    config_root = root / CONFIG
    granted = has_grant(data)
    grant_dir = Path(os.path.realpath(grant_file(data).parent))
    guard_script = Path(os.path.realpath(__file__))

    # The grant is issued only by this hook's own process; tools can never create or alter it.
    if tool in WRITE_TOOLS | READ_TOOLS:
        target = resolve(data, ti.get("file_path") or ti.get("notebook_path") or ti.get("path"))
        if target and within(target, grant_dir):
            deny(GUARD_MSG)
        if target and tool in WRITE_TOOLS and target == guard_script and not granted:
            deny(GUARD_MSG)
    if tool == "Bash" and "claude-interface-guard" in str(ti.get("command") or ""):
        deny(GUARD_MSG)

    # Non-Human invocation of Agent Native Sync.
    if tool == "Skill":
        name = str(ti.get("skill") or ti.get("command") or ti.get("name") or "")
        if name.lstrip("/").split(":")[-1].split()[0:1] == [SYNC_SKILL]:
            deny(SYNC_INVOKE_MSG)
        return

    if tool in READ_TOOLS | WRITE_TOOLS:
        path = resolve(data, ti.get("file_path") or ti.get("notebook_path") or ti.get("path"))
        if path is None:
            return
        if tool in WRITE_TOOLS and within(path, iface_root) and not within(path, config_root):
            deny(MUTATION_MSG)
        if within(path, agent_root) and not granted:
            deny(BOUNDARY_MSG)
        return

    if tool in SEARCH_TOOLS:
        path = resolve(data, ti.get("path")) or Path(os.path.realpath(data.get("cwd") or root))
        if granted or not (within(path, agent_root) or within(agent_root, path)):
            return
        if within(path, agent_root):
            deny(BOUNDARY_MSG)
        # The search root contains the Agent Module.
        if tool == "Glob":
            pattern = str(ti.get("pattern") or "")
            if pattern and glob_reaches(pattern, path, agent_root):
                deny(BOUNDARY_MSG + " Narrow the Glob path or pattern so it excludes .interface/agent/.")
            return
        # Grep: exclude the Agent Module when no glob filter is set; otherwise fail closed.
        if not ti.get("glob"):
            updated = dict(ti)
            updated["glob"] = "!**/.interface/agent/**"  # root-independent ripgrep exclusion
            allow_with_input(updated)
        deny(BOUNDARY_MSG + " Narrow the Grep path so it excludes .interface/agent/.")

    if tool == "Bash":
        cmd = str(ti.get("command") or "")
        if re.search(rf"\bclaude\b.*{re.escape(SYNC_SKILL)}", cmd):
            deny(SYNC_INVOKE_MSG)
        if not granted and re.search(r"interface/agent", cmd):
            deny(BOUNDARY_MSG)
        # Recursive or wildcard access to the whole Interface tree would reach the Agent Module.
        if not granted and re.search(r"\.interface/?(\*|\s|$|['\"])", cmd) and RECURSIVE_CMD.search(cmd):
            deny(BOUNDARY_MSG + " Target a specific Interface sub-path outside .interface/agent/.")
        if not granted and re.search(r"\.interface/\*", cmd):
            deny(BOUNDARY_MSG + " Target a specific Interface sub-path outside .interface/agent/.")
        mentions_iface = re.findall(r"\.interface(?:/[\w./*-]*)?", cmd)
        outside_config = [m for m in mentions_iface if not m.startswith(".interface/config")]
        benign = re.sub(r"\d?>&\d|\d?>>?\s*/dev/null", " ", cmd)
        if outside_config and WRITE_CMD.search(benign):
            deny(MUTATION_MSG)
        return


def main() -> None:
    event = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}
    if event == "pretool" and not (isinstance(data, dict) and data.get("tool_name")):
        deny("Interface boundary guard failed closed (unreadable hook input); tool call blocked.")
    try:
        {
            "expansion": on_expansion,
            "submit": on_submit,
            "session": on_session,
            "pretool": on_pretool,
        }[event](data)
    except SystemExit:
        raise
    except Exception as exc:  # fail closed
        if event == "pretool":
            deny(f"Interface boundary guard failed closed ({type(exc).__name__}); tool call blocked.")
        print(f"interface_guard {event} failed: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
