<!-- Rule `interface-agent-capabilities` · Scope: global — applies to all work in this project, loaded at session start. Derived Rule: its text is composed by /my-interface-agent-native from the Human-owned Skill and Command declarations. Synchronized realization; the Human-owned declarations are the authority and this file is not edited by hand. Conflicts: none declared; where this Rule and an owning authority disagree, the authority holds and the conflict is reported. -->

# Agent Interface capabilities

This is the synchronized map of the Agent Interface capabilities available in this project and how each one is invoked in Claude Code. Use it instead of any Agent Module source. When a capability listed here is missing or unusable, report Runtime drift with the capability status vocabulary and ask the Human to run `/my-interface-agent-native`; do not reconstruct the capability yourself.

## Core Skills

Each Core Skill is a project Skill in `.claude/skills/<name>/SKILL.md`. Every one may be invoked directly by the Human (`/<name>`) or by an Agent (Skill tool, `<name>`). Each is self-contained: its meaning is established at run time from the current Operation Definition and Preferences it names, which are Implementation sources located through `.interface/interface.md`.

| Stable key | Skill name / slash command | Inputs | Requires before it runs | Operation source it realizes |
|---|---|---|---|---|
| `configure` | `my-interface-configure` | an invocation request | — | `.interface/implementation/operations/configure/configure.md` + `.yaml` |
| `plan` | `my-interface-plan` | an invocation request and optional phase selection | a successful Configure has established the required Config records | `.interface/implementation/operations/plan/plan.md` + `.yaml` |
| `develop` | `my-interface-develop` | an invocation request and optional phase selection | required Config records; a current Plan for each selected phase | `.interface/implementation/operations/develop/develop.md` + `.yaml` |
| `review` | `my-interface-review` | an invocation request and optional phase selection | required Config records; a current Plan and a Development result for each selected phase | `.interface/implementation/operations/review/review.md` + `.yaml` |
| `implement` | `my-interface-implement` | an invocation request and optional phase selection | — (coordinates Configure when Config is absent or invalid) | `.interface/implementation/operations/implement/implement.md` + `.yaml` |

A phase selection is one or more Target phase identifiers passed as arguments, for example `/my-interface-plan <phase-id>`.

Every Core Skill execution records exactly one Log Entry of its own in the State Config (`.interface/config/state.yaml`): created at start with its ID, Skill, and `started_at`; updated at completion — or when it stops or is blocked — with `completed_at`, `duration_ms`, the actual outcome, a report, and any applicable data, Open Questions, or Blockers.

No Coordinating Skill is selected. No Provider Skill is declared.

## Commands

No Agent Command is declared (`not_configured`). The Core Skills above are reached through their own slash commands.

## Agent Native Sync (Human-only)

`/my-interface-agent-native` synchronizes this realization. Only the Human invokes it, directly. No Agent, Skill, subagent, hook, scheduled task, or automation may invoke it or act on its behalf; an attempt through the Skill tool is blocked by the project's PreToolUse guard.
