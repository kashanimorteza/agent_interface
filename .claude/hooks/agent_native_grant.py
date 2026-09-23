#!/usr/bin/env python3
"""Grant lifecycle: realization of the Enforced Guarantee `agent-native-read-grant`.

Native realization (Claude Code) synchronized by /my-interface-agent-native. The Human-owned
Agent Module remains authoritative; this script is not a second authority.

Guarantee: grant Agent Module read access only to the prompt created by the Human's direct
explicit invocation of Agent Native Sync; nothing else can create, inherit, or borrow it.

  grant  — UserPromptExpansion (matcher my-interface-agent-native): fires only for a
           Human-typed slash command, never for a model Skill call. Records a grant bound
           to this session's main agent.
  revoke — UserPromptSubmit (fires before the expansion of every new prompt), Stop, and
           SessionEnd: removes the grant so it never outlives the exact prompt.

Allowed effects: create or remove this session's grant file under .claude/hooks/state/ only.
Failure policy: fail_closed — a failed grant leaves no grant (reads stay blocked); a failed
revoke on UserPromptSubmit blocks the prompt visibly. May block: only on its own failure.
"""
import json
import os
import re
import sys
import time

SYNC_SKILL = "my-interface-agent-native"
PREFIX = "[agent-native-read-grant] "


def grant_path(data):
    root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())
    session_id = re.sub(r"[^A-Za-z0-9_.-]", "_", str(data.get("session_id") or ""))
    if not session_id:
        raise ValueError("missing session_id")
    return os.path.join(root, ".claude", "hooks", "state", "agent-native-grant-" + session_id + ".json")


def grant(data):
    if data.get("hook_event_name") != "UserPromptExpansion":
        return
    if data.get("agent_id") or data.get("agent_type"):
        return
    if data.get("expansion_type") not in (None, "slash_command"):
        return
    name = str(data.get("command_name") or "").lstrip("/")
    if name != SYNC_SKILL and not name.endswith(":" + SYNC_SKILL):
        return
    path = grant_path(data)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    record = {"session_id": data.get("session_id"), "command_name": name, "created_at": time.time()}
    with open(path, "w") as handle:
        json.dump(record, handle)


def revoke(data):
    path = grant_path(data)
    if os.path.exists(path):
        os.remove(path)


def main(data):
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    if action == "grant":
        grant(data)
    elif action == "revoke":
        revoke(data)
    else:
        raise ValueError("unknown action " + repr(action))


if __name__ == "__main__":
    event = None
    try:
        payload = json.load(sys.stdin)
        event = payload.get("hook_event_name")
        main(payload)
    except Exception as error:
        sys.stderr.write(PREFIX + "failed (" + type(error).__name__ + ": " + str(error) + "); failing closed.\n")
        # Exit 2 blocks the triggering prompt or expansion. On Stop it would force the turn to
        # continue (a loop), and SessionEnd cannot block, so those report without blocking; the
        # next UserPromptSubmit revoke and the guard's grant age limit keep the grant closed.
        sys.exit(1 if event in ("Stop", "SessionEnd") else 2)
