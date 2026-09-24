#!/usr/bin/env python3
"""Interface boundary guard for Claude Code (project hook).

Realizes two Enforced Guarantees, both fail_closed:

interface-boundary-guard (PreToolUse: Read|Glob|Grep|Edit|Write|NotebookEdit|Bash|Skill)
  - blocks Agent Module (.interface/agent/) reads outside the exact prompt created
    by the Human's direct /my-interface-agent-native invocation;
  - blocks every non-Human attempt to invoke Agent Native Sync (Skill tool);
  - blocks direct Interface (.interface/) mutations outside .interface/config/.

agent-native-read-grant (UserPromptExpansion matcher my-interface-agent-native)
  - grants Agent Module reads only to the prompt the Human's direct invocation creates;
  - the grant is revoked by the next UserPromptSubmit, by Stop, and by SessionEnd;
  - it is never usable from a subagent (agent_id present) and no tool may touch
    the grant state, so it cannot be created, inherited, or borrowed.

Usage: interface_guard.py <pre-tool-use|grant|submit|revoke>  (hook JSON on stdin)
"""

import fnmatch
import hashlib
import json
import os
import re
import shlex
import sys
import tempfile
import time

SYNC_SKILL = "my-interface-agent-native"
GRANT_TOKEN = "claude-agent-native-grant"
GRANT_TTL_SECONDS = 6 * 60 * 60

PROJECT_DIR = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
INTERFACE_DIR = os.path.join(PROJECT_DIR, ".interface")
AGENT_DIR = os.path.join(INTERFACE_DIR, "agent")
CONFIG_DIR = os.path.join(INTERFACE_DIR, "config")

AGENT_MSG = (
    "interface-boundary-guard: the Agent Module (.interface/agent/) is readable only within the "
    "prompt created by the Human's direct /my-interface-agent-native invocation (never from a "
    "subagent). Use the synchronized Claude Code artifacts (.claude/rules, .claude/skills, "
    ".claude/settings.json). If a Runtime capability is missing, report Runtime drift and ask the "
    "Human to run /my-interface-agent-native."
)
MUTATION_MSG = (
    "interface-boundary-guard: .interface/ is read-only; only .interface/config/ may be changed. "
    "Report the needed change and leave the source for direct Human authorship."
)
SYNC_INVOKE_MSG = (
    "interface-boundary-guard: Agent Native Sync (/my-interface-agent-native) may be invoked only "
    "directly by the Human. Report Runtime drift and ask the Human to run it."
)
GRANT_STATE_MSG = "interface-boundary-guard: the Agent Native Sync grant state is not accessible to any tool."


# ----------------------------------------------------------------------------- grant state
def _grant_dir():
    digest = hashlib.sha256(PROJECT_DIR.encode()).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), GRANT_TOKEN, digest)


def _grant_file(session_id):
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", session_id or "")
    return os.path.join(_grant_dir(), safe + ".json")


def _load_grant(session_id):
    if not session_id:
        return None
    try:
        with open(_grant_file(session_id)) as f:
            grant = json.load(f)
    except (OSError, ValueError):
        return None
    if grant.get("session_id") != session_id:
        return None
    if time.time() - float(grant.get("created", 0)) > GRANT_TTL_SECONDS:
        return None
    return grant


def _write_grant(session_id, state):
    os.makedirs(_grant_dir(), mode=0o700, exist_ok=True)
    path = _grant_file(session_id)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump({"session_id": session_id, "state": state, "created": time.time()}, f)
    os.replace(tmp, path)


def _revoke(session_id):
    try:
        os.remove(_grant_file(session_id))
    except FileNotFoundError:
        pass


# ----------------------------------------------------------------------------- path helpers
def _resolve(path, cwd):
    if not path:
        return None
    path = os.path.expanduser(str(path))
    if not os.path.isabs(path):
        path = os.path.join(cwd, path)
    return os.path.realpath(path)


