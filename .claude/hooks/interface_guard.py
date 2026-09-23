#!/usr/bin/env python3
"""Agent Interface enforced guarantees for Claude Code.

Synchronized by Agent Native Sync (/my-interface-agent-native). This file is a Runtime
realization, not an authority.

Guarantees realized here (all fail closed):
  interface-boundary-guard (PreToolUse):
    - block Agent Module (.interface/agent/) reads outside the exact prompt created by the
      Human's direct /my-interface-agent-native invocation, and always inside subagents;
    - block every tool attempt to invoke Agent Native Sync;
    - block .interface/ mutations outside .interface/config/.
  agent-native-read-grant (UserPromptExpansion, revoked on UserPromptSubmit):
    - grant Agent Module reads only to the main session, bound to the prompt_id of the
      Human's /my-interface-agent-native expansion; the grant is never transferable.

Usage: interface_guard.py pretool | expansion | prompt-submit   (hook JSON on stdin)
"""

import glob
import hashlib
import json
import os
import re
import shlex
import sys
import tempfile
import time

SYNC_SKILL = "my-interface-agent-native"
BOUNDARY = "interface-boundary-guard"

GLOB_CHARS = re.compile(r"[*?\[{]")
PATH_TOKEN = re.compile(r"""[^\s'"`;|&<>()=,]*\.interface(?:/[^\s'"`;|&<>(),]*)?""")
SEGMENT_SPLIT = re.compile(r"\|\||&&|[;|\n]|\$\(|`")
REDIRECT = re.compile(r"(?:^|[^0-9&<>])(?:[0-9]?|&)>>?\|?\s*([^\s;|&<>]+)")

READ_ONLY_LISTING = {"ls", "stat", "test", "[", "file", "realpath", "readlink", "dirname", "basename", "cd", "pwd"}
MUTATING_ANY = {"rm", "rmdir", "unlink", "touch", "mkdir", "chmod", "chown", "chflags", "truncate",
                "tee", "ln", "patch", "mv", "shred", "xattr", "setfacl"}
MUTATING_DEST = {"cp", "rsync", "install", "ditto", "scp"}
GIT_MUTATING = {"checkout", "restore", "rm", "mv", "clean", "apply", "am", "stash", "reset", "switch"}
SEARCHERS = {"grep", "egrep", "fgrep", "rg", "ag", "ack", "rgrep"}
INTERPRETERS = re.compile(r"^(python[0-9.]*|node|perl|ruby|php|osascript|deno|bun|sh|bash|zsh|dash|ksh|fish)$")
WRITE_HINTS = re.compile(
    r"open\([^)]*['\"][wax+]|write_text|write_bytes|\.write\(|unlink|remove|rmtree|rename|replace\(|"
    r"mkdir|touch|shutil\.|os\.system|subprocess|writeFile|appendFile|fs\.|File\.write|>\s*\S"
)


# ----------------------------------------------------------------------------- helpers

def project_dir(event):
    return os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd())


def grant_file(project, session_id):
    key = hashlib.sha256(project.encode()).hexdigest()[:16]
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id or "no-session")
    folder = os.path.join(tempfile.gettempdir(), "claude-interface-grant", key)
    return folder, os.path.join(folder, safe + ".json")


def resolve(path, base):
    path = os.path.expanduser(os.path.expandvars(path))
    if not os.path.isabs(path):
        path = os.path.join(base, path)
    return os.path.realpath(path)


def inside(path, root):
    return path == root or path.startswith(root + os.sep)


class Layout:
    def __init__(self, project):
        self.project = project
        self.interface = os.path.join(project, ".interface")
        self.agent = os.path.join(self.interface, "agent")
        self.config = os.path.join(self.interface, "config")

    def is_agent(self, p):
        return inside(p, self.agent)

    def is_agent_ancestor(self, p):
        return p != self.agent and inside(self.agent, p)

    def is_protected(self, p):
        return inside(p, self.interface) and not inside(p, self.config)


def has_grant(event, layout):
    """True only in the main session, within the prompt the Human's Sync invocation created."""
    if event.get("agent_id"):
        return False
    _, path = grant_file(layout.project, event.get("session_id"))
    try:
        with open(path) as fh:
            grant = json.load(fh)
    except (OSError, ValueError):
        return False
    if grant.get("session_id") != event.get("session_id"):
        return False
    granted_prompt, current_prompt = grant.get("prompt_id"), event.get("prompt_id")
    if granted_prompt and current_prompt:
        return granted_prompt == current_prompt
    # Runtime omitted prompt_id: fall back to the session grant, which UserPromptSubmit revokes.
    return True


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"[{BOUNDARY}] {reason}",
        }
    }))
    sys.exit(0)


