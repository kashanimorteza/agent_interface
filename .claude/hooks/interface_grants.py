"""Grant-state helpers shared by the Interface hooks.

Synchronized by /my-interface-agent-native. Native realization of the Permission
guarantees `agent-native-read-grant` and `interface-boundary-guard`; do not edit by hand.

A grant is a marker file keyed by session id. It is created only by the
UserPromptExpansion hook for a Human-typed slash command and is cleared at the
next UserPromptSubmit and at SessionEnd, so it lives for exactly one Human prompt.
"""
import os
import re

HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(HOOK_DIR, ".state")

AGENT_NATIVE = "agent-native"   # grant for /my-interface-agent-native
IMPLEMENT = "implement"         # coordinator grant for /my-interface-implement

GRANT_COMMANDS = {
    "my-interface-agent-native": AGENT_NATIVE,
    "my-interface-implement": IMPLEMENT,
}

_SAFE = re.compile(r"[^A-Za-z0-9_.-]")


def _path(session_id, kind):
    sid = _SAFE.sub("_", str(session_id or ""))
    if not sid:
        raise ValueError("missing session_id")
    return os.path.join(STATE_DIR, "{}.{}".format(sid, kind))


def ensure_state_dir():
    if not os.path.isdir(STATE_DIR):
        os.makedirs(STATE_DIR)
    ignore = os.path.join(STATE_DIR, ".gitignore")
    if not os.path.exists(ignore):
        with open(ignore, "w") as f:
            f.write("*\n")


def grant(session_id, kind, note=""):
    ensure_state_dir()
    with open(_path(session_id, kind), "w") as f:
        f.write(note)


def has_grant(session_id, kind):
    try:
        return os.path.isfile(_path(session_id, kind))
    except ValueError:
        return False


def clear(session_id):
    if not os.path.isdir(STATE_DIR):
        return
    for kind in set(GRANT_COMMANDS.values()):
        try:
            os.remove(_path(session_id, kind))
        except (OSError, ValueError):
            pass
