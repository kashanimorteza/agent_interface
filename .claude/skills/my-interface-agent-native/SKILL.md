---
name: my-interface-agent-native
description: Agent Native Sync for Claude Code. Reads the complete Human-owned Agent Module under .interface/agent/ and realizes every declaration (Components, Skills, Rules, Permissions, Commands, Tools, Connections, Context, Runtime choices, Personalities, Agent Instances) as project-scoped Claude Code artifacts, then verifies and reports. Invoked only by the Human as /my-interface-agent-native.
disable-model-invocation: true
---

# Agent Native Sync (Claude Code)

This Skill is the Agent Native Sync Skill for this project. It is the **only** process authorized to read the Agent Module (`.interface/agent/`) for Native realization. It transfers the Human's portable Agent definition into Claude Code and makes Claude Code apply it wherever Claude Code has a corresponding mechanism.

Invocation: the Human runs `/my-interface-agent-native` with no mode or numeric argument. Every invocation is a **full synchronization**. The existence of this Skill or of any previously generated Native artifact never satisfies an invocation and never permits skipping creation, reconciliation, or verification.

## Authority

- The Agent Module is Human-owned and **read-only**. Never create, edit, move, or delete anything under `.interface/agent/`.
- The Human's direct invocation of this Skill is standing authorization for every additive, project-scoped Claude Code change within this procedure. Create, update, save, and verify the required Native artifacts **without asking** for per-change approval.
- Pause an item only for: credentials, external trust, authentication, broader authority, an irreversible action, or a declaration Claude Code cannot realize. Stop that item, record the exact reason, and continue independent items when safe.
- A Native artifact is never a second authority. The Agent Module stays authoritative.

## Never

- Read or try to understand Target sources (`.interface/target/` or the Target codebase). Target Understanding is never needed.
- Inspect Git status, history, branches, diffs, tracked state, deleted files, or earlier versions; never restore, compare, or recover from Git or any past project state.
- Choose or change Implementation decisions.
- Install plugins, packages, or external capabilities.
- Change application dependencies, project code, `.interface/config/`, credentials, user-level settings (`~/.claude/`), or machine settings.
- Create new Agent declarations, narrow a declaration's scope, or silently change its authority.
- Remove unrelated Native content.
- Rely on a hardcoded Component list or on results of an earlier synchronization run.

## Procedure

### 1. Confirm current instructions

Read `.interface/foundation/agent-native-sync.md` in full. Every synchronization runs against its current instructions. If it now differs from this Skill, follow the Foundation File and report the difference.

### 2. Understand the complete Agent Module (before changing anything)

Read in full, read-only:

1. `.interface/agent/agent.md` — the Module's structure and shared meaning.
2. Every Component directory under `.interface/agent/`, discovered from the Module itself (list the directory; do not assume names). For each Component read `<component>/<component>.md` (portable meaning and Principles) and `<component>/<component>.yaml` (current declarations and selections).
3. Every file explicitly referenced by those sources.

`.interface/interface.md` may be consulted only as a navigation map when needed. Nothing else is required.

Record every declaration, including explicit **empty** categories and any Component that is new or unfamiliar. Preserve meaning, scope, ownership, boundaries, and mandatory Principles exactly as declared.

### 3. Enumerate Skill Contracts

Before realizing any Skill, list **every** Contract in `.interface/agent/skill/contracts/`. Each Contract is one required synchronization item:

- Its named Operation Component Definition and Preferences are the source of its **meaning**.
- The Contract is the source of its **invocation** and **Native boundary**.
- No declared Skill may be skipped because it is unfamiliar, already present, or not the coordinating Skill. The coordinating Skill selection affects invocation and coordination only.
- An Operation Component with **no** Contract (e.g. State when not declared as a Skill) must **not** be turned into a Skill merely because it exists in the Implementation Module.

When a Contract references an Operation Component Definition or Preferences outside `.interface/agent/`, read that referenced file because it is explicitly referenced — and only that file.

### 4. Learn the Native mechanisms

Confirm Claude Code's current documented mechanisms, file conventions, invocation rules, and limitations before choosing destinations (use the `claude-code-guide` agent or official docs when uncertain). Candidate project-scoped mechanisms to verify:

| Declaration | Likely Claude Code mechanism |
|---|---|
| Skill | `.claude/skills/<name>/SKILL.md` (frontmatter: `name`, `description`, optional `disable-model-invocation`, `allowed-tools`, `argument-hint`) |
| Command | Skill invoked as `/<name>` (or `.claude/commands/<name>.md`) |
| Rule / Context | `CLAUDE.md` at project root and/or `.claude/rules/*.md` (optionally path-scoped) |
| Permission | `permissions` (`allow` / `ask` / `deny`) in `.claude/settings.json` |
| Tool | Tool allow-lists in settings, Skill `allowed-tools`, or subagent `tools` |
| Connection | `.mcp.json` at project root (no credentials written; reference env vars) |
| Runtime choice | Project `.claude/settings.json` keys (e.g. `model`, `env`, `hooks`) |
| Personality | `.claude/output-styles/<name>.md` and/or subagent system prompts |
| Agent Instance | `.claude/agents/<name>.md` subagents |
| Hook-like behavior | `hooks` in `.claude/settings.json` with scripts in `.claude/hooks/` |

Use the mechanism that fits; do not force every concept into a Skill. Restate a declaration in Claude Code's idiom only when needed for Claude Code to apply it, preserving meaning, scope, ownership, and authority.

### 5. Realize each declaration

For **each** declared Component, capability, and Skill Contract:

1. Identify the corresponding Claude Code mechanism.
2. Read the existing Native realization completely when one exists.
3. Compare the declaration with that realization.
4. Create or update the Native artifact when missing or stale. Existing or apparently current artifacts are still reconciled against current sources.
5. Preserve Native metadata and compatible Native content the Agent Module does not own (e.g. unrelated keys in `.claude/settings.json`, unrelated sections in `CLAUDE.md`). Merge; do not overwrite wholesale.
6. Re-read the result and judge whether the declaration was realized faithfully.

If Claude Code has no equivalent mechanism, mark the item **unsupported** or **approximated** and state the exact difference. Never invent, narrow, or re-scope.

Every generated artifact that restates Agent Module content must note that it is a Native realization synchronized from `.interface/agent/` and that the Agent Module remains authoritative. Generated artifacts (other Skills, subagents, rules, hooks, context) must **not** instruct anything to read `.interface/agent/` directly; they use the synchronized Native realization only.

### 6. Verify

Re-read every created or updated Native artifact. Confirm each matches its source declaration and that no file under `.interface/agent/` was modified.

## Output

Report:

- The Agent Module sources read (every path).
- For each declaration and each Skill Contract: the Native mechanism and artifact path used.
- Status per item: **created**, **updated**, **already current**, **approximated**, **unsupported**, or **blocked**.
- The exact difference for every approximated or unsupported item, and the exact reason for every blocked item.
- Whether re-reading the Native artifacts confirmed faithful synchronization.

Overall result is **successful** only when the complete current Agent Module was read and every required declaration was realized and verified. Never claim a Native artifact is authoritative over the Agent Module.
