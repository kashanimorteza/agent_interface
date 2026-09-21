#!/usr/bin/env python3
"""agent-native-read-grant — Claude Code hook (UserPromptExpansion / UserPromptSubmit / Stop / SessionEnd).

Synchronized realization of the Enforced Guarantee `agent-native-read-grant`
declared in the Human-owned Agent Module (Permission Component). Realized by
Agent Native Sync (/my-interface-agent-native). The declaration is the
authority; this script is its Claude Code mechanism.

Guarantee (verbatim from the declaration):
  Grant Agent Module read access only to the prompt created by the Human's
  direct explicit invocation of Agent Native Sync; a model, Agent Native, Agent
  Instance, Skill, coordinator, Hook, lifecycle routine, or automation can never
  create, inherit, or borrow this grant.

Failure policy: fail_closed. On any error the grant is removed, never created.

Mechanism:
  * UserPromptExpansion (matcher: my-interface-agent-native) — fires only when the
    Human types `/my-interface-agent-native`; creates a session-scoped grant marker.
  * UserPromptSubmit — every other Human prompt removes any stale marker.
  * Stop / SessionEnd — the marker is removed when the turn or session ends.

The marker is consumed by `interface-boundary-guard.py`, which ignores it inside
subagents (hook input carries `agent_id`), so the grant cannot be inherited.
"""

import json
import os
import re
import sys
import tempfile
import time

SYNC_SKILL = "my-interface-agent-native"
GRANT_PREFIX = "interface-agent-native-grant-"


def marker_path(session_id: str) -> str:
    return os.path.join(tempfile.gettempdir(), GRANT_PREFIX + session_id)


def valid_session(session_id) -> bool:
    return isinstance(session_id, str) and re.fullmatch(r"[A-Za-z0-9_.-]+", session_id) is not None


def revoke(session_id) -> None:
    if not valid_session(session_id):
        return
    try:
        os.remove(marker_path(session_id))
    except FileNotFoundError:
        pass


def grant(session_id: str, prompt_id) -> None:
    with open(marker_path(session_id), "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"granted_at": time.time(), "prompt_id": prompt_id, "skill": SYNC_SKILL}))


def is_direct_human_sync_invocation(payload: dict) -> bool:
    if payload.get("agent_id") or payload.get("agent_type"):
        return False  # never from inside an Agent Instance
    if payload.get("expansion_type") not in (None, "slash_command"):
        return False
    name = str(payload.get("command_name") or "").strip().lstrip("/")
    if name != SYNC_SKILL:
        return False
    prompt = str(payload.get("prompt") or "").strip()
    # The Human's own typed line must be the bare command (no mode or numeric argument).
    return prompt == "/" + SYNC_SKILL


def main() -> None:
    session_id = None
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            raise ValueError("hook input is not a JSON object")
        session_id = payload.get("session_id")
        event = payload.get("hook_event_name", "")

        if event == "UserPromptExpansion":
            if valid_session(session_id) and is_direct_human_sync_invocation(payload):
                grant(session_id, payload.get("prompt_id"))
            else:
                revoke(session_id)
            sys.exit(0)

        if event == "UserPromptSubmit":
            prompt = str(payload.get("prompt") or "").strip()
            if prompt != "/" + SYNC_SKILL:
                revoke(session_id)
            sys.exit(0)

        # Stop, SessionEnd, or any other event: the grant never outlives the turn.
        revoke(session_id)
        sys.exit(0)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        revoke(session_id)
        sys.stderr.write(
            "agent-native-read-grant failed closed (grant revoked): "
            f"{exc.__class__.__name__}: {exc}\n"
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
