---
name: my-interface-implement
description: Agent Interface Core Skill for implementing (stable key `implement`), the coordinating Skill. Coordinates Configure, Plan, Develop, and Review across the selected Target phases and reports aggregate Open Question and Blocker counts. Use when the Human runs /my-interface-implement [phase ...] or asks for an end-to-end Agent Interface run.
argument-hint: "[phase-id ...]"
---

# Implement

Synchronized Runtime realization of the required Implement Core Skill. Stable key `implement`, Skill name `my-interface-implement`. This is the coordinating Skill. This file is self-contained. Never consult `.interface/agent/`.

## Personality

No Personality is declared yet.

## Inputs

An invocation request and an optional phase selection: `$ARGUMENTS`. Zero or more Target phase identifiers may be given.

## Invocation

Either the Human (`/my-interface-implement [phase ...]`) or an Agent (Skill tool) may invoke this Skill directly.

## Coordinated Skills

Coordinate the other Core Skills only through their synchronized Skills, invoked with the Skill tool:

| Operation | Skill |
|---|---|
| Configure | `my-interface-configure` |
| Plan | `my-interface-plan` |
| Develop | `my-interface-develop` |
| Review | `my-interface-review` |

Each coordinated Skill establishes its own Understanding, does its own work, and records its own outcome. Implement never performs their work itself. When invoking one, pass the phase selection it needs and `parent_id=<this execution's Log Entry ID>` in its arguments.

If a coordinated Skill is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Workflow

1. **Apply the Runtime Rules.** Re-read the synchronized Rules in `.claude/rules/` at the start of this Workflow. They bind every step: `interface-bootstrap`, `interface-skill-policy`, `git-discipline`, `interface-agent-capabilities`, and `interface-component-principles`.
2. **Establish Interface Understanding** as `interface-bootstrap` defines it, but only as far as coordination needs.
3. **Read the Operation authority in full on every run:**
   - `.interface/implementation/operations/implement/implement.md` (Definition and mandatory Principle)
   - `.interface/implementation/operations/implement/implement.yaml` (Preferences)

   These sources govern phase selection, the Config check, the order of coordinated Operations, the Review behavior after a blocked Develop, and stopping conditions. This Skill never replaces, narrows, or weakens them. If either is missing or unreadable, stop and report a Blocker.
4. **Execution Log.** Create one Log Entry in State for this execution, including its ID and Skill (`my-interface-implement`). Supply that ID as the `parent_id` of every Core Skill this execution coordinates. Update that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked. Its execution data includes the unique counts of associated Open Questions and Blockers. Locate State Config, the State Schema, and the State Operation Definition through `.interface/interface.md`, and follow them.
5. **Coordinate** exactly as the Implement Definition requires, carrying each Operation's outcome forward.
6. **Report** the output below.

## Outputs

The Skill execution result and status, including the aggregate counts of associated Open Questions and Blockers.
