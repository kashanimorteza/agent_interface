---
name: my-interface-develop
description: Agent Interface Core Skill `develop`. Executes the authorized, eligible Tasks of the current Plan for each selected (or every active and developable) Target phase — claiming each Task, producing and verifying its result, and recording evidence in its Task Log. Use when the Human or a coordinating Agent asks to develop planned work.
argument-hint: "[phase-id ...]"
---

# Develop (`develop`)

The Core Skill for developing. Required. Stable key: `develop`. Skill name: `my-interface-develop`.

This Skill is a synchronized, self-contained Runtime realization. Its meaning comes from the Develop Operation Definition and Preferences, read fresh on every run; this file never replaces them. Never read or search `.interface/agent/`. If something this Skill needs is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Personality

No Personality is declared. Work under the global Rules and the active Output Style.

## Invocation and inputs

- May be invoked directly by the Human (`/my-interface-develop [phase-id ...]`) or by an Agent (Skill tool), including a coordinating Skill.
- Inputs: an invocation request and an optional phase selection — zero or more Target phase identifiers in `$ARGUMENTS`. With none, consider every active and developable Target phase.
- When invoked by a coordinator, the coordinator supplies its reserved Log identifier; record it as this Log Entry's `parent_id`.

## Requirements

- A successful Configure execution must have established the required Config records before this Skill runs.
- Each selected phase must have a current Plan.

If either is absent, stop and record the unmet prerequisite in State. Never run Configure or Plan yourself.

## Workflow

1. **Execution Log — start.** Create one Log Entry in the State Config (`.interface/config/state.yaml`) for this execution with its `id`, `skill: develop`, and `started_at`.
2. **Establish Understanding.** Read `.interface/interface.md` and the Foundation section files it links, as the global `interface-bootstrap` Rule requires; then establish Target Understanding from the Target definitions the Interface locates, under the precedence it declares. Apply the Development Components' Definitions and Preferences the Interface locates for the work at hand.
3. **Read the Develop Operation completely** — `.interface/implementation/operations/develop/develop.md` (Definition and mandatory Principle) and `.interface/implementation/operations/develop/develop.yaml` (Preferences). Read the Plan Schema `.interface/foundation/schema/plan.yaml` for Task status values and the Task Log. These are authoritative; if they differ from anything in this file, they win.
4. **Validate prerequisites** as stated under Requirements. Once they hold, record the active Workflow position as `development`.
5. **Execute eligible Tasks, phase by phase in Target order.** A Task is eligible when its dependencies are complete, no blocking condition remains, and its authority, scope, inputs, outputs, and completion conditions are understood. For each:
   - claim it before changing its result;
   - if a new Task names an earlier developed Task through `replaces`, mark the earlier Task `replaced` and record the relationship in its Task Log first;
   - consider its Task Skills and use any other suitable available Skill;
   - preserve valid existing work;
   - build and run the concrete executable check that satisfies the Task's verification condition;
   - append evidence, progress transitions, the check used and its outcome, and any Task-specific Blocker to its Task Log, and update its status. A Task is `done` only when its check has passed.
   - when a blocking condition is verified resolved, record the evidence, clear the obsolete Blocker reference, and return the Task to pending; recheck dependencies before claiming it again.
6. **Update aggregate development progress** for each phase in State. If no eligible Task exists, record that no development was required.
7. **Never invoke another Core Operation.** When another Operation is required, stop and report it.
8. **Execution Log — completion.** Update the same Log Entry with `completed_at`, `duration_ms`, `outcome`, a concise `report`, the Skills actually used, unresolved conditions, and any applicable `data`, Open Questions, or Blockers. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Stop conditions

Stop when a dependency or prerequisite is unmet, verification fails, or an unresolved condition prevents completion — and record why.

## Boundaries

- Inside `.interface/`, write only Task progress fields and Task Logs in the Plan Config and this execution's State records. Every other `.interface/` path is read-only.
- Never change Target meaning, Plan content, Development Principles, or another Component's owned record; never design or change Tasks or expand Task scope.
- Never read `.interface/agent/` and never invoke `/my-interface-agent-native`.

## Outputs

The Skill execution result and status: Tasks completed, blocked, or left pending with their evidence; the Log Entry `id`; and any Open Questions or Blockers.
