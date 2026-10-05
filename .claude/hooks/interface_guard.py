#!/usr/bin/env python3
"""Enforced Guarantees for the Agent Interface boundary.

Synchronized Native realization of two Permission guarantees:

- interface-boundary-guard (PreToolUse, fail_closed, blocking): blocks Agent Module
  reads outside the exact prompt created by the Human's direct invocation of
  /my-interface-agent-native, blocks every non-Human attempt to invoke that Skill,
  and blocks every Interface mutation.
- agent-native-read-grant (UserPromptExpansion, fail_closed): binds the Agent Module
  read grant to the session and prompt that the Human's direct /my-interface-agent-native
  invocation created. The grant is never transferable to a subagent or a later prompt.

Modes: `pre-tool-use` and `grant`. Any internal failure exits 2 (blocking).
"""

import json
import os
import re
import shlex
import sys
import time

SYNC_SKILL = "my-interface-agent-native"
GRANT_TTL_SECONDS = 24 * 60 * 60

AGENT_RE = re.compile(r"(^|/)\.interface/agent(/|$)")
INTERFACE_RE = re.compile(r"(^|/)\.interface(/|$)")

# Text-level indicators that a command addresses the Agent Module.
AGENT_TEXT_RE = re.compile(r"interface/+agent\b|\.interface/+(\*|\?|\[|\{|a\*|ag\*|age\*|agen\*)")
CD_INTO_INTERFACE_THEN_AGENT_RE = re.compile(
    r"\bcd\s+['\"]?[^;&|\n]*\.interface/?['\"]?\s*(;|&&|\|\||\n)[\s\S]*(?<![\w.-])agent(?![\w-])"
)
# Exclusion constructs that mention the Agent Module only to keep it out of scope.
EXCLUSION_RE = re.compile(
    r"--exclude-dir[= ]\S+|--exclude[= ]\S+|(?:-g|--glob|--iglob)[= ]['\"]?!\S+"
    r"|(?:-not|!)\s+-(?:path|name|wholename)\s+\S+|:\(exclude\)\S+|:!\S+"
)

SEPARATORS = {";", "&&", "||", "|", "&", "\n", "|&", ";;", "(", ")"}
REDIRECTS = {">", ">>", ">|", "&>", "&>>", "<>"}
MUTATORS = {
    "rm", "rmdir", "mv", "touch", "mkdir", "truncate", "tee", "unlink", "shred",
    "chmod", "chown", "chgrp", "patch", "trash", "srm",
}
DEST_MUTATORS = {"cp", "rsync", "install", "ln", "ditto"}
INPLACE_EDITORS = {"sed", "gsed", "perl", "ruby"}
GIT_MUTATING = {"rm", "mv", "checkout", "restore", "clean", "reset", "stash", "apply", "am"}
INTERPRETERS = {"python", "python3", "node", "perl", "ruby", "bash", "sh", "zsh", "deno", "bun"}
WRITE_HINT_RE = re.compile(
    r"open\([^)]*['\"][wax]|\.write|write_text|write_bytes|writeFile|appendFile|unlink|"
    r"remove\(|rmtree|rename|mkdir|touch|shutil\.|os\.replace|>\s*['\"]?\S*\.interface"
)
PREFIX_WORDS = {"sudo", "command", "builtin", "exec", "nohup", "time", "env", "xargs", "nice"}
SEARCH_TOOLS = {"rg", "ag", "ack", "grep", "egrep", "fgrep", "ggrep"}
RG_VALUE_FLAGS = set("efgtTmABCMjEr")
GREP_VALUE_FLAGS = set("efmABCdD")
LONG_VALUE_FLAGS = {
    "--glob", "--iglob", "--type", "--type-not", "--max-count", "--regexp", "--file",
    "--include", "--exclude", "--exclude-dir", "--context", "--after-context",
    "--before-context", "--max-depth", "--encoding", "--replace", "--type-add",
    "--ignore-file", "--pre", "--sort", "--sortr", "--threads", "--color", "--colors",
}


class Deny(Exception):
    pass


def project_dir(data):
    return os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())


def state_dir(data):
    return os.path.join(project_dir(data), ".claude", "hooks", "state")


