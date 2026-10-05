#!/usr/bin/env python3
"""Interface boundary guard and Agent Native Sync read grant for Claude Code hooks.

Synchronized Native realization of the Permission guarantees
`interface-boundary-guard` (blocking, fail closed) and `agent-native-read-grant`
(blocking, fail closed). Regenerated only by /my-interface-agent-native.

Modes (run through interface-guard.sh, which turns any crash into a block):
  pretooluse  PreToolUse: block Agent Module reads and searches without a valid
              grant, block every non-Human invocation of Agent Native Sync, and
              block every direct Interface mutation. Exit 2 blocks.
  grant       UserPromptSubmit: record a session- and prompt-bound grant when the
              Human directly invokes /my-interface-agent-native; otherwise revoke.
  revoke      Stop / SessionEnd: revoke the session's grant.
"""
import fnmatch
import json
import os
import re
import shlex
import subprocess
import sys
import time

SYNC = "my-interface-agent-native"
SYNC_PROMPT = re.compile(r"^\s*/" + SYNC + r"(?:\s|$)")
SYNC_EXPANDED = re.compile(r"<command-name>\s*/?" + SYNC + r"\s*</command-name>|"
                           r"^\s*(?:---\s*\nname:\s*" + SYNC + r"\b|# Agent Native Sync \(Claude Code\))")
MESSAGE = (
    "interface-boundary-guard: {reason} The Agent Module (.interface/agent/) may be read only "
    "within the prompt created by the Human's direct /" + SYNC + " invocation, and the "
    ".interface/ tree is read-only to every Agent action. Do not retry through another tool, "
    "path form, script, or alias. If a synchronized Runtime artifact is missing, report Runtime "
    "drift and ask the Human to run /" + SYNC + "."
)


class Block(Exception):
    pass


# ---------------------------------------------------------------- paths


class Ctx:
    def __init__(self, data):
        self.data = data
        project = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
        self.project = os.path.realpath(project)
        self.cwd = os.path.realpath(data.get("cwd") or self.project)
        self.iface = os.path.join(self.project, ".interface")
        self.agent = os.path.join(self.iface, "agent")
        self.grants = os.path.join(self.project, ".claude", "hooks", ".grants")
        self._granted = None

    def resolve(self, path, base=None):
        path = os.path.expanduser(str(path))
        if not os.path.isabs(path):
            path = os.path.join(base or self.cwd, path)
        return os.path.realpath(os.path.normpath(path))

    @property
    def granted(self):
        if self._granted is None:
            self._granted = grant_valid(self)
        return self._granted


def within(path, base):
    return path == base or path.startswith(base.rstrip(os.sep) + os.sep)


def related(path, target):
    """True when path is target, inside it, or an ancestor of it."""
    return within(path, target) or within(target, path)


def glob_enters(base, pattern, target, dot_rule):
    """True when a glob evaluated from base could name target or a path inside it."""
    if not os.path.isabs(pattern):
        pattern = os.path.join(base, pattern)
    pattern = os.path.normpath(pattern)
    parts = [p for p in pattern.split(os.sep) if p]
    goal = [p for p in target.split(os.sep) if p]
    for i, want in enumerate(goal):
        if i >= len(parts):
            return False
        comp = parts[i]
        if comp == "**" and not dot_rule:
            return True
        if dot_rule and want.startswith(".") and not comp.startswith("."):
            return False
        if "{" in comp:
            options = re.findall(r"\{([^}]*)\}", comp)
            if any(fnmatch.fnmatchcase(want, re.sub(r"\{[^}]*\}", o, comp, count=1))
                   for group in options for o in group.split(",")):
                continue
            return False
        if not fnmatch.fnmatchcase(want, comp):
            return False
    return True


# ---------------------------------------------------------------- grant


def grant_file(ctx, session_id):
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", str(session_id))
    return os.path.join(ctx.grants, safe + ".json")


def is_subagent(data):
    if data.get("agent_id") or data.get("agent_type"):
        return True
    return "/subagents/" in str(data.get("transcript_path") or "")


