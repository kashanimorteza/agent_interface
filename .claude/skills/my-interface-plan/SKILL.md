---
name: my-interface-plan
description: Agent Interface Core Skill for planning (stable key `plan`). Turns selected Target phases into Plans of Groups and Tasks in the Plan Config. Use when the Human runs /my-interface-plan [phase ...], or when an Agent or the Implement Skill needs a phase planned or replanned.
argument-hint: "[phase-id ...]"
---

# Plan

Synchronized Runtime realization of the required Plan Core Skill. Stable key `plan`, Skill name `my-interface-plan`. This file is self-contained. Never consult `.interface/agent/`.

## Personality

No Personality is declared yet.

## Inputs

An invocation request and an optional phase selection: `$ARGUMENTS`. Zero or more Target phase identifiers may be given. When a coordinating Skill invokes this Skill, the request carries `parent_id=<Log Entry ID>`.

## Invocation

Either the Human (`/my-interface-plan [phase ...]`) or an Agent (Skill tool) may invoke this Skill directly.

## Requirements

A successful Configure execution must have established the required Config records before this Skill runs. If they are missing or invalid, stop and report it. Do not run Configure and do not create or repair a Config record.

## Workflow

1. **Apply the Runtime Rules.** Re-read the synchronized Rules in `.claude/rules/` at the start of this Workflow. They bind every step: `interface-bootstrap`, `interface-skill-policy`, `git-discipline`, `interface-agent-capabilities`, and `interface-component-principles`.
2. **Establish Interface Understanding** as `interface-bootstrap` defines it, and establish Target Understanding for the phases in scope.
3. **Read the Operation authority in full on every run:**
   - `.interface/implementation/operations/plan/plan.md` (Definition and mandatory Principles)
   - `.interface/implementation/operations/plan/plan.yaml` (Preferences)

   These sources govern phase selection, decomposition, Plan content, reconciliation, and stopping conditions. This Skill never replaces, narrows, or weakens them. If either is missing or unreadable, stop and report a Blocker.
4. **Check the Requirements** above.
5. **Execution Log.** Create one Log Entry in State for this execution, including its ID and Skill (`my-interface-plan`). Add `parent_id` and the phase when they apply. Update that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked. Locate State Config, the State Schema, and the State Operation Definition through `.interface/interface.md`, and follow them.
6. **Plan** the applicable phases exactly as the Plan Definition requires. Use any suitable available Skill, but never invoke another Core Skill.
7. **Report** the output below.

## Outputs

The Skill execution result and status.
