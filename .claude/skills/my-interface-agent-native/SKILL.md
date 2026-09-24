---
name: my-interface-agent-native
description: Agent Native Sync for Claude Code. Reads the complete Human-owned Agent Module under .interface/agent/ and realizes every declaration (Components, Skills, Rules, Permissions, Commands, Tools, Connections, Context, Runtime choices, Personalities, Agent Instances) as project-scoped Claude Code artifacts, then verifies and reports. Run only on explicit Human invocation of /my-interface-agent-native.
disable-model-invocation: true
---

# Agent Native Sync (Claude Code)

This Skill is the Agent Native Sync Skill for this project. It is the **only** reader of the Agent Module (`.interface/agent/`). It transfers the Human's portable Agent definition into Claude Code, the selected Agent Native.

The Human invokes it only as `/my-interface-agent-native`, with no mode or numeric argument. Ignore any arguments if supplied.

Every invocation is a **full synchronization** against the current Agent Module. The existence of this Skill or of any previously generated Native artifact never satisfies an invocation and never permits skipping creation, reconciliation, or verification.

## Authority and boundaries

- The Agent Module is Human-owned. Read it **read-only**. Never create, edit, move, or delete any file or directory under `.interface/agent/`.
- The Human's explicit invocation is standing authorization for every **additive, project-scoped** Claude Code change within this Skill's scope. Create, update, save, and verify the required artifacts **without asking** for approval of individual changes.
- Pause or stop an item only for: credentials, external trust, authentication, broader authority, an irreversible action, or a Native capability that cannot realize the declaration. Independent items continue when safe.
- No other Skill, Agent Instance, coordinator, startup routine, Context, or Runtime operation may read, resolve, or depend on Agent Module sources. Generated Native artifacts must be self-contained and must never instruct anything to read `.interface/agent/`.
- A Native artifact is never a second authority. Never claim a Native artifact overrides the Agent Module.

This Skill must **not**:

