---
name: my-interface-develop
description: Agent Interface Core Skill for developing (stable key `develop`). Executes the eligible planned Tasks of selected Target phases and records Task progress and evidence. Use when the Human runs /my-interface-develop [phase ...], or when an Agent or the Implement Skill needs planned work developed.
argument-hint: "[phase-id ...]"
---

# Develop

Synchronized Runtime realization of the required Develop Core Skill. Stable key `develop`, Skill name `my-interface-develop`. This file is self-contained. Never consult `.interface/agent/`.

## Personality

No Personality is declared yet.

## Inputs

An invocation request and an optional phase selection: `$ARGUMENTS`. Zero or more Target phase identifiers may be given. When a coordinating Skill invokes this Skill, the request carries `parent_id=<Log Entry ID>`.

## Invocation

Either the Human (`/my-interface-develop [phase ...]`) or an Agent (Skill tool) may invoke this Skill directly.

## Requirements

- A successful Configure execution must have established the required Config records before this Skill runs.
- Each selected phase must have a current Plan.

If a requirement is unmet, stop and report it. Do not run Configure or Plan.

## Workflow

1. **Apply the Runtime Rules.** Re-read the synchronized Rules in `.claude/rules/` at the start of this Workflow. They bind every step: `interface-bootstrap`, `interface-skill-policy`, `git-discipline`, `interface-agent-capabilities`, and `interface-component-principles`.
2. **Establish Interface Understanding** as `interface-bootstrap` defines it, and establish Target Understanding for the phases in scope.
3. **Read the Operation authority in full on every run:**
   - `.interface/implementation/operations/develop/develop.md` (Definition and mandatory Principles)
   - `.interface/implementation/operations/develop/develop.yaml` (Preferences)

   These sources govern phase selection, Task eligibility and claiming, generation, Task Logs, and stopping conditions. This Skill never replaces, narrows, or weakens them. If either is missing or unreadable, stop and report a Blocker. Resolve the Development authorities each Task needs through `.interface/interface.md`.
4. **Check the Requirements** above.
5. **Execution Log.** Create one Log Entry in State for this execution, including its ID and Skill (`my-interface-develop`). Add `parent_id` and the phase when they apply. Update that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked. Locate State Config, the State Schema, and the State Operation Definition through `.interface/interface.md`, and follow them.
6. **Develop** the eligible Tasks exactly as the Develop Definition requires. Consider each Task's Task Skills and use any other suitable available Skill, but never invoke another Core Skill.
7. **Report** the output below.

## Outputs

The Skill execution result and status.
