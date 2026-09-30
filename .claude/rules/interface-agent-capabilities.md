<!-- Rule `interface-agent-capabilities` · scope: global (loaded for all work; no path condition) · required.
     Derived by Agent Native Sync (/my-interface-agent-native) from the Human-owned Skill Definition, the Skill Contracts, and the Command Preferences.
     Change those Human-owned sources and re-run that synchronization; do not edit this copy. -->

# Agent Interface capabilities

These are the synchronized Runtime capability identifiers and their Claude Code mappings. Use them as they stand; never resolve them from the Agent Module. If a capability listed here is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Core Skills

A Skill is a reusable capability an Agent activates to perform a defined kind of work. Each Core Skill below is required and is realized as a project Skill in `.claude/skills/<skill name>/SKILL.md`. Each may be invoked directly by the Human as `/<skill name>` or by an Agent through the Skill tool.

| Stable key | Skill name | Used for | Inputs |
|---|---|---|---|
| `configure` | `my-interface-configure` | configuring | an invocation request |
| `plan` | `my-interface-plan` | planning | an invocation request and an optional phase selection |
| `develop` | `my-interface-develop` | developing | an invocation request and an optional phase selection |
| `review` | `my-interface-review` | reviewing | an invocation request and an optional phase selection |
| `implement` | `my-interface-implement` | implementing | an invocation request and an optional phase selection |

- Prerequisites: Plan, Develop, and Review require a prior successful Configure execution that established the required Config records. Develop also requires a current Plan for each selected phase. Review also requires a current Plan and generated Source available for examination for each selected phase; Development need not have completed.
- Coordination: `my-interface-implement` coordinates Configure, Plan, Develop, and Review, and supplies its own State Log Entry ID as each coordinated Skill's `parent_id`. No other Core Skill invokes another Core Skill.
- Every execution of every Core Skill creates one Log Entry in State and updates that same Entry when the work completes, stops, or is blocked.

## Provider Skills

`not_configured` — no Provider Skill is declared.

## Commands

`not_configured` — no named or slash Command is declared beyond the Skill invocations above.

## Agent Native Sync

`/my-interface-agent-native` is the only entry point that reconciles this Runtime realization with its Human-owned declarations. Only the Human invokes it, directly, without a mode or numeric argument. No Agent, Agent Instance, Skill, coordinator, Hook, or automation invokes it, schedules it, or simulates it.
