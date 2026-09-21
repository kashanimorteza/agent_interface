---
name: my-interface-agent-native
description: Use when the Human explicitly invokes /my-interface-agent-native to synchronize the Human-owned Agent Module under .interface/agent/ into this Claude Code project. Never invoke on your own, from another Skill, hook, agent, or startup routine.
disable-model-invocation: true
---

# Agent Native Sync (Claude Code)

## Overview

This Skill is the **only** process allowed to read the Agent Module (`.interface/agent/`). On every invocation it reads the complete, current Agent Module and realizes every declaration as project-scoped Claude Code artifacts under `.claude/` (and `.mcp.json` when a Connection needs it). The Agent Module is Human-owned and always authoritative; every artifact this Skill writes is a derived realization, never a second authority.

Every invocation is a **full synchronization**. An existing artifact, a previous run, or an artifact that looks current never permits skipping the read, reconcile, or verify steps.

## Authorization

The Human's direct invocation of `/my-interface-agent-native` is standing authorization for every additive, project-scoped Native change described here. Create, update, save, and verify without asking whether you may save or whether each change is approved.

Pause an item only for: credentials, external trust, authentication, broader authority than project scope, an irreversible action, or a Native capability that cannot realize the declaration. Report the exact reason and continue with independent items.

## Never

- Write, rename, delete, or reformat anything under `.interface/agent/`. Read it only.
- Read Target sources (`.interface/target/` or the Target's own files). Target Understanding is not needed.
- Run any `git` command, or inspect Git status, history, branches, diffs, tracked state, deleted files, or earlier versions. Never restore or compare against past project state.
- Choose or change Implementation decisions, project code, dependencies, or `.interface/config/`.
- Install plugins, packages, MCP servers, or external capabilities.
- Change user settings (`~/.claude/`), machine settings, or credentials.
- Invent, narrow, widen, or re-authorize a declaration. Restate in Claude Code idiom only when needed for Claude Code to apply it, keeping meaning, scope, ownership, and authority.
- Remove unrelated Native content, or overwrite Native metadata the Agent Module does not own (for example `enabledPlugins`, `outputStyle`, or Human-added permissions in `.claude/settings.json`).
- Turn an Operation Component into a Skill because it exists in the Implementation Module. Only entries in the Skill catalog are Skills.

## Procedure

### Step 1 — Read the complete Agent Module

Read fully, in this order, before touching any artifact:

1. `.interface/agent/agent.md` — Module structure and shared meaning.
2. Discover the Component directories under `.interface/agent/` from the filesystem. Do not use a hardcoded list; new or unfamiliar Components are still required.
3. For each Component: `<component>/<component>.md` (portable meaning and mandatory Principles), then `<component>/<component>.yaml` (current declarations and selections). Follow each YAML file's `policy`, `resolution`, `read_order`, and `content_map` sections to read `content` correctly.
4. Any file those sources explicitly reference (for example Personality contracts, bridge files, or an Operation Component's `<component>.md` and `<component>.yaml` under `.interface/implementation/` when a Skill entry names it as its definition). Read only what is referenced.
5. `.interface/interface.md` only when navigation is needed. It is a map, not a source.

### Step 2 — Enumerate the Skill catalog

List every entry in `.interface/agent/skill/skill.yaml`. Each entry is one required synchronization item:

- Its declared Operation Component Definition and Preferences are the source of its **meaning**.
- Its Agent-side bridge is the source of its **invocation and Native boundary**.

No entry may be skipped because it is unfamiliar, already present, or not the coordinating Skill. The coordinating Skill selection affects invocation and coordination only. If the catalog declares this Skill itself, reconcile that entry's invocation and boundary; its procedure remains defined by `.interface/foundation/agent-native-sync.md`.

### Step 3 — Map each declaration to a Claude Code mechanism

Before choosing a destination, confirm the mechanism against Claude Code's current documented conventions (use the `claude-code-guide` agent or official docs if unsure). Default map:

| Declaration | Claude Code mechanism | Project-scoped artifact |
|---|---|---|
| Skill (each catalog entry) | Skill | `.claude/skills/<name>/SKILL.md` (+ supporting files) |
| Rule | Rules / memory | `.claude/rules/<name>.md`, or `CLAUDE.md` when always-on |
| Permission | Permission policy | `permissions` in `.claude/settings.json` |
| Command | Skill invoked as `/<name>` | `.claude/skills/<name>/SKILL.md` |
| Tool | Tool allow/deny, hook | `permissions` or `hooks` in `.claude/settings.json`, scripts in `.claude/hooks/` |
| Connection | MCP server | `.mcp.json` (never store credentials; pause for them) |
| Context | Memory / rules | `CLAUDE.md`, `.claude/rules/` |
| Runtime choice | Settings | `.claude/settings.json` (model, env, mode) |
| Personality | Agent or output style body | System prompt of the owning `.claude/agents/<name>.md`, or `CLAUDE.md` section |
| Agent Instance | Subagent | `.claude/agents/<name>.md` |

Use the mechanism that matches the concept. Do not force every concept into a Skill. If no mechanism exists, report the item as **unsupported** or **approximated** with the exact difference.

### Step 4 — Reconcile each declaration

For every declaration, including explicit empty categories:

1. Identify the mechanism and target path.
2. Read the existing artifact completely when one exists.
3. Compare declaration to artifact: meaning, scope, ownership, boundaries, mandatory Principles.
4. Create the artifact when missing; update it when stale. Keep an existing artifact only after comparing it against the current sources.
5. Preserve Native metadata and compatible content the Agent Module does not own. Merge JSON settings; never replace the file wholesale.
6. Re-read the written artifact and confirm it matches the declaration.

Work item by item. A blocked item stops only that item.

### Step 5 — Verify and report

Re-read every artifact touched or confirmed. Then report using this shape:

```
Sources read:
- <each Agent Module file and referenced file, full path>

Realizations:
| Declaration | Mechanism | Artifact | Result | Difference |
| <name> | <mechanism> | <path> | created / updated / already current / approximated / unsupported / blocked | <exact difference, or —> |

Skill catalog: <n> declared, <n> realized, <list any not realized with reason>

Verification: re-read confirmed faithful synchronization: yes / no (<which items failed>)

Overall: successful / incomplete (<reason>)
```

Overall is **successful** only when the complete current Agent Module was read and every required declaration was realized and verified. Never state that a Native artifact is authoritative over the Agent Module.

## Red Flags — stop and re-read the Procedure

- "The skill directory already exists, so it's current."
- "This Component wasn't here last time, skip it."
- "I'll check `git diff` to see what changed."
- "The Target's code will tell me what this Rule means."
- "State is an Operation Component, so it needs a Skill."
- "I'll ask before saving each file."
- "This Component is empty, nothing to report."

Each of these violates the Foundation File. Return to Step 1.
