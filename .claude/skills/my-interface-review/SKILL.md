---
name: my-interface-review
description: Agent Interface Core Skill for reviewing (stable key `review`). Independently judges selected phases' generated Source and evidence against their current Plan and records Findings in State. Use when the Human runs /my-interface-review [phase ...], or when an Agent or the Implement Skill needs a phase reviewed.
argument-hint: "[phase-id ...]"
---

# Review

Synchronized Runtime realization of the required Review Core Skill. Stable key `review`, Skill name `my-interface-review`. This file is self-contained. Never consult `.interface/agent/`.

## Personality

No Personality is declared yet.

## Inputs

An invocation request and an optional phase selection: `$ARGUMENTS`. Zero or more Target phase identifiers may be given. When a coordinating Skill invokes this Skill, the request carries `parent_id=<Log Entry ID>`.

## Invocation

Either the Human (`/my-interface-review [phase ...]`) or an Agent (Skill tool) may invoke this Skill directly.

## Requirements

- A successful Configure execution must have established the required Config records before this Skill runs.
- Each selected phase must have a current Plan and generated Source available for examination. Development need not have completed when Source is available.

If a requirement is unmet, stop and report it. Do not run another Core Skill.

## Workflow

1. **Apply the Runtime Rules.** Re-read the synchronized Rules in `.claude/rules/` at the start of this Workflow. They bind every step: `interface-bootstrap`, `interface-skill-policy`, `git-discipline`, `interface-agent-capabilities`, and `interface-component-principles`.
2. **Establish Interface Understanding** as `interface-bootstrap` defines it. Establish Target Understanding and Source Understanding within each selected phase's scope.
3. **Read the Operation authority in full on every run:**
   - `.interface/implementation/operations/review/review.md` (Definition and mandatory Principles)
   - `.interface/implementation/operations/review/review.yaml` (Preferences)

   These sources govern phase selection, the Plan and Component baselines, Findings, resolution and recheck, independence, and conformance checks. This Skill never replaces, narrows, or weakens them. If either is missing or unreadable, stop and report a Blocker.
4. **Check the Requirements** above.
5. **Execution Log.** Create one Log Entry in State for this execution, including its ID and Skill (`my-interface-review`). Add `parent_id` and the phase when they apply. Update that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked. Review's Findings live in that entry's `data`. Locate State Config, the State Schema, and the State Operation Definition through `.interface/interface.md`, and follow them.
6. **Review** exactly as the Review Definition requires, with independent judgment. Never invoke another Core Skill.
7. **Report** the output below.

## Outputs

The Skill execution result and status.
