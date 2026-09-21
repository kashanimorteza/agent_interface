#!/usr/bin/env python3
"""Enforced Guarantee `interface-boundary-guard` (PreToolUse, fail_closed).

Synchronized by /my-interface-agent-native; do not edit by hand.

Blocks:
1. Agent Module (.interface/agent/) access outside the exact Human-invoked
   /my-interface-agent-native prompt, and always from a subagent (non-transferable).
2. Every non-Human attempt to invoke /my-interface-agent-native.
3. Direct mutation of any .interface/ path outside .interface/config/.
4. Tampering with the grant state (.claude/hooks/.state/).
5. Model invocation of Interface Operation Skills outside their declared
   invocation policy (only my-interface-implement may coordinate
   configure/plan/develop/review; launch/implement/reset are Human-only).

Exit 2 = block (reason on stderr). Any internal error also exits 2.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import interface_grants as g  # noqa: E402

AGENT_MSG = ("Blocked by interface-boundary-guard: the Agent Module (.interface/agent/) is readable only "
             "inside the prompt the Human creates by typing /my-interface-agent-native, and never from a "
             "subagent. Use the synchronized Runtime artifacts; if one is missing, report Runtime drift and "
             "ask the Human to run /my-interface-agent-native.")
MUTATE_MSG = ("Blocked by interface-boundary-guard: .interface/ is read-only except exact records under "
              ".interface/config/ owned by the active Skill. Report the needed change for direct Human authorship.")
STATE_MSG = "Blocked by interface-boundary-guard: grant state under .claude/hooks/.state/ cannot be created or changed by the Agent."
SYNC_MSG = ("Blocked by interface-boundary-guard: /my-interface-agent-native can be invoked only by the Human "
            "typing it directly. Ask the Human to run it.")

COORDINATED = {"my-interface-configure", "my-interface-plan", "my-interface-develop", "my-interface-review"}
HUMAN_ONLY = {"my-interface-launch", "my-interface-implement", "my-interface-reset"}

READ_TOOLS = {"Read", "Glob", "Grep", "NotebookRead", "LS"}
WRITE_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}
PATH_KEYS = ("file_path", "path", "notebook_path")

MUTATING_BASH = re.compile(
    r"(^|[\s;&|(`])(rm|rmdir|mv|cp|rsync|ln|touch|mkdir|chmod|chown|truncate|tee|install|dd|unlink|shred|"
    r"sed\s+(-[A-Za-z]*\s+)*-i|perl\s+(-[A-Za-z]*\s+)*-[A-Za-z]*i|"
    r"git\s+(checkout|restore|clean|reset|rm|mv|stash|apply|am|merge|pull|rebase|cherry-pick|revert))\b")
REDIRECT = re.compile(r"(?<![0-9&])>{1,2}\s*([^\s;|&)]+)")


def project_dir(data):
    return os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())


def resolve(p, cwd):
    p = os.path.expanduser(str(p))
    if not os.path.isabs(p):
        p = os.path.join(cwd, p)
    return os.path.realpath(p)


def inside(path, root):
    return path == root or path.startswith(root + os.sep)


def deny(msg):
    sys.stderr.write(msg + "\n")
    return 2


def main():
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    sid = data.get("session_id")
    in_subagent = bool(data.get("agent_id"))
    proj = project_dir(data)
    cwd = os.path.realpath(data.get("cwd") or proj)

    iface = os.path.join(proj, ".interface")
    agent_mod = os.path.join(iface, "agent")
    config = os.path.join(iface, "config")
    state = os.path.realpath(g.STATE_DIR)

    sync_grant = (not in_subagent) and g.has_grant(sid, g.AGENT_NATIVE)
    # Only path-like fields count as a reference; file content or a search regex
    # that merely mentions the path is not an access.
    path_fields = list(PATH_KEYS) + (["pattern"] if tool == "Glob" else []) + ["glob", "command"]
    blob = " ".join(str(ti.get(k)) for k in path_fields if ti.get(k)).replace("\\", "/")
    mentions_agent = "interface/agent" in blob
    mentions_state = "hooks/.state" in blob

    # --- Skill invocation policy -------------------------------------------------
    if tool == "Skill":
        name = str(ti.get("skill") or ti.get("command") or ti.get("name") or "").strip().lstrip("/").split(" ")[0]
        name = name.split(":")[-1]
        if name == "my-interface-agent-native":
            return deny(SYNC_MSG)
        if name in HUMAN_ONLY:
            return deny("Blocked by interface-boundary-guard: /{} is invocable only by the Human typing it.".format(name))
        if name in COORDINATED and not g.has_grant(sid, g.IMPLEMENT):
            return deny("Blocked by interface-boundary-guard: /{} may be invoked by the model only while the "
                        "Human-invoked /my-interface-implement coordinates it; otherwise the Human types it.".format(name))
        return 0

    # --- Resolved paths ------------------------------------------------------------
    paths = [resolve(ti[k], cwd) for k in PATH_KEYS if isinstance(ti.get(k), str) and ti.get(k)]
    if tool == "Glob" and isinstance(ti.get("pattern"), str):
        base = paths[0] if paths else cwd
        pat = ti["pattern"]
        paths.append(resolve(pat if os.path.isabs(pat) else os.path.join(base, pat), cwd))

    if tool in READ_TOOLS:
        if mentions_agent or any(inside(p, agent_mod) for p in paths):
            return 0 if sync_grant else deny(AGENT_MSG)
        return 0

    if tool in WRITE_TOOLS:
        for p in paths:
            if inside(p, state):
                return deny(STATE_MSG)
            if inside(p, iface) and not inside(p, config):
                return deny(MUTATE_MSG)
        if mentions_agent or mentions_state:
            return deny(MUTATE_MSG)
        return 0

    if tool == "Bash":
        cmd = str(ti.get("command") or "")
        if mentions_state:
            return deny(STATE_MSG)
        mutating = bool(MUTATING_BASH.search(cmd))
        # Redirection targets
        for target in REDIRECT.findall(cmd):
            t = resolve(target.strip("'\""), cwd)
            if inside(t, state):
                return deny(STATE_MSG)
            if inside(t, iface) and not inside(t, config):
                return deny(MUTATE_MSG)
        if "interface/agent" in cmd:
            if mutating:
                return deny(MUTATE_MSG)
            return 0 if sync_grant else deny(AGENT_MSG)
        if mutating and ".interface" in cmd:
            # Allow only when every .interface path mentioned is inside .interface/config/
            refs = re.findall(r"[^\s'\";|&()<>]*\.interface[^\s'\";|&()<>]*", cmd)
            for r in refs:
                if not inside(resolve(r, cwd), config):
                    return deny(MUTATE_MSG)
        return 0

    # Any other matched tool: block Agent Module reference without the grant.
    if mentions_agent and not sync_grant:
        return deny(AGENT_MSG)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.stderr.write("interface-boundary-guard failed closed: {}\n".format(exc))
        sys.exit(2)