def grant_valid(ctx):
    data = ctx.data
    session_id = data.get("session_id")
    if not session_id or is_subagent(data):
        return False
    try:
        with open(grant_file(ctx, session_id), encoding="utf-8") as handle:
            grant = json.load(handle)
    except (OSError, ValueError):
        return False
    if grant.get("session_id") != session_id:
        return False
    granted_prompt, prompt = grant.get("prompt_id"), data.get("prompt_id")
    if granted_prompt and prompt and granted_prompt != prompt:
        return False
    return True


def revoke(ctx, session_id):
    if not session_id:
        return
    try:
        os.remove(grant_file(ctx, session_id))
    except FileNotFoundError:
        pass


def mode_grant(data):
    ctx = Ctx(data)
    session_id = data.get("session_id")
    prompt = str(data.get("prompt") or "")
    os.makedirs(ctx.grants, exist_ok=True)
    ignore = os.path.join(ctx.grants, ".gitignore")
    if not os.path.exists(ignore):
        with open(ignore, "w", encoding="utf-8") as handle:
            handle.write("*\n")
    if session_id and (SYNC_PROMPT.search(prompt) or SYNC_EXPANDED.search(prompt)):
        path = grant_file(ctx, session_id)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump({"session_id": session_id, "prompt_id": data.get("prompt_id"),
                       "created": int(time.time())}, handle)
        os.replace(tmp, path)
    else:
        revoke(ctx, session_id)


def mode_revoke(data):
    revoke(Ctx(data), data.get("session_id"))


# ---------------------------------------------------------------- file and search tools

READ_TOOLS = {"Read", "NotebookRead", "LS", "View"}
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def tool_path(tool_input):
    for key in ("file_path", "notebook_path", "path"):
        if tool_input.get(key):
            return tool_input[key]
    return None


def check_write_path(ctx, raw):
    path = ctx.resolve(raw)
    if within(path, ctx.iface):
        raise Block("Direct Interface mutation is blocked.")
    if within(path, ctx.grants):
        raise Block("The Agent Native Sync grant store is written only by its own hook.")


def check_read_path(ctx, raw):
    if within(ctx.resolve(raw), ctx.agent) and not ctx.granted:
        raise Block("Agent Module read outside the Agent Native Sync prompt.")


def check_grep(ctx, tool_input):
    root = ctx.resolve(tool_input.get("path") or ctx.cwd)
    if ctx.granted or not related(root, ctx.agent):
        return None
    if within(root, ctx.agent):
        raise Block("Agent Module search outside the Agent Native Sync prompt.")
    glob = str(tool_input.get("glob") or "")
    if not glob:
        updated = dict(tool_input)
        updated["glob"] = "!**/.interface/agent/**"
        return {"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "interface-boundary-guard: search scope excludes the Agent Module.",
            "updatedInput": updated}}
    if glob.startswith("!") and exclusion_covers(glob):
        return None
    raise Block("This search's scope includes the Agent Module. Narrow `path` to a directory "
                "outside .interface/agent/, or omit `glob` so the guard can exclude it.")


def check_glob(ctx, tool_input):
    root = ctx.resolve(tool_input.get("path") or ctx.cwd)
    if ctx.granted:
        return
    if within(root, ctx.agent):
        raise Block("Agent Module search outside the Agent Native Sync prompt.")
    pattern = str(tool_input.get("pattern") or "")
    if pattern and glob_enters(root, pattern, ctx.agent, dot_rule=False) and \
            not pattern.split("/")[0] == "**":
        raise Block("Agent Module search outside the Agent Native Sync prompt.")


# ---------------------------------------------------------------- shell commands

