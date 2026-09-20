---
name: my-interface-agent-native
description: Agent Native Sync for this project. Reads the complete Human-owned Agent Module (.interface/agent/) and realizes its declarations (Components, Skills, Rules, Permissions, Commands, Tools, Connections, Context, Runtime, Personalities, Agent Instances) in Claude Code's native mechanisms. Invoke only explicitly via /my-interface-agent-native, with no mode or numeric argument.
disable-model-invocation: true
---

# Agent Native Sync (Claude Code)

Created from `.interface/foundation/agent-native-sync.md`. This Skill is self-contained: its procedure below does not require re-reading that Foundation File. It is the ONLY process allowed to read the Agent Module for Native realization. Native artifacts it writes are never a second authority; the Agent Module stays authoritative.

## When to run
Only when the Human explicitly invokes `/my-interface-agent-native`. Explicit invocation is standing authorization for every additive, project-scoped Native change described here; do not ask per-change permission.

## Sources (read in full, read-only)
1. `.interface/agent/guide.md`
2. every `.interface/agent/<component>/definition.md` that exists
3. every `.interface/agent/<component>/preferences.yaml` that exists
4. any file those Agent sources explicitly reference

Discover Components by listing `.interface/agent/`; never rely on a hardcoded list or an earlier run. `.interface/interface.md` may be consulted only as a navigation map. Never read Target sources.

Then enumerate EVERY entry in `.interface/agent/skill/preferences.yaml` before realizing any Skill. Each entry is a required item: its Process Component Definition and Preferences give its meaning; its Agent-side bridge gives its invocation and Native boundary. Do not skip an entry because it is unfamiliar, already present, or not the coordinating Skill. Do not create a Skill for a Process Component that has no catalog entry.

## Procedure, per declaration (including explicit empty categories)
1. Identify the Claude Code mechanism.
2. Read the existing Native realization completely, if any.
3. Compare it with the declaration.
4. Create or update it when missing or stale.
5. Preserve Native metadata and compatible content the Agent Module does not own.
6. Re-read the result and judge faithfulness.

Claude Code mechanisms (learn current docs if unsure):
- Skill → `.claude/skills/<name>/SKILL.md` (frontmatter `name`, `description`)
- Rule → `.claude/rules/*.md`
- Agent Instance / Personality → `.claude/agents/*.md` (or a Skill/rule if that fits better)
- Permission → `permissions` in `.claude/settings.json`
- Command → a Skill (slash-invocable) in `.claude/skills/`
- Tool / Connection → only existing project config (e.g. `.mcp.json`); never install anything
- Context → `CLAUDE.md` / rules files, restated only as needed
- Runtime choice → project-scoped settings where a documented key exists

If no equivalent exists, report the declaration as unsupported or approximated with the exact difference. Never invent declarations, narrow scope, or change authority. Restate a declaration in Native idiom only when needed, preserving meaning, scope, ownership, authority.

## Boundaries (never do)
- Modify anything under `.interface/agent/`
- Read Target sources
- Inspect Git status/history/branches/diffs/deleted files or restore from past state
- Choose or change Implementation decisions
- Install plugins, packages, or external capabilities
- Change application dependencies, project code, Config, credentials, user or machine settings
- Create new Agent declarations
- Remove unrelated Native content

Pause only for credentials, external trust, authentication, broader authority, an irreversible action, or a missing Native capability. Stop only that item, report the exact reason, and continue independent items when safe.

Other Skills, Agent Instances, coordinators, startup routines, Context and Runtime operations must NOT read the Agent Module; they use the synchronized Native realization.

## Output report
- Agent Module sources read
- Native mechanism and artifact for each declaration
- Result per declaration: created / updated / already current / approximated / unsupported / blocked (one line per declared Skill entry, none omitted)
- Exact difference for every approximation or unsupported item
- Whether re-reading confirmed faithful synchronization

Overall success only if the complete current Agent Module was read and every required declaration was realized and verified. Never claim a Native artifact is authoritative over the Agent Module.
