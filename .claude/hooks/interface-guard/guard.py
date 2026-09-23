#!/usr/bin/env python3
"""Interface boundary guard — Claude Code realization of two Enforced Guarantees.

interface-boundary-guard (PreToolUse, fail_closed):
    Blocks Agent Module reads (.interface/agent/) outside the exact prompt the Human
    created by typing /my-interface-agent-native, blocks every non-Human attempt to
    invoke Agent Native Sync, and blocks Interface mutations outside .interface/config/.

agent-native-read-grant (UserPromptSubmit + UserPromptExpansion, fail_closed):
    Grants Agent Module reads only to the main thread of the prompt the Human typed as
    /my-interface-agent-native. UserPromptSubmit never fires for scheduled, looped, or
    remote prompts, so a grant needs both the typed prompt and its expansion. Subagents
    (agent_id present) never inherit it. Stop and SessionEnd revoke it.

Synchronized by /my-interface-agent-native. Do not edit by hand.

Usage: guard.py pre-tool-use | prompt-submit | prompt-expansion | revoke   (hook JSON on stdin)
"""

import json
import os
import re
import shlex
import sys
import time

SYNC_NAME = "my-interface-agent-native"
GUARD_DIR = os.path.dirname(os.path.realpath(__file__))
STATE_DIR = os.path.join(GUARD_DIR, "state")
GRANT_MAX_AGE_S = 12 * 3600

AGENT_MSG = (
    "interface-boundary-guard: the Agent Module (.interface/agent/) is readable only within the "
    "prompt the Human creates by typing /my-interface-agent-native, and never from a subagent. "
    "Use the synchronized Native artifacts (.claude/rules, .claude/skills, .claude/settings.json). "
    "If one is missing or unusable, report Runtime drift and ask the Human to run "
    "/my-interface-agent-native. For searches, scope the path to a directory that does not "
    "contain .interface/agent/ or exclude it explicitly."
)
MUTATION_MSG = (
    "interface-boundary-guard: .interface/ is read-only; only files inside .interface/config/ "
    "may be changed. Report the needed change for direct Human authorship instead."
)
SYNC_INVOKE_MSG = (
    "interface-boundary-guard: Agent Native Sync (/my-interface-agent-native) may be invoked only "
    "by the Human typing it directly. No Agent, Skill, subagent, schedule, or automation may "
    "invoke, chain, or simulate it."
)
TAMPER_MSG = (
    "interface-boundary-guard: the guard and its grant state are changed only by "
    "/my-interface-agent-native within the Human's own invocation."
)
FAILURE_MSG = "interface-boundary-guard: guard failed ({}); blocking (fail_closed)."


# ----------------------------------------------------------------------------- output

def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))
    sys.stderr.write(reason + "\n")
    sys.exit(2)


def allow():
    sys.exit(0)


# ----------------------------------------------------------------------------- grant state

def _safe(value):
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(value or "none"))[:128]


def _grant_path(session_id):
    return os.path.join(STATE_DIR, "grant-" + _safe(session_id) + ".json")


def _pending_path(session_id):
    return os.path.join(STATE_DIR, "pending-" + _safe(session_id) + ".json")


