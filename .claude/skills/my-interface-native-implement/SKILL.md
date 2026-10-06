---
name: my-interface-native-implement
description: Agent Native Implement. Reads the complete Executor Module (.interface/executor/) read-only and realizes the Human's declared Agent Components — Rules, Skills, Permissions, Connections, Output Style, and any other declared Component — in Claude Code as the selected Agent Native. Invoked only by the Human as /my-interface-native-implement, with no mode or numeric argument.
disable-model-invocation: true
---

# Agent Native Implement

This Skill transfers the Executor Module's portable definition of the Agent into Claude Code, the selected Agent Native. It is the only process authorized to read the Executor Module for Native realization. Its realization procedure is `.interface/foundation/create-agent-native-implement.md`; the procedure below restates it so this Skill is self-contained, and the Foundation File is re-read at the start of every invocation.

Run only when the Human explicitly invokes `/my-interface-native-implement`. Ignore any mode or numeric argument. No other Skill, Agent Instance, coordinator, startup routine, or runtime operation may invoke this Skill, read the Executor Module, or depend directly on its sources; they use the Native realization.

Every invocation is a full realization against the current Executor Module and the current Foundation File. The existence of this Skill, of any previously generated Native artifact, or of a prior run never satisfies the invocation and never permits skipping creation, reconciliation, or verification.

## Step 0 — Re-read the procedure

Read `.interface/foundation/create-agent-native-implement.md` completely. If it differs from what follows, the Foundation File governs; apply its current instructions for this run and report the difference.

## Step 1 — Source Understanding (read-only)

Read in full, before changing any Native artifact:

- `.interface/executor/executor.md` — the Executor Module's structure and shared meaning;
- every applicable `.interface/executor/<component>/<component>.md` — portable meaning and Principles;
- every applicable `.interface/executor/<component>/<component>.yaml` — current declarations and selections;
- every file explicitly referenced by those Executor sources.

Discover the current Components and referenced sources from the Executor Module itself (list `.interface/executor/` and follow its references). Never rely on a hardcoded Component list or on an earlier run.

`.interface/interface.md` may be consulted as a navigation map only when necessary. Interface Understanding and Target Understanding are not required; never read Target sources.

Then, before realizing any Skill:

- Enumerate every Contract in `.interface/executor/skill/contracts/`. Each Contract is one required realization item. Its named Operation Component Definition and Preferences are the source of its meaning; the Contract is the source of its invocation and Native boundary. No declared Skill may be skipped because it is unfamiliar, already present, or not the coordinating Skill. An Operation Component with no Contract (for example State, when not declared as a Skill) must not be turned into a Skill merely because it exists in the Implementation Module.
- Enumerate every folder in `.interface/executor/skill/providers/`. Each folder is one required realization item, copied byte-for-byte into the Native Skill location. It has no Contract or Source and is never reconstructed.

## Step 2 — Learn the Native

Before choosing any destination, confirm Claude Code's current documented mechanisms, file conventions, invocation rules, and limitations for each declared concept (consult the Claude Code documentation when unsure). Typical project-scoped mechanisms, to be confirmed rather than assumed:

- Rules → project memory (`CLAUDE.md`, `.claude/rules/*.md`);
- Skills → `.claude/skills/<name>/SKILL.md` (with supporting files in the same folder);
- Permissions → `permissions` in `.claude/settings.json`;
- Connections → `.mcp.json` / MCP settings in `.claude/settings.json`;
- Output Style → `.claude/output-styles/*.md` and `outputStyle` in `.claude/settings.json`;
- Extensions → desired state in project-scoped settings (e.g. `enabledPlugins`, `extraKnownMarketplaces` in `.claude/settings.json`).

Native-specific paths, formats, commands, and configuration details belong to the Native realization, never to the Executor Module. Use the corresponding Native mechanism for each Component instead of forcing every concept into a Skill.

## Step 3 — Realization Procedure

Preserve the meaning, scope, ownership, boundaries, and mandatory Principles the Human declared. For each declared Component or capability:

