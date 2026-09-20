<!-- Native realization of a Human-owned Agent Rule (global scope, derived from the declared Skill and Command catalogs), synchronized by /my-interface-agent-native. Not authoritative; do not edit here. -->

# Agent Interface capabilities (synchronized Runtime identifiers)

This Rule exposes the Runtime capability identifiers and native mappings so no operation needs to read the Agent Module. If a capability below is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never consult the Agent Module.

## Declared Skills (Claude Code: `.claude/skills/<name>/SKILL.md`, invoked as `/<name>`)

Each Skill is Process-backed: the owning Implementation Process Component (`.interface/implementation/process/<key>/definition.md` and `preferences.yaml`) owns its meaning; the Skill only bridges to it. All are required. Autonomous invocation is disabled for every Skill.

| Key | Skill | Invocation | Trigger |
|---|---|---|---|
| configure | `/my-interface-configure` | Human or declared coordinator | Invoked by the Human or a declared coordinator |
| plan | `/my-interface-plan` | Human or declared coordinator | Explicitly, for zero or more phase selections, or when a declared coordinator requires a current Plan |
| develop | `/my-interface-develop` | Human or declared coordinator | Explicitly, for zero or more phase selections, after a valid current Plan exists and prerequisites are ready |
| review | `/my-interface-review` | Human or declared coordinator | Explicitly, for zero or more phase selections, after implementation exists |
| launch | `/my-interface-launch` | Human or declared coordinator | Explicitly, or when end-to-end orchestration establishes the current Launch prerequisites |
| implement | `/my-interface-implement` | Explicit Human only (coordinator: disabled) | Explicit Human invocation for zero or more phase selections; coordinates configure, plan, develop, review, and launch through the Runtime's own Skill mechanism only |
| reset | `/my-interface-reset` | Explicit Human only (coordinator: disabled) | Explicit Human invocation with one reset scope |

Declared coordinator: only `/my-interface-implement` may invoke `configure`, `plan`, `develop`, `review`, and `launch`, and only through the Skill tool; each Process Component keeps ownership of its own records and outputs.

## Commands

No Commands are declared beyond the Skills above.

## Agent Native Sync

`/my-interface-agent-native` is the only entry point that reads the Agent Module. It is explicit-Human-only and is never invoked by a Skill, coordinator, Agent Instance, hook, or automation.