def _within(path, root):
    return path == root or path.startswith(root + os.sep)


def _mentions_agent(text):
    """True when text names the Agent Module in a non-excluding way."""
    norm = re.sub(r"/+(\./+)*", "/", text)
    for m in re.finditer(r"interface/agent(?=$|[/\s\"'*?\[{)]|\*)", norm):
        prefix = norm[max(0, m.start() - 16):m.start()]
        # negated globs such as '!.interface/agent/**' or '!**/.interface/agent' are exclusions
        if re.search(r"![\s\"'*/.]*$", prefix):
            continue
        return True
    return False


EXCLUSION_RES = (
    r"(-not|!)\s+-(i?path|i?wholename)\s+[\"']?[^\s\"']*interface/agent[^\s\"']*[\"']?",
    r"![\s\"'*/.]*interface/agent[^\s\"']*",
    r"--exclude-dir[= ]+[\"']?(\.interface/)?agent\b[\"']?",
)


def _has_agent_exclusion(text):
    return any(re.search(r, text) for r in EXCLUSION_RES)


def _strip_exclusions(text):
    for r in EXCLUSION_RES:
        text = re.sub(r, " ", text)
    return text


# ----------------------------------------------------------------------------- decisions
def _deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def _allow_with(updated_input, reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": reason,
            "updatedInput": updated_input,
        }
    }))
    sys.exit(0)


# ----------------------------------------------------------------------------- Bash analysis
RECURSIVE_TOOLS = {"rg", "ag", "ack", "find", "tree", "tar", "zip", "rsync", "fd", "fzf"}
GREP_LIKE = {"grep", "egrep", "fgrep"}
REDIRECT_RE = re.compile(r"(?<![<&])\d?>{1,2}\|?\s*([^\s;&|<>]+)")
MUTATION_RE = re.compile(
    r"\btee\b|\bsed\s+(-[A-Za-z]*i|--in-place)|\bperl\s+-[A-Za-z]*i|"
    r"\b(rm|mv|cp|touch|truncate|mkdir|rmdir|ln|chmod|chown|chflags|dd|install|rsync|unlink|patch|"
    r"shred|xattr)\b|\bgit\s+(checkout|restore|rm|mv|clean|reset|stash|apply|am|pull|merge|revert|"
    r"cherry-pick|switch)\b|\.write\(|write_text|write_bytes|writeFile|os\.(remove|rename|replace|"
    r"unlink|rmdir|makedirs|mkdir)|shutil\.|\bopen\([^)]*['\"][wax+]"
)


def _segments(command):
    return [s for s in re.split(r"\|\||&&|[;|&\n]", command) if s.strip()]


def _tokens(segment):
    try:
        return shlex.split(segment, posix=True)
    except ValueError:
        return segment.split()


def _ancestor_of_agent(resolved):
    return resolved is not None and _within(AGENT_DIR, resolved)


def _glob_reaches_agent(arg, cwd):
    """A shell glob argument whose expansion could include .interface (or the Agent Module)."""
    if not re.search(r"[*?\[]", arg):
        return False
    base = _resolve(os.path.dirname(arg) or ".", cwd)
    name = os.path.basename(arg)
    if base == PROJECT_DIR and (fnmatch.fnmatch(".interface", name) or "**" in arg):
        return True
    if base == INTERFACE_DIR and fnmatch.fnmatch("agent", name):
        return True
    return _ancestor_of_agent(base) and "**" in arg


