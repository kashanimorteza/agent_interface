#!/usr/bin/env python3
"""Interface boundary enforcement for Claude Code.

Synchronized realization (by /my-interface-agent-native) of two Enforced Guarantees:

- interface-boundary-guard (PreToolUse, fail_closed, blocking): blocks Agent Module
  reads outside the exact direct-Human Agent Native Sync prompt, blocks every non-Human
  attempt to invoke Agent Native Sync, and blocks Interface mutations outside
  `.interface/config/`.
- agent-native-read-grant (UserPromptExpansion, fail_closed): creates the Agent Module
  read grant only for the prompt created by the Human's `/my-interface-agent-native`
  invocation. The grant belongs to the main agent of that session only (never to a
  subagent) and is revoked when that prompt's turn ends or any other prompt begins.

Usage: interface_guard.py pre-tool-use | grant | revoke
Exit 0 = allow / no-op. Exit 2 = block (reason on stderr). Any internal error exits 2.
"""

import json
import os
import re
import sys
import time

SYNC_SKILL = "my-interface-agent-native"
BOUNDARY = (
    "Interface boundary: {what} is blocked. The Agent Module (.interface/agent/) is readable only "
    "within the Human's direct /my-interface-agent-native prompt, only the Human may invoke "
    "Agent Native Sync, and .interface/ is read-only except .interface/config/. If a Runtime "
    "capability is missing, report Runtime drift and ask the Human to run /my-interface-agent-native."
)


def project_dir(payload):
    return os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())


def grant_path(root, session_id):
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", str(session_id or "unknown"))
    return os.path.join(root, ".claude", "hooks", ".state", "agent-native-grant-" + safe)


def is_subagent(payload):
    return bool(payload.get("agent_id"))


def has_grant(payload, root):
    if is_subagent(payload):
        return False
    return os.path.isfile(grant_path(root, payload.get("session_id")))


def resolve(path, payload, root):
    if not path:
        return None
    path = os.path.expanduser(str(path))
    if not os.path.isabs(path):
        path = os.path.join(payload.get("cwd") or root, path)
    return os.path.realpath(path)


def inside(path, base):
    return path == base or path.startswith(base + os.sep)


def block(what):
    sys.stderr.write(BOUNDARY.format(what=what) + "\n")
    sys.exit(2)


# Bash is checked lexically; any reference that could reach a protected path fails closed.
AGENT_REF = re.compile(r"(^|[^\w-])\.?interface/+agent(?![\w-])|(^|[^\w-])agent/+(agent|skill|rule|permission|runtime|personality|command|tool|connection|context)(\.(md|yaml)|/|\b)")
INTERFACE_GLOB = re.compile(r"\.?interface/+[^\s'\"]*[*?\[{]")
MUTATION = re.compile(
    r"(^|[\s;&|(`])(rm|rmdir|mv|cp|install|ln|touch|truncate|tee|mkdir|chmod|chown|chflags|dd|rsync|unlink|patch|shred)\b"
    r"|\bsed\s+(-[^\s]*\s+)*-i|\bperl\s+(-[^\s]*\s+)*-[^\s]*i|>|\bgit\s+(checkout|restore|reset|clean|rm|mv|stash|apply)\b"
)
GRANT_REF = re.compile(r"\.claude/+hooks/+\.state|agent-native-grant")


def check_bash(payload, root, granted):
    cmd = str((payload.get("tool_input") or {}).get("command") or "")
    if GRANT_REF.search(cmd):
        block("Access to the Agent Native Sync grant store")
    if not granted and (AGENT_REF.search(cmd) or INTERFACE_GLOB.search(cmd)):
        block("A shell command that can reach the Agent Module")
    if ".interface" in cmd and MUTATION.search(cmd):
        # Allow only when every referenced .interface path is inside .interface/config/.
        refs = re.findall(r"\.interface(?:/[^\s'\";|&)]*)?", cmd)
        if any(not re.match(r"\.interface/+config(/|$)", r) for r in refs):
            block("A shell command that can mutate a protected Interface path")


