---
name: my-interface-agent-native
description: Agent Native Sync for Claude Code. Reads the complete Human-owned Agent Module under .interface/agent/ and fully realizes, reconciles, and verifies it as Claude Code Native artifacts (skills, rules, permissions, commands, tools, connections, context, runtime, personalities, agent instances). Invoked only by the Human as /my-interface-agent-native with no arguments.
disable-model-invocation: true
---

# Agent Native Sync — Claude Code

You are the Agent Native Sync Skill for Claude Code in this project. You are the **only** process authorized to read the Agent Module (`.interface/agent/`) for Native realization. You transfer the Human's portable Agent definition into Claude Code's own mechanisms. This procedure is self-contained; you do not need any other file to understand how to synchronize.

## Invocation

- Run only when the Human explicitly invokes `/my-interface-agent-native`. It takes no mode or numeric argument; ignore any argument text beyond noting it in the report.
- Every invocation is a **full synchronization** against the current Agent Module and this procedure. The existence of this Skill or of previously generated Native artifacts never satisfies an invocation and never permits skipping creation, reconciliation, or verification.
- The Human's direct invocation is standing authorization for every additive, project-scoped Native change within this scope. Create, update, save, and verify the required artifacts without asking for per-change approval. Pause only for credentials, external trust, authentication, broader authority, an irreversible action, or a missing Native capability.

## Authority and Boundaries

- The Agent Module is Human-owned and **read-only**. Never create, edit, move, or delete anything under `.interface/agent/`.
- Native artifacts are realizations, never a second authority. The Agent Module always wins.
- Do **not**:
  - read or try to understand Target sources (`.interface/target/` or the application code it describes);
  - inspect Git status, history, branches, diffs, tracked state, deleted files, or earlier versions; restore, compare, or recover anything from Git or any past state;
  - choose or change Implementation decisions;
  - install plugins, packages, MCP servers, or other external capabilities;
  - change application dependencies, project code, the Interface Config module, credentials, user settings (`~/.claude/…`), or machine settings;
  - create new Agent declarations that the Agent Module does not contain;
  - remove Native content the Agent Module does not own.
- `.interface/interface.md` may be consulted only as a navigation map when needed. Interface Understanding and Target Understanding are not required.

## Step 1 — Read the Agent Module in full

Before changing any Native artifact, read completely:

1. `.interface/agent/agent.md` — the Module's structure and shared meaning.
2. Every Component the Module itself declares or contains: discover them by listing `.interface/agent/` and by following `agent.md`. Do **not** rely on a hardcoded component list or on an earlier run. For each Component read both:
   - `.interface/agent/<component>/<component>.md` — portable meaning and Principles;
   - `.interface/agent/<component>/<component>.yaml` — current declarations and selections.
3. Every file explicitly referenced by those Agent sources (for example Operation Component Definitions and Preferences referenced by Skill entries). Read referenced files only as far as the reference requires; never extend into Target sources.

Record every source path you read. Form a complete Understanding of the Module — meaning, scope, ownership, boundaries, mandatory Principles — before Step 3.

## Step 2 — Enumerate the Skill catalog

Before realizing any Skill, enumerate **every** entry in `.interface/agent/skill/skill.yaml`.

- Each entry is one required synchronization item. Its declared Operation Component Definition and Preferences are the source of its meaning; its Agent-side bridge is the source of its invocation and Native boundary.
- No entry may be skipped because it is unfamiliar, already present, or not the coordinating Skill. The coordinating Skill selection affects invocation and coordination only.
- An Operation Component with no entry in this catalog (e.g. State when not declared as a Skill) must **not** be turned into a Skill merely because it exists in the Implementation Module.

## Step 3 — Map declarations to Claude Code mechanisms

Before choosing a destination, confirm Claude Code's current documented conventions (use the `claude-code-guide` agent or official docs if unsure). Default project-scoped mappings:

| Declared concept | Claude Code mechanism | Project artifact |
|---|---|---|
| Skill | Skill | `.claude/skills/<name>/SKILL.md` (+ supporting files in that folder) |
| Command | Skill invoked as `/name` (set `disable-model-invocation: true` when only the Human invokes it) | `.claude/skills/<name>/SKILL.md` |
| Rule | Project memory rules | `.claude/rules/<name>.md` (use `paths:` frontmatter for scoped rules) |
| Context | Project memory | `CLAUDE.md` / `.claude/rules/*.md`, or skill supporting files |
| Permission | Permission rules | `permissions` in `.claude/settings.json` (allow / ask / deny) |
| Tool | Tool allow/deny lists | `allowed-tools` in skill or agent frontmatter; `permissions` in `.claude/settings.json` |
| Connection | MCP server config | `.mcp.json` — only for servers already available without install, credentials, or new trust; otherwise **blocked** |
| Runtime choice | Settings / hooks | `.claude/settings.json` keys (e.g. `model`, `env`, `hooks`) and scripts in `.claude/hooks/` |
| Personality | Output style or agent system prompt | `.claude/output-styles/<name>.md`, or the body of an agent file |
| Agent Instance | Subagent | `.claude/agents/<name>.md` |

Use the mechanism that fits; do not force every concept into a Skill. Restate a declaration in Claude Code's idiom only when necessary, preserving its meaning, scope, ownership, and authority. Never invent content, narrow scope, or silently change authority. Explicitly empty categories are still realized (e.g. confirm and report that no artifact is required, or that an existing managed artifact reflects emptiness) — never silently skipped.

When editing shared files (`.claude/settings.json`, `CLAUDE.md`, `.mcp.json`): change only the entries the Agent Module owns; preserve every other key, entry, and Native metadata exactly.

## Step 4 — Realize each declaration

For every declared Component or capability, and for every Skill catalog entry:

1. Identify the corresponding Claude Code mechanism (Step 3).
2. Read the existing Native realization completely when one exists.
3. Compare the declaration with that realization.
4. Create the artifact when missing; update it when stale. Reconcile even when it looks current.
5. Preserve Native metadata and compatible Native content that the Agent Module does not own.
6. Re-read the result and judge whether the declaration was realized faithfully.

Never silently skip an unfamiliar or newly added Component. If Claude Code has no equivalent mechanism, mark the item **unsupported** or **approximated** and state the exact difference. If an item needs Human input, broader authority, external trust, authentication, or a missing capability, stop that item, record the exact reason as **blocked**, and continue with independent items when safe.

Generated artifacts must not instruct any other Skill, agent, startup routine, hook, or context to read `.interface/agent/` directly. Other Native operations depend only on the synchronized realization.

## Step 5 — Verify and report

Re-read every Native artifact you created or touched. Then report:

1. **Sources read** — every Agent Module path read.
2. **Per declaration** (one row each, including every Skill catalog entry): declaration → Claude Code mechanism → artifact path → status: `created` | `updated` | `already current` | `approximated` | `unsupported` | `blocked`.
3. **Exact difference** for every approximated or unsupported item, and the exact reason for every blocked item.
4. **Verification** — whether re-reading confirmed faithful synchronization.
5. **Overall result** — `successful` only when the complete current Agent Module was read and every required declaration was realized and verified; otherwise `incomplete`, listing what remains. Never claim a Native artifact is authoritative over the Agent Module.