EXCLUSIONS = [
    r"--exclude(?:-dir)?[= ]\s*['\"]?[^\s'\";|&]*['\"]?",
    r"--ignore(?:-dir|-file)?[= ]\s*['\"]?[^\s'\";|&]*['\"]?",
    r"--extend-exclude[= ]\s*['\"]?[^\s'\";|&]*['\"]?",
    r"--ignore-path[= ]\s*['\"]?[^\s'\";|&]*['\"]?",
    r"(?:-g|--glob|--iglob)(?:=|\s+)?['\"]?![^\s'\";|&]*['\"]?",
    r"['\"]?:(?:\(exclude\)|!|\^)[^\s'\";|&]*['\"]?",
    r"(?:-not|!|\\!)\s+-(?:path|wholename|ipath|name)\s+['\"]?[^\s'\";|&]*['\"]?",
    r"-(?:path|wholename|name)\s+['\"]?[^\s'\";|&]*['\"]?\s+-prune",
]
EXCLUSION_RE = re.compile("|".join("(?:%s)" % p for p in EXCLUSIONS))

WRAPPERS = {"sudo", "env", "nice", "nohup", "time", "command", "builtin", "exec", "stdbuf", "ionice"}
INTERPRETERS = {"python", "python3", "python2", "node", "perl", "ruby", "php", "bash", "sh", "zsh",
                "dash", "ksh", "fish", "deno", "bun", "pwsh", "lua", "Rscript", "osascript"}
RECURSIVE_SEARCH = {"rg", "ag", "ack", "ack-grep", "ugrep", "ug", "fd", "fdfind"}
GREPS = {"grep", "egrep", "fgrep", "zgrep", "diff"}
ARCHIVERS = {"tar", "zip", "7z", "cpio", "rsync", "scp", "rclone"}
GIT_READERS = {"grep", "show", "whatchanged", "format-patch", "archive", "bundle", "difftool",
               "range-diff"}
GIT_TREE_WRITERS = {"checkout", "switch", "restore", "reset", "clean", "stash", "merge", "pull",
                    "rebase", "cherry-pick", "revert", "am", "apply", "mv", "rm", "read-tree",
                    "checkout-index"}
GIT_READ_ONLY = {"status", "log", "show", "diff", "ls-files", "ls-tree", "blame", "grep",
                 "rev-parse", "cat-file", "describe", "shortlog", "rev-list", "check-ignore",
                 "check-attr", "branch", "remote", "config", "help", "version", "reflog"}
READ_ONLY = {"cat", "head", "tail", "less", "more", "bat", "batcat", "ls", "tree", "wc", "grep",
             "egrep", "fgrep", "zgrep", "rg", "ag", "ack", "find", "stat", "file", "diff", "cmp",
             "md5sum", "sha1sum", "sha256sum", "sha512sum", "cksum", "du", "readlink",
             "realpath", "basename", "dirname", "test", "[", "[[", "echo", "printf", "true",
             "false", "pwd", "cd", "pushd", "popd", "sort", "uniq", "cut", "tr", "nl", "column",
             "fold", "jq", "yq", "awk", "gawk", "sed", "strings", "xxd", "od", "hexdump",
             "base64", "tac", "rev", "comm", "join", "paste", "expand", "git", "graphify",
             "fd", "fdfind", "ugrep", "ug"}
FORMATTERS = {"prettier", "black", "ruff", "isort", "autopep8", "yapf", "eslint", "mdformat",
              "yamlfmt", "dprint", "biome", "gofmt", "rustfmt", "clang-format", "shfmt",
              "markdownlint", "markdownlint-cli2", "taplo", "autoflake", "pyupgrade"}
MUTATORS = {"rm", "rmdir", "unlink", "shred", "mv", "cp", "install", "ln", "touch", "truncate",
            "mkdir", "chmod", "chown", "chgrp", "setfacl", "dd", "tee", "patch", "sed", "perl",
            "rsync"}
LISTERS = {"find", "rg", "grep", "egrep", "fgrep", "ls", "fd", "fdfind", "ag", "ack"}
REDIRECT = re.compile(r"(?:^|[^<>&0-9])(?:\d?>>?|&>>?|>\|)\s*['\"]?([^\s'\";|&<>()]+)")
CD_RE = re.compile(r"(?:^|[;&|(\s])(?:cd|pushd)\s+['\"]?([^\s'\";&|)]+)")
GIT_INDEX_ONLY = {"add", "commit", "push", "fetch", "tag", "notes"}