def log_event(data, event, decision, code):
    """Append a non-content audit line so guarantee outcomes stay observable."""
    try:
        os.makedirs(state_dir(data), exist_ok=True)
        entry = {
            "at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "event": event,
            "tool": data.get("tool_name") or data.get("command_name"),
            "subagent": bool(data.get("agent_id")),
            "prompt_id_present": bool(data.get("prompt_id")),
            "decision": decision,
            "code": code,
        }
        with open(os.path.join(state_dir(data), "guard.log"), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def resolve(path, cwd):
    path = os.path.expanduser(str(path).strip().strip("'\""))
    if not os.path.isabs(path):
        path = os.path.join(cwd, path)
    return os.path.abspath(path), os.path.realpath(path)


def any_form(path, cwd, predicate):
    return any(predicate(p) for p in resolve(path, cwd))


def is_agent(p):
    return bool(AGENT_RE.search(p))


def is_protected_interface(p):
    return bool(INTERFACE_RE.search(p))


def contains_agent(scope, data):
    """True when a directory scope is, or recursively contains, the Agent Module."""
    agent_dir = os.path.join(project_dir(data), ".interface", "agent")
    scope = scope.rstrip("/") or "/"
    return is_agent(scope) or agent_dir.startswith(scope + "/") or scope == "/"


def guard_paths(data):
    hooks = os.path.join(project_dir(data), ".claude", "hooks")
    return os.path.join(hooks, "state"), os.path.join(hooks, "interface_guard.py")


def is_grant_state(p, data):
    state, _ = guard_paths(data)
    return p == state or p.startswith(state + "/")


def is_guard_script(p, data):
    return p == guard_paths(data)[1]


def grant_file(data):
    session = re.sub(r"[^A-Za-z0-9_-]", "_", str(data.get("session_id") or ""))
    return os.path.join(state_dir(data), f"agent-native-grant-{session}.json")


def grant_valid(data):
    """The grant holds only in the main thread of the exact granted prompt."""
    if data.get("agent_id"):
        return False
    session, prompt = data.get("session_id"), data.get("prompt_id")
    if not session or not prompt:
        return False
    try:
        with open(grant_file(data), encoding="utf-8") as fh:
            grant = json.load(fh)
    except (OSError, ValueError):
        return False
    return grant.get("session_id") == session and grant.get("prompt_id") == prompt


AGENT_DENY = (
    "interface-boundary-guard: the Agent Module (.interface/agent/) may be read only within the exact "
    "prompt created by the Human's direct /my-interface-agent-native invocation, and never by a subagent. "
    "Use the synchronized Native realization (.claude/rules, .claude/skills, .claude/settings.json). "
    "If a required Native capability is missing, report Runtime drift and ask the Human to run "
    "/my-interface-agent-native."
)
MUTATION_DENY = (
    "interface-boundary-guard: .interface/ is read-only to every Agent Instance and Skill. "
    "Operational records live in config/ at the project root. Report the needed change for direct "
    "Human authorship instead."
)
SYNC_INVOKE_DENY = (
    "interface-boundary-guard: /my-interface-agent-native can be started only by the Human typing it "
    "directly. No Agent, Skill, subagent, hook, or automation may invoke it."
)
GRANT_STATE_DENY = "interface-boundary-guard: the Agent Native Sync grant state is managed only by its hook."
GUARD_SCRIPT_DENY = (
    "interface-boundary-guard: the enforcement script changes only through /my-interface-agent-native."
)


def check_mutation_target(path, cwd, data, granted):
    for p in resolve(path, cwd):
        if is_protected_interface(p):
            raise Deny(MUTATION_DENY)
        if is_grant_state(p, data):
            raise Deny(GRANT_STATE_DENY)
        if is_guard_script(p, data) and not granted:
            raise Deny(GUARD_SCRIPT_DENY)


def check_file_tool(tool, tool_input, cwd, data, granted):
    if tool == "Read":
        path = tool_input.get("file_path") or ""
        if path and any_form(path, cwd, is_agent) and not granted:
            raise Deny(AGENT_DENY)
        return
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if path:
        check_mutation_target(path, cwd, data, granted)


def check_search_tool(tool, tool_input, cwd, data, granted):
    if granted:
        return
    scope = tool_input.get("path") or cwd
    text = " ".join(str(tool_input.get(k) or "") for k in ("pattern", "glob", "path"))
    if AGENT_TEXT_RE.search(text) or any_form(scope, cwd, is_agent):
        raise Deny(AGENT_DENY)
    if tool == "Grep" and any(contains_agent(p, data) for p in resolve(scope, cwd)):
        raise Deny(
            AGENT_DENY + " This Grep scope contains .interface/agent/; search a narrower path that excludes it."
        )


def tokenize(command):
    command = command.replace("\r", " ").replace("\n", " ; ")
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|<>()")
    lexer.whitespace_split = True
    lexer.commenters = ""
    tokens = []
    for tok in lexer:
        tokens.append(tok)
    return tokens


def split_commands(tokens):
    commands, current = [], []
    for tok in tokens:
        if tok in SEPARATORS:
            if current:
                commands.append(current)
            current = []
        else:
            current.append(tok)
    if current:
        commands.append(current)
    return commands


def strip_prefix(words):
    i = 0
    while i < len(words) and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[i]) or words[i] in PREFIX_WORDS):
        i += 1
        while i < len(words) and words[i].startswith("-") and words[i - 1] in {"env", "nice", "xargs", "sudo"}:
            i += 1
    return words[i:]


