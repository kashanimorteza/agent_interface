#!/usr/bin/env python3
"""Agent Interface boundary guard for Claude Code hooks.

Synchronized by /my-interface-agent-native. Realizes two Enforced Guarantees
declared by the Human-owned Agent Permission Preferences; this file is a
Runtime realization, never an authority.

- interface-boundary-guard (PreToolUse, fail closed): blocks Agent Module reads
  outside the Human's direct Agent Native Sync prompt, blocks every non-Human
  attempt to invoke Agent Native Sync, and blocks Interface mutations outside
  the Config boundary.
- agent-native-read-grant (UserPromptExpansion, fail closed): grants Agent
  Module reads only to the exact prompt created by the Human typing
  /my-interface-agent-native. The grant is bound to that session and prompt,
  is revoked by the next prompt, and is never honoured inside a subagent.

Modes: grant (UserPromptExpansion), revoke (UserPromptSubmit), guard (PreToolUse).
A PreToolUse block exits 2 with the reason on stderr.
"""

import fnmatch
import glob
import hashlib
import json
import os
import re
import shlex
import sys
import tempfile
from pathlib import Path

SYNC_SKILL = "my-interface-agent-native"
STORE_NAME = "claude-interface-guard"
MUTATING_TOOLS = {"Edit", "Write", "NotebookEdit"}
READ_TOOLS = {"Read", "Glob", "Grep"}

READ_BLOCK = (
    "Blocked by interface-boundary-guard: the Agent Module (.interface/agent/) is readable only "
    "within the prompt created by the Human's direct /my-interface-agent-native invocation, and "
    "never from a subagent. Use the synchronized Runtime artifacts (.claude/rules/, .claude/skills/); "
    "if one is missing, report Runtime drift and ask the Human to run /my-interface-agent-native."
)
SEARCH_BLOCK = (
    READ_BLOCK + " This search would include .interface/agent/; scope it to a path or glob that "
    "excludes that directory."
)
MUTATION_BLOCK = (
    "Blocked by interface-boundary-guard: .interface/ is read-only to every Agent Instance and Skill; "
    "only .interface/config/ may change. Report the needed change for direct Human authorship."
)
INVOKE_BLOCK = (
    "Blocked by interface-boundary-guard: Agent Native Sync can only be started by the Human typing "
    "/my-interface-agent-native. No Agent, Skill, subagent, hook, or automation may invoke it."
)
GRANT_STORE_BLOCK = "Blocked by interface-boundary-guard: the Agent Native Sync read grant cannot be created or changed by a tool call."

BASH_MUTATING = re.compile(
    r"(^|[\s;&|(`])(rm|rmdir|mv|cp|touch|mkdir|tee|truncate|ln|chmod|chown|install|rsync|dd|patch|unlink|"
    r"sed\s+(-\w+\s+)*-i|perl\s+(-\w+\s+)*-\w*i|git\s+(checkout|restore|clean|rm|mv|reset|stash|apply|am|merge|pull|rebase|switch))\b"
)
BASH_GIT_WHOLESALE = re.compile(r"\bgit\s+(clean|stash|reset\s+(\S+\s+)*--hard)\b")
BASH_RECURSIVE_READ = re.compile(
    r"(^|[\s;&|(`])(rg|ag|ack|find|tree|tar|zip|rsync)\b|\bgrep\s+(-\w*[rR]\w*|--recursive)|\bls\s+-\w*R|\bcp\s+-\w*[rRa]|\bgit\s+grep\b"
)
REDIRECT = re.compile(r"(?<![0-9&])>>?\s*([^\s;&|)]+)")


def project_dir(event):
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()).resolve()


def store_dir(project, override=None):
    if override:
        return Path(override)
    digest = hashlib.sha256(str(project).encode()).hexdigest()[:16]
    return Path(tempfile.gettempdir()) / STORE_NAME / digest


def grant_path(store, session_id):
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id or "unknown")
    return store / f"{safe}.json"


