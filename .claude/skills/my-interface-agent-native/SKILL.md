---
name: my-interface-agent-native
description: Agent Native Sync for Claude Code. Performs a full synchronization of the Human-owned Agent Module (.interface/agent/) into this project's Claude Code realization (skills, rules, permissions, commands, tools, connections, context, runtime, personalities, agent instances). Invoked only explicitly by the Human as /my-interface-agent-native, with no arguments.
disable-model-invocation: true
---

# Agent Native Sync (Claude Code)

This Skill transfers the Human's portable Agent definition in the Agent Module into Claude Code, the selected Agent Native. It is the **only** process authorized to read the Agent Module for Native realization. It is invoked only by an explicit Human command `/my-interface-agent-native`, with no mode or numeric argument. Ignore any arguments passed.

The Agent Module is the sole authority. Every Native artifact this Skill writes is a realization, never a second authority.

## Invariants

- **Full sync every time.** Every invocation is a full synchronization against the current Agent Module and this procedure. The existence of this Skill or of any previously generated Native artifact never satisfies the invocation and never permits skipping creation, reconciliation, or verification.
- **Read-only Agent Module.** Never create, edit, move, or delete anything under `.interface/agent/`. Only the Human changes Agent Definitions and Preferences.
- **Standing authorization.** The Human's explicit invocation authorizes every additive, project-scoped Native change within this Skill's scope. Create, update, save, and verify Native artifacts without asking for per-change approval. Pause an item only for credentials, external trust, authentication, broader authority, an irreversible action, or a missing Native capability.
- **Forbidden actions.** Do not:
  - read or understand Target sources (`.interface/target/` or the Target code it describes);
  - inspect Git status, history, branches, diffs, tracked state, deleted files, or earlier versions;
  - restore, compare, or recover anything from Git or any past project state;
  - choose or change Implementation decisions;
  - install plugins, packages, or external capabilities;
  - change application dependencies, project code, Interface Config (`.interface/config/`), credentials, user settings (`~/.claude/`), or machine settings;
  - create new Agent declarations, narrow a declaration's scope, or change its authority; or
  - remove unrelated Native content.
- **No downstream dependency on sources.** Native artifacts produced here must not instruct any other Skill, Agent Instance, coordinator, startup routine, Context, or Runtime operation to read, resolve, or depend on `.interface/agent/`. They carry the synchronized meaning themselves.

## Procedure

Track progress with a todo list: one item per phase, then one item per declaration discovered in Phase 2.

### Phase 1 — Source Understanding (read everything before changing anything)

1. Read `.interface/agent/agent.md` completely for the Agent Module's structure and shared meaning.
2. Discover the current Components from the Agent Module itself (list `.interface/agent/` and follow what `agent.md` declares). Do not rely on a hardcoded component list or on any earlier synchronization run.
3. For each applicable Component, read completely:
   - `.interface/agent/<component>/<component>.md` — portable meaning and Principles;
   - `.interface/agent/<component>/<component>.yaml` — current declarations and selections.
4. Read completely every file explicitly referenced by those Agent sources (including Operation Component Definitions and Preferences referenced by Skill Contracts).
5. Only if navigation is necessary, consult `.interface/interface.md` as a map. Interface Understanding is not otherwise required. Never read Target sources.
6. Enumerate **every** Contract in `.interface/agent/skill/contracts/` before realizing any Skill. Each Contract is one required synchronization item:
   - its named Operation Component Definition and Preferences are the source of the Skill's **meaning**;
   - the Contract is the source of its **invocation** and **Native boundary**.
   No declared Skill may be skipped because it is unfamiliar, already present, or not the coordinating Skill. An Operation Component without a Contract (for example State, when not declared as a Skill) must **not** be turned into a Skill.
7. Record the list of sources read; it is part of the final report.

### Phase 2 — Inventory declarations

