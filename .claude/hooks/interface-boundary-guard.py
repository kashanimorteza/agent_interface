#!/usr/bin/env python3
"""interface-boundary-guard — Claude Code PreToolUse hook.

Synchronized realization of the Enforced Guarantee `interface-boundary-guard`
declared in the Human-owned Agent Module (Permission Component). Realized by
Agent Native Sync (/my-interface-agent-native). The declaration is the
authority; this script is its Claude Code mechanism.

Guarantee (verbatim from the declaration):
  Block Agent Module reads outside the exact direct-Human Agent Sync prompt,
  block every non-Human attempt to invoke Agent Sync, and block direct
  Interface mutations outside the authorized Config boundary.

Failure policy: fail_closed. Any error in this script denies the tool call.

Event: PreToolUse. Matcher: Read|Glob|Grep|Edit|Write|NotebookEdit|Bash|Skill

The read grant for the Agent Module is a session-scoped marker file created by
the companion hook `agent-native-read-grant.py` when the Human directly submits
`/my-interface-agent-native`, and removed when that turn stops. The grant is
non-transferable: a tool call fired from inside a subagent (hook input carries
`agent_id`) never sees it.
"""

import json
import os
import re
import sys
import tempfile

SYNC_SKILL = "my-interface-agent-native"
GRANT_PREFIX = "interface-agent-native-grant-"

DENY_AGENT_READ = (
    "Interface boundary: `.interface/agent/` (the Agent Module) is readable only "
    "inside the exact prompt created by the Human's direct `/my-interface-agent-native` "
    "invocation, and that grant is non-transferable. Use the synchronized Runtime "
    "artifacts under `.claude/` instead. If a required capability is missing, report "
    "Runtime drift and ask the Human to run `/my-interface-agent-native`."
)
DENY_SYNC_INVOKE = (
    "Interface boundary: `/my-interface-agent-native` (Agent Native Sync) may only be "
    "invoked directly by the Human. No Skill, Agent Instance, coordinator, hook, or "
    "model-generated action may invoke it. Ask the Human to run it."
)
DENY_INTERFACE_WRITE = (
    "Interface boundary: the `.interface/` tree is read-only to every Skill and Agent "
    "Instance. The only writable exception is an exact operational record under "
    "`.interface/config/` that the active Skill's owning Component authorizes. Report the "
    "needed change and leave the source for direct Human authorship."
)
DENY_BASH_INTERFACE_MUTATION = (
    "Interface boundary: this shell command references a protected `.interface/` path "
    "together with a mutation-capable operation. Protected Interface paths are read-only; "
    "only exact records under `.interface/config/` may be changed by an authorized Skill. "
    "Narrow the command so its write targets cannot include a protected path."
)

# Shell tokens that can mutate files. Heuristic by design (reported as such by Sync).
MUTATION_TOKENS = re.compile(
    r"(?<![\w-])(rm|mv|cp|rmdir|mkdir|touch|truncate|ln|chmod|chown|tee|install|rsync|dd|shred|unlink)(?![\w-])"
    r"|(?<![\w-])sed\s+(-[a-zA-Z]*i|--in-place)"
    r"|(?<![\w-])perl\s+(-[a-zA-Z]*i|--in-place)"
    r"|(?<![\w-])git\s+(checkout|restore|reset|clean|stash|rm|mv|apply)(?![\w-])"
    r"|(?<![\w-])(python3?|perl|ruby|node|deno|bun|php)(?![\w-])"
    r"|>"
)

# Any reference to the Interface tree inside a shell command, with its sub-path.
INTERFACE_REF = re.compile(r"\.interface(?:/[^\s'\"`;|&()<>]*)?")


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    sys.exit(0)


def fail_closed(detail: str) -> None:
    sys.stderr.write(
        "interface-boundary-guard failed closed (security/integrity control): "
        + detail
        + "\n"
    )
    sys.exit(2)


def project_root(payload: dict) -> str:
    root = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    return os.path.realpath(root)