def positional(words, value_short, value_long):
    """Positional arguments after the command name, skipping flags and their values."""
    out, i, explicit_pattern = [], 1, False
    while i < len(words):
        w = words[i]
        if w == "--":
            out.extend(words[i + 1:])
            break
        if w.startswith("--"):
            name = w.split("=", 1)[0]
            if name in ("--regexp", "--file"):
                explicit_pattern = True
            if "=" not in w and name in value_long:
                i += 1
        elif w.startswith("-") and len(w) > 1:
            flags = w[1:]
            for j, ch in enumerate(flags):
                if ch in ("e", "f") and ch in value_short:
                    explicit_pattern = True
                if ch in value_short:
                    if j == len(flags) - 1:
                        i += 1
                    break
        else:
            out.append(w)
        i += 1
    return out, explicit_pattern


def search_scopes(words, cwd):
    """Resolved search scopes of a recursive content search, or None when not one."""
    name = os.path.basename(words[0])
    if name == "git" and len(words) > 1 and words[1] == "grep":
        args, _ = positional(words[1:], GREP_VALUE_FLAGS, LONG_VALUE_FLAGS)
        paths = [a for a in args[1:] if not a.startswith(":")]
        return [resolve(p, cwd)[1] for p in paths] or [cwd]
    if name not in SEARCH_TOOLS:
        return None
    if name in ("grep", "egrep", "fgrep", "ggrep"):
        flags = [w for w in words[1:] if w.startswith("-")]
        recursive = any(
            f in ("--recursive", "--dereference-recursive", "-d", "--directories=recurse")
            or (not f.startswith("--") and ("r" in f[1:] or "R" in f[1:]))
            for f in flags
        )
        if not recursive:
            return None
        value_short = GREP_VALUE_FLAGS
    else:
        value_short = RG_VALUE_FLAGS
    args, explicit = positional(words, value_short, LONG_VALUE_FLAGS)
    paths = args if explicit else args[1:]
    return [resolve(p, cwd)[1] for p in paths] or [cwd]


def check_bash(command, cwd, data, granted):
    residual = EXCLUSION_RE.sub(" ", command)
    if not granted and (AGENT_TEXT_RE.search(residual) or CD_INTO_INTERFACE_THEN_AGENT_RE.search(residual)):
        raise Deny(AGENT_DENY)
    if "hooks/state" in command and ".claude" in command:
        if re.search(r"agent-native-grant|>|\b(rm|mv|cp|tee|touch|truncate|ln|sed|python3?|perl)\b", command):
            raise Deny(GRANT_STATE_DENY)

    try:
        tokens = tokenize(command)
    except ValueError:
        # Unbalanced quoting cannot be analysed safely; fail closed only when it touches a guarded area.
        if ".interface" in command or "hooks/state" in command or "interface_guard" in command:
            raise Deny(MUTATION_DENY)
        return

    # Redirection targets.
    for i, tok in enumerate(tokens[:-1]):
        if tok in REDIRECTS or (tok.endswith(">") and set(tok) <= set("0123456789&>|")):
            nxt = tokens[i + 1]
            if nxt not in SEPARATORS and nxt not in REDIRECTS and not nxt.startswith("&"):
                check_mutation_target(nxt, cwd, data, granted)

    eff_cwd = cwd
    for words in split_commands(tokens):
        words = [w for w in words if w not in REDIRECTS]
        words = strip_prefix(words)
        if not words:
            continue
        name = os.path.basename(words[0])

        if name == "cd":
            target = words[1] if len(words) > 1 else os.path.expanduser("~")
            eff_cwd = resolve(target, eff_cwd)[1]
            continue

        scopes = search_scopes(words, eff_cwd)
        if scopes is not None and not granted:
            if not EXCLUSION_RE.search(" ".join(words)) and any(contains_agent(s, data) for s in scopes):
                raise Deny(
                    AGENT_DENY + " This recursive search scope contains .interface/agent/; "
                    "search a narrower path or exclude .interface/."
                )

        if name == "find" and not granted:
            find_paths = [w for w in words[1:] if not w.startswith("-") and w not in ("!", "(", ")")][:1]
            reads_contents = any(w in ("-exec", "-execdir", "-ok", "-okdir") for w in words)
            if reads_contents and any(contains_agent(resolve(p, eff_cwd)[1], data) for p in (find_paths or ["."])):
                if not EXCLUSION_RE.search(" ".join(words)):
                    raise Deny(AGENT_DENY + " This find -exec scope contains .interface/agent/.")
        if name == "find" and "-delete" in words:
            for p in [w for w in words[1:] if not w.startswith("-")][:1]:
                check_mutation_target(p, eff_cwd, data, granted)

        args = [w for w in words[1:] if not w.startswith("-")]
        if name in MUTATORS:
            for a in args:
                check_mutation_target(a, eff_cwd, data, granted)
        elif name in DEST_MUTATORS and args:
            check_mutation_target(args[-1], eff_cwd, data, granted)
        elif name in INPLACE_EDITORS and any(w.startswith("-i") or w == "--in-place" for w in words[1:]):
            for a in args:
                check_mutation_target(a, eff_cwd, data, granted)
        elif name == "dd":
            for w in words[1:]:
                if w.startswith("of="):
                    check_mutation_target(w[3:], eff_cwd, data, granted)
        elif name == "git" and len(words) > 1 and words[1] in GIT_MUTATING:
            for a in [w for w in words[2:] if not w.startswith("-")]:
                if any_form(a, eff_cwd, lambda p: INTERFACE_RE.search(p) is not None):
                    check_mutation_target(a, eff_cwd, data, granted)
        elif name in INTERPRETERS:
            segment = " ".join(words)
            mentions = re.findall(r"[^\s'\"()\[\],;]*\.interface(?:/[^\s'\"()\[\],;]*)?", command)
            protected = [m for m in mentions if any_form(m, eff_cwd, is_protected_interface)]
            if protected and (WRITE_HINT_RE.search(command) or WRITE_HINT_RE.search(segment)):
                raise Deny(MUTATION_DENY)


