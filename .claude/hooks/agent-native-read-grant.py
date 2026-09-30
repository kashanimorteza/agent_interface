"""Enforced Guarantee `agent-native-read-grant` (fail closed, required).

Grants Agent Module read access only to the prompt created by the Human's direct
explicit invocation of Agent Native Sync. No model, Agent Native, Agent Instance,
Skill, coordinator, Hook, lifecycle routine, or automation can create, inherit,
or borrow this grant.

Events:
  UserPromptExpansion (matcher my-interface-agent-native) -> create the grant for this prompt.
  UserPromptSubmit                                          -> revoke any earlier grant, so a grant never
                                                               outlives the prompt that created it.
Synchronized by Agent Native Sync (/my-interface-agent-native).
"""

import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import interface_grant  # noqa: E402


def main():
    payload = json.load(sys.stdin)
    event = payload.get("hook_event_name")

    if event == "UserPromptSubmit":
        record = interface_grant.read_grant(payload)
        if record is None:
            return 0
        same_prompt = record.get("prompt_id") is not None and record.get("prompt_id") == payload.get("prompt_id")
        unbound_sync = record.get("prompt_id") is None and str(payload.get("prompt") or "").strip().startswith(
            "/" + interface_grant.SYNC_COMMAND
        )
        if not (same_prompt or unbound_sync):
            interface_grant.revoke_grant(payload)
        return 0

    if event != "UserPromptExpansion":
        return 0
    if payload.get("command_name") != interface_grant.SYNC_COMMAND:
        return 0
    if payload.get("agent_id") or payload.get("expansion_type") != "slash_command":
        sys.stderr.write("Agent Native Sync can only be started by the Human typing /my-interface-agent-native.\n")
        return 2

    interface_grant.write_grant(payload)
    print("Agent Module read grant is active for this prompt only; it is not available to subagents or later prompts.")
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except Exception as error:  # fail closed: a broken grant hook blocks the expansion
        sys.stderr.write("agent-native-read-grant failed closed: %s\n" % error)
        code = 2
    sys.exit(code)
