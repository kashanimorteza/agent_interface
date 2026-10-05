---
name: my-interface-agent-native
description: Agent Native Sync. Reads the complete Human-owned Agent Module under .interface/agent/ (read-only) and realizes every current declaration in Claude Code's native mechanisms. Invoked by the Human only, as /my-interface-agent-native with no arguments.
disable-model-invocation: true
---

# Agent Native Sync (Claude Code)

This Skill is the Agent Native Sync Skill for this project. Claude Code is the selected Agent Native. This Skill is the only process authorized to read the Agent Module (`.interface/agent/`) for Native realization. It transfers the Human's portable Agent definition into Claude Code's native mechanisms.

The Human invokes this Skill only as `/my-interface-agent-native`, with no mode or numeric argument. Ignore any arguments that are passed.

## Invocation semantics

- Every explicit invocation is a **full synchronization** against the current Agent Module and the current procedure in this Skill.
- The existence of this Skill, or of any Native artifact generated earlier, never satisfies an invocation. It never permits skipping creation, reconciliation, or verification.
- Do not rely on any earlier synchronization run, a hardcoded component list, or memory of past Agent Module contents.

## Purpose

Make Claude Code understand and apply the Human's declared Components, Skills, Rules, Permissions, Commands, Tools, Connections, Context, Runtime choices, Personalities, and Agent Instances wherever Claude Code provides a corresponding mechanism.

## Authority and boundaries

- The Agent Module is Human-owned. Read it read-only. Never create, modify, move, or delete any file or directory under `.interface/agent/`. Only the Human may change Agent Definitions and Preferences.
- Invoking this Skill directly is the Human's standing authorization for every additive, project-scoped Native change within this Skill's scope. Create, update, save, and verify the required Native artifacts without asking for approval of individual changes. Pause only for:
  - credentials;
  - external trust;
  - authentication;
  - broader authority;
  - an irreversible action; or
  - a declaration that Claude Code has no capability to realize.
- No other Skill, Agent Instance, coordinator, startup routine, Context, hook, or Runtime operation may read, resolve, or depend directly on Agent Module sources. Native artifacts produced here must not instruct anything to read `.interface/agent/`. They must use the synchronized Native realization instead.
- A Native artifact is never a second authority. The Agent Module is always authoritative.

This Skill must NOT:

- read or try to understand Target sources (`.interface/target/` or the application source code it governs);
- inspect Git status, history, branches, diffs, tracked state, deleted files, or earlier versions;
- restore, compare, or recover anything from Git or from any past project state;
- choose or change Implementation decisions;
- install plugins, packages, MCP servers, or other external capabilities;
- change application dependencies, project code, Config, credentials, user settings (`~/.claude/`), or machine settings;
- create new Agent declarations; or
- remove unrelated Native content.

If a declaration needs Human input, broader authority, external trust, authentication, or a capability Claude Code lacks, stop that item and report the exact reason. Continue with independent declarations when that is safe.

## Procedure

### 1. Source understanding (before changing anything)

Read these sources in full. Do not skim or read partially.

1. `.interface/agent/agent.md` for the Agent Module's structure and shared meaning.
2. Discover the current Components from the Agent Module itself: from `agent.md` and the directory listing of `.interface/agent/`. For each applicable Component, read:
   - `.interface/agent/<component>/<component>.md` for portable meaning and Principles;
   - `.interface/agent/<component>/<component>.yaml` for current declarations and selections.
3. Any file explicitly referenced by those Agent sources. Follow references transitively when they are explicitly made.
4. Enumerate **every** Contract in `.interface/agent/skill/contracts/` before realizing any Skill. Each Contract is one required synchronization item:
   - the Contract defines the Skill's invocation and Native boundary;
   - the Operation Component Definition and Preferences it names define the Skill's meaning. Read every Source the Contract names, in full.

You do not need Interface Understanding for synchronization. When you need navigation, you may consult `.interface/interface.md` as a map only. Never read Target sources.