def pre_tool_use(data):
    tool = data.get("tool_name") or ""
    tool_input = data.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        raise ValueError("tool_input is not an object")
    cwd = os.path.realpath(data.get("cwd") or project_dir(data))
    granted = grant_valid(data)

    if tool in ("Skill", "SlashCommand"):
        names = " ".join(str(tool_input.get(k) or "") for k in ("skill", "command", "name"))
        if SYNC_SKILL in names or SYNC_SKILL in json.dumps(tool_input):
            raise Deny(SYNC_INVOKE_DENY)
        return
    if tool in ("Read", "Edit", "Write", "NotebookEdit", "MultiEdit"):
        check_file_tool(tool, tool_input, cwd, data, granted)
        return
    if tool in ("Glob", "Grep"):
        check_search_tool(tool, tool_input, cwd, data, granted)
        return
    if tool == "Bash":
        check_bash(str(tool_input.get("command") or ""), cwd, data, granted)


def grant(data):
    def block(reason):
        log_event(data, "UserPromptExpansion", "block", "grant_refused")
        print(json.dumps({"decision": "block", "reason": reason}))
        sys.exit(0)

    if data.get("command_name") != SYNC_SKILL:
        return
    if data.get("agent_id"):
        block("agent-native-read-grant: a subagent cannot create the Agent Native Sync grant.")
    if data.get("expansion_type") not in (None, "slash_command"):
        block("agent-native-read-grant: only the Human's typed /my-interface-agent-native creates the grant.")
    if not data.get("session_id") or not data.get("prompt_id"):
        block(
            "agent-native-read-grant: Claude Code did not supply session_id and prompt_id, so the Agent "
            "Module read grant cannot be bound to this exact prompt (fail closed). Update Claude Code; the "
            "Human may review the hooks in .claude/settings.json directly."
        )
    os.makedirs(state_dir(data), exist_ok=True)
    now = time.time()
    for name in os.listdir(state_dir(data)):
        path = os.path.join(state_dir(data), name)
        if name.startswith("agent-native-grant-") and now - os.path.getmtime(path) > GRANT_TTL_SECONDS:
            os.remove(path)
    record = {"session_id": data["session_id"], "prompt_id": data["prompt_id"], "granted_at": int(now)}
    tmp = grant_file(data) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(record, fh)
    os.replace(tmp, grant_file(data))
    log_event(data, "UserPromptExpansion", "grant", "granted")
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptExpansion",
            "additionalContext": (
                "agent-native-read-grant: Agent Module read access is granted to this prompt's main thread "
                "only. It is not transferable to subagents and ends with this prompt."
            ),
        }
    }))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
        if not isinstance(data, dict):
            raise ValueError("hook input is not an object")
        if mode == "pre-tool-use":
            try:
                pre_tool_use(data)
            except Deny as deny:
                log_event(data, "PreToolUse", "deny", str(deny).split(":", 1)[0])
                print(json.dumps({
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": str(deny),
                    }
                }))
        elif mode == "grant":
            grant(data)
        else:
            raise ValueError(f"unknown mode {mode!r}")
    except SystemExit:
        raise
    except Exception as exc:  # fail closed: security and integrity controls
        print(f"interface guard failed closed ({mode}): {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
