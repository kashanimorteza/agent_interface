<!-- Rule: interface-agent-capabilities · scope: global (always loaded) · Derived Synchronized Runtime realization maintained by /my-interface-agent-native. -->

# Agent Interface capabilities

The synchronized Runtime capability identifiers and their Claude Code mappings. Use these artifacts directly; never resolve a capability, invocation, or mapping through Agent Module sources. If a listed capability is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Skills

A Skill is a reusable capability an Agent can activate to perform a defined kind of work.

### Core Skills

Each Core Skill is required, may be invoked directly by a Human or by an Agent, and is realized as a project Skill in `.claude/skills/<skill-name>/SKILL.md`.

| Stable key | Skill name | Invocation | Purpose | Inputs |
|---|---|---|---|---|
| `configure` | `my-interface-configure` | `/my-interface-configure` | Configuring | An invocation request |
| `plan` | `my-interface-plan` | `/my-interface-plan [phase-id ...]` | Planning | An invocation request and an optional phase selection |
| `develop` | `my-interface-develop` | `/my-interface-develop [phase-id ...]` | Developing | An invocation request and an optional phase selection |
| `review` | `my-interface-review` | `/my-interface-review [phase-id ...]` | Reviewing | An invocation request and an optional phase selection |
| `implement` | `my-interface-implement` | `/my-interface-implement [phase-id ...]` | Implementing (coordinates Configure, Plan, Develop, Review) | An invocation request and an optional phase selection |

Every Core Skill records one Execution Log Entry in State per execution. When `my-interface-implement` coordinates another Core Skill, it supplies its own Log Entry ID as that Skill's `parent_id`.

### Provider Skills

None are declared.

## Commands

No Commands are declared. The only slash entry points are the Core Skill invocations above and Agent Native Sync.

## Agent Native Sync

`/my-interface-agent-native` — invoked only directly by the Human, with no mode or numeric argument. No Agent Native, Agent Instance, Skill, coordinator, Hook, lifecycle routine, automation, or model-generated action may invoke it; this is enforced by the project's PreToolUse guard.
