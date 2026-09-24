---
name: my-interface-develop
description: Core Skill for developing. Executes the authorized, unfinished, eligible Tasks of each selected (or every active and developable) Target phase's current Plan, claiming each Task and recording evidence and progress in its Task Log. Use when planned work must be implemented.
argument-hint: "[phase-id ...]"
---

# Develop (Core Skill)

The Core Skill for developing. Required. Stable key: `develop`. Skill name: `my-interface-develop`.

This Skill is the Claude Code realization of the Develop Operation. The current Develop Operation Definition and Preferences, located through the Interface, remain the authority for Develop's meaning; this Skill restates them so it can run. If they disagree with this Skill, follow the current owning source and report Runtime drift so the Human can run Agent Native Sync. Develop Preferences may supply execution defaults only where the Plan and owning Development authorities are silent; they currently declare none (an empty section is an absence of defaults, not a wildcard).

## Personality

No Personality is declared.

## Invocation and inputs

- May be invoked directly by a Human (`/my-interface-develop [phase-id ...]`) or by an Agent (for example, coordinated by `my-interface-implement`).
- Inputs: an invocation request and an optional phase selection (one or more Target phase identifiers). When coordinated by Implement, the request carries the coordinator's Log Entry ID as `parent_id`; record it on this execution's Log Entry.

## Requirements

- A successful Configure execution must have established the required Config records before this Skill runs.
- Each selected phase must have a current Plan.
- If Config or Plan is unavailable, stop. Develop never executes Configure or Plan.

## Terms

- **Development Result** — the authorized Source, interface, configuration, or evidence produced by a completed development Task.
- **Task Evidence** — the observable information showing what a Develop operation produced and verified.
- **Developable Phase** — an active Target phase whose required Config records are valid and whose current Plan exists.

## Procedure

1. Apply the project Rules loaded as project memory (Interface bootstrap, Interface Skill policy, Git discipline).
2. **Execution Log — start.** Create one Log Entry in State for this execution, with its ID, Skill (`my-interface-develop`), `started_at`, and `parent_id` when supplied.
3. Verify the required Config records are valid; otherwise stop.
4. Establish current Interface and Target Understanding from their current sources.
5. Select phases: the given Target phase identifiers, or every active and developable Target phase when none is selected, in Target order. A phase is developable only when the required Config records are valid and its current Plan exists; otherwise stop.
6. Read the current Plan for each applicable phase (Groups, Tasks, context, dependencies, completion conditions).
7. For each selected eligible, unfinished Task whose authority, scope, inputs, outputs, and completion conditions are understood:
   1. If the Task identifies an earlier developed Task through `replaces`, mark that earlier Task `replaced` and record the relationship in its Task Log before executing the new Task.
   2. Claim the Task before changing its result.
   3. Consider the Task's Task Skills; you may also use any other suitable available Skill. Never invoke another Core Operation (Configure, Plan, Review, Implement).
   4. Realize the result under the current Development Components' Definitions and Preferences. Preserve valid existing work.
   5. Construct and run the concrete check that satisfies the Task's verification condition. Record Task-specific evidence, progress transitions, verification results, and any Task-specific Blocker in the Task Log (append-only; secret values excluded), and update the Task status accordingly. A Task is complete only when its check has passed.
   6. When a blocking condition is verified as resolved: record the resolution evidence and transition in the Task Log, clear the obsolete Blocker reference, and return unfinished blocked work to its initial pending status; recheck dependencies and remaining blocking conditions before claiming it again. Resolution never marks work complete; a missing Blocker record alone is not evidence of resolution. If another condition still blocks the Task, its reference identifies that current condition. Coordinate removal of the State Blocker with these updates.
8. If no eligible Task exists, complete without changing implementation work.
9. **Stop** when a dependency or prerequisite is unmet, verification fails, or an unresolved condition prevents completion. Stop and report when another Operation is required. Report the exact reason.
10. **Execution Log — completion.** Update the same Log Entry with `completed_at`, `duration_ms`, readable `duration`, outcome, report, and any applicable data, Open Questions, or Blockers. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Principle (mandatory) — Develop executes planned work within its authority

- **Must** — select one or more Target phases, or every active and developable phase when none is selected, in Target order.
- **Must** — require valid Config and a current Plan before development, and stop when either is absent.
- **Must** — execute only understood, claimed, eligible Tasks; consider their Task Skills and record Task evidence and progress in their Task Logs.
- **Must** — mark an earlier developed Task as `replaced` and record the relationship before executing a new Task that identifies it through `replaces`.
- **Never** — invoke another Core Operation, expand Task scope, or replace Target, Plan, or Development authority.
- Develop never changes Target meaning, Plan authority, Development Principles, or another Component's owned record without explicit authority. It does not design or change Tasks.

Ownership: Develop owns Task execution. Technical choices and defaults belong to the owning Development Component Preferences; Plan owns the work definition, Development owns product meaning, Task Logs own Task evidence and progress, and State owns Operation Logs and aggregate progress.

## Outputs

The Skill execution result and status.
