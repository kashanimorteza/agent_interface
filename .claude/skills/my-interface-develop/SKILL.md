---
name: my-interface-develop
description: Core Skill for developing (stable key `develop`). Executes the authorized, eligible, unfinished Tasks of each selected (or every active and developable) Target phase's current Plan, claiming each Task, recording evidence and progress in its Task Log, and generating verified Development results only inside the Component each Task realizes. Use when planned Tasks must be implemented. Invocable by the Human (/my-interface-develop [phase-id ...]) or by an Agent.
argument-hint: "[phase-id ...]"
---

<!-- Synchronized by Agent Native Sync (/my-interface-agent-native) from the Develop Skill Contract and the Develop Operation Definition and Preferences it names. Change those Human-owned sources and re-run that synchronization; do not edit this copy. -->

# Develop

The Core Skill for developing. Required. Stable key: `develop`. Skill name: `my-interface-develop`.

## Personality

No Personality is declared yet.

## Inputs

An invocation request and an optional phase selection: zero or more Target phase identifiers (`$ARGUMENTS`). When a coordinating Skill supplies a `parent_id`, record it on this execution's Log Entry.

## Invocation

This Skill may be invoked directly by a Human or by an Agent.

## Requirements

A successful Configure execution must have established the required Config records before this Skill runs. Each selected phase must have a current Plan. If valid Config or a current Plan is absent, stop; this Skill never runs Configure or Plan.

## Sources

Read these current Operation sources in full before acting. They are the authority for Develop; this Skill never copies their facts and never writes to them.

- `.interface/implementation/operations/develop/develop.md` — Develop Definition and its mandatory Execution and Generation Principles.
- `.interface/implementation/operations/develop/develop.yaml` — Develop Preferences (currently no defaults; an empty section is an absence of defaults, not a wildcard).

Technical choices and product meaning belong to the owning Development Component Definitions and Preferences; locate them through `.interface/interface.md` and read the ones each Task's Component requires.

## Workflow

1. Apply the project Rules (`interface-bootstrap`, `interface-skill-policy`, `git-discipline`, `interface-agent-capabilities`). If one is missing, report Runtime drift.
2. Verify the Requirements. Execution Log: create one Log Entry in State for this execution, including its ID and Skill, following the current State Definition and Schema.
3. Establish current Interface Understanding and Target Understanding, then read the Sources above.
4. Resolve the phases: the selected phase identifiers, or every active and developable Target phase when none is selected, in Target order. Read the current Plan for each.
5. For each eligible Task whose authority, scope, inputs, outputs, and completion conditions are understood and whose dependencies are complete:
   1. If the Task identifies an earlier developed Task through `replaces`, mark that earlier Task `replaced` and record the relationship in its Task Log first.
   2. Claim the Task before changing its result.
   3. Consider its Task Skills; use any other suitable available Skill. Never invoke another Core Skill.
   4. Construct and run the concrete check that satisfies its verification condition.
   5. Record Task-specific evidence, progress transitions, the check used and its outcome, and any Task-specific Blocker in its append-only Task Log, and update its status. A Task is complete only when its check has passed.
6. When a blocking condition is verified as resolved, record the resolution evidence and transition in the Task Log, clear the obsolete Blocker reference, return unfinished work to its initial pending status, and recheck dependencies and remaining conditions before claiming it. A missing Blocker record alone is not evidence of resolution, and resolution never marks work complete.
7. Record State's development position and each phase's aggregate development progress as the State Definition prescribes. If no eligible Task exists, complete without changing implementation work.
8. Update the same Log Entry with the outcome, a concise report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked.

## Generation obligations

- Generate, change, verify, document, and remove artifacts only inside the Component a Task realizes; never change a Component's contract because another Component lacks a capability.
- Unchanged authorities produce the same ordered output with zero diff. Regeneration classifies authoritative additions, modifications, explicit renames, and removals; updates every affected public surface together; removes only the Component's own obsolete output; and never infers a rename or removal from name similarity, missing understanding, or generator limitation. Develop owns no data migration.
- Before publication, validate input completeness, uniqueness, compatibility, naming, reference resolution, and technology support; verify the Component's own conformance contracts, Architecture, dependencies, Documentation, source quality, and zero-diff regeneration. Disabled persistent testing requires transient verification, never skipping it.
- Failure is explicit and atomic: collect independent actionable failures, identify affected items without exposing sensitive values, publish candidate output only after every required check passes, and preserve the last valid output.
- Generated output is installable, importable, and passes applicable format, import, compile, build, lint, static type, dependency, and runtime checks, with only necessary, version-stabilized dependencies and no dead, duplicate, incomplete, cached, compiled, machine-specific, Agent-identifying, timestamped, or narratively generated artifact.

## Boundaries

Never change Target meaning, Plan authority or Task definitions, Development Principles, or another Component's owned record without explicit authority. Never expand Task scope. Stop and report when another Operation is required.

## Stop conditions

Stop and report the exact reason, recording it on the Log Entry, when a dependency or prerequisite is unmet, verification fails, or an unresolved condition prevents completion.

## Outputs

The Skill execution result and status.
