---
name: my-interface-agent-native
description: Agent Native Sync for Agent Interface. Reads the complete Human-owned Agent Module under .interface/agent/ and realizes it in Claude Code (skills, rules, permissions, commands, tools, connections, context, runtime choices, personalities, subagents). Run only when the Human explicitly invokes /my-interface-agent-native.
disable-model-invocation: true
---

# Agent Native Sync — Claude Code

This Skill is the Claude Code realization of the Agent Interface Foundation File `agent-native-sync.md`. It is the only process authorized to read the Agent Module for Native realization. It transfers the Human's portable Agent definition into Claude Code.

Invocation is `/my-interface-agent-native` with no mode or numeric argument. Ignore any arguments passed.

Every invocation is a **full synchronization** against the current Agent Module. The existence of this Skill, of previously generated Claude Code artifacts, or of an earlier run never satisfies an invocation and never permits skipping creation, reconciliation, or verification.

## Authority

- The Agent Module (`.interface/agent/`) is Human-owned. Read it **read-only**. Never create, edit, move, or delete anything under `.interface/agent/`.
- The Human's explicit invocation is standing authorization for every additive, project-scoped Claude Code change within this Skill's scope. Create, update, save, and verify the required artifacts without asking per change.
- Pause an item only for: credentials, external trust, authentication, broader authority, an irreversible action, or a declaration Claude Code cannot realize. Report the exact reason, then continue with independent items when safe.
- A Claude Code artifact is never a second authority. The Agent Module stays authoritative.

## Do not

- Read or try to understand Target sources (`.interface/target/` content or the application source it describes).
- Inspect Git status, history, branches, diffs, tracked state, deleted files, or earlier versions; restore, compare, or recover anything from Git or any past project state.
- Choose or change Implementation decisions.
- Install plugins, packages, MCP servers, or other external capabilities.
- Change application dependencies, project code, `.interface/config/` records, credentials, user settings (`~/.claude/`), or machine settings.
- Create Agent declarations that the Agent Module does not contain, narrow a declaration's scope, or change its authority.
- Remove Claude Code content unrelated to the Agent Module.

## Step 1 — Source Understanding (before changing anything)

Read these in full, discovering them from the Agent Module itself (never from a hardcoded list or a previous run):

1. `.interface/agent/agent.md` — Agent Module structure and shared meaning.
2. Every Component directory under `.interface/agent/`: its `<component>/<component>.md` (portable meaning and Principles) and `<component>/<component>.yaml` (current declarations, selections, empty categories).
3. Every file explicitly referenced by those sources (for example Operation Component Definitions and Preferences under `.interface/implementation/`, Foundation Schemas, or personality files). Read only what is referenced.
4. Enumerate **every** Contract in `.interface/agent/skill/contracts/` before realizing any Skill. Each Contract is one required synchronization item:
   - the Operation Component Definition and Preferences it names are the source of its **meaning**;
   - the Contract is the source of its **invocation** and **Claude Code boundary**.
   - An Operation Component with no Contract (for example State when not declared as a Skill) must **not** be turned into a Skill.

`.interface/interface.md` may be consulted only as a navigation map when needed. Interface or Target Understanding is not required.

Build a declaration inventory: one row per declared Component/capability/entry, including explicit empty categories.

## Step 2 — Learn Claude Code mechanisms

Before choosing a destination, confirm Claude Code's current documented mechanism for each concept (use the `claude-code-guide` agent or official docs when unsure). Default mapping, all project-scoped:

| Agent concept | Claude Code mechanism | Artifact |
|---|---|---|
| Skill | Project skill | `.claude/skills/<name>/SKILL.md` (+ supporting files) |
| Command | Skill invoked as `/<name>` (commands merged into skills) | `.claude/skills/<name>/SKILL.md` |
| Rule | Project rule memory (optional `paths:` frontmatter for scope) | `.claude/rules/<name>.md` |
| Context | Project memory | `CLAUDE.md` or `.claude/rules/` |
| Permission / Tool access | Permission rules; per-skill `allowed-tools`; per-agent `tools` | `.claude/settings.json` → `permissions`; frontmatter |
| Hook | Hook configuration | `.claude/settings.json` → `hooks` |
| Connection | Project MCP configuration | `.mcp.json` (block if credentials/trust needed) |
| Runtime choice | Settings / frontmatter (`model`, etc.) | `.claude/settings.json` or skill/agent frontmatter |
| Personality | Output style | `.claude/output-styles/<name>.md` + `outputStyle` setting |
| Agent Instance / Agent Role | Subagent | `.claude/agents/<name>.md` |
| Installed capability | Plugin / marketplace already enabled | Verify only; never install |

Use a non-Skill mechanism whenever one fits; do not force every concept into a Skill. Restate a declaration in Claude Code idiom only when necessary, preserving meaning, scope, ownership, and authority.

## Step 3 — Realize each declaration

For every inventory row:

1. Identify the corresponding Claude Code mechanism.
2. Read the existing artifact completely when it exists.
3. Compare the declaration with that artifact.
4. Create or update the artifact when missing or stale.
5. Preserve Claude Code metadata and compatible content that the Agent Module does not own (for example unrelated keys in `.claude/settings.json`, unrelated skills, rules, or agents).
6. Re-read the result and judge whether the declaration was realized faithfully.

### Declared Skills (every Contract)

- Create the skill when missing.
- On **every** run, reconstruct its Agent-owned content from the current Contract plus every Source it names. Preserve only Claude Code metadata and compatible non-Agent-owned content.
- Verify the reconstructed skill against the Contract and every Source. It is `already current` only when verification finds no omitted, weakened, or contradictory requirement. File existence, matching name, matching Contract, or a prior sync never establishes `already current`. Any mismatch means `updated`, even if the Contract is unchanged.
- The coordinating Skill selection affects invocation and coordination only; it never makes another declared Skill optional.
- Realized skills and subagents must operate from their synchronized content and must not read, resolve, or depend on `.interface/agent/` sources at runtime.

### No equivalent mechanism

Report the declaration as `unsupported` or `approximated` and state the exact difference. Never silently skip an unfamiliar or newly added Component.

## Step 4 — Report

Report:

- every Agent Module source read;
- for each declaration: Claude Code mechanism, artifact path, and result — `created`, `updated`, `already current`, `approximated`, `unsupported`, or `blocked`;
- the exact difference for every approximation or unsupported item, and the exact reason for every blocked item;
- whether re-reading the artifacts confirmed faithful synchronization.

The overall result is **successful** only when the complete current Agent Module was read and every required declaration was realized and verified. Never claim that a Claude Code artifact is authoritative over the Agent Module.