def _bash_recursive_reaches_agent(command, cwd):
    if _has_agent_exclusion(command):
        return False
    cur = cwd
    for seg in _segments(command):
        toks = _tokens(seg)
        while toks and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[0]):
            toks = toks[1:]
        if not toks:
            continue
        cmd = os.path.basename(toks[0])
        args = toks[1:]
        if cmd == "cd":
            target = next((a for a in args if not a.startswith("-")), os.path.expanduser("~"))
            cur = _resolve(target, cur) or cur
            continue
        if cmd in ("sudo", "command", "xargs", "env", "nice", "time"):
            toks = args
            if not toks:
                continue
            cmd, args = os.path.basename(toks[0]), toks[1:]
        recursive = False
        pattern_first = False
        if cmd in RECURSIVE_TOOLS:
            recursive = True
            pattern_first = cmd in ("rg", "ag", "ack", "fd")
        elif cmd in GREP_LIKE:
            recursive = any(re.match(r"^-[A-Za-z]*[rR]", a) or a in ("--recursive", "--dereference-recursive") for a in args) \
                or "-d" in args and "recurse" in args
            pattern_first = True
        elif cmd == "git" and args[:1] == ["grep"]:
            recursive, pattern_first, args = True, True, args[1:]
        elif cmd == "ls":
            recursive = any(re.match(r"^-[A-Za-z]*R", a) for a in args)
        elif cmd == "cp":
            recursive = any(re.match(r"^-[A-Za-z]*[rRa]", a) for a in args)
        elif cmd == "du":
            recursive = False
        if not recursive:
            continue
        positionals = []
        uses_e = any(a in ("-e", "-f", "--regexp", "--file") or a.startswith("--regexp=") for a in args)
        for a in args:
            if cmd == "find" and (a.startswith("-") or a in ("(", "!", ")")):
                break
            if a.startswith("-"):
                continue
            positionals.append(a)
        if pattern_first and positionals and not uses_e:
            positionals = positionals[1:]
        if not positionals:
            positionals = ["."]
        for p in positionals:
            if _glob_reaches_agent(p, cur):
                return True
            if _ancestor_of_agent(_resolve(p, cur)):
                return True
    return False


def _protected(path):
    return path is not None and _within(path, INTERFACE_DIR) and not _within(path, CONFIG_DIR)


def _mentions_protected(text):
    for m in re.finditer(r"\.interface(?=$|[/\s\"';&|)*])(/[^\s;&|<>\"')]*)?", text):
        if not re.match(r"^/+config(/|$)", m.group(1) or ""):
            return True
    return False


def _bash_mutates_interface(command, cwd):
    """Per command segment: a redirect into a protected Interface path, or a mutating
    command in a segment that names a protected Interface path or runs inside one."""
    cleaned = re.sub(r"\d?>&\d|&>\s*/dev/null", " ", command)
    cur = cwd
    for seg in _segments(cleaned):
        toks = _tokens(seg)
        if toks and toks[0] == "cd":
            target = next((a for a in toks[1:] if not a.startswith("-")), os.path.expanduser("~"))
            cur = _resolve(target, cur) or cur
            continue
        for target in REDIRECT_RE.findall(seg):
            if target != "/dev/null" and _protected(_resolve(target.strip("\"'"), cur)):
                return True
        rest = REDIRECT_RE.sub(" ", seg)
        if (_mentions_protected(rest) or _protected(cur)) and MUTATION_RE.search(rest):
            return True
    return False


