#!/usr/bin/env python3
# managed by /my-interface-native-implement
# Native realization of the Permission Enforced Guarantees `interface-boundary-guard`
# and `agent-native-read-grant`. Regenerated on every run — do not edit by hand.
#
# Modes (argv[1]):
#   pre     PreToolUse        — block Executor Module reads outside the grant, every
#                               non-Human invocation of Agent Native Implement, and
#                               every Interface mutation. Fails closed (exit 2).
#   prompt  UserPromptSubmit  — record a session- and prompt-bound read grant when the
#                               Human directly types /my-interface-native-implement;
#                               revoke any grant for every other prompt. Fails closed.
#   revoke  Stop/SessionStart — revoke the grant when the granted prompt ends.

import fnmatch
import json
import os
import re
import shlex
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
INTERFACE = PROJECT / ".interface"
EXECUTOR = INTERFACE / "executor"
HOOKS_DIR = PROJECT / ".claude" / "hooks"
STATE_DIR = HOOKS_DIR / ".state"
GRANT_FILE = STATE_DIR / "native-implement-grant.json"
SETTINGS = PROJECT / ".claude" / "settings.json"
NATIVE_IMPLEMENT = "my-interface-native-implement"
INVOCATION = re.compile(r"^\s*/" + re.escape(NATIVE_IMPLEMENT) + r"(\s|$)")

BOUNDARY = (
    "Blocked by interface-boundary-guard: {reason}. The Executor Module is readable only "
    "within the prompt of the Human's direct /" + NATIVE_IMPLEMENT + " invocation, that "
    "grant is non-transferable, Agent Native Implement is invoked only by the Human, and "
    "the .interface/ tree is read-only. Do not work around this boundary; report Runtime "
    "drift or the needed change to the Human."
)


class Block(Exception):
    pass


# --------------------------------------------------------------------------- paths

def resolve(raw, cwd):
    raw = os.path.expandvars(os.path.expanduser(raw))
    p = Path(raw)
    if not p.is_absolute():
        p = Path(cwd) / p
    return Path(os.path.realpath(p))


def under(p, root):
    try:
        p.relative_to(root)
        return True
    except ValueError:
        return False


def ancestor_of(p, target):
    return under(target, p) and p != target


def executor_files():
    out = []
    for dirpath, _dirs, files in os.walk(EXECUTOR):
        for f in files:
            out.append(Path(dirpath) / f)
    return out or [EXECUTOR / "executor.md"]


def glob_regex(pattern):
    i, out = 0, ""
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
            continue
        if pattern.startswith("**", i):
            out += ".*"
            i += 2
            continue
        if c == "*":
            out += "[^/]*"
        elif c == "?":
            out += "[^/]"
        elif c == "{":
            j = pattern.find("}", i)
            if j == -1:
                out += re.escape(c)
            else:
                out += "(?:" + "|".join(re.escape(x) for x in pattern[i + 1:j].split(",")) + ")"
                i = j
        elif c == "[":
            j = pattern.find("]", i)
            if j == -1:
                out += re.escape(c)
            else:
                out += pattern[i:j + 1]
                i = j
        else:
            out += re.escape(c)
        i += 1
    return re.compile("^" + out + "$")


TYPE_EXT = {
    "md": {".md", ".markdown", ".mdx", ".mkd", ".mkdn", ".mdwn", ".mdown", ".mdtxt", ".mdtext"},
    "markdown": {".md", ".markdown", ".mdx", ".mkd", ".mkdn", ".mdwn", ".mdown", ".mdtxt", ".mdtext"},
    "yaml": {".yaml", ".yml"},
    "py": {".py", ".pyi"},
    "python": {".py", ".pyi"},
    "js": {".js", ".jsx", ".mjs", ".cjs", ".vue"},
    "ts": {".ts", ".tsx", ".mts", ".cts"},
    "json": {".json", ".jsonl", ".sarif"},
    "toml": {".toml"},
    "sql": {".sql", ".psql"},
    "sh": {".sh", ".bash", ".zsh", ".bashrc", ".zshrc"},
    "html": {".html", ".htm", ".xhtml"},
    "css": {".css", ".scss", ".sass", ".less"},
    "go": {".go"},
    "rust": {".rs"},
    "java": {".java"},
    "c": {".c", ".h"},
    "cpp": {".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx", ".h"},
    "txt": {".txt"},
    "xml": {".xml"},
    "csv": {".csv"},
    "ini": {".ini", ".cfg"},
    "dockerfile": {"dockerfile"},
}