- read or try to understand Target sources (`.interface/target/` and the project's application code);
- inspect Git status, history, branches, diffs, tracked state, deleted files, or earlier versions;
- restore, compare, or recover anything from Git or any past project state;
- choose or change Implementation decisions;
- install plugins, packages, MCP servers, or other external capabilities (including enabling a plugin not already enabled);
- change application dependencies, project code, Interface Config (`.interface/config/`), credentials, user settings (`~/.claude/…`), or machine settings;
- create new Agent declarations, or narrow, widen, or reinterpret an existing one; or
- remove Native content that the Agent Module does not own.

## Procedure

Track progress with a task list: one task per phase, then one task per declared item.

### Phase 1 — Understand the complete Agent Module (no Native changes yet)

Read these **in full** (never partial reads, never excerpts):

1. `.interface/agent/agent.md` — structure and shared meaning of the Agent Module.
2. Discover the current Components from the Agent Module itself (list `.interface/agent/` and follow what `agent.md` declares). Do **not** rely on a hardcoded component list or on any earlier run.
3. For each applicable Component: `.interface/agent/<component>/<component>.md` (portable meaning and Principles) and `.interface/agent/<component>/<component>.yaml` (current declarations and selections).
4. Every file explicitly referenced by those Agent sources, recursively.
5. Enumerate **every** Contract in `.interface/agent/skill/contracts/`. Each Contract is one required synchronization item:
   - its named Operation Component Definition and Preferences are the source of its **meaning**;
   - the Contract is the source of its **invocation and Native boundary**.
   Read every Source each Contract names, in full.
6. Only if navigation is necessary, `.interface/interface.md` may be consulted as a map. Interface Understanding and Target Understanding are not required.

Build an inventory before changing anything: for each Component and declaration record its meaning, scope, ownership, boundaries, mandatory Principles, and current selection. Include **explicit empty categories** as items. Include every unfamiliar or newly added Component as an item.

Rules for Skills inventory:

- Every Contract yields exactly one declared Skill entry. None may be skipped because it is unfamiliar, already present, or not the coordinating Skill.
- The coordinating Skill selection affects invocation and coordination only; it does not make any other declared Skill optional.
- An Operation Component without a Contract (for example State when it is not declared as a Skill) must **not** become a Skill merely because it exists in the Implementation Module.

### Phase 2 — Learn the Native mechanisms

Before choosing destinations, confirm Claude Code's current documented mechanisms, conventions, invocation rules, and limitations (use the `claude-code-guide` agent or official Claude Code docs when unsure). Default project-scoped mapping:

| Declaration | Claude Code mechanism | Project artifact |
|---|---|---|
| Skill | Skill | `.claude/skills/<name>/SKILL.md` (+ supporting files) |
| Command | Skill invoked by `/name` (legacy: `.claude/commands/`) | `.claude/skills/<name>/SKILL.md` |
| Rule | Modular memory rules | `.claude/rules/<name>.md` (optional `paths` frontmatter for scoping) |
| Context | Project memory | `CLAUDE.md` or `.claude/CLAUDE.md`; imports via `@path` |
| Permission | Permission rules | `.claude/settings.json` → `permissions.allow` / `ask` / `deny` / `defaultMode` |
| Tool | Built-in tool access, Skill `allowed-tools`, subagent `tools` | settings / frontmatter |
| Connection | MCP servers | `.mcp.json` (project scope) |
| Runtime choice | Settings (`model`, `env`, hooks, etc.) | `.claude/settings.json`; hook scripts in `.claude/hooks/` |
| Personality | Output style or subagent system prompt | `.claude/output-styles/<name>.md` + `outputStyle` setting |
| Agent Instance | Subagent | `.claude/agents/<name>.md` |

Use the mechanism that fits each declaration; do not force every concept into a Skill. If Claude Code has no equivalent, the item is `unsupported` or `approximated` (state the exact difference). Never write to user or machine settings (`~/.claude/…`, `.claude/settings.local.json`); a declaration that can only be realized there is `blocked` (broader authority).

### Phase 3 — Realize each declaration

For every inventory item:

1. Identify the corresponding Claude Code mechanism.
2. Read the existing Native realization **completely** when one exists.
3. Compare the declaration with that realization.
4. Create or update the artifact when it is missing or stale. Restate the declaration in Claude Code's idiom only as far as needed to apply it, preserving meaning, scope, ownership, and authority.
5. Preserve Native metadata and compatible Native content that the Agent Module does not own. For JSON settings, merge — never replace unrelated keys or entries.
6. Re-read the result and record whether the declaration was realized faithfully.

For every declared **Skill** entry specifically:

- Create the Native Skill when missing.
- On **every** run, reconstruct its Agent-owned content from the current Contract and every Source it names; keep only Native metadata and compatible non-owned content.
- The generated Skill must be self-contained: it must not reference or read `.interface/agent/`.
- Verify the reconstructed result against the Contract and every Source. It is `already current` **only** when verification finds no omitted, weakened, or contradictory requirement. File existence, matching name, matching Contract, or a prior run never establishes `already current`. Any mismatch → `updated`, even if the Contract is unchanged.
- Do not realize this Skill (`my-interface-agent-native`) from a Contract unless a Contract declares it; never alter its own synchronization procedure from Agent Module content.

If an item needs Human input, credentials, authentication, external trust, broader authority, an irreversible action, or a missing Native capability: stop that item, record `blocked` with the exact reason, and continue with independent items.

### Phase 4 — Verify

Re-read every created or updated artifact and every `already current` artifact. Confirm, per item, that nothing was omitted, weakened, contradicted, or widened, and that no generated artifact depends on the Agent Module. Validate edited JSON parses.

## Output

Report:

1. **Sources read** — every Agent Module file read (full paths).
2. **Per declaration** — one row each (including every Contract, empty categories, and unfamiliar Components): declaration → Native mechanism → artifact path → result (`created` | `updated` | `already current` | `approximated` | `unsupported` | `blocked`).
3. **Differences** — the exact difference for every `approximated` or `unsupported` item, and the exact reason for every `blocked` item.
4. **Verification** — whether re-reading the Native artifacts confirmed faithful synchronization.
5. **Overall result** — `successful` only when the complete current Agent Module was read and every required declaration was realized and verified; otherwise `incomplete`, listing what remains. Never state that a Native artifact is authoritative over the Agent Module.
