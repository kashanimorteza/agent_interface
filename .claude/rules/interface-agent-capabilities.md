<!-- Synchronized by /my-interface-agent-native. Derived Agent Rule "interface-agent-capabilities" (scope: global), derived from the Agent Skill Definition, the Skill Contracts, and the Command Preferences. Do not edit here; this file is a Runtime realization, never an authority. -->

# Agent Interface capabilities

These are the synchronized Runtime capability identifiers and their Claude Code mappings. Use this list instead of any Agent Module source. If a capability listed here is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never resolve it from `.interface/agent/`.

## Core Skills

A Skill is a reusable capability an Agent activates to perform a defined kind of work. Every Core Skill below is required; each may be invoked directly by the Human (`/<skill-name>`) or by an Agent (Skill tool).

| Stable key | Claude Code Skill | Invocation | Purpose | Inputs |
|---|---|---|---|---|
| `configure` | `my-interface-configure` | `/my-interface-configure` | Create and reconcile the Config records from their Schemas | An invocation request |
| `plan` | `my-interface-plan` | `/my-interface-plan [phase ...]` | Turn Target phases into Plans of Groups and Tasks | An invocation request and an optional phase selection |
| `develop` | `my-interface-develop` | `/my-interface-develop [phase ...]` | Execute authorized planned Tasks | An invocation request and an optional phase selection |
| `review` | `my-interface-review` | `/my-interface-review [phase ...]` | Independently judge Plans and implemented results | An invocation request and an optional phase selection |
| `implement` | `my-interface-implement` | `/my-interface-implement [phase ...]` | Coordinate Configure, Plan, Develop, and Review | An invocation request and an optional phase selection |

Each Skill records one Log Entry per execution in the State Config and reports its execution result and status.

## Provider Skills

None are declared.

## Commands

No additional Commands are declared. The Skill invocations above are the only Interface entry points besides Agent Native Sync.

## Agent Native Sync

- Claude Code Skill `my-interface-agent-native`, invoked only by the Human typing `/my-interface-agent-native` with no argument.
- It is the only reader of the Agent Module. No Agent, Skill, subagent, hook, or automation may invoke it or borrow its read grant; Claude Code blocks model invocation of it (`disable-model-invocation`) and the `interface-boundary-guard` hook blocks non-Human attempts.