def search_reaches_executor(root, glob=None, ftype=None, pattern=None):
    """True when a recursive listing/search rooted at `root` can reach an Executor file."""
    if under(root, EXECUTOR):
        return True
    if not ancestor_of(root, EXECUTOR):
        return False
    for f in executor_files():
        rel = f.relative_to(root).as_posix()
        if pattern is not None:
            pat = pattern
            if os.path.isabs(pat):
                pat_root = Path(os.path.realpath(pat.split("*")[0] or "/"))
                if not (under(EXECUTOR, pat_root) or under(pat_root, EXECUTOR)):
                    continue
                rel = f.as_posix()
            if not glob_regex(pat).match(rel):
                continue
        if glob:
            g = glob.lstrip("!")
            if glob.startswith("!"):
                if fnmatch.fnmatch(f.name, g) or glob_regex(g.lstrip("/")).match(rel):
                    continue
            elif "/" in g:
                if not glob_regex(g.lstrip("/")).match(rel) and not glob_regex("**/" + g).match(rel):
                    continue
            elif not glob_regex(g).match(f.name):
                continue
        if ftype:
            exts = TYPE_EXT.get(ftype)
            if exts is not None and f.suffix.lower() not in exts and f.name.lower() not in exts:
                continue
        return True
    return False


# --------------------------------------------------------------------------- grant

def grant_active(data):
    if data.get("agent_id") or data.get("agent_type"):
        return False  # the grant is non-transferable to any delegated Agent Instance
    try:
        g = json.loads(GRANT_FILE.read_text())
    except (OSError, ValueError):
        return False
    return bool(g.get("session_id")) and g.get("session_id") == data.get("session_id")


def write_grant(data):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    ignore = STATE_DIR / ".gitignore"
    if not ignore.exists():
        ignore.write_text("*\n")
    tmp = GRANT_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps({
        "session_id": data.get("session_id"),
        "granted_at": int(time.time()),
        "prompt": NATIVE_IMPLEMENT,
    }))
    os.replace(tmp, GRANT_FILE)


def revoke_grant():
    try:
        GRANT_FILE.unlink()
    except FileNotFoundError:
        pass


# --------------------------------------------------------------------------- bash

SEPARATORS = {";", "&&", "||", "|", "&", "(", ")", "|&", ";;", "\n"}
WRAPPERS = {"sudo", "env", "nohup", "time", "command", "builtin", "exec", "nice", "timeout", "stdbuf"}
RECURSIVE = {"rg", "ag", "ack", "find", "fd", "fdfind", "tree", "du", "tar", "zip", "rsync", "locate"}
GREP = {"grep", "egrep", "fgrep", "zgrep"}
INTERPRETERS = {"python", "python3", "node", "ruby", "perl", "php", "bash", "sh", "zsh", "dash",
                "ksh", "fish", "pwsh", "deno", "bun", "lua", "osascript", "eval", "source", "."}
MUTATORS = {"rm", "rmdir", "mv", "cp", "touch", "mkdir", "chmod", "chown", "chgrp", "ln",
            "truncate", "dd", "install", "rsync", "tee", "patch", "unlink", "shred", "xargs",
            "vi", "vim", "nvim", "nano", "ed", "ex", "emacs", "split", "csplit", "tar", "unzip",
            "gunzip", "bunzip2", "unxz", "mkfifo", "mknod", "setfacl", "chattr", "sponge"}
DEST_ONLY = {"cp", "install", "ln", "rsync"}
GIT_MUTATING = {"checkout", "restore", "reset", "clean", "rm", "mv", "stash", "apply", "am",
                "pull", "merge", "rebase", "switch", "cherry-pick", "revert", "commit", "add",
                "worktree", "submodule", "filter-branch", "update-index", "read-tree", "checkout-index"}