def check_path_tools(payload, root, granted):
    tool = payload.get("tool_name")
    ti = payload.get("tool_input") or {}
    agent_dir = os.path.join(root, ".interface", "agent")
    iface_dir = os.path.join(root, ".interface")
    config_dir = os.path.join(iface_dir, "config")
    grant_dir = os.path.join(root, ".claude", "hooks", ".state")

    target = resolve(ti.get("file_path") or ti.get("notebook_path") or ti.get("path"), payload, root)

    if tool in ("Edit", "Write", "NotebookEdit", "MultiEdit"):
        if target is None:
            block("A file mutation without a resolvable path")
        if inside(target, grant_dir):
            block("Writing the Agent Native Sync grant store")
        if inside(target, iface_dir) and not inside(target, config_dir):
            block("Mutating a protected Interface path (" + os.path.relpath(target, root) + ")")
        return

    if tool in ("Read", "Glob", "Grep"):
        if target is not None and inside(target, grant_dir):
            block("Reading the Agent Native Sync grant store")
        if granted:
            return
        if target is not None and inside(target, agent_dir):
            block("Reading or searching the Agent Module (" + os.path.relpath(target, root) + ")")
        pattern_text = " ".join(str(ti.get(k) or "") for k in ("pattern", "glob")) if tool == "Glob" else str(ti.get("glob") or "")
        if AGENT_REF.search(pattern_text):
            block("A search pattern that targets the Agent Module")
        # A search rooted at or above .interface/ would include the Agent Module: exclude it.
        search_root = target or resolve(payload.get("cwd") or root, payload, root)
        if tool == "Grep" and inside(agent_dir, search_root):
            if ti.get("glob"):
                block("A Grep with its own glob rooted above the Agent Module (narrow the path to exclude .interface/agent/)")
            updated = dict(ti)
            updated["glob"] = "!**/.interface/agent/**"
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Interface boundary: Agent Module excluded from this search.",
                "updatedInput": updated,
            }}))
            sys.exit(0)


def pre_tool_use(payload):
    root = project_dir(payload)
    tool = payload.get("tool_name")
    ti = payload.get("tool_input") or {}
    if tool == "Skill":
        name = str(ti.get("skill") or ti.get("name") or ti.get("command") or "").lstrip("/")
        if name.split(":")[-1].split()[0:1] == [SYNC_SKILL] or SYNC_SKILL in name:
            block("Invoking Agent Native Sync from a non-Human mechanism")
        return
    granted = has_grant(payload, root)
    if tool == "Bash":
        check_bash(payload, root, granted)
        return
    check_path_tools(payload, root, granted)


def grant(payload):
    # Only the Human's slash-command expansion of the sync Skill creates the grant.
    if is_subagent(payload):
        return
    if payload.get("hook_event_name") != "UserPromptExpansion":
        return
    if str(payload.get("command_name") or "").lstrip("/") != SYNC_SKILL:
        return
    if payload.get("expansion_type") not in (None, "slash_command"):
        return
    root = project_dir(payload)
    path = grant_path(root, payload.get("session_id"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump({"session_id": payload.get("session_id"), "granted_at": time.time()}, fh)


def revoke(payload):
    event = payload.get("hook_event_name")
    if event == "UserPromptSubmit":
        prompt = str(payload.get("prompt") or "").strip()
        if prompt.split()[0:1] == ["/" + SYNC_SKILL]:
            return  # the Human's own sync prompt keeps the grant created at expansion
    if event == "Stop" and is_subagent(payload):
        return
    root = project_dir(payload)
    path = grant_path(root, payload.get("session_id"))
    if os.path.exists(path):
        os.remove(path)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
    if mode == "pre-tool-use":
        pre_tool_use(payload)
    elif mode == "grant":
        grant(payload)
    elif mode == "revoke":
        revoke(payload)
    else:
        raise ValueError("unknown mode " + mode)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException as exc:
        sys.stderr.write("Interface boundary guard error: %s\n" % exc)
        # Fail closed for enforcement points. A failed revoke at Stop/SessionStart must not
        # trap the session (exit 2 on Stop forces continuation); it is reported instead, and
        # the next UserPromptSubmit revoke fails closed.
        mode = sys.argv[1] if len(sys.argv) > 1 else ""
        event_blocks = mode in ("pre-tool-use", "grant") or (mode == "revoke" and "UserPromptSubmit" in sys.argv[2:])
        sys.exit(2 if event_blocks else 1)
