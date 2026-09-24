---
name: my-interface-develop
description: Core Interface Skill "develop" — executes the authorized, eligible, unfinished Tasks of the current Plan for selected (or every active and developable) Target phases, claiming each Task, recording Task Log evidence and status, and recording one State Log Entry. Use when planned phases need their Tasks implemented.
argument-hint: "[phase-id ...]"
---

<!-- Synchronized by /my-interface-agent-native from the Develop Skill Contract and its Sources. Do not edit here; this Skill is a Runtime realization, never an authority. -->

# Develop

The Core Skill for developing. Stable key: `develop`. Required. No Personality is declared.

## Invocation and inputs

- May be invoked directly by the Human (`/my-interface-develop [phase-id ...]`) or by an Agent (for example the Implement coordinator).
- Inputs: an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers). When a coordinator supplies a parent Log identifier, record it as `parent_id`.

## Requirements

- A successful Configure execution must have established the required Config records before this Skill runs.
- Each selected phase must have a current Plan.
- A phase is developable only when the required Config records are valid and its current Plan exists. If either is absent, stop and record the unmet prerequisite in State; never run Configure or Plan.

## Before acting

1. Apply the project Rules `interface-bootstrap`, `interface-skill-policy`, and `git-discipline` (`.claude/rules/`). Never read `.interface/agent/`.
2. Read the current Operation authorities in full — they govern over this summary if they differ:
   - `.interface/implementation/operations/develop/develop.md` (Definition and mandatory Principle)
   - `.interface/implementation/operations/develop/develop.yaml` (Preferences; currently no defaults — they may supply execution defaults only where the Plan and owning Development authorities are silent)
3. Establish current Interface and Target Understanding from `.interface/interface.md` and the sources it locates, and read the owning Development Component Definitions and Preferences that govern each Task.

## Workflow

1. Resolve phases: the selected Target phase identifiers, or every active and developable Target phase when none is selected, in Target order.
2. Once prerequisites hold, record the active Workflow position as `development` in State.
3. Read the current Plan for each applicable phase. For each eligible Task (dependencies complete, authority, scope, inputs, outputs, and completion conditions understood):
   - If the Task identifies an earlier developed Task through `replaces`, first mark that earlier Task `replaced` and record the relationship in its Task Log.
   - Claim the Task (`claimed`) before changing its result.
   - Consider its Task Skills and use any other suitable available Skill. Never invoke another Core Operation (Configure, Plan, Review, Implement).
   - Preserve valid existing work; realize the result under the owning Development authorities.
   - Construct and run the concrete executable check that satisfies the Task's verification condition; record the check and its observed outcome in the Task Log. The Task is `done` only when that check has passed.
   - Record Task-specific evidence, progress transitions, verification results, and any Task-specific Blocker in the append-only Task Log, and update the status (`todo`, `claimed`, `blocked`, `done`, `replaced`).
   - When a blocking condition is verified resolved: record the resolution evidence and transition in the Task Log, clear the obsolete Blocker reference, return the Task to `todo`, and recheck dependencies and remaining conditions before claiming it. A missing Blocker record alone never proves resolution, and resolution never marks work complete.
4. If no eligible Task exists, record that no development was required.
5. Record the overall outcome, unresolved conditions, and Skills used in this execution's State Log Entry, and update aggregate phase `development` progress.

Stop when a dependency or prerequisite is unmet, verification fails, or an unresolved condition prevents completion — and report when another Operation is required instead of performing it.

## Boundaries

- Never change Target meaning, Plan authority (never design or change Tasks beyond their progress fields), Development Principles, or another Component's owned record without explicit authority.
- Never expand Task scope. Never modify any `.interface/` path outside `.interface/config/`.

## Execution Log

At the start of every execution, create one Log Entry in State with its `id` (next project-wide sequential identifier, zero-padded to at least three digits), `skill: develop`, and `started_at`. At completion, update that same entry with `completed_at`, `duration_ms`, `outcome`, `report`, `skills_used`, and any applicable `data`, `open_questions`, or `blockers`. If execution stops or is blocked, update the same entry with the actual outcome and reason.

## Output

The Skill execution result and status: Tasks claimed, completed, blocked, or replaced with their verification evidence; Blockers and Open Questions; and the Log Entry id.