AGENT_READ_MSG = (
    "Agent Module sources (.interface/agent/) are readable only within the prompt created by the "
    "Human's direct /my-interface-agent-native invocation, and never from a subagent. Use the "
    "synchronized Runtime artifacts (.claude/rules, .claude/skills, settings) instead; if one is "
    "missing, report Runtime drift and ask the Human to run /my-interface-agent-native."
)
MUTATION_MSG = (
    "The .interface/ tree is read-only to every Agent Instance and Skill; only records inside "
    ".interface/config/ may change, under the owning Component's rules. Report the needed change "
    "for direct Human authorship instead."
)
SYNC_INVOKE_MSG = (
    "Agent Native Sync can be started only by the Human typing /my-interface-agent-native. No "
    "model, Skill, Agent Instance, hook, or automation may invoke it."
)


# ----------------------------------------------------------------------------- tool checks

def check_file_tool(tool, inp, event, layout, base):
    if tool in ("Read",):
        paths = [inp.get("file_path")]
        writes = False
    elif tool in ("Edit", "Write", "MultiEdit"):
        paths = [inp.get("file_path")]
        writes = True
    elif tool == "NotebookEdit":
        paths = [inp.get("notebook_path") or inp.get("file_path")]
        writes = True
    else:
        return
    for raw in paths:
        if not raw:
            continue
        p = resolve(raw, base)
        if writes and layout.is_protected(p):
            deny(MUTATION_MSG + f" Target: {raw}")
        if layout.is_agent(p) and not has_grant(event, layout):
            deny(AGENT_READ_MSG)


def glob_regex(pattern):
    out, i = "", 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
            continue
        if pattern.startswith("**", i):
            out, i = out + ".*", i + 2
            continue
        if c == "*":
            out += "[^/]*"
        elif c == "?":
            out += "[^/]"
        elif c == "{":
            end = pattern.find("}", i)
            if end < 0:
                out += re.escape(c)
            else:
                out += "(?:" + "|".join(glob_regex(p) for p in pattern[i + 1:end].split(",")) + ")"
                i = end
        elif c == "[":
            end = pattern.find("]", i)
            out += pattern[i:end + 1] if end > 0 else re.escape(c)
            i = end if end > 0 else i
        else:
            out += re.escape(c)
        i += 1
    return out


def glob_reaches_agent(pattern, root, layout):
    """Whether a Glob pattern rooted at `root` can match the Agent Module or anything inside it."""
    rx = re.compile(glob_regex(pattern) + r"\Z")
    candidates = [layout.agent]
    for folder, _, files in os.walk(layout.agent):
        candidates.append(folder)
        candidates.extend(os.path.join(folder, f) for f in files)
    return any(rx.match(os.path.relpath(c, root)) for c in candidates)


def check_search_tool(tool, inp, event, layout, base):
    root = resolve(inp.get("path") or base, base)
    text = " ".join(str(inp.get(k) or "") for k in ("pattern", "glob", "path"))
    if has_grant(event, layout):
        return
    if layout.is_agent(root) or "interface/agent" in text:
        deny(AGENT_READ_MSG)
    if tool == "Glob":
        if layout.is_agent_ancestor(root) and glob_reaches_agent(inp.get("pattern") or "", root, layout):
            deny(AGENT_READ_MSG + " Narrow the Glob so it cannot match inside .interface/agent/.")
        return
    if layout.is_agent_ancestor(root):
        deny(AGENT_READ_MSG + " This content search would descend into .interface/agent/; search a "
             "narrower path that excludes it.")


def check_skill_tool(inp):
    for value in inp.values():
        if isinstance(value, str):
            name = value.strip().lstrip("/").split()[0] if value.strip() else ""
            if name.split(":")[-1] == SYNC_SKILL:
                deny(SYNC_INVOKE_MSG)


# ----------------------------------------------------------------------------- Bash

def split_tokens(segment):
    try:
        return shlex.split(segment, posix=True)
    except ValueError:
        return segment.split()