# ----------------------------------------------------------------------------- handlers
def pre_tool_use(data):
    tool = data.get("tool_name") or ""
    ti = data.get("tool_input") or {}
    cwd = os.path.realpath(data.get("cwd") or PROJECT_DIR)
    in_subagent = bool(data.get("agent_id"))
    granted = (not in_subagent) and _load_grant(data.get("session_id")) is not None
    blob = json.dumps(ti)

    if GRANT_TOKEN in blob:
        _deny(GRANT_STATE_MSG)

    if tool == "Skill":
        name = str(ti.get("skill") or ti.get("command") or ti.get("name") or "")
        first = name.strip().lstrip("/").split()[0] if name.strip() else ""
        if first == SYNC_SKILL or first.endswith(":" + SYNC_SKILL):
            _deny(SYNC_INVOKE_MSG)
        return

    if tool in ("Edit", "Write", "NotebookEdit"):
        target = _resolve(ti.get("file_path") or ti.get("notebook_path"), cwd)
        if target and _within(target, INTERFACE_DIR) and not _within(target, CONFIG_DIR):
            _deny(MUTATION_MSG)
        return

    if tool == "Read":
        target = _resolve(ti.get("file_path"), cwd)
        if target and _within(target, AGENT_DIR) and not granted:
            _deny(AGENT_MSG)
        return

    if tool in ("Glob", "Grep"):
        if granted:
            return
        root = _resolve(ti.get("path") or cwd, cwd)
        if _within(root, AGENT_DIR):
            _deny(AGENT_MSG)
        pattern_field = ti.get("pattern") if tool == "Glob" else ti.get("glob")
        if pattern_field:
            if _mentions_agent(os.path.join(root, str(pattern_field))):
                _deny(AGENT_MSG)
        if tool == "Grep" and _ancestor_of_agent(root):
            rel = os.path.relpath(AGENT_DIR, root)
            if not pattern_field:
                updated = dict(ti)
                updated["glob"] = "!" + rel + "/**"
                _allow_with(updated, "interface-boundary-guard: excluded the protected Agent Module from this search.")
            excluded = str(pattern_field).rstrip("*/") in ("!" + rel, "!**/" + rel)
            if not (excluded or _has_agent_exclusion(str(pattern_field))):
                _deny(
                    AGENT_MSG + " This Grep searches a tree containing the Agent Module: narrow `path`, "
                    "or filter with `type` and set `glob` to '!" + rel + "/**'."
                )
        return

    if tool == "Bash":
        command = str(ti.get("command") or "")
        if _bash_mutates_interface(command, cwd):
            _deny(MUTATION_MSG)
        if granted:
            return
        stripped = _strip_exclusions(command)
        if _mentions_agent(stripped):
            _deny(AGENT_MSG)
        if re.search(r"\.interface\b", stripped) and re.search(r"(?<![\w.-])agent(?=/|\s|$|[\"'])", stripped):
            _deny(AGENT_MSG)
        if re.search(r"\.interface/+[^\s/;&|]*[*?\[]", stripped):
            _deny(AGENT_MSG + " (a glob under .interface/ could expand into the Agent Module)")
        if _bash_recursive_reaches_agent(command, cwd):
            _deny(
                AGENT_MSG + " This command scans a tree containing the Agent Module: narrow its path or "
                "exclude it (e.g. rg --glob '!.interface/agent/**', grep --exclude-dir=agent, "
                "find ... -not -path '*/.interface/agent/*')."
            )
        return


def grant(data):
    if data.get("agent_id"):
        raise RuntimeError("grant requested from a subagent")
    if SYNC_SKILL not in json.dumps(data):
        raise RuntimeError("expansion is not the Agent Native Sync invocation")
    _write_grant(data["session_id"], "pending")


def submit(data):
    session_id = data.get("session_id")
    current = _load_grant(session_id)
    if current is None:
        _revoke(session_id)
        return
    prompt = data.get("prompt")
    if current.get("state") == "pending" and (prompt is None or SYNC_SKILL in str(prompt)):
        _write_grant(session_id, "active")
    else:
        _revoke(session_id)


def revoke(data):
    _revoke(data.get("session_id"))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}
    if mode == "pre-tool-use":
        try:
            pre_tool_use(data)
        except SystemExit:
            raise
        except Exception as exc:  # fail_closed
            _deny("interface-boundary-guard failed (%s); blocking under fail_closed policy." % exc)
        return
    handler = {"grant": grant, "submit": submit, "revoke": revoke}.get(mode)
    if handler is None:
        print("interface_guard: unknown mode %r" % mode, file=sys.stderr)
        sys.exit(2)
    try:
        handler(data)
    except Exception as exc:
        print("agent-native-read-grant: %s failed (%s); failing closed." % (mode, exc), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
