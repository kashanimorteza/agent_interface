#!/usr/bin/env python3
"""PreToolUse guard: realization of the Enforced Guarantee `interface-boundary-guard`.

Native realization (Claude Code) synchronized by /my-interface-agent-native. The Human-owned
Agent Module remains authoritative; this script is not a second authority.

Guarantee: block Agent Module reads outside the exact direct-Human Agent Native Sync prompt,
block every non-Human attempt to invoke Agent Native Sync, and block direct Interface mutations
outside the authorized Config boundary.
Event: PreToolUse (matcher Read|Glob|Grep|Edit|Write|NotebookEdit|Bash|Skill).
Allowed effects: allow or block the triggering tool call; never writes anything.
Failure policy: fail_closed (any internal error blocks the call). May block: yes.
"""
import json
import os
import re
import sys
import time

SYNC_SKILL = "my-interface-agent-native"
GRANT_MAX_AGE_SECONDS = 6 * 60 * 60
PREFIX = "[interface-boundary-guard] "


def block(reason):
    sys.stderr.write(PREFIX + reason + "\n")
    sys.exit(2)


def allow():
    sys.exit(0)


def project_dir(data):
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    return os.path.realpath(root)


def resolve(path, cwd):
    path = os.path.expanduser(str(path))
    if not os.path.isabs(path):
        path = os.path.join(cwd, path)
    return os.path.realpath(path)


def within(path, directory):
    return path == directory or path.startswith(directory + os.sep)


def has_grant(state_dir, data):
    """True only for the main agent of the session whose Human typed /my-interface-agent-native
    in the current prompt. Subagents never inherit the grant."""
    if data.get("agent_id") or data.get("agent_type"):
        return False
    session_id = re.sub(r"[^A-Za-z0-9_.-]", "_", str(data.get("session_id") or ""))
    if not session_id:
        return False
    grant_file = os.path.join(state_dir, "agent-native-grant-" + session_id + ".json")
    try:
        with open(grant_file) as handle:
            grant = json.load(handle)
    except (OSError, ValueError):
        return False
    if grant.get("session_id") != data.get("session_id"):
        return False
    return time.time() - float(grant.get("created_at", 0)) < GRANT_MAX_AGE_SECONDS


def strings_in(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            for text in strings_in(item):
                yield text
    elif isinstance(value, list):
        for item in value:
            for text in strings_in(item):
                yield text


def names_sync_skill(text):
    name = text.strip().lstrip("/").split()[0] if text.strip() else ""
    return name == SYNC_SKILL or name.endswith(":" + SYNC_SKILL)


MUTATING = re.compile(
    r"(^|[\s;&|(`])("
    r"rm|rmdir|mv|cp|touch|mkdir|truncate|tee|ln|chmod|chown|install|rsync|dd|unlink|shred|"
    r"sed\s+[^|;&]*-i|perl\s+[^|;&]*-i|git\s+(checkout|restore|rm|mv|clean|reset|stash|apply)"
    r")\b"
)
REDIRECT_TARGET = re.compile(r">{1,2}\s*([^\s;|&<>]+)")
INTERFACE_REF = re.compile(r"\.interface(/[^\s;|&'\"<>)]*)?")


def guard_bash(command, granted):
    if SYNC_SKILL in command:
        block("Agent Native Sync can only be invoked by the Human typing /" + SYNC_SKILL + ".")
    if "hooks/state" in command or "agent_native_grant" in command:
        block("The Agent Native Sync grant state and grant handler cannot be touched by a tool call.")
    if not granted and re.search(r"\.interface/+agent\b", command):
        block("Agent Module sources (.interface/agent/) are readable only within the Human's "
              "direct /" + SYNC_SKILL + " prompt. Use the synchronized Native realization; "
              "report Runtime drift if something is missing.")
    refs = [m.group(0) for m in INTERFACE_REF.finditer(command)]
    protected = [r for r in refs if not re.match(r"\.interface/+config(/|$)", r)]
    if not protected:
        return
    for target in REDIRECT_TARGET.findall(command):
        if ".interface" in target and not re.search(r"\.interface/+config(/|$)", target):
            block("Interface paths are read-only outside .interface/config/ (redirect to " + target + ").")
    if MUTATING.search(command):
        block("This command could mutate a protected Interface path (" + ", ".join(sorted(set(protected))) +
              "). The Interface is read-only outside .interface/config/; leave the change for direct Human authorship.")


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        block("Malformed hook input; failing closed.")
    tool = data.get("tool_name") or ""
    tool_input = data.get("tool_input") or {}
    root = project_dir(data)
    cwd = os.path.realpath(data.get("cwd") or root)
    interface_dir = os.path.join(root, ".interface")
    agent_dir = os.path.join(interface_dir, "agent")
    config_dir = os.path.join(interface_dir, "config")
    state_dir = os.path.join(root, ".claude", "hooks", "state")
    granted = has_grant(state_dir, data)
    denied_read = ("Agent Module sources (.interface/agent/) are readable only within the Human's direct /" +
                   SYNC_SKILL + " prompt, and never by a subagent. Use the synchronized Native realization; "
                   "report Runtime drift if something is missing.")

    if tool == "Skill":
        for text in strings_in(tool_input):
            if names_sync_skill(text):
                block("Agent Native Sync can only be invoked by the Human typing /" + SYNC_SKILL + ".")
        allow()

    if tool == "Bash":
        guard_bash(str(tool_input.get("command") or ""), granted)
        allow()

    if tool in ("Edit", "Write", "NotebookEdit"):
        raw = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not raw:
            block("No target path in " + tool + " input; failing closed.")
        target = resolve(raw, cwd)
        if within(target, state_dir):
            block("The Agent Native Sync grant state cannot be written by a tool call.")
        if within(target, interface_dir) and not within(target, config_dir):
            block("Interface paths are read-only; only exact records inside .interface/config/ may be changed, "
                  "by the Skill that owns them. Leave " + raw + " for direct Human authorship.")
        allow()

    if tool == "Read":
        target = resolve(tool_input.get("file_path") or "", cwd)
        if within(target, agent_dir) and not granted:
            block(denied_read)
        allow()

    if tool in ("Glob", "Grep"):
        search_root = resolve(tool_input.get("path") or cwd, cwd)
        if within(search_root, agent_dir):
            if not granted:
                block(denied_read)
            allow()
        if granted or not within(agent_dir, search_root):
            allow()
        relative = os.path.relpath(agent_dir, search_root).replace(os.sep, "/")
        if tool == "Glob":
            pattern = str(tool_input.get("pattern") or "")
            if "interface/agent" in pattern or pattern.lstrip("./").startswith(relative):
                block(denied_read)
            allow()
        glob = str(tool_input.get("glob") or "")
        if glob.startswith("!") and relative in glob:
            allow()
        block("This search would include Agent Module sources (" + relative + "/). Narrow `path` to a "
              "directory that does not contain it, or pass glob \"!" + relative + "/**\".")

    allow()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as error:  # fail closed on any internal failure
        block("Guard error (" + type(error).__name__ + "); failing closed.")
