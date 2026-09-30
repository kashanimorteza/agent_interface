"""Shared grant store for the Agent Module read grant.

Realizes the Permission guarantee `agent-native-read-grant` together with
agent-native-read-grant.py (creates a grant) and interface-boundary-guard.py
(honours it). Synchronized by Agent Native Sync (/my-interface-agent-native).

A grant is bound to one session and to the exact user prompt (`prompt_id`)
created by the Human's direct `/my-interface-agent-native` invocation. It is
never valid inside a subagent and never outlives that prompt.
"""

import hashlib
import json
import os
import tempfile

SYNC_COMMAND = "my-interface-agent-native"
GRANT_DIR_NAME = "claude-interface-agent-grants"


def project_dir(payload):
    return os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())


def grant_root():
    return os.path.join(tempfile.gettempdir(), GRANT_DIR_NAME)


def grant_path(payload):
    digest = hashlib.sha256(project_dir(payload).encode("utf-8")).hexdigest()[:16]
    session = "".join(c for c in str(payload.get("session_id") or "") if c.isalnum() or c in "-_")
    if not session:
        raise ValueError("hook input carries no session_id")
    return os.path.join(grant_root(), digest, session + ".json")


def write_grant(payload):
    path = grant_path(payload)
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    record = {
        "session_id": payload.get("session_id"),
        "prompt_id": payload.get("prompt_id"),
        "command_name": payload.get("command_name"),
    }
    tmp = path + ".tmp"
    with open(tmp, "w") as handle:
        json.dump(record, handle)
    os.replace(tmp, path)


def read_grant(payload):
    path = grant_path(payload)
    if not os.path.exists(path):
        return None
    with open(path) as handle:
        return json.load(handle)


def revoke_grant(payload):
    path = grant_path(payload)
    if os.path.exists(path):
        os.remove(path)


def has_grant(payload):
    """True only on the main thread, in the granting session, within the granting prompt."""
    if payload.get("agent_id"):
        return False
    record = read_grant(payload)
    if record is None:
        return False
    path = grant_path(payload)
    if record.get("session_id") != payload.get("session_id"):
        return False
    granted, current = record.get("prompt_id"), payload.get("prompt_id")
    if granted is None:
        # Expansion ran before a prompt_id existed: bind the grant to the first prompt that uses it.
        # UserPromptSubmit revokes it before any later prompt, so it cannot migrate.
        if current is None:
            return True
        record["prompt_id"] = current
        with open(path, "w") as handle:
            json.dump(record, handle)
        return True
    return granted == current
