#!/usr/bin/env python3
"""Deterministic Interface boundary guarantees (Claude Code hooks).

Synchronized realization of two Human-owned Enforced Guarantees, both fail-closed:
  interface-boundary-guard   mode `guard`  (PreToolUse)
  agent-native-read-grant    mode `grant`  (UserPromptExpansion), `revoke` (Stop, SessionEnd)

Not authoritative: regenerate through /my-interface-agent-native; do not edit by hand.
Python 3.7+ standard library only.
"""
import hashlib
import json
import os
import re
import sys
import tempfile
import time

SYNC_NAME = "my-interface-agent-native"
GRANT_PREFIX = "claude-interface-sync-grant-"
GRANT_TTL_SECONDS = 2 * 60 * 60  # fail-safe expiry if no Stop/SessionEnd revokes the grant


def grant_path(session_id):
    digest = hashlib.sha256(str(session_id).encode("utf-8")).hexdigest()[:32]
    return os.path.join(tempfile.gettempdir(), GRANT_PREFIX + digest)


def grant_active(payload):
    """Main-thread only: a subagent never holds, inherits, or borrows the grant."""
    if payload.get("agent_id") or payload.get("agent_type"):
        return False
    sid = payload.get("session_id")
    if not sid:
        return False
    try:
        with open(grant_path(sid)) as fh:
            data = json.load(fh)
        return data.get("session_id") == sid and (time.time() - float(data["created"])) < GRANT_TTL_SECONDS
    except Exception:
        return False


def deny(reason):
    sys.stdout.write(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Interface boundary: " + reason,
        }
    }))
    sys.exit(0)


def project_root(payload):
    return os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())


def resolve(path, payload):
    if not path:
        return None
    if not os.path.isabs(path):
        path = os.path.join(payload.get("cwd") or os.getcwd(), path)
    return os.path.realpath(path)


def within(path, base):
    return path == base or path.startswith(base + os.sep)


def check_skill(tool_input, payload):
    name = str(tool_input.get("skill") or "").strip().lstrip("/")
    if name.split(":")[-1] == SYNC_NAME and not grant_active(payload):
        deny("Agent Native Sync can be started only by the Human's direct /%s invocation, never by a model, Skill, coordinator, or Agent Instance." % SYNC_NAME)


def check_path_tool(tool, tool_input, payload, root, granted):
    agent_dir = os.path.join(root, ".interface", "agent")
    interface_dir = os.path.join(root, ".interface")
    config_dir = os.path.join(interface_dir, "config")
    mutating = tool in ("Edit", "Write", "NotebookEdit")
    if tool in ("Read", "Edit", "Write"):
        target = resolve(tool_input.get("file_path"), payload)
    elif tool == "NotebookEdit":
        target = resolve(tool_input.get("notebook_path"), payload)
    else:  # Glob, Grep
        target = resolve(tool_input.get("path") or payload.get("cwd") or root, payload)
    if target is None:
        return
    if os.path.basename(target).startswith(GRANT_PREFIX):
        deny("the Agent Module read grant is managed only by its hook.")
    if mutating and within(target, interface_dir) and not within(target, config_dir):
        deny("the Interface is read-only; only exact Config records under .interface/config/ may change, and only through their owning Skill.")
    if not granted:
        if within(target, agent_dir):
            deny("Agent Module sources are readable only within the Human's direct /%s prompt. Use the synchronized Native artifacts and report Runtime drift instead." % SYNC_NAME)
        if tool in ("Glob", "Grep"):
            if target == interface_dir:
                deny("a search rooted at .interface/ would reach the Agent Module; search a specific subdirectory instead.")
            text = " ".join(str(tool_input.get(k) or "") for k in ("pattern", "glob"))
            if re.search(r"interface/+agent\b", text):
                deny("Agent Module sources are readable only within the Human's direct /%s prompt." % SYNC_NAME)


BASH_MUTATION = re.compile(
    r"(?<![\w&>])>{1,2}(?!&)|\b(rm|rmdir|mv|cp|tee|touch|mkdir|truncate|chmod|chown|ln|install|dd|rsync)\b"
    r"|\bsed\s+(-\w*i|--in-place)|\bperl\s+-\w*i|\bgit\s+(apply|checkout|restore|clean|reset|stash|mv|rm)\b"
)


def check_bash(tool_input, payload, granted):
    command = str(tool_input.get("command") or "")
    if GRANT_PREFIX in command:
        deny("the Agent Module read grant is managed only by its hook.")
    if SYNC_NAME in command and re.search(r"claude\b.*-p|\bskill\b", command, re.I) and not granted:
        deny("Agent Native Sync can be started only by the Human's direct invocation.")
    mentions_interface = re.search(r"(?<![\w-])\.interface\b", command) is not None
    if not mentions_interface:
        return
    if not granted and (re.search(r"\.interface/+agent\b", command) or re.search(r"(?<![\w])agent(/|\b(?!_))", command)):
        deny("Agent Module sources are readable only within the Human's direct /%s prompt. Use the synchronized Native artifacts and report Runtime drift instead." % SYNC_NAME)
    outside_config = re.sub(r"\.interface/+config\b", "", command)
    if re.search(r"(?<![\w-])\.interface\b", outside_config) and BASH_MUTATION.search(outside_config):
        deny("a shell command that can write to .interface/ outside .interface/config/ is blocked; the Interface is read-only.")


def run_guard(payload):
    tool = payload.get("tool_name") or ""
    tool_input = payload.get("tool_input") or {}
    root = project_root(payload)
    granted = grant_active(payload)
    if tool == "Skill":
        check_skill(tool_input, payload)
    elif tool in ("Read", "Glob", "Grep", "Edit", "Write", "NotebookEdit"):
        check_path_tool(tool, tool_input, payload, root, granted)
    elif tool == "Bash":
        check_bash(tool_input, payload, granted)


def run_grant(payload):
    name = str(payload.get("command_name") or "").strip().lstrip("/").split(":")[-1]
    if payload.get("expansion_type") == "slash_command" and name == SYNC_NAME and payload.get("session_id"):
        with open(grant_path(payload["session_id"]), "w") as fh:
            json.dump({"session_id": payload["session_id"], "created": time.time()}, fh)


def run_revoke(payload):
    sid = payload.get("session_id")
    if sid:
        try:
            os.remove(grant_path(sid))
        except OSError:
            pass


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError("payload is not an object")
        if mode == "guard":
            run_guard(payload)
        elif mode == "grant":
            run_grant(payload)
        elif mode == "revoke":
            run_revoke(payload)
        else:
            raise ValueError("unknown mode")
    except SystemExit:
        raise
    except Exception as exc:  # fail closed and visibly
        if mode == "guard":
            deny("guard failed closed (%s: %s)." % (type(exc).__name__, exc))
        sys.stderr.write("interface_guard %s failed: %s: %s\n" % (mode, type(exc).__name__, exc))
        sys.exit(2 if mode == "grant" else 0)


if __name__ == "__main__":
    main()
