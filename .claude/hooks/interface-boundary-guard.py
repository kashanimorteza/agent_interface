"""Enforced Guarantee `interface-boundary-guard` (PreToolUse, fail closed, required, blocking).

Blocks:
  1. Agent Module reads (.interface/agent/) outside the exact direct-Human Agent Native Sync prompt;
  2. every non-Human attempt to invoke Agent Native Sync (Skill tool calls for it);
  3. direct Interface mutations outside the authorized Config boundary (.interface/config/);
  4. any tool call that touches the grant store, so a grant cannot be forged.

Any internal error blocks the call (exit 2). Synchronized by Agent Native Sync (/my-interface-agent-native).
"""

import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import interface_grant  # noqa: E402

READ_DENIED = (
    "Blocked by interface-boundary-guard: the Agent Module (.interface/agent/) is readable only within the prompt "
    "the Human creates by typing /my-interface-agent-native, and never from a subagent. Use the synchronized "
    "Native artifacts (.claude/rules, .claude/skills, .claude/settings.json); if one is missing, report Runtime "
    "drift and ask the Human to run /my-interface-agent-native."
)
WRITE_DENIED = (
    "Blocked by interface-boundary-guard: .interface/ is read-only; only .interface/config/ may be changed. "
    "Report the needed change for direct Human authorship instead."
)
SYNC_DENIED = (
    "Blocked by interface-boundary-guard: Agent Native Sync can only be started by the Human typing "
    "/my-interface-agent-native. Do not invoke, schedule, or simulate it; ask the Human instead."
)
GRANT_DENIED = "Blocked by interface-boundary-guard: the Agent Module read grant store cannot be accessed by tools."
SEARCH_DENIED = (
    "Blocked by interface-boundary-guard: this search would reach the Agent Module (.interface/agent/). "
    "Narrow the path or pattern so it excludes .interface/agent/."
)

SAFE_INTERFACE_READ = re.compile(r"^/(config|foundation|implementation|target)(/|$)|^/interface\.md$")
INTERFACE_TOKEN = re.compile(r"\.interface((?:/[^\s'\"`;|&()<>]*)?)", re.IGNORECASE)
MUTATING_WORD = re.compile(
    r"(^|[\s;&|(`])(rm|rmdir|mv|cp|tee|touch|truncate|ln|chmod|chown|install|rsync|dd|unlink|mkdir|patch)(\s|$)"
    r"|\bsed\s+(-[a-zA-Z]*i|--in-place)|\bperl\s+-[a-zA-Z]*i"
    r"|\bgit\s+(checkout|restore|reset|clean|rm|mv|stash|apply|am|merge|pull|switch)\b",
)
REDIRECT_TARGET = re.compile(r"(?:^|[^0-9&>])>{1,2}\|?\s*([^\s;|&()]+)")


def norm(path):
    return os.path.normcase(os.path.realpath(path)).lower()


def inside(path, root):
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


class Boundary(object):
    def __init__(self, payload):
        self.cwd = payload.get("cwd") or os.getcwd()
        project = interface_grant.project_dir(payload)
        self.interface = norm(os.path.join(project, ".interface"))
        self.agent = norm(os.path.join(project, ".interface", "agent"))
        self.config = norm(os.path.join(project, ".interface", "config"))
        self.grants = norm(interface_grant.grant_root())
        self.agent_raw = os.path.join(project, ".interface", "agent")

    def resolve(self, path):
        path = os.path.expanduser(str(path))
        if not os.path.isabs(path):
            path = os.path.join(self.cwd, path)
        return norm(path)

    def agent_files(self, root):
        """Agent Module file paths relative to a search root that contains it."""
        found = []
        for base, _dirs, files in os.walk(self.agent_raw):
            for name in files:
                full = os.path.join(base, name)
                found.append(os.path.relpath(os.path.realpath(full), os.path.realpath(root)).replace(os.sep, "/"))
        return found or ["agent/agent.md"]


def glob_regex(pattern):
    """Translate a glob (with **, *, ?, [..], {a,b}) into an anchored case-insensitive regex."""
    out, i = [], 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif c == "*":
            out.append("[^/]*")
            i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        elif c == "[":
            end = pattern.find("]", i + 1)
            if end == -1:
                out.append(re.escape(c))
                i += 1
            else:
                body = pattern[i + 1:end].replace("\\", "\\\\")
                if body.startswith("!"):
                    body = "^" + body[1:]
                out.append("[" + body + "]")
                i = end + 1
        elif c == "{":
            end = pattern.find("}", i + 1)
            if end == -1:
                out.append(re.escape(c))
                i += 1
            else:
                alternatives = pattern[i + 1:end].split(",")
                out.append("(?:" + "|".join(glob_regex(a)[4:-1] for a in alternatives) + ")")
                i = end + 1
        else:
            out.append(re.escape(c))
            i += 1
    return "(?i)" + "".join(out) + "$"


