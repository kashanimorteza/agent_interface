---
name: my-interface-agent-native
description: Agent Native Sync. Reads the complete Human-owned Agent Module under .interface/agent/ and realizes it in Claude Code's native mechanisms. Run only on explicit Human invocation of /my-interface-agent-native.
disable-model-invocation: true
---

# Agent Native Sync

This Skill transfers the Agent Module's portable definition of the Agent into Claude Code (the selected Agent Native). It is the only process authorized to read the Agent Module for Native realization. It is invoked only by the Human through `/my-interface-agent-native`, without a mode or numeric argument.

Every invocation is a full synchronization against the current Agent Module and the current `.interface/foundation/agent-native-sync.md`. The existence of this Skill or of any previously generated Native artifact never satisfies an invocation and never permits skipping creation, reconciliation, or verification.

## Authority and Boundaries

- The Agent Module is Human-owned. Read it read-only. Never create, change, move, or delete any file or directory under `.interface/agent/`.
- This explicit invocation is standing authorization for every additive, project-scoped Native change within this Skill's scope. Create, update, save, and verify required Native artifacts without asking for per-change approval.
- Pause an item only for credentials, external trust, authentication, broader authority, an irreversible action, or a Native capability that cannot realize the declaration. Report the exact reason and continue with independent items when safe.
- Do not:
  - read or understand Target sources (`.interface/target/` or the project's application code);
  - inspect Git status, history, branches, diffs, tracked state, deleted files, or earlier versions;
  - restore, compare, or recover anything from Git or any past project state;
  - choose or change Implementation decisions;
  - install plugins, packages, or external capabilities;
  - change application dependencies, project code, `config/`, credentials, user settings (`~/.claude/`), or machine settings;
  - create new Agent declarations; or
  - remove unrelated Native content.
- No other Skill, Agent Instance, coordinator, startup routine, Context, or Runtime operation may read, resolve, or depend directly on Agent Module sources. Native artifacts produced here must not instruct anything to read `.interface/agent/`; they carry the synchronized meaning themselves.
- A Native artifact is never a second authority. The Agent Module remains authoritative.

## Procedure

### 1. Source Understanding (before changing anything)

Read in full:

1. `.interface/agent/agent.md` for the Agent Module's structure and shared meaning.
2. Every applicable `.interface/agent/<component>/<component>.md` for portable meaning and Principles.
3. Every applicable `.interface/agent/<component>/<component>.yaml` for current declarations and selections.
4. Any file explicitly referenced by those Agent sources.

Discover Components and referenced sources from the Agent Module itself (list `.interface/agent/` and follow its own references). Never rely on a hardcoded Component list or on an earlier run. `.interface/interface.md` may be consulted only as a navigation map. Target Understanding is never needed.

Then enumerate every Contract in `.interface/agent/skill/contracts/` before realizing any Skill. Each Contract is one required synchronization item: its named Operation Component Definition and Preferences are the source of its meaning; the Contract is the source of its invocation and Native boundary. No declared Skill may be skipped because it is unfamiliar, already present, or not the coordinating Skill. An Operation Component with no Contract (for example State, when not declared as a Skill) must not be turned into a Skill merely because it exists.

Establish an Understanding of the complete Agent Module, preserving the meaning, scope, ownership, boundaries, and mandatory Principles declared by the Human, before editing any Native artifact.

### 2. Learn the Native

Before choosing destinations, confirm Claude Code's current documented mechanisms, conventions, invocation rules, and limitations. Project-scoped Claude Code mechanisms typically include:

| Declaration | Claude Code mechanism |
|---|---|
| Skill | `.claude/skills/<name>/SKILL.md` (frontmatter `name`, `description`; optional `disable-model-invocation`, `allowed-tools`, `argument-hint`) |
| Command | A Skill invoked as `/<name>` |
| Rule / Context | `CLAUDE.md` or `.claude/rules/*.md` |
| Permission / Tool | `permissions` in project `.claude/settings.json`; Skill `allowed-tools` |
| Connection | Project `.mcp.json` (external trust or authentication → blocked, report it) |
| Personality | `.claude/output-styles/*.md` |
| Runtime choice | Project `.claude/settings.json` (e.g. `model`), hooks in `.claude/hooks/` |
| Agent Instance | `.claude/agents/<name>.md` subagents |

Use the mechanism that fits; do not force every concept into a Skill. Native paths, formats, and configuration belong to the Native realization, never to the Agent Module.

### 3. Realize each declaration

For every declared Component or capability, including explicit empty categories:

1. Identify the corresponding Native mechanism.
2. Read the existing Native realization completely when one exists.
3. Compare the declaration with that realization.
4. Create or update the Native artifact when missing or stale.
5. Preserve Native metadata and compatible Native content that the Agent Module does not own.
6. Re-read the result and determine whether the declaration was realized faithfully.

Restate a declaration in Claude Code's idiom only when necessary for the Native to apply it, preserving meaning, scope, ownership, and authority. Never invent a declaration, narrow its scope, or silently change its authority. If no equivalent mechanism exists, report the declaration as unsupported or approximated with the exact difference.

For every declared Skill entry (every Contract):

- Create the Native Skill when missing.
- Reconstruct its Agent-owned content from the current Contract and every Source it names on every run. Preserve only Native metadata and compatible content the Agent Module does not own.
- Verify the reconstructed result against the Contract and every Source.
- Mark it `already current` only when verification finds no omitted, weakened, or contradictory requirement. File existence, matching name, matching Contract, or a prior run never establishes that. Any mismatch means `updated`, even if the Contract is unchanged.
- The coordinating Skill selection affects invocation and coordination only; it never makes another declared Skill optional.

## Output

Report:

- the Agent Module sources read;
- the Native mechanism and artifact used for each declaration;
- one result per declaration: `created`, `updated`, `already current`, `approximated`, `unsupported`, or `blocked`;
- the exact difference for every approximation or unsupported declaration, and the exact reason for every blocked item; and
- whether re-reading the Native artifacts confirmed faithful synchronization.

The overall result is successful only when the complete current Agent Module was read and every required declaration was realized and verified. Never claim a Native artifact is authoritative over the Agent Module.