def _remove(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def _write_json(path, data):
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(data, fh)
    os.replace(tmp, path)


def _read_json(path):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (FileNotFoundError, ValueError):
        return None


def revoke(data):
    sid = data.get("session_id")
    _remove(_grant_path(sid))
    _remove(_pending_path(sid))


def prompt_submit(data):
    """Every Human prompt ends any earlier grant; only a typed sync command opens a pending one."""
    revoke(data)
    prompt = data.get("prompt") or ""
    if re.match(r"^\s*/" + re.escape(SYNC_NAME) + r"(\s|$)", prompt):
        _write_json(_pending_path(data.get("session_id")), {
            "prompt_id": data.get("prompt_id"),
            "at": time.time(),
        })


def prompt_expansion(data):
    """The typed command's expansion turns the pending grant into the prompt's grant."""
    sid = data.get("session_id")
    pending = _read_json(_pending_path(sid))
    _remove(_pending_path(sid))
    name = (data.get("command_name") or "").split(":")[-1].lstrip("/")
    if pending is None or name != SYNC_NAME:
        return
    if pending.get("prompt_id") and data.get("prompt_id") and pending["prompt_id"] != data["prompt_id"]:
        return
    if time.time() - float(pending.get("at", 0)) > 600:
        return
    _write_json(_grant_path(sid), {
        "prompt_id": pending.get("prompt_id") or data.get("prompt_id"),
        "at": time.time(),
    })


def granted(data):
    """True only on the main thread of the exact prompt that holds the grant."""
    if data.get("agent_id"):
        return False
    grant = _read_json(_grant_path(data.get("session_id")))
    if grant is None:
        return False
    if time.time() - float(grant.get("at", 0)) > GRANT_MAX_AGE_S:
        return False
    if grant.get("prompt_id") and data.get("prompt_id") and grant["prompt_id"] != data["prompt_id"]:
        return False
    return True


# ----------------------------------------------------------------------------- paths

def _norm(path, cwd):
    if not path:
        path = "."
    path = os.path.expanduser(str(path))
    if not os.path.isabs(path):
        path = os.path.join(cwd, path)
    real = os.path.realpath(path)
    return os.path.normpath(real).lower(), os.path.normpath(path).lower()


def _contains_seq(p, seq):
    return ("/" + p.strip("/") + "/").find("/" + seq + "/") >= 0


def is_agent_path(path, cwd):
    return any(_contains_seq(p, ".interface/agent") for p in _norm(path, cwd))


def _outside_config(p):
    wrapped = "/" + p.strip("/") + "/"
    idx = wrapped.find("/.interface/")
    if idx < 0:
        return False
    rest = wrapped[idx + len("/.interface/"):]
    return not (rest.startswith("config/") and len(rest) > len("config/"))


def is_protected_mutation_path(path, cwd):
    return any(_outside_config(p) for p in _norm(path, cwd))


def is_guard_path(path, cwd):
    return any(_contains_seq(p, ".claude/hooks/interface-guard") for p in _norm(path, cwd))


def agent_dirs(project):
    dirs = []
    for root in {project}:
        cand = os.path.join(root, ".interface", "agent")
        if os.path.isdir(cand):
            dirs.append(os.path.realpath(cand).lower())
    return dirs


def is_agent_ancestor(path, cwd, project):
    """True when a recursive operation rooted at path would reach an Agent Module."""
    real, _ = _norm(path, cwd)
    if _contains_seq(real, ".interface/agent"):
        return True
    for d in agent_dirs(project):
        if d.startswith(real.rstrip("/") + "/"):
            return True
    if os.path.isdir(os.path.join(real, ".interface", "agent")):
        return True
    if real.endswith("/.interface") and os.path.isdir(os.path.join(real, "agent")):
        return True
    return False


def is_interface_ancestor(path, cwd, project):
    real, _ = _norm(path, cwd)
    iface = os.path.realpath(os.path.join(project, ".interface")).lower()
    return iface == real or iface.startswith(real.rstrip("/") + "/") or os.path.isdir(os.path.join(real, ".interface"))


def agent_files(project):
    out = []
    for d in agent_dirs(project):
        for root, _dirs, files in os.walk(d):
            for name in files:
                out.append(os.path.join(root, name))
    return out


def _glob_regex(pattern):
    """Glob to regex: `*` and `?` stay within one path segment, `**` crosses segments."""
    i, out = 0, ""
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
        elif pattern.startswith("**", i):
            out += ".*"
            i += 2
        elif c == "*":
            out += "[^/]*"
            i += 1
        elif c == "?":
            out += "[^/]"
            i += 1
        elif c == "{":
            j = pattern.find("}", i)
            if j < 0:
                out += re.escape(c)
                i += 1
            else:
                out += "(?:" + "|".join(_glob_regex(x) for x in pattern[i + 1:j].split(",")) + ")"
                i = j + 1
        elif c == "[":
            j = pattern.find("]", i)
            if j < 0:
                out += re.escape(c)
                i += 1
            else:
                out += "[" + pattern[i + 1:j].replace("!", "^", 1) + "]"
                i = j + 1
        else:
            out += re.escape(c)
            i += 1
    return out


def glob_could_match_agent(pattern, root, cwd, project, basename_only_if_no_slash):
    real_root, _ = _norm(root, cwd)
    try:
        rx = re.compile("^" + _glob_regex(pattern.lower()) + "$")
    except re.error:
        return True
    for f in agent_files(project):
        f = f.lower()
        if not f.startswith(real_root.rstrip("/") + "/"):
            continue
        rel = f[len(real_root.rstrip("/")) + 1:]
        target = os.path.basename(rel) if (basename_only_if_no_slash and "/" not in pattern) else rel
        if rx.match(target):
            return True
    return False


# ----------------------------------------------------------------------------- bash analysis

EXCLUSION_PATTERNS = [
    r":\(exclude\)\S*interface/agent\S*",
    r":[!^]\S*interface/agent\S*",
    r"(--glob|-g|--iglob)(=|\s+)['\"]?!\S*interface/agent\S*",
    r"--exclude(-dir)?(=|\s+)['\"]?\S*(interface/agent|agent)\S*",
    r"(-not|!)\s+(-path|-wholename|-ipath)\s+['\"]?\S*interface/agent\S*",
    r"-path\s+['\"]?\S*interface/agent\S*['\"]?\s+-prune",
]
SEPARATORS = {"|", "||", "&&", ";", "&", ";;", "(", ")", "|&", "\n"}
REDIRECTS = {">", ">>", ">|", "&>", "&>>"}
RECURSIVE_ALWAYS = {"rg", "ag", "ack", "fd", "fdfind", "tree", "du", "find"}
RECURSIVE_IMPLICIT_CWD = {"rg", "ag", "ack", "fd", "fdfind", "tree", "du"}
WRITE_ANY_ARG = {"rm", "rmdir", "mv", "touch", "mkdir", "truncate", "tee", "chmod", "chown",
                 "chgrp", "chflags", "xattr", "unlink", "shred", "patch", "setfacl"}
WRITE_DEST_ARG = {"cp", "rsync", "install", "ln", "ditto", "scp"}
INTERPRETERS = {"python", "python3", "node", "ruby", "perl", "php", "osascript", "awk", "gawk",
                "bash", "sh", "zsh", "dash", "ksh", "fish", "deno", "bun", "swift", "eval", "xargs"}
WRITE_INDICATORS = re.compile(
    r"(open\s*\([^)]*['\"][wax+]|\.write|write_text|write_bytes|writefile|appendfile|unlink|"
    r"rmtree|remove|rename|replace\s*\(|truncate|shutil|os\.system|subprocess|[^0-9&]>\s*[^&/]|"
    r"\brm\b|\bmv\b|\bcp\b|\btouch\b|\bmkdir\b|\btee\b|sed\s+-i|perl\s+-p?i)",
    re.IGNORECASE,
)


def _strip_exclusions(cmd):
    out = cmd
    for pat in EXCLUSION_PATTERNS:
        out = re.sub(pat, " ", out, flags=re.IGNORECASE)
    return out


def _has_agent_exclusion(cmd):
    return any(re.search(p, cmd, flags=re.IGNORECASE) for p in EXCLUSION_PATTERNS)


def _mentions_agent(cmd):
    low = _strip_exclusions(cmd).lower()
    if "interface/agent" in low:
        return True
    if re.search(r"\.interface/(?!config/)[^\s'\"]*[*?\[{]", low):
        return True
    if ".interface" in low and re.search(r"(?<![\w-])agent(?![\w-])", low):
        return True
    return False


def _mentions_protected(cmd):
    for m in re.finditer(r"\.interface(/[^\s'\"|;&)<>]*)?", cmd, flags=re.IGNORECASE):
        rest = (m.group(1) or "").lower()
        if not re.match(r"^/config/[^\s]", rest):
            return True
    return False


def _tokens(cmd):
    lexer = shlex.shlex(cmd, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    return list(lexer)


def _segments(tokens):
    seg = []
    for t in tokens:
        if t in SEPARATORS:
            if seg:
                yield seg
            seg = []
        else:
            seg.append(t)
    if seg:
        yield seg


def _strip_prefix(argv):
    """Drop env assignments and wrappers such as sudo, env, command, time, nice, xargs."""
    i = 0
    while i < len(argv):
        t = argv[i]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t):
            i += 1
        elif t in ("sudo", "env", "command", "builtin", "time", "nice", "nohup", "exec", "caffeinate"):
            i += 1
        else:
            break
    return argv[i:]


def _flags(argv):
    return [a for a in argv[1:] if a.startswith("-") and a != "-"]


def _positionals(argv):
    return [a for a in argv[1:] if not a.startswith("-") and a not in REDIRECTS]


def _redirect_targets(tokens):
    out = []
    for i, t in enumerate(tokens):
        if (t in REDIRECTS or re.match(r"^\d?>{1,2}\|?$", t)) and i + 1 < len(tokens):
            out.append(tokens[i + 1])
    return out


def bash_check(cmd, cwd, project, has_grant, depth=0):
    """Return a deny reason for the command, or None when it may run."""
    if depth > 3:
        return FAILURE_MSG.format("command nesting too deep")

    low = cmd.lower()
    if SYNC_NAME in low and re.search(r"(^|[\s;&|(`$])(\S*/)?(claude|claude-code)(\s|$)", low):
        return SYNC_INVOKE_MSG
    if _mentions_protected(cmd) and re.search(
            r"xargs\s+(-\S+\s+)*(rm|rmdir|mv|cp|sed|perl|tee|touch|truncate|chmod|chown|ln|unlink)\b", low):
        return MUTATION_MSG
    if ("interface-guard" in low or "hooks/interface" in low) and not has_grant:
        if re.search(r"(>|\brm\b|\bmv\b|\bcp\b|\btee\b|sed\s+-i|\btouch\b|\bchmod\b|\bln\b|write|unlink)", low):
            return TAMPER_MSG
    if _contains_seq(os.path.realpath(cwd).lower(), ".interface/agent") and not has_grant:
        return AGENT_MSG
    if _mentions_agent(cmd) and not has_grant:
        return AGENT_MSG

    try:
        tokens = _tokens(cmd)
    except ValueError:
        if _mentions_protected(cmd):
            return FAILURE_MSG.format("unparseable command touching .interface")
        return None

    # Mutations: redirect targets anywhere in the command.
    for target in _redirect_targets(tokens):
        if target.startswith("&") or target in ("/dev/null", "/dev/stderr", "/dev/stdout"):
            continue
        if is_protected_mutation_path(target, cwd):
            return MUTATION_MSG
        if is_guard_path(target, cwd) and not has_grant:
            return TAMPER_MSG

    # Inline code and heredocs that mention a protected path and write.
    if _mentions_protected(cmd) and ("<<" in cmd or re.search(r"(^|\s)-(c|e|E|p?i)\b", cmd)):
        if WRITE_INDICATORS.search(cmd):
            return MUTATION_MSG

    for seg in _segments(tokens):
        argv = _strip_prefix(seg)
        if not argv:
            continue
        prog = os.path.basename(argv[0]).lower()
        flags = _flags(argv)
        pos = [a for a in _positionals(argv)]

        # Nested shells: analyze their payload as a command of its own.
        if prog in ("bash", "sh", "zsh", "dash", "ksh") and "-c" in argv:
            idx = argv.index("-c")
            if idx + 1 < len(argv):
                reason = bash_check(argv[idx + 1], cwd, project, has_grant, depth + 1)
                if reason:
                    return reason
        if prog == "eval":
            reason = bash_check(" ".join(argv[1:]), cwd, project, has_grant, depth + 1)
            if reason:
                return reason

        if prog in INTERPRETERS and _mentions_protected(" ".join(argv)) and WRITE_INDICATORS.search(" ".join(argv[1:])):
            return MUTATION_MSG

        # Writes through file utilities.
        if prog in WRITE_ANY_ARG:
            for a in pos:
                if is_protected_mutation_path(a, cwd):
                    return MUTATION_MSG
                if is_guard_path(a, cwd) and not has_grant:
                    return TAMPER_MSG
            if prog == "rm" and any("r" in f.lower() for f in flags if not f.startswith("--")) | ("--recursive" in flags):
                for a in pos:
                    if is_interface_ancestor(a, cwd, project):
                        return MUTATION_MSG
        if prog in WRITE_DEST_ARG and pos:
            dest = pos[-1]
            if is_protected_mutation_path(dest, cwd):
                return MUTATION_MSG
            if is_guard_path(dest, cwd) and not has_grant:
                return TAMPER_MSG
        if prog in ("sed", "gsed", "perl") and any(re.match(r"^-[a-z]*i", f) or f.startswith("--in-place") for f in flags):
            for a in pos:
                if is_protected_mutation_path(a, cwd):
                    return MUTATION_MSG
        if prog == "dd":
            for a in argv[1:]:
                if a.startswith("of=") and is_protected_mutation_path(a[3:], cwd):
                    return MUTATION_MSG
        if prog == "find" and any(f in ("-delete", "-exec", "-execdir", "-ok", "-okdir") for f in argv[1:]):
            starts = []
            for a in argv[1:]:
                if a.startswith("-") or a in ("(", "!", ")"):
                    break
                starts.append(a)
            for a in starts or ["."]:
                if is_interface_ancestor(a, cwd, project) or is_protected_mutation_path(a, cwd):
                    return MUTATION_MSG
        if prog == "git" and len(argv) > 1:
            sub = argv[1]
            if sub in ("rm", "mv", "checkout", "restore", "reset", "clean", "stash", "apply", "am", "switch"):
                for a in argv[2:]:
                    if not a.startswith("-") and is_protected_mutation_path(a, cwd):
                        return MUTATION_MSG

        if has_grant:
            continue

        # Reads: recursive traversals that would reach an Agent Module.
        recursive = prog in RECURSIVE_ALWAYS
        implicit_cwd = prog in RECURSIVE_IMPLICIT_CWD
        if prog in ("grep", "egrep", "fgrep", "ggrep") and any(
            f in ("--recursive", "--dereference-recursive") or (not f.startswith("--") and ("r" in f or "R" in f))
            for f in flags
        ):
            recursive = implicit_cwd = True
        if prog == "ls" and any(not f.startswith("--") and "R" in f for f in flags) or (prog == "ls" and "--recursive" in flags):
            recursive = implicit_cwd = True
        if prog in ("cp", "scp") and any(f in ("-r", "-R", "-a", "--recursive", "--archive") or (not f.startswith("--") and ("r" in f or "R" in f or "a" in f)) for f in flags):
            recursive = True
        if prog in ("tar", "zip", "rsync", "ditto", "7z"):
            recursive = True
        if prog == "git" and len(argv) > 1 and argv[1] == "grep":
            recursive = implicit_cwd = True
        if prog == "find":
            implicit_cwd = True
        if recursive and not _has_agent_exclusion(cmd):
            roots = [a for a in pos if os.path.exists(os.path.join(cwd, os.path.expanduser(a))) or os.path.isabs(a)]
            if prog == "find":
                roots = []
                for a in argv[1:]:
                    if a.startswith("-") or a in ("(", "!", ")"):
                        break
                    roots.append(a)
            if not roots and implicit_cwd:
                roots = ["."]
            for r in roots:
                if is_agent_ancestor(r, cwd, project):
                    return AGENT_MSG

        # Reads: git commands that print file content repository-wide.
        if prog == "git" and len(argv) > 1 and not _has_agent_exclusion(cmd):
            sub = argv[1]
            rest = argv[2:]
            names_only = any(f in ("--stat", "--name-only", "--name-status", "--shortstat", "--numstat",
                                   "--no-patch", "-s", "--summary", "--dirstat", "--quiet", "--exit-code")
                             for f in rest)
            pathspecs = rest[rest.index("--") + 1:] if "--" in rest else []
            safe_paths = bool(pathspecs) and all(
                not is_agent_ancestor(p, cwd, project) for p in pathspecs
            )
            dumps = False
            if sub in ("diff", "format-patch", "archive", "cat-file", "whatchanged"):
                dumps = True
            elif sub == "show":
                dumps = not any(re.match(r"^[^-][^:\s]*:.+", a) for a in rest)
            elif sub == "log" and any(f in ("-p", "-u", "--patch", "--full-diff") or re.match(r"^-[a-z]*p", f) for f in rest):
                dumps = True
            elif sub == "stash" and "show" in rest and any(f in ("-p", "--patch") for f in rest):
                dumps = True
            if dumps and not names_only and not safe_paths:
                return (AGENT_MSG + " For git, limit output with a pathspec that excludes it, e.g. "
                        "`git diff -- . ':(exclude).interface/agent'`.")
    return None


# ----------------------------------------------------------------------------- pre-tool-use

def pre_tool_use(data):
    tool = data.get("tool_name") or ""
    ti = data.get("tool_input") or {}
    cwd = data.get("cwd") or os.getcwd()
    project = os.environ.get("CLAUDE_PROJECT_DIR") or cwd
    has_grant = granted(data)

    if tool == "Skill":
        name = str(ti.get("skill") or ti.get("command") or ti.get("name") or "")
        if name.split(":")[-1].lstrip("/").strip().lower() == SYNC_NAME:
            deny(SYNC_INVOKE_MSG)
        allow()

    if tool in ("Read", "Edit", "Write", "NotebookEdit"):
        path = ti.get("file_path") or ti.get("notebook_path") or ti.get("path")
        if not path:
            deny(FAILURE_MSG.format("missing path for " + tool))
        if tool != "Read" and is_protected_mutation_path(path, cwd):
            deny(MUTATION_MSG)
        if tool != "Read" and is_guard_path(path, cwd) and not has_grant:
            deny(TAMPER_MSG)
        if is_agent_path(path, cwd) and not has_grant:
            deny(AGENT_MSG)
        allow()

    if tool in ("Grep", "Glob"):
        root = ti.get("path") or cwd
        pattern = str(ti.get("pattern") or "")
        glob = ti.get("glob")
        if has_grant:
            allow()
        if is_agent_path(root, cwd):
            deny(AGENT_MSG)
        if tool == "Glob":
            if "interface/agent" in pattern.lower():
                deny(AGENT_MSG)
            if is_agent_ancestor(root, cwd, project) and glob_could_match_agent(pattern, root, cwd, project, False):
                deny(AGENT_MSG)
            allow()
        # Grep
        if glob and "interface/agent" in str(glob).lower() and not str(glob).startswith("!"):
            deny(AGENT_MSG)
        if is_agent_ancestor(root, cwd, project):
            if glob and not str(glob).startswith("!") and not glob_could_match_agent(str(glob), root, cwd, project, True):
                allow()
            gtype = str(ti.get("type") or "").lower()
            if gtype and not glob:
                exts = {os.path.splitext(f)[1].lstrip(".").lower() for f in agent_files(project)}
                type_exts = {"md": {"md", "markdown", "mdx", "mkd", "mkdn", "mdwn", "mdown", "markdown"},
                             "markdown": {"md", "markdown", "mdx", "mkd", "mkdn", "mdwn", "mdown"},
                             "yaml": {"yaml", "yml"}, "yml": {"yaml", "yml"},
                             "txt": {"txt"}, "json": {"json"}}
                if not (type_exts.get(gtype, {gtype}) & exts):
                    allow()
            deny(AGENT_MSG)
        allow()

    if tool == "Bash":
        reason = bash_check(str(ti.get("command") or ""), cwd, project, has_grant)
        if reason:
            deny(reason)
        allow()

    # Strengthening matcher: scheduling and delegation tools must not start Agent Native Sync.
    blob = json.dumps(ti)
    for value in _string_values(ti):
        if re.search(r"(^|\n)\s*/" + re.escape(SYNC_NAME) + r"\b", value):
            deny(SYNC_INVOKE_MSG)
    if SYNC_NAME in blob and tool in ("CronCreate", "RemoteTrigger", "ScheduleWakeup"):
        deny(SYNC_INVOKE_MSG)
    allow()


def _string_values(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _string_values(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _string_values(v)


# ----------------------------------------------------------------------------- main

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except ValueError:
        if mode == "pre-tool-use":
            deny(FAILURE_MSG.format("malformed hook input"))
        sys.stderr.write(FAILURE_MSG.format("malformed hook input") + "\n")
        sys.exit(1)

    if mode == "pre-tool-use":
        try:
            pre_tool_use(data)
        except SystemExit:
            raise
        except Exception as exc:  # fail_closed
            deny(FAILURE_MSG.format(type(exc).__name__ + ": " + str(exc)))
        return

    try:
        if mode == "prompt-submit":
            prompt_submit(data)
        elif mode == "prompt-expansion":
            prompt_expansion(data)
        elif mode == "revoke":
            revoke(data)
        else:
            raise ValueError("unknown mode " + repr(mode))
    except Exception as exc:
        # A failed grant step leaves no grant, so reads stay denied (fail_closed); make it visible.
        try:
            revoke(data)
        except Exception:
            pass
        sys.stderr.write("agent-native-read-grant: " + type(exc).__name__ + ": " + str(exc) + "\n")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