def grant_active(payload: dict) -> bool:
    if payload.get("agent_id") or payload.get("agent_type"):
        return False  # non-transferable: never inside a subagent
    session_id = payload.get("session_id")
    if not session_id or not re.fullmatch(r"[A-Za-z0-9_.-]+", session_id):
        return False
    marker = os.path.join(tempfile.gettempdir(), GRANT_PREFIX + session_id)
    return os.path.isfile(marker)


def norm(root: str, path: str) -> str:
    if not path:
        return ""
    expanded = os.path.expanduser(path)
    if not os.path.isabs(expanded):
        expanded = os.path.join(root, expanded)
    return os.path.realpath(expanded)


def within(path: str, base: str) -> bool:
    if not path:
        return False
    return path == base or path.startswith(base + os.sep)


def main() -> None:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            fail_closed("hook input is not a JSON object")
    except Exception as exc:  # noqa: BLE001
        fail_closed(f"could not parse hook input ({exc.__class__.__name__})")

    try:
        tool = payload.get("tool_name", "")
        tool_input = payload.get("tool_input") or {}
        if not isinstance(tool_input, dict):
            tool_input = {}

        root = project_root(payload)
        interface_dir = os.path.join(root, ".interface")
        agent_dir = os.path.join(interface_dir, "agent")
        config_dir = os.path.join(interface_dir, "config")
        granted = grant_active(payload)

        # 1. Non-Human invocation of Agent Native Sync is always blocked.
        if tool == "Skill":
            name = str(tool_input.get("skill") or tool_input.get("name") or "").strip()
            name = name.lstrip("/")
            if name == SYNC_SKILL or name.endswith(":" + SYNC_SKILL):
                deny(DENY_SYNC_INVOKE)
            sys.exit(0)

        # 2. Reads of the Agent Module (Read / Glob / Grep).
        if tool in ("Read", "Glob", "Grep"):
            targets = []
            for key in ("file_path", "path", "notebook_path"):
                value = tool_input.get(key)
                if isinstance(value, str) and value:
                    targets.append(norm(root, value))
            for key in ("pattern", "glob"):
                value = tool_input.get(key)
                if isinstance(value, str) and ".interface/agent" in value.replace("\\", "/"):
                    targets.append(agent_dir)
            if any(within(t, agent_dir) for t in targets) and not granted:
                deny(DENY_AGENT_READ)
            sys.exit(0)

        # 3. Mutations of the Interface tree (Edit / Write / NotebookEdit).
        if tool in ("Edit", "Write", "NotebookEdit"):
            for key in ("file_path", "notebook_path", "path"):
                value = tool_input.get(key)
                if not isinstance(value, str) or not value:
                    continue
                target = norm(root, value)
                if within(target, interface_dir) and not within(target, config_dir):
                    deny(DENY_INTERFACE_WRITE)
                if target == config_dir:
                    deny(DENY_INTERFACE_WRITE)
            sys.exit(0)

        # 4. Shell commands.
        if tool == "Bash":
            command = str(tool_input.get("command") or "")
            refs = [m.group(0).replace("\\", "/") for m in INTERFACE_REF.finditer(command)]
            if not refs:
                sys.exit(0)

            touches_agent = any(
                r == ".interface/agent" or r.startswith(".interface/agent/") for r in refs
            )
            touches_protected = any(
                not (r.startswith(".interface/config/") and len(r) > len(".interface/config/"))
                for r in refs
            )
            # A bare `.interface`, `.interface/`, or `.interface/config` reference is an
            # ancestor of protected content and therefore protected.

            if touches_agent and not granted:
                deny(DENY_AGENT_READ)
            if touches_protected and MUTATION_TOKENS.search(command):
                deny(DENY_BASH_INTERFACE_MUTATION)
            sys.exit(0)

        sys.exit(0)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        fail_closed(f"unexpected error ({exc.__class__.__name__}: {exc})")


if __name__ == "__main__":
    main()