def split_segments(text):
    """Split a shell command on ; | || && & and newlines outside quotes."""
    segments, current, quote, i = [], [], None, 0
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\" and quote == '"' and i + 1 < len(text):
                current.append(text[i:i + 2])
                i += 2
                continue
            if ch == quote:
                quote = None
            current.append(ch)
        elif ch in "'\"":
            quote = ch
            current.append(ch)
        elif ch == "\\" and i + 1 < len(text):
            current.append(text[i:i + 2])
            i += 2
            continue
        elif ch in ";\n|" or (ch == "&" and not (current and current[-1] in "<>") and
                              not text[i + 1:i + 2] == ">"):
            segments.append("".join(current))
            current = []
            if text[i:i + 2] in ("||", "&&"):
                i += 1
        else:
            current.append(ch)
        i += 1
    segments.append("".join(current))
    return [s for s in segments if s.strip()]


def exclusion_covers(span):
    """True when an exclusion expression excludes the whole Agent Module or Interface."""
    value = re.sub(r"['\"\\]", "", span).strip()
    value = re.sub(r"\s+-prune$", "", value)
    value = re.split(r"[=\s]", value, maxsplit=1)[-1] if re.match(r"^-", value) else value
    value = re.sub(r"^(?:-(?:path|wholename|ipath|name)\s+)", "", value.strip())
    value = re.sub(r"^(?::\(exclude\)|:!|:\^|!)", "", value.strip())
    value = re.sub(r"^(?:\./)+", "", value)
    value = re.sub(r"^\*\*?/", "", value)
    value = re.sub(r"(?:/\*\*?|/\*|/)+$", "", value)
    value = value.rstrip("*")
    return value in (".interface", ".interface/agent", "agent", "interface/agent")


def split_tokens(text):
    try:
        return shlex.split(text, comments=False, posix=True)
    except ValueError:
        return text.split()


def program(tokens):
    """Return (program, remaining tokens) after env assignments and wrappers."""
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tok):
            i += 1
            continue
        name = os.path.basename(tok)
        if name in WRAPPERS:
            i += 1
            while i < len(tokens) and tokens[i].startswith("-"):
                i += 1
            continue
        if name == "timeout":
            i += 1
            while i < len(tokens) and tokens[i].startswith("-"):
                i += 1
            i += 1
            continue
        if name in ("npx", "pnpx", "bunx") or (name in ("pnpm", "yarn", "npm") and
                                                i + 1 < len(tokens) and tokens[i + 1] in ("exec", "dlx")):
            i += 2 if name in ("pnpm", "yarn", "npm") else 1
            while i < len(tokens) and tokens[i].startswith("-"):
                i += 1
            continue
        return name, tokens[i + 1:]
    return "", []


def operands(args):
    return [a for a in args if a and not a.startswith("-")]


def existing_paths(ctx, args):
    found = []
    for arg in operands(args):
        path = ctx.resolve(arg)
        if os.path.exists(path):
            found.append(path)
    return found


def has_flag(args, short=None, long=()):
    for a in args:
        if a in long or any(a.startswith(l + "=") for l in long):
            return True
        if short and re.match(r"^-[A-Za-z]+$", a) and any(c in a[1:] for c in short):
            return True
    return False


def git_sub(args):
    i = 0
    root = None
    while i < len(args):
        a = args[i]
        if a in ("-C", "-c", "--git-dir", "--work-tree", "--namespace"):
            if a == "-C" and i + 1 < len(args):
                root = args[i + 1]
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        return a, args[i + 1:], root
    return "", [], root


