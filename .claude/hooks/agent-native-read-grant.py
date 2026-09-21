#!/usr/bin/env python3
"""Enforced Guarantee `agent-native-read-grant` (fail_closed).

Synchronized by /my-interface-agent-native; do not edit by hand.

- UserPromptExpansion (matcher my-interface-agent-native|my-interface-implement):
  a Human-typed slash command creates a grant for this session only.
- UserPromptSubmit / SessionEnd: clear every grant for the session, so a grant
  covers exactly one Human prompt and cannot be inherited by a later one.

Failure here never creates a grant, so every failure leaves reads denied.
"""
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import interface_grants as g  # noqa: E402


def command_name(data):
    for key in ("command_name", "command", "skill", "skill_name", "name"):
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip().lstrip("/").split()[0]
    prompt = data.get("prompt") or data.get("original_prompt") or ""
    if isinstance(prompt, str) and prompt.lstrip().startswith("/"):
        return prompt.lstrip()[1:].split()[0] if prompt.strip() != "/" else ""
    return ""


def main():
    data = json.load(sys.stdin)
    event = data.get("hook_event_name", "")
    sid = data.get("session_id")

    if event in ("UserPromptSubmit", "SessionEnd"):
        g.clear(sid)
        return 0

    if event == "UserPromptExpansion":
        # Only a Human-typed slash command reaches this event; model Skill-tool
        # calls are handled (and denied for these names) by the PreToolUse guard.
        kind = g.GRANT_COMMANDS.get(command_name(data))
        if kind:
            g.grant(sid, kind, "granted by UserPromptExpansion")
        return 0

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # never grant on error; report visibly
        # Exit 2 blocks the prompt: a grant that could not be cleared must not
        # silently carry into a new Human prompt (fail_closed).
        sys.stderr.write("agent-native-read-grant hook error (no grant issued; prompt blocked): {}\n".format(exc))
        sys.exit(2)
