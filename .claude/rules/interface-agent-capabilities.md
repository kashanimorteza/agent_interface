<!--
Native realization (Claude Code) of the derived Agent Rule `interface-agent-capabilities`,
synchronized by /my-interface-agent-native from the Skill Definition, the Skill Contracts, and
the Command Preferences. The Human-owned Agent Module remains authoritative; this file is not a
second authority. Scope: global (loaded for all work). Required: true.
-->

# Agent Interface capabilities

The synchronized Runtime capability identifiers and their Claude Code mappings. Use these; never resolve a capability through Agent Module sources. If one is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Core Skills

Each is a project Skill under `.claude/skills/<name>/SKILL.md`, invocable directly by the Human as `/<name>` or by an Agent through the Skill tool.

| Stable key | Skill name / invocation | Inputs | Requirements |
|---|---|---|---|
| `configure` | `my-interface-configure` | invocation request | — |
| `plan` | `my-interface-plan [phase-id ...]` | invocation request, optional phase selection | successful Configure established the required Config records |
| `develop` | `my-interface-develop [phase-id ...]` | invocation request, optional phase selection | Config established by Configure; each selected phase has a current Plan |
| `review` | `my-interface-review [phase-id ...]` | invocation request, optional phase selection | Config established by Configure; each selected phase has a current Plan and a Development result |
| `implement` | `my-interface-implement [phase-id ...]` | invocation request, optional phase selection | — (coordinates Configure only when Config is absent or invalid) |

Every Core Skill outputs its execution result and status. All five are required.

## Provider Skills

`not_configured` — none are declared.

## Commands

`not_configured` — no named or slash Command, argument, alias, or routing is declared beyond the Skills above.

## Agent Native Sync

`/my-interface-agent-native` — Human-only. Never invoked, scheduled, chained, or simulated by the model, a Skill, a subagent, a hook, or any automation (enforced by the project's PreToolUse guard and the Skill's `disable-model-invocation`).