def git_pathspecs(ctx, rest, base):
    if "--" in rest:
        specs = rest[rest.index("--") + 1:]
    else:
        specs = [a for a in operands(rest) if os.path.exists(ctx.resolve(a, base))]
    return [ctx.resolve(s, base) for s in specs if not s.startswith(":")]


def git_quiet(ctx, *args):
    try:
        result = subprocess.run(["git", "-C", ctx.project] + list(args), capture_output=True,
                                text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    return result


def interface_untouched_by(ctx, ref):
    """True when the Interface has no local change and ref (if any) has identical content."""
    status = git_quiet(ctx, "status", "--porcelain", "--", ".interface")
    if status is None or status.returncode != 0 or status.stdout.strip():
        return False
    if ref:
        diff = git_quiet(ctx, "diff", "--quiet", ref, "--", ".interface")
        if diff is None or diff.returncode != 0:
            return False
    return True


def agent_has_worktree_changes(ctx):
    status = git_quiet(ctx, "status", "--porcelain", "--", ".interface/agent")
    return status is None or status.returncode != 0 or bool(status.stdout.strip())


def check_bash(ctx, command):
    if re.search(r"hooks/+\.grants", command):
        raise Block("The Agent Native Sync grant store is written only by its own hook.")

    has_exclusion = any(exclusion_covers(m.group(0)) for m in EXCLUSION_RE.finditer(command))
    scrubbed = EXCLUSION_RE.sub(" ", command)
    plain = re.sub(r"['\"\\]", "", scrubbed)
    parsed = []
    for seg in split_segments(scrubbed):
        prog, args = program(split_tokens(seg))
        parsed.append((seg, prog, args))
    progs = {p for _, p, _ in parsed}
    resolved = [ctx.resolve(tok) for _, _, args in parsed for tok in operands(args)
                if "/" in tok or tok.startswith((".", "~"))]

    # ---- Interface mutation (blocked even within the Agent Native Sync prompt)
    mentions_iface = bool(re.search(r"\.interface(?![A-Za-z0-9_-])", plain))
    for seg, prog, args in parsed:
        for tok in split_tokens(seg):
            if any(c in tok for c in "*?[{") and glob_enters(ctx.cwd, tok, ctx.iface, dot_rule=True):
                mentions_iface = True
    for target in CD_RE.findall(scrubbed):
        if within(ctx.resolve(target), ctx.iface):
            mentions_iface = True
    if within(ctx.cwd, ctx.iface) or any(within(p, ctx.iface) for p in resolved):
        mentions_iface = True

    for target in REDIRECT.findall(scrubbed):
        if target.startswith("&") or target == "/dev/null":
            continue
        path = ctx.resolve(target)
        if within(path, ctx.iface) or within(path, ctx.grants):
            raise Block("Direct Interface mutation is blocked.")

    if mentions_iface:
        for seg, prog, args in parsed:
            if not read_only(prog, args):
                raise Block("Commands that reference the Interface may use only read-only programs "
                            "(`%s` is not one); use the Read tool for Interface files." % (prog or seg.strip()))

    for seg, prog, args in parsed:
        check_bulk_mutation(ctx, seg, prog, args, parsed, has_exclusion)

    # ---- Agent Module reads (allowed only within the Agent Native Sync prompt)
    if ctx.granted:
        return
    if within(ctx.cwd, ctx.agent) or any(within(p, ctx.agent) for p in resolved):
        raise Block("Agent Module access outside the Agent Native Sync prompt.")
    if re.search(r"interface/+agent(?![A-Za-z0-9_-])", plain) or \
            (within(ctx.cwd, ctx.iface) and "agent" in plain):
        raise Block("Agent Module access outside the Agent Native Sync prompt.")
    for match in re.finditer(r"\.interface/+([^\s/;|&<>()]*)", plain):
        comp = match.group(1)
        if comp and any(c in comp for c in "*?[{") and glob_enters(ctx.iface, comp, ctx.agent, dot_rule=False):
            raise Block("Agent Module access outside the Agent Native Sync prompt.")
    for seg, prog, args in parsed:
        for tok in split_tokens(seg):
            if any(c in tok for c in "*?[{") and glob_enters(ctx.cwd, tok, ctx.agent, dot_rule=True):
                raise Block("Agent Module access outside the Agent Native Sync prompt.")
    for target in CD_RE.findall(scrubbed):
        if within(ctx.resolve(target), ctx.iface):
            raise Block("Changing into the Interface directory is blocked; use full paths outside the Agent Module.")
    for seg, prog, args in parsed:
        if prog in INTERPRETERS and "interface" in seg and "agent" in seg:
            raise Block("Agent Module access outside the Agent Native Sync prompt.")
        check_recursive_read(ctx, prog, args, progs, has_exclusion)


def read_only(prog, args):
    if prog not in READ_ONLY:
        return False
    if prog == "find" and any(a in ("-delete", "-exec", "-execdir", "-ok", "-okdir", "-fprint",
                                     "-fprint0", "-fprintf", "-fls") for a in args):
        return False
    if prog == "sed" and any(a.startswith("-i") or a.startswith("--in-place") for a in args):
        return False
    if prog == "yq" and any(a in ("-i", "--inplace") for a in args):
        return False
    if prog in ("awk", "gawk") and any(">" in a or "system" in a for a in args):
        return False
    if prog in ("sort", "tree") and has_flag(args, short="o", long=("--output",)):
        return False
    if prog == "uniq" and len(operands(args)) > 1:
        return False
    if prog == "git":
        sub, _, _ = git_sub(args)
        return sub in GIT_READ_ONLY or sub in GIT_INDEX_ONLY
    if prog == "graphify":
        sub = operands(args)[:1]
        return bool(sub) and sub[0] in ("query", "path", "explain", "affected", "diagnose")
    return True


def check_bulk_mutation(ctx, seg, prog, args, parsed, has_exclusion):
    block = Block("This command could write inside the Interface; exclude .interface/ or target exact paths outside it.")
    paths = [ctx.resolve(a) for a in operands(args)]
    if prog in ("rm", "rmdir", "shred", "chmod", "chown", "chgrp", "setfacl") and \
            (prog == "rmdir" or has_flag(args, short="rR", long=("--recursive",))):
        if any(within(ctx.iface, p) for p in paths):
            raise block
    if prog in MUTATORS:
        for tok in operands(args):
            if any(c in tok for c in "*?[{") and glob_enters(ctx.cwd, tok, ctx.iface, dot_rule=True):
                raise block
    if prog == "find" and any(a in ("-delete", "-exec", "-execdir", "-ok", "-okdir") for a in args):
        roots = []
        for a in args:
            if a.startswith("-") or a in ("(", "!"):
                break
            roots.append(ctx.resolve(a))
        if any(within(ctx.iface, r) for r in (roots or [ctx.cwd])) and not has_exclusion:
            raise block
    if prog == "xargs":
        inner = next((os.path.basename(a) for a in args
                      if os.path.basename(a) in MUTATORS or os.path.basename(a) in FORMATTERS), "")
        if inner:
            for _, other, other_args in parsed:
                if other in LISTERS:
                    roots = existing_paths(ctx, other_args) or [ctx.cwd]
                    if any(within(ctx.iface, r) for r in roots) and not has_exclusion:
                        raise block
    if prog in FORMATTERS and formatter_writes(prog, args):
        roots = existing_paths(ctx, args) or [ctx.cwd]
        if any(within(ctx.iface, r) for r in roots) and not has_exclusion:
            raise block
    if prog == "git":
        sub, rest, root = git_sub(args)
        if sub in GIT_TREE_WRITERS and not git_tree_write_safe(ctx, sub, rest, root, has_exclusion):
            raise block


def git_tree_write_safe(ctx, sub, rest, root, has_exclusion):
    """True when a working-tree-changing git command cannot change the Interface."""
    base = ctx.resolve(root) if root else None
    words = operands(rest)
    if sub in ("checkout", "switch") and has_flag(rest, long=("-b", "-B", "-c", "-C", "--orphan",
                                                                "--create", "--force-create")) \
            and len(words) <= 1 and "--" not in rest:
        return True
    if sub == "reset" and not has_flag(rest, long=("--hard", "--merge", "--keep")):
        return True
    if sub == "stash" and words[:1] in (["list"], ["show"], ["drop"], ["clear"], ["branch"]):
        return words[:1] != ["branch"]
    if sub in ("apply", "am"):
        for path in existing_paths(ctx, rest):
            try:
                with open(path, encoding="utf-8", errors="replace") as handle:
                    if "interface/" in handle.read():
                        return False
            except OSError:
                return False
        return bool(existing_paths(ctx, rest)) and interface_untouched_by(ctx, None)
    if sub in ("mv", "rm"):
        return not any(related(s, ctx.iface) for s in git_pathspecs(ctx, rest, base) or [ctx.cwd])
    specs = git_pathspecs(ctx, rest, base)
    if specs and not any(within(ctx.iface, s) for s in specs):
        return True
    if has_exclusion:
        return True
    if not interface_untouched_by(ctx, None):
        return False
    refs = [a for a in words if not os.path.exists(ctx.resolve(a, base))]
    if sub in ("checkout", "switch", "reset"):
        if "--" in rest or not refs:
            return True
        return len(refs) == 1 and interface_untouched_by(ctx, refs[0])
    if sub == "restore":
        return True
    if sub == "stash":
        if words[:1] in (["pop"], ["apply"]):
            ref = words[1] if len(words) > 1 else "stash@{0}"
            return not git_changes_interface(ctx, ref + "^1", ref)
        return True
    if sub in ("merge", "rebase") and len(refs) == 1:
        return not git_changes_interface(ctx, "HEAD..." + refs[0])
    if sub in ("cherry-pick", "revert") and refs and all("." not in r for r in refs):
        return not any(git_changes_interface(ctx, r + "^", r) for r in refs)
    return False


def git_changes_interface(ctx, *revisions):
    diff = git_quiet(ctx, "diff", "--quiet", *revisions, "--", ".interface")
    return diff is None or diff.returncode != 0


def formatter_writes(prog, args):
    if prog in ("black", "isort", "rustfmt", "autoflake", "pyupgrade"):
        return not has_flag(args, long=("--check", "--diff"))
    if prog == "ruff":
        sub = operands(args)[:1]
        if sub == ["format"]:
            return not has_flag(args, long=("--check", "--diff"))
        return has_flag(args, long=("--fix",))
    if prog in ("prettier", "biome"):
        return has_flag(args, short="w", long=("--write", "--apply", "--fix"))
    if prog in ("autopep8", "yapf", "clang-format"):
        return has_flag(args, short="i", long=("--in-place",))
    if prog in ("gofmt", "shfmt"):
        return has_flag(args, short="w", long=("--write",))
    if prog in ("eslint", "markdownlint", "markdownlint-cli2"):
        return has_flag(args, long=("--fix",))
    if prog in ("mdformat", "yamlfmt", "dprint", "taplo"):
        return not has_flag(args, long=("--check", "-lint", "-dry"))
    return True


def check_recursive_read(ctx, prog, args, progs, has_exclusion):
    roots = None
    if prog in RECURSIVE_SEARCH:
        roots = existing_paths(ctx, args) or [ctx.cwd]
    elif prog in GREPS and (has_flag(args, short="rR", long=("--recursive", "--dereference-recursive"))
                            or "recurse" in " ".join(args)):
        roots = existing_paths(ctx, args) or [ctx.cwd]
    elif prog == "find" and (any(a in ("-exec", "-execdir", "-ok", "-okdir", "-fprint", "-fprintf")
                                 for a in args) or "xargs" in progs):
        roots = []
        for a in args:
            if a.startswith("-") or a in ("(", "!"):
                break
            roots.append(ctx.resolve(a))
        roots = roots or [ctx.cwd]
    elif prog in ARCHIVERS or (prog == "cp" and has_flag(args, short="rRa", long=("--recursive", "--archive"))):
        roots = existing_paths(ctx, args)
    elif prog == "graphify":
        sub = operands(args)[:1]
        if sub and sub[0] in ("extract", "watch", "add"):
            ignore = os.path.join(ctx.project, ".graphifyignore")
            try:
                with open(ignore, encoding="utf-8") as handle:
                    if re.search(r"(?m)^\s*/?\.interface(?:/agent)?/?\s*$", handle.read()):
                        return
            except OSError:
                pass
            roots = existing_paths(ctx, args[1:]) or [ctx.cwd]
    elif prog == "git":
        sub, rest, root = git_sub(args)
        base = ctx.resolve(root) if root else None
        reader = sub in GIT_READERS
        if sub == "log" and has_flag(rest, short="pu", long=("--patch", "--full-diff")):
            reader = True
        if sub == "stash" and operands(rest)[:1] == ["show"] and has_flag(rest, short="pu", long=("--patch",)):
            reader = True
        if sub == "diff":
            revisions = [a for a in operands(rest) if "--" not in rest or rest.index(a) < rest.index("--")]
            revisions = [a for a in revisions if not os.path.exists(ctx.resolve(a, base))]
            reader = bool(revisions) or has_flag(rest, long=("--cached", "--staged")) or \
                agent_has_worktree_changes(ctx)
        if not reader:
            return
        specs = git_pathspecs(ctx, rest, base)
        roots = specs or [base or ctx.cwd]
        if specs and not any(related(s, ctx.agent) for s in specs):
            return
    if not roots:
        return
    if any(within(r, ctx.agent) for r in roots):
        raise Block("Agent Module search outside the Agent Native Sync prompt.")
    if any(within(ctx.agent, r) for r in roots) and not has_exclusion:
        raise Block("This command reads or searches a tree that includes the Agent Module. Narrow it "
                    "to paths outside .interface/agent/, or exclude it explicitly (for example "
                    "`rg -g '!.interface/agent'`, `grep -r --exclude-dir=agent`, or "
                    "`git ... -- . ':!.interface/agent'`).")


# ---------------------------------------------------------------- entry


def mode_pretooluse(data):
    ctx = Ctx(data)
    tool = str(data.get("tool_name") or "")
    tool_input = data.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        tool_input = {}

    if tool in ("Skill", "SlashCommand"):
        name = str(tool_input.get("skill") or tool_input.get("command") or tool_input.get("name") or "")
        name = (name.strip().lstrip("/").split() or [""])[0]
        if name == SYNC or name.endswith(":" + SYNC):
            raise Block("Agent Native Sync can be invoked only directly by the Human.")
        return None
    if tool in WRITE_TOOLS:
        raw = tool_path(tool_input)
        if raw:
            check_write_path(ctx, raw)
        return None
    if tool in READ_TOOLS:
        raw = tool_path(tool_input)
        if raw:
            check_read_path(ctx, raw)
        return None
    if tool == "Grep":
        return check_grep(ctx, tool_input)
    if tool == "Glob":
        check_glob(ctx, tool_input)
        return None
    if tool == "Bash":
        check_bash(ctx, str(tool_input.get("command") or ""))
        return None
    if tool.startswith("mcp__"):
        text = json.dumps(tool_input)
        if re.search(r"interface/+agent", text) and not ctx.granted:
            raise Block("Agent Module access outside the Agent Native Sync prompt.")
    return None


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    data = json.load(sys.stdin)
    if mode == "grant":
        mode_grant(data)
        return 0
    if mode == "revoke":
        mode_revoke(data)
        return 0
    if mode != "pretooluse":
        print("interface-guard: unknown mode %r" % mode, file=sys.stderr)
        return 1
    try:
        output = mode_pretooluse(data)
    except Block as block:
        print(MESSAGE.format(reason=str(block)), file=sys.stderr)
        return 2
    if output:
        print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