1. identify the Native mechanism that corresponds to the declaration;
2. read the existing Native realization completely when one exists;
3. compare the declaration with that realization;
4. create or update the Native artifact when it is missing or stale;
5. preserve Native metadata and compatible Native content that the Executor Module does not own;
6. re-read the result, run every Component's Review checks in the Native — including each Enforced Guarantee's `probe` and `allow_probe` — and determine whether the declaration was realized faithfully.

Realize every current declaration; never silently skip an unfamiliar or newly added Component. If the Native has no equivalent mechanism, report the declaration as `unsupported` or `approximated` and state the exact difference. Never invent a declaration, narrow its scope, or silently change its authority.

Restate a declaration in Claude Code's idiom only when necessary for the Native to apply it, preserving meaning, scope, ownership, and authority. A Native artifact is never a second authority.

### Core Skills (each Contract)

- Create the Native Skill when missing. On every run, reconstruct its Executor-owned content from the current Contract and every Source it names; preserve only Native metadata and compatible content the Executor Module does not own.
- Verify the reconstructed result against the Contract and every Source. It is `already current` only when that verification finds no omitted, weakened, or contradictory requirement. File existence, a matching name, a matching Contract, or a prior run never establishes `already current`. Any mismatch requires `updated`, even when the Contract itself is unchanged.
- The coordinating Skill selection affects invocation and coordination only; it never makes another declared Skill optional.

### Provider Skills (each `providers/` folder)

- Copy the folder byte-for-byte into the Native Skill location; never edit, reconstruct, or add a marker inside the copy.
- It is `already current` only when the Native copy is byte-for-byte identical to its `providers/` folder (compare every file, including file set); any difference requires a fresh copy.

### Ownership record and stale removal

- Record every generated Native artifact as this Skill's own: by a marker inside the artifact (for example an HTML comment or a `# managed by /my-interface-native-implement` line appropriate to the format), or — for a Provider Skill copy — by an entry in the realization record `.claude/skills/my-interface-native-implement/realization-record.json`, kept outside every copied folder. For settings entries that cannot carry a marker, record them in that same realization record.
- Remove any recorded artifact whose declaration no longer exists in the Executor Module. Never remove unrecorded Native content.

## Authority and Boundaries

The Executor Module is Human-owned. Read it read-only; never create, change, move, or delete any file or directory under `.interface/executor/`. Only the Human may change Executor Definitions, Preferences, Contracts, and Provider Skills.

The Human's direct explicit invocation is standing authorization for every project-scoped Native change within this scope, including removal of this Skill's own recorded stale artifacts. Create, update, save, and verify the required Native artifacts without asking whether to save or whether each change is approved. Pause only for credentials, external trust, authentication, broader authority, an irreversible action, or a Native capability that cannot realize the declaration.

This Skill does not:

- read or understand Target sources;
- inspect Git status, history, branches, diffs, tracked state, deleted files, or earlier versions;
- restore, compare, or recover anything from Git or any past project state;
- choose or change Implementation decisions;
- install plugins, packages, or external capabilities — it records each declared Extension's desired state in the Native's project-scoped settings and reports an Extension that is not installed as `activation_required` for the Human to install;
- change application dependencies, project code, Config, credentials, user settings, or machine settings;
- create new Executor declarations; or
- remove unrelated Native content.

If a declaration needs Human input, broader authority, external trust, authentication, or a Native capability that does not exist, stop that item and report the exact reason. Continue independent declarations when safe.

## Output

Report:

- the Executor Module sources read;
- the Native mechanism and artifact used for each declaration;
- one result for every declared entry (every Contract, every Provider folder, every other declaration): `created`, `updated`, `removed`, `already current`, `approximated`, `unsupported`, `blocked`, or `activation_required`;
- the exact difference for every approximation or unsupported declaration, and the exact reason for every blocked item;
- whether re-reading the Native artifacts and running every Review check and probe confirmed faithful realization.

The overall result is successful only when the complete current Executor Module was read and every required declaration was realized and verified. Never claim that a Native artifact is authoritative over the Executor Module.