Build a complete Understanding of the whole Agent Module before modifying any Native artifact. Preserve the declared meaning, scope, ownership, boundaries, and mandatory Principles.

### 2. Learn the Native mechanisms

Before choosing a destination, confirm Claude Code's current documented mechanisms, file conventions, invocation rules, and limitations. Use the claude-code-guide agent or the official documentation when you are unsure. The typical project-scoped mappings are:

| Agent concept | Claude Code mechanism (project scope) |
|---|---|
| Skill | `.claude/skills/<name>/SKILL.md` (YAML frontmatter `name`, `description`, and optionally `disable-model-invocation`, `allowed-tools`, `argument-hint`) plus supporting files |
| Command | A Skill invoked as `/<name>`; legacy `.claude/commands/<name>.md` |
| Rule / Context / Personality | `CLAUDE.md`, `.claude/CLAUDE.md`, or `.claude/rules/*.md` |
| Permission | `permissions` (`allow` / `ask` / `deny`) in `.claude/settings.json` |
| Tool / Connection | `.mcp.json` (project MCP servers) or settings. Never install anything; report as blocked if installation or credentials are required |
| Runtime choice | Project `.claude/settings.json` keys (for example `model` or `env`), or hooks in `.claude/hooks/` registered in settings |
| Agent Instance | `.claude/agents/<name>.md` subagent definitions |

These mappings are defaults. Use another mechanism when Claude Code's documentation says it fits a declaration better. Do not force every concept into a Skill.

### 3. Realize each declaration

For each declared Component or capability:

1. Identify the Claude Code mechanism that corresponds to the declaration.
2. If a Native realization exists, read it completely.
3. Compare the declaration with that realization.
4. Create or update the Native artifact when it is missing or stale.
5. Preserve Native metadata and compatible Native content that the Agent Module does not own, such as unrelated settings keys, unrelated CLAUDE.md sections, and other Skills.
6. Re-read the result and judge whether the declaration was realized faithfully.

Realize every current declaration. Never silently skip an unfamiliar or newly added Component. If Claude Code has no equivalent mechanism, report the declaration as `unsupported` or `approximated` and state the exact difference. Never invent a declaration, narrow its scope, or silently change its authority. You may restate a declaration in Claude Code's idiom only when Claude Code needs that to apply it, and the restatement must preserve meaning, scope, ownership, and authority.

**Declared Skills (one per Contract):**

- Create the Native Skill when it is missing.
- On **every** synchronization, reconstruct its Agent-owned content from the current Contract and every Source it names. Keep only Native metadata and compatible content that the Agent Module does not own.
- Verify the reconstructed result against the Contract and every Source.
- A Native Skill is `already current` only when that verification finds no omitted, weakened, or contradictory requirement. A matching file, name, or Contract, or a prior synchronization, never establishes `already current` by itself. Any mismatch means `updated`, even when the Contract is unchanged.
- The coordinating Skill selection affects only invocation and coordination. It does not make any other declared Skill optional. No declared Skill may be skipped because it is unfamiliar, already present, or not the coordinating Skill.
- Do not turn an Operation Component that has no Contract into a Skill merely because it exists in the Implementation Module. State is an example when it is not declared as a Skill.
- Native Skills you generate must be self-contained. They must not instruct any later read of `.interface/agent/`.

### 4. Verify

Re-read every Native artifact you created or updated. Also re-read every artifact you judged `already current`. Confirm that each one faithfully realizes its declaration and contains no instruction that reads the Agent Module.

## Output

Report:

- every Agent Module source read;
- for each declaration, the Claude Code mechanism and the artifact path used;
- the result for each declaration: `created`, `updated`, `already current`, `approximated`, `unsupported`, or `blocked`. Report every declared Skill entry, including entries that are current, unsupported, approximated, or blocked;
- the exact difference for every approximation or unsupported declaration, and the exact reason for every blocked item; and
- whether re-reading the Native artifacts confirmed faithful synchronization.

The overall result is **successful** only when the complete current Agent Module was read and every required declaration was realized and verified. Never claim that a Native artifact is authoritative over the Agent Module.