NATIVE_INVOKERS = {"claude", "npx", "bunx"}


def tokenize(cmd):
    try:
        lex = shlex.shlex(cmd, posix=True, punctuation_chars=";&|()")
        lex.whitespace_split = True
        lex.commenters = ""
        return list(lex)
    except ValueError:
        return re.findall(r"[^\s;&|()]+|[;&|()]+", cmd)


def segments(tokens):
    seg = []
    for t in tokens:
        if t in SEPARATORS or (t and set(t) <= set(";&|()")):
            if seg:
                yield seg
            seg = []
        else:
            seg.append(t)
    if seg:
        yield seg


def command_name(seg):
    for i, t in enumerate(seg):
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t) or t in WRAPPERS:
            continue
        if i > 0 and seg[i - 1] in WRAPPERS and (t.startswith("-") or re.match(r"^[0-9.]+[smhd]?$", t)):
            continue
        return os.path.basename(t), i
    return "", len(seg)


def git_subcommand(args):
    skip = False
    for a in args:
        if skip:
            skip = False
            continue
        if a in ("-C", "-c", "--git-dir", "--work-tree", "--namespace"):
            skip = True
            continue
        if a.startswith("-"):
            continue
        return a
    return ""


def path_candidates(tok):
    out = [tok]
    if "=" in tok:
        out.append(tok.split("=", 1)[1])
    if tok.startswith("-") and len(tok) > 2 and tok[1] != "-":
        out.append(tok[2:])
    return [c for c in out if c]


def looks_like_path(c, cwd):
    if c.startswith("-") or not c:
        return False
    if "/" in c or c.startswith(".") or c.startswith("~") or c.startswith("$"):
        return True
    return os.path.exists(os.path.join(cwd, c))


def expand(c, cwd):
    if any(ch in c for ch in "*?["):
        import glob as _glob
        base = os.path.expandvars(os.path.expanduser(c))
        if not os.path.isabs(base):
            base = os.path.join(cwd, base)
        hits = _glob.glob(base, recursive=True)
        return [Path(os.path.realpath(h)) for h in hits] or [resolve(c.split("*")[0].split("?")[0].split("[")[0] or ".", cwd)]
    return [resolve(c, cwd)]


def is_exclusion(tok):
    t = tok.lower()
    return ("!" in t or t.startswith("--exclude") or t.startswith("--ignore")) and (".interface" in t or "executor" in t)


