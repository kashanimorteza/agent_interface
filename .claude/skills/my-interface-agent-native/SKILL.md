---
name: my-interface-agent-native
description: Agent Native Sync for Claude Code. Reads the complete Human-owned Agent Module under .interface/agent/ and realizes every current declaration (Components, Skills, Rules, Permissions, Commands, Tools, Connections, Context, Runtime choices, Personalities, Agent Instances) as project-scoped Claude Code artifacts, then verifies and reports. Invoked only by the Human via /my-interface-agent-native.
disable-model-invocation: true
---

# Agent Native Sync — Claude Code

This Skill is the Claude Code realization of the Agent Native Sync Foundation. It is the **only** process authorized to read the Agent Module (`.interface/agent/`) for Native realization. It transfers the Human's portable Agent definition into Claude Code. The Agent Module is the sole authority; every artifact this Skill produces is a realization, never a second authority.

Invocation: the Human runs `/my-interface-agent-native` with no mode or numeric argument. Ignore any arguments if supplied. Never invoke, schedule, or chain this Skill from another process.

Every invocation is a **full synchronization** against the current Agent Module. The existence of this Skill or of any previously generated Native artifact never satisfies an invocation and never permits skipping creation, reconciliation, or verification.

## Authority and boundaries

The Human's direct invocation is standing authorization for every additive, project-scoped Claude Code change within this Skill's scope. Create, update, save, and verify the required artifacts without asking for per-change approval. Pause an item only for credentials, external trust, authentication, broader authority, an irreversible action, or a missing Claude Code capability.

Hard limits — never:

- write, rename, or delete anything under `.interface/agent/` (read-only, Human-owned);
- read or try to understand Target sources (application/project code outside `.interface/` and the Claude Code artifacts this Skill manages);
- inspect Git status, history, branches, diffs, tracked or deleted files, or earlier versions; never restore, compare, or recover from Git or any past state;
- choose or change Implementation decisions;
- install plugins, packages, MCP servers' binaries, or other external capabilities;
- change application dependencies, project code, application Config, credentials, user-level settings (`~/.claude/…`), or machine settings;
- create Agent declarations the Agent Module does not contain, narrow a declaration's scope, or change its authority;
- remove unrelated Native content (content in `.claude/`, `CLAUDE.md`, `.mcp.json`, etc. that the Agent Module does not own).

If an item needs Human input, broader authority, external trust, authentication, or a capability Claude Code lacks, stop that item, record the exact reason, and continue with independent items when safe.

## Procedure

### Step 1 — Source Understanding (read-only, complete)

Establish understanding of the entire Agent Module **before changing any Native artifact**.

1. Read `.interface/agent/agent.md` in full — the Module's structure and shared meaning.
2. Discover the current Components from the Agent Module itself (list `.interface/agent/` and follow what `agent.md` describes). Do not rely on a hardcoded component list or on any earlier run.
3. For each Component, read in full `.interface/agent/<component>/<component>.md` (portable meaning and Principles) and `.interface/agent/<component>/<component>.yaml` (current declarations and selections).
4. Read in full every file explicitly referenced by those Agent sources (e.g., Operation Component Definitions and Preferences a Skill entry points to). Follow references transitively, but never into Target sources.
5. `.interface/interface.md` may be consulted only as a navigation map when needed. Interface Understanding and Target Understanding are not required.
6. Record the list of every source read for the final report.

### Step 2 — Enumerate the Skill catalog

Before realizing any Skill, enumerate **every** entry in `.interface/agent/skill/skill.yaml`. Each entry is one required synchronization item:

- its declared Operation Component Definition and Preferences are the source of its **meaning**;
- its Agent-side bridge is the source of its **invocation and Native boundary**.

No entry may be skipped because it is unfamiliar, already present, or not the coordinating Skill. The coordinating Skill selection affects invocation and coordination only. An Operation Component with no entry in this catalog (e.g., State when not declared as a Skill) must **not** be turned into a Skill merely because it exists in the Implementation Module.

### Step 3 — Learn the Native mechanisms

Choose destinations from Claude Code's own documented mechanisms. Use the fitting mechanism per concept rather than forcing everything into a Skill. Default mapping (all project-scoped):

| Declaration | Claude Code mechanism |
|---|---|
| Skill | `.claude/skills/<name>/SKILL.md` (frontmatter `name`, `description`; `disable-model-invocation: true` when only the Human may invoke; `allowed-tools` when declared) plus supporting files in that folder |
| Command | a user-invocable Skill (`.claude/skills/<name>/SKILL.md`), which Claude Code exposes as `/<name>` |
| Rule | `.claude/rules/*.md` (optionally path-scoped via `paths` frontmatter) and/or project `CLAUDE.md` |
| Context | project `CLAUDE.md` (or `.claude/rules/*.md`) |
| Permission | `permissions.allow` / `ask` / `deny` / `defaultMode` in project `.claude/settings.json` |
| Tool | tool permissions in `.claude/settings.json`, `tools` lists on Skills/Agents, hooks in `.claude/settings.json` + `.claude/hooks/` |
| Connection | project `.mcp.json` server entries (never install binaries; never add credentials — block and report if secrets are needed) |
| Runtime choice | `model` / other runtime keys in `.claude/settings.json`, or `model` frontmatter on Skills/Agents |
| Personality | project output style `.claude/output-styles/<name>.md` and/or Agent system prompts; `outputStyle` in `.claude/settings.json` when selected |
| Agent Instance | subagent `.claude/agents/<name>.md` (frontmatter `name`, `description`, `tools`, `model`) |

If the Claude Code documentation or current behavior differs from this table, follow the Native's documented mechanism and report the difference. Native-specific paths and formats belong only in the realization, never in the Agent Module. Restate a declaration in Claude Code idiom only when necessary, preserving its meaning, scope, ownership, and authority.

Generated Native artifacts must not instruct any Skill, Agent, hook, Context, or startup routine to read or depend on `.interface/agent/`; they carry the realized content themselves.

### Step 4 — Realize each declaration

For every declared Component or capability — including explicit empty categories and any unfamiliar or newly added Component:

1. Identify the corresponding Claude Code mechanism.
2. Read the existing Native realization completely, if one exists.
3. Compare the declaration with that realization.
4. Create or update the artifact when missing or stale. For every declared Skill entry: create when missing; reconcile and update on every run when present; an apparently current Skill is still re-read against current sources.
5. Preserve Native metadata and compatible content the Agent Module does not own. When editing shared files (`settings.json`, `CLAUDE.md`, `.mcp.json`), change only the parts this declaration owns.
6. For an explicit empty category, ensure no stale Native content previously realized for that category remains **only if** it is clearly owned by this synchronization; otherwise leave it and report.
7. If no equivalent mechanism exists, mark the declaration **unsupported** or **approximated** and state the exact difference.

### Step 5 — Verify

Re-read every created or updated artifact. Confirm it faithfully realizes its declaration (meaning, scope, ownership, authority, mandatory Principles) and is valid for Claude Code (well-formed frontmatter, valid JSON). Fix and re-verify any mismatch.

### Step 6 — Report

Report:

- every Agent Module source read;
- for each declaration (one line per declared Skill entry, plus every other declaration): the Native mechanism and artifact path;
- its status: **created**, **updated**, **already current**, **approximated**, **unsupported**, or **blocked**;
- the exact difference for every approximation or unsupported item, and the exact reason for every blocked item;
- whether re-reading confirmed faithful synchronization.

Overall result is **successful** only when the complete current Agent Module was read and every required declaration was realized and verified. Never claim any Native artifact is authoritative over the Agent Module.