Build a table of every current declaration, including explicit empty categories, across: Components, Skills (one row per Contract), Rules, Permissions, Commands, Tools, Connections, Context, Runtime choices, Personalities, and Agent Instances — plus any unfamiliar or newly added Component, which must not be silently skipped. For each row note its meaning, scope, ownership, boundaries, and mandatory Principles as declared.

### Phase 3 — Learn the Native before choosing destinations

Confirm Claude Code's documented mechanisms, file conventions, invocation rules, and limitations before writing (use the `claude-code-guide` agent or official docs when unsure). Typical project-scoped mappings:

| Agent concept | Claude Code mechanism (project-scoped) |
|---|---|
| Skill | `.claude/skills/<name>/SKILL.md` (frontmatter `name`, `description`; `disable-model-invocation: true` for Human-only invocation; supporting files beside it) |
| Command | a Skill invoked as `/<name>` (or `.claude/commands/<name>.md`) |
| Rule / Context | `CLAUDE.md` at project root and/or `.claude/rules/*.md` |
| Permission | `permissions` (`allow` / `ask` / `deny`) in `.claude/settings.json` |
| Tool | tool allow/deny lists in settings, Skill `allowed-tools`, or agent `tools` |
| Connection | `.mcp.json` (credentials/auth → blocked, report exact reason) |
| Runtime choice | `model` / related keys in `.claude/settings.json`, or Skill/agent `model` |
| Personality | `.claude/output-styles/<name>.md` and `outputStyle` in project settings |
| Agent Instance | `.claude/agents/<name>.md` subagent definitions |
| Hook-shaped behavior | `hooks` in `.claude/settings.json`, scripts in `.claude/hooks/` |

Use the non-Skill mechanism when one fits; do not force every concept into a Skill. Restate a declaration in Claude Code idiom only when needed for the Native to apply it, preserving meaning, scope, ownership, and authority. If no equivalent mechanism exists, mark the item **unsupported** or **approximated** and state the exact difference.

### Phase 4 — Realize each declaration

For every row in the Phase 2 table:

1. Identify the corresponding Native mechanism and artifact path.
2. If a Native realization exists, read it completely.
3. Compare the declaration with that realization.
4. Create the artifact if missing; update it if stale. Always reconcile, even when it looks current.
5. Preserve Native metadata and compatible Native content the Agent Module does not own (e.g., existing unrelated settings keys, plugins, hooks, rules). Edit surgically; never wholesale-overwrite shared files such as `.claude/settings.json`.
6. Re-read the result and judge whether the declaration was realized faithfully.

For every declared Skill entry: create the Native Skill when missing and reconstruct its Agent-owned content from the current Contract and every Source it names on every sync. Preserve only Native metadata and compatible content the Agent Module does not own. Then verify the result against the Contract and every Source. Mark a Skill `already current` only when this verification finds no omitted, weakened, or contradictory requirement; file existence, a matching name, a matching Contract, or a previous sync never establish that result. Any mismatch requires an `updated` result even when the Contract itself is unchanged. The coordinating Skill selection affects invocation and coordination only; it does not make any other declared Skill optional. This Skill (`my-interface-agent-native`) is the sync entry point, not an Agent declaration — do not rewrite it from the Agent Module.

If an item needs Human input, broader authority, external trust, authentication, or a missing Native capability, stop that item, record the exact reason as **blocked**, and continue with independent items when safe.

### Phase 5 — Verify

Re-read every Native artifact created or updated, and every artifact judged already current, against the Phase 2 table. Confirm no file under `.interface/agent/` was modified.

## Output

Report:

- the Agent Module sources read;
- for each declaration: the Native mechanism and artifact used;
- its status: **created**, **updated**, **already current**, **approximated**, **unsupported**, or **blocked** — one result for every declared entry, including every Skill Contract;
- the exact difference for every approximation or unsupported declaration, and the exact reason for every blocked item; and
- whether re-reading the Native artifacts confirmed faithful synchronization.

The overall result is **successful** only when the complete current Agent Module was read and every required declaration was realized and verified. Never claim that a Native artifact is authoritative over the Agent Module.