def check_bash(cmd, cwd, granted):
    raw = cmd
    tokens = tokenize(cmd)
    segs = list(segments(tokens))
    cwd_p = Path(os.path.realpath(cwd))

    # 1. Non-Human invocation of Agent Native Implement through a CLI.
    if "native-implement" in raw:
        for seg in segs:
            name, _ = command_name(seg)
            if name in NATIVE_INVOKERS or "claude" in seg:
                raise Block("a non-Human attempt to invoke Agent Native Implement")

    # Collect referenced paths.
    refs = []  # (segment index, token index, resolved path)
    for si, seg in enumerate(segs):
        for ti, tok in enumerate(seg):
            if is_exclusion(tok):
                continue
            for c in path_candidates(tok):
                if looks_like_path(c, cwd):
                    for p in expand(c, cwd):
                        refs.append((si, ti, p))
    redirect_targets = [resolve(t, cwd) for t in re.findall(r"(?:^|[^<0-9&>-])(?:&>|>>|>\|?|[0-9]>>?)\s*([^\s;&|<>()]+)", raw)]
    redirect_targets = [p for p in redirect_targets if str(p) not in ("/dev/null", "/dev/stdout", "/dev/stderr")]

    # 2. Executor Module reads outside the grant.
    if not granted:
        scrubbed = " ".join(t for t in tokens if not is_exclusion(t))
        if under(cwd_p, EXECUTOR):
            raise Block("a shell command running inside the Executor Module")
        if re.search(r"interface[/\\]+executor", scrubbed):
            raise Block("a shell command naming the Executor Module")
        if "executor" in scrubbed and ("interface" in scrubbed and re.search(r"[$`*?\[{]|\beval\b|base64|printf", scrubbed)):
            raise Block("a shell command that may construct an Executor Module path")
        for _si, _ti, p in refs:
            if under(p, EXECUTOR):
                raise Block("a shell command reading the Executor Module")
        for si, seg in enumerate(segs):
            name, ni = command_name(seg)
            args = seg[ni + 1:]
            recursive = (
                name in RECURSIVE
                or (name in GREP and any(re.match(r"^-[A-Za-z]*[rR]", a) or a in ("--recursive", "--dereference-recursive") for a in args))
                or (name == "ls" and any(re.match(r"^-[A-Za-z]*R", a) or a == "--recursive" for a in args))
                or (name in ("cp", "scp") and any(re.match(r"^-[A-Za-z]*[rRa]", a) or a in ("--recursive", "--archive") for a in args))
                or (name == "git" and args[:1] == ["grep"])
                or any("**" in a for a in args)
            )
            if not recursive:
                continue
            if any(is_exclusion(a) for a in args):
                continue
            seg_refs = [p for s, _t, p in refs if s == si]
            if any(ancestor_of(p, EXECUTOR) for p in seg_refs):
                raise Block("a recursive shell search or listing that reaches the Executor Module")
            if not seg_refs and ancestor_of(cwd_p, EXECUTOR):
                raise Block("a recursive shell search or listing from a directory containing the Executor Module")

    # 3. Interface (and guard-integrity) mutation.
    always = [INTERFACE, STATE_DIR]
    guarded = [] if granted else [HOOKS_DIR, SETTINGS]
    protected = always + guarded

    def is_protected(p):
        return any(under(p, root) for root in protected)

    for p in redirect_targets:
        if is_protected(p):
            raise Block("a shell redirection writing into a protected path")
    in_protected_cwd = is_protected(cwd_p)
    for si, seg in enumerate(segs):
        name, ni = command_name(seg)
        args = seg[ni + 1:]
        mutating = (
            name in MUTATORS
            or name in INTERPRETERS
            or (name == "sed" and any(a.startswith("-i") or a.startswith("--in-place") for a in args))
            or (name in ("awk", "gawk") and any("inplace" in a for a in args))
            or (name == "find" and any(a in ("-delete", "-exec", "-execdir", "-ok", "-okdir", "-fprint", "-fprintf", "-fls") for a in args))
            or (name == "git" and git_subcommand(args) in GIT_MUTATING)
        )
        if not mutating:
            continue
        seg_refs = [(t, p) for s, t, p in refs if s == si]
        if name in DEST_ONLY:
            operands = [t for t, _p in seg_refs]
            if operands:
                last = max(operands)
                targets = [p for t, p in seg_refs if t == last]
                if any(is_protected(p) for p in targets) or (in_protected_cwd and not seg_refs):
                    raise Block("a shell command writing into a protected path")
            continue
        if any(is_protected(p) for _t, p in seg_refs):
            raise Block("a shell command that can mutate a protected path")
        if in_protected_cwd:
            raise Block("a mutating shell command running inside a protected path")
        if name in INTERPRETERS or name == "xargs":
            # Interpreters and xargs receive their targets indirectly; refuse when the
            # command as a whole refers to a protected path at all.
            if any(is_protected(p) for _s, _t, p in refs) or re.search(r"(^|[\s'\"=:(/])\.interface\b", raw):
                raise Block("an interpreter or xargs command that refers to a protected path")


# --------------------------------------------------------------------------- tools

PATH_KEYS = ("file_path", "path", "notebook_path")
NON_FILE_TOOLS = {"Agent", "Task", "SendMessage", "TodoWrite", "TaskCreate", "TaskGet", "TaskList",
                  "TaskUpdate", "TaskStop", "WebFetch", "WebSearch", "AskUserQuestion", "ExitPlanMode",
                  "EnterPlanMode", "ToolSearch", "ListAgents", "ReadNotifications", "ScheduleWakeup",
                  "SendFeedback", "ReportFindings", "PushNotification", "SendUserFile", "Monitor",
                  "CronCreate", "CronDelete", "CronList", "EndConversation", "Workflow", "Artifact"}