def expand_token(token, base, layout):
    """Resolve a shell word to real paths, expanding globs the way the shell would."""
    p = resolve(token, base)
    if GLOB_CHARS.search(token):
        hits = glob.glob(p, recursive=True)
        if "{" in token:
            inner = re.findall(r"\{([^}]*)\}", token)
            for group in inner:
                for alt in group.split(","):
                    hits += glob.glob(resolve(re.sub(r"\{[^}]*\}", alt, token, count=1), base), recursive=True)
        return [os.path.realpath(h) for h in hits[:5000]] or [p]
    return [p]


def verb_of(tokens):
    for i, tok in enumerate(tokens):
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tok):
            continue
        if tok in ("sudo", "command", "exec", "nohup", "time", "env", "xargs", "nice"):
            continue
        return os.path.basename(tok), tokens[i + 1:]
    return "", []


SEARCH_VALUE_OPTS = {
    "-g", "--glob", "--iglob", "-t", "--type", "-T", "--type-not", "-e", "--regexp", "-f", "--file",
    "-m", "--max-count", "-A", "-B", "-C", "--after-context", "--before-context", "--context",
    "-j", "--threads", "--exclude-dir", "--exclude", "--include", "--ignore-dir", "--sort", "--sortr",
    "-M", "--max-columns", "--max-depth", "-d", "--color", "--colors", "-E", "--encoding", "--pre",
    "--pre-glob", "--type-add", "--ignore-file", "--path-separator", "-D", "--devices", "--label",
}
# Exclusions of the Agent Module are not reads of it.
EXCLUSION_ARG = re.compile(
    r"""(?:--exclude-dir|--exclude|--ignore-dir)(?:=|\s+)['"]?[^\s'"]*['"]?"""
    r"""|(?:--glob|--iglob|-g)(?:=|\s+)['"]?![^\s'"]*['"]?"""
)


def search_roots(verb, args, cwd):
    """Positional search roots of grep/rg-style commands, skipping option values and the pattern."""
    positional, pattern_by_flag, skip = [], False, False
    for a in args:
        if skip:
            skip = False
            continue
        if a == "--":
            continue
        if a.startswith("-"):
            name = a.split("=", 1)[0]
            if name in ("-e", "--regexp", "-f", "--file"):
                pattern_by_flag = True
            if (name in SEARCH_VALUE_OPTS or (verb == "rg" and name in ("-r", "--replace"))) and "=" not in a:
                skip = True
            continue
        positional.append(a)
    if not pattern_by_flag:
        positional = positional[1:]
    return [resolve(a, cwd) for a in positional] or [cwd]