def glob_reaches(pattern, relpaths, basename_only):
    negated = pattern.startswith("!")
    regex = re.compile(glob_regex(pattern[1:] if negated else pattern))
    for rel in relpaths:
        subject = rel.rsplit("/", 1)[-1] if basename_only else rel
        matched = bool(regex.match(subject))
        if matched != negated:
            return True
    return False


def check_path_tool(tool, data, b, granted):
    path = data.get("notebook_path") if tool == "NotebookEdit" else data.get("file_path")
    if not path:
        return None
    target = b.resolve(path)
    if inside(target, b.grants):
        return GRANT_DENIED
    if tool == "Read":
        if inside(target, b.agent) and not granted:
            return READ_DENIED
        return None
    if inside(target, b.interface) and not inside(target, b.config):
        return WRITE_DENIED
    return None


def check_search_tool(tool, data, b, granted):
    root = b.resolve(data.get("path") or b.cwd)
    if inside(root, b.grants):
        return GRANT_DENIED, None
    if granted:
        return None, None
    if inside(root, b.agent):
        return READ_DENIED, None
    if not inside(b.agent, root):
        return None, None
    relpaths = b.agent_files(data.get("path") or b.cwd)
    if tool == "Glob":
        pattern = str(data.get("pattern") or "")
        if os.path.isabs(pattern):
            pattern = os.path.relpath(pattern, os.path.realpath(data.get("path") or b.cwd)).replace(os.sep, "/")
        return (SEARCH_DENIED, None) if glob_reaches(pattern, relpaths, False) else (None, None)
    glob = data.get("glob")
    if glob:
        return (SEARCH_DENIED, None) if glob_reaches(str(glob), relpaths, "/" not in str(glob)) else (None, None)
    # Repository-wide Grep with no glob: exclude the Agent Module from the search.
    exclusion = os.path.relpath(b.agent_raw, os.path.realpath(data.get("path") or b.cwd)).replace(os.sep, "/")
    updated = dict(data)
    updated["glob"] = "!" + exclusion + "/**"
    return None, updated


def check_bash(data, b, granted):
    command = str(data.get("command") or "")
    lowered = command.lower()
    if interface_grant.GRANT_DIR_NAME in lowered:
        return GRANT_DENIED
    tokens = [m.group(1) for m in INTERFACE_TOKEN.finditer(command)]
    reaches_agent = "interface/agent" in lowered or any(not SAFE_INTERFACE_READ.search(t) for t in tokens)
    if reaches_agent and not granted:
        return READ_DENIED
    outside_config = [t for t in tokens if not re.match(r"^/config(/|$)", t, re.IGNORECASE)]
    if outside_config:
        stripped = re.sub(r"\d?>>?\s*/dev/null|&>\s*/dev/null|\d?>&\d", " ", command)
        if MUTATING_WORD.search(stripped):
            return WRITE_DENIED
        for target in REDIRECT_TARGET.findall(stripped):
            if ".interface" in target.lower() and not re.search(r"\.interface/config(/|$)", target, re.IGNORECASE):
                return WRITE_DENIED
    return None


def check_skill(data):
    requested = json.dumps(data).lower()
    if interface_grant.SYNC_COMMAND in requested:
        return SYNC_DENIED
    return None


def main():
    payload = json.load(sys.stdin)
    tool = payload.get("tool_name") or ""
    data = payload.get("tool_input") or {}
    b = Boundary(payload)
    granted = interface_grant.has_grant(payload)
    updated = None

    if tool == "Skill":
        reason = check_skill(data)
    elif tool in ("Read", "Edit", "Write", "NotebookEdit"):
        reason = check_path_tool(tool, data, b, granted)
    elif tool in ("Glob", "Grep"):
        reason, updated = check_search_tool(tool, data, b, granted)
    elif tool == "Bash":
        reason = check_bash(data, b, granted)
    else:
        reason = None

    if reason:
        sys.stderr.write(reason + "\n")
        return 2
    if updated is not None:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "interface-boundary-guard excluded .interface/agent/ from this search",
                "updatedInput": updated,
            }
        }))
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except Exception as error:  # fail closed: a broken guard blocks the call
        sys.stderr.write("interface-boundary-guard failed closed: %s\n" % error)
        code = 2
    sys.exit(code)