WRITE_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)


def check_settings_write(tool, inp):
    try:
        current = SETTINGS.read_text()
    except OSError:
        current = ""
    if tool == "Write":
        new = inp.get("content", "")
        if "interface_guard" in current and "interface_guard" not in new:
            raise Block("removing the Enforced Guarantee hooks from project settings")
        if '"hooks"' in current and new.count("interface_guard") < current.count("interface_guard"):
            raise Block("changing the Enforced Guarantee hooks in project settings")
    else:
        old = inp.get("old_string", "") + json.dumps(inp.get("edits", ""))
        if "interface_guard" in old or '"hooks"' in old or "PreToolUse" in old or "UserPromptSubmit" in old:
            raise Block("changing the Enforced Guarantee hooks in project settings")


def check_tool(data):
    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}
    cwd = data.get("cwd") or str(PROJECT)
    granted = grant_active(data)

    if tool in ("Skill", "SlashCommand"):
        if any(NATIVE_IMPLEMENT in s or "native-implement" in s for s in strings(inp)):
            raise Block("a non-Human attempt to invoke Agent Native Implement")
        return

    if tool == "Bash":
        check_bash(inp.get("command", ""), cwd, granted)
        return

    if tool in WRITE_TOOLS:
        p = resolve(inp.get("file_path") or inp.get("notebook_path") or "", cwd)
        if under(p, INTERFACE):
            raise Block("a direct Interface mutation")
        if under(p, STATE_DIR):
            raise Block("a direct write to the Agent Native Implement grant record")
        if not granted and under(p, HOOKS_DIR):
            raise Block("a change to the Enforced Guarantee hooks outside Agent Native Implement")
        if not granted and p == SETTINGS:
            check_settings_write(tool, inp)
        return

    if tool == "Read":
        p = resolve(inp.get("file_path", ""), cwd)
        if under(p, EXECUTOR) and not granted:
            raise Block("an Executor Module read")
        return

    if tool == "Grep":
        root = resolve(inp.get("path") or ".", cwd)
        if not granted and search_reaches_executor(root, glob=inp.get("glob"), ftype=inp.get("type")):
            raise Block("a search that reaches the Executor Module (narrow the path or glob to exclude it)")
        return

    if tool == "Glob":
        root = resolve(inp.get("path") or ".", cwd)
        if not granted and search_reaches_executor(root, pattern=inp.get("pattern") or "*"):
            raise Block("a file discovery that reaches the Executor Module (narrow the path or pattern to exclude it)")
        return

    if tool in NON_FILE_TOOLS:
        return

    # Any other tool (MCP servers, LSP, future tools): inspect every string argument.
    for s in strings(inp):
        if not granted and re.search(r"interface[/\\]+executor", s):
            raise Block("an Executor Module access through " + tool)
        if any(k in tool.lower() for k in ("write", "edit", "create", "delete", "move", "rename", "remove", "update")):
            if re.search(r"(^|[\s'\"=:(/])\.interface(/|$)", s) or (os.path.isabs(s) and under(Path(os.path.realpath(s)), INTERFACE)):
                raise Block("a direct Interface mutation through " + tool)


# --------------------------------------------------------------------------- main

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pre"
    if mode == "revoke":
        try:
            revoke_grant()
        except Exception as exc:  # visible, non-blocking
            print("interface-guard: grant revocation failed: %s" % exc, file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    try:
        data = json.load(sys.stdin)
    except Exception as exc:
        print(BOUNDARY.format(reason="malformed hook input (%s)" % exc), file=sys.stderr)
        sys.exit(2)

    if mode == "prompt":
        try:
            if INVOCATION.match(data.get("prompt") or ""):
                write_grant(data)
            else:
                revoke_grant()
        except Exception as exc:
            print("interface-guard: could not update the Agent Native Implement grant: %s" % exc, file=sys.stderr)
            sys.exit(2)
        sys.exit(0)

    try:
        check_tool(data)
    except Block as b:
        print(BOUNDARY.format(reason=str(b)), file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        print(BOUNDARY.format(reason="guard failure, failing closed (%s: %s)" % (type(exc).__name__, exc)), file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