def resolve(raw, cwd):
    p = Path(os.path.expanduser(str(raw)))
    if not p.is_absolute():
        p = Path(cwd) / p
    return Path(os.path.normpath(str(p)))


def within(path, root):
    return path == root or root in path.parents


def is_protected(path, iface, config):
    return within(path, iface) and not within(path, config)


def has_grant(event, store):
    """True only in the main thread of the exact prompt the Human opened with /my-interface-agent-native."""
    if event.get("agent_id"):
        return False
    try:
        grant = json.loads(grant_path(store, event.get("session_id")).read_text())
    except (OSError, ValueError):
        return False
    if grant.get("session_id") != event.get("session_id"):
        return False
    granted_prompt = grant.get("prompt_id")
    return not granted_prompt or granted_prompt == event.get("prompt_id")


def mode_grant(event, store):
    if event.get("command_name") != SYNC_SKILL:
        return 0
    if event.get("expansion_type") not in (None, "slash_command"):
        return 0
    store.mkdir(parents=True, exist_ok=True)
    record = {"session_id": event.get("session_id"), "prompt_id": event.get("prompt_id")}
    grant_path(store, event.get("session_id")).write_text(json.dumps(record))
    return 0


def mode_revoke(event, store):
    target = grant_path(store, event.get("session_id"))
    if not target.exists():
        return 0
    try:
        grant = json.loads(target.read_text())
    except (OSError, ValueError):
        grant = {}
    same_prompt = grant.get("prompt_id") and grant.get("prompt_id") == event.get("prompt_id")
    typed_sync = (event.get("prompt") or "").strip().split(maxsplit=1)[:1] == ["/" + SYNC_SKILL]
    if not (same_prompt or typed_sync):
        try:
            target.unlink()
        except FileNotFoundError:
            pass
    return 0


def search_reaches(base, pattern_glob, agent):
    """Whether a search rooted at base (optionally filtered by a glob) can include Agent Module files."""
    if within(base, agent):
        return True
    if not within(agent, base):
        return False
    if not pattern_glob:
        return True
    for root, _dirs, files in os.walk(agent):
        for name in files:
            full = Path(root) / name
            rel = str(full.relative_to(base))
            if fnmatch.fnmatch(name, pattern_glob) or fnmatch.fnmatch(rel, pattern_glob):
                return True
    return False


def glob_regex(pattern):
    """Translate a Glob-tool pattern (**, *, ?, [..], {a,b}) to a regex; hidden paths match like any other."""
    out, i = [], 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
            continue
        if pattern.startswith("**", i):
            out.append(".*")
            i += 2
            continue
        if c == "*":
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        elif c == "[":
            end = pattern.find("]", i + 1)
            if end == -1:
                out.append(re.escape(c))
            else:
                out.append(pattern[i:end + 1])
                i = end
        elif c == "{":
            end = pattern.find("}", i + 1)
            if end == -1:
                out.append(re.escape(c))
            else:
                out.append("(?:" + "|".join(re.escape(p) for p in pattern[i + 1:end].split(",")) + ")")
                i = end
        else:
            out.append(re.escape(c))
        i += 1
    return re.compile("".join(out) + r"\Z")


def glob_reaches(base, pattern, agent):
    """Whether a Glob call (base directory + pattern) can match any Agent Module path."""
    combined = pattern if os.path.isabs(pattern) else str(base / pattern)
    prefix = re.split(r"[*?\[{]", combined, maxsplit=1)[0]
    prefix_path = Path(os.path.normpath(prefix)) if prefix else base
    if within(prefix_path, agent):
        return True
    if not (within(agent, prefix_path) or within(agent, prefix_path.parent)):
        return False
    matcher = glob_regex(os.path.normpath(combined))
    candidates = [agent]
    for root, dirs, files in os.walk(str(agent)):
        candidates.extend(Path(root) / name for name in dirs + files)
    return any(matcher.match(str(c)) for c in candidates)