def check_bash(command, event, layout, base):
    granted = has_grant(event, layout)

    if not granted and re.search(r"interface/+agent", EXCLUSION_ARG.sub(" ", command), re.I):
        deny(AGENT_READ_MSG)

    cwd = base
    entered_protected = False
    for segment in SEGMENT_SPLIT.split(command):
        segment = segment.strip()
        if not segment:
            continue
        tokens = split_tokens(segment)
        verb, args = verb_of(tokens)
        operands = [a for a in args if not a.startswith("-")]
        resolved = []
        for a in operands:
            if ".interface" in a or GLOB_CHARS.search(a) or a in (".", "..") or a.startswith("/"):
                resolved.extend(expand_token(a, cwd, layout))
            else:
                resolved.append(resolve(a, cwd))

        # Agent Module reads (explicit paths, globs, or ancestors of .interface/agent)
        if not granted:
            if any(layout.is_agent(p) for p in resolved):
                deny(AGENT_READ_MSG)
            if verb in SEARCHERS or (verb == "git" and args[:1] == ["grep"]):
                recursive = (verb not in ("grep", "egrep", "fgrep")) or any(
                    re.match(r"^-[A-Za-z]*[rR]|^--(recursive|dereference-recursive)$", a) for a in args)
                roots = search_roots(verb, args[1:] if verb == "git" else args, cwd)
                excluded = any("agent" in m or m.rstrip("'\"/").endswith(".interface")
                               for m in EXCLUSION_ARG.findall(segment))
                if recursive and not excluded and any(layout.is_agent_ancestor(r) for r in roots):
                    deny(AGENT_READ_MSG + " This recursive search would read .interface/agent/; exclude it "
                         "(for example rg --glob '!.interface/agent/**' or grep --exclude-dir=agent) or "
                         "search a narrower path.")
            elif verb not in READ_ONLY_LISTING and any(
                p == layout.interface for p in resolved
            ):
                deny(AGENT_READ_MSG + " Operating on the whole .interface/ tree would include .interface/agent/.")

        # Interface mutations outside .interface/config/
        for target in REDIRECT.findall(segment):
            for p in expand_token(target.strip("'\""), cwd, layout):
                if layout.is_protected(p):
                    deny(MUTATION_MSG + f" Redirect target: {target}")
        protected = [p for p in resolved if layout.is_protected(p)]
        if verb in MUTATING_ANY and protected:
            deny(MUTATION_MSG)
        if verb == "sed" and any(re.match(r"^(-[A-Za-z]*i|--in-place)", a) for a in args) and protected:
            deny(MUTATION_MSG)
        if verb == "perl" and any(re.match(r"^-[A-Za-z]*i", a) for a in args) and protected:
            deny(MUTATION_MSG)
        if verb in MUTATING_DEST and operands and layout.is_protected(resolve(operands[-1], cwd)):
            deny(MUTATION_MSG)
        if verb == "dd" and any(a.startswith("of=") and layout.is_protected(resolve(a[3:], cwd)) for a in args):
            deny(MUTATION_MSG)
        if verb == "find" and protected and re.search(r"-delete|-exec\s+(rm|mv|sed|perl|tee|truncate)", segment):
            deny(MUTATION_MSG)
        if verb == "git" and args and args[0] in GIT_MUTATING and protected:
            deny(MUTATION_MSG)
        if INTERPRETERS.match(verb or ""):
            if entered_protected and WRITE_HINTS.search(command):
                deny(MUTATION_MSG + " (inline code runs inside a protected .interface/ path)")
            # A write hint on the same code line as a protected path literal is treated as a mutation.
            for line in re.split(r"[\n;]", command):
                if WRITE_HINTS.search(line) and any(
                    layout.is_protected(resolve(t, cwd)) for t in PATH_TOKEN.findall(line)
                ):
                    deny(MUTATION_MSG + " Inline code writes near a protected .interface/ path.")
        if (entered_protected and (verb in MUTATING_ANY | MUTATING_DEST or verb == "dd"
                                   or REDIRECT.search(segment))):
            deny(MUTATION_MSG + " (working directory is inside a protected .interface/ path)")

        if verb == "cd":
            cwd = resolve(operands[0], cwd) if operands else os.path.expanduser("~")
            entered_protected = layout.is_protected(cwd)
            if layout.is_agent(cwd) and not granted:
                deny(AGENT_READ_MSG)


# ----------------------------------------------------------------------------- modes

def mode_pretool(event):
    layout = Layout(project_dir(event))
    base = os.path.realpath(event.get("cwd") or layout.project)
    tool = event.get("tool_name") or ""
    inp = event.get("tool_input") or {}
    if tool == "Skill":
        check_skill_tool(inp)
    elif tool in ("Read", "Edit", "Write", "MultiEdit", "NotebookEdit"):
        check_file_tool(tool, inp, event, layout, base)
    elif tool in ("Glob", "Grep"):
        check_search_tool(tool, inp, event, layout, base)
    elif tool == "Bash":
        check_bash(inp.get("command") or "", event, layout, base)
    sys.exit(0)


def mode_expansion(event):
    if event.get("agent_id") or event.get("expansion_type", "slash_command") != "slash_command":
        sys.exit(0)
    if (event.get("command_name") or "").split(":")[-1].lstrip("/") != SYNC_SKILL:
        sys.exit(0)
    project = project_dir(event)
    folder, path = grant_file(project, event.get("session_id"))
    os.makedirs(folder, mode=0o700, exist_ok=True)
    with open(path, "w") as fh:
        json.dump({"session_id": event.get("session_id"), "prompt_id": event.get("prompt_id"),
                   "granted_at": time.time()}, fh)
    sys.exit(0)


def mode_prompt_submit(event):
    _, path = grant_file(project_dir(event), event.get("session_id"))
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
    sys.exit(0)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        event = json.load(sys.stdin)
        {"pretool": mode_pretool, "expansion": mode_expansion,
         "prompt-submit": mode_prompt_submit}[mode](event)
    except SystemExit:
        raise
    except Exception as exc:  # fail closed and visible
        print(f"[{BOUNDARY}] guard failure in mode '{mode}' ({type(exc).__name__}: {exc}); "
              "blocking by fail-closed policy.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