def bash_paths(command, cwd):
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        tokens = command.split()
    paths = []
    for token in tokens:
        for piece in re.split(r"[=:]", token) if "=" in token else [token]:
            if not piece or piece.startswith("-"):
                continue
            if any(ch in piece for ch in "*?["):
                matches = glob.glob(str(resolve(piece, cwd)), recursive=True)
                paths.extend(Path(os.path.normpath(m)) for m in matches)
            paths.append(resolve(piece, cwd))
    return paths


def guard_bash(event, command, project, store):
    cwd = Path(event.get("cwd") or project)
    iface = project / ".interface"
    agent = iface / "agent"
    config = iface / "config"
    if STORE_NAME in command:
        return GRANT_STORE_BLOCK
    if SYNC_SKILL in command and re.search(r"\bclaude\b", command):
        return INVOKE_BLOCK
    paths = bash_paths(command, cwd)
    lowered = command.replace("\\", "/")

    if BASH_MUTATING.search(command) or REDIRECT.search(command):
        targets = paths + [resolve(t, cwd) for t in REDIRECT.findall(command)]
        if any(is_protected(p, iface, config) for p in targets):
            return MUTATION_BLOCK
        if BASH_GIT_WHOLESALE.search(command) and (
            within(iface, cwd) or any(within(iface, p) for p in paths)
        ):
            return MUTATION_BLOCK

    if has_grant(event, store):
        return None
    if re.search(r"interface/+agent(/|\b)", lowered) or any(within(p, agent) for p in paths):
        return READ_BLOCK
    if BASH_RECURSIVE_READ.search(command):
        existing = [p for p in paths if p.exists()]
        if any(within(agent, p) for p in existing) or (not existing and within(agent, cwd)):
            return SEARCH_BLOCK
    return None


def mode_guard(event, store):
    project = project_dir(event)
    iface = project / ".interface"
    agent = iface / "agent"
    config = iface / "config"
    cwd = Path(event.get("cwd") or project)
    tool = event.get("tool_name") or ""
    tool_input = event.get("tool_input") or {}

    if tool == "Skill":
        blob = json.dumps(tool_input)
        return INVOKE_BLOCK if SYNC_SKILL in blob else None

    if tool == "Bash":
        return guard_bash(event, str(tool_input.get("command") or ""), project, store)

    if tool in MUTATING_TOOLS:
        raw = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not raw:
            return MUTATION_BLOCK
        target = resolve(raw, cwd)
        if STORE_NAME in str(target):
            return GRANT_STORE_BLOCK
        return MUTATION_BLOCK if is_protected(target, iface, config) else None

    if tool in READ_TOOLS:
        if has_grant(event, store):
            return None
        if tool == "Read":
            raw = tool_input.get("file_path")
            return READ_BLOCK if raw and within(resolve(raw, cwd), agent) else None
        base = resolve(tool_input.get("path") or cwd, cwd)
        if tool == "Glob":
            return READ_BLOCK if glob_reaches(base, str(tool_input.get("pattern") or ""), agent) else None
        if tool == "Grep":
            reaches = search_reaches(base, tool_input.get("glob"), agent)
            return (READ_BLOCK if within(base, agent) else SEARCH_BLOCK) if reaches else None
    return None


def main(argv):
    mode = argv[1] if len(argv) > 1 else ""
    override = argv[argv.index("--store") + 1] if "--store" in argv else None
    try:
        event = json.load(sys.stdin)
        store = store_dir(project_dir(event), override)
        if mode == "grant":
            return mode_grant(event, store)
        if mode == "revoke":
            return mode_revoke(event, store)
        if mode == "guard":
            reason = mode_guard(event, store)
            if reason:
                print(reason, file=sys.stderr)
                return 2
            return 0
        print(f"interface_guard: unknown mode {mode!r}", file=sys.stderr)
        return 2
    except Exception as exc:  # fail closed and visible
        print(f"interface_guard failed ({mode}): {exc!r}; blocking by fail_closed policy.", file=sys.stderr)
        return 2 if mode == "guard" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
