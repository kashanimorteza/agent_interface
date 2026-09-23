---
name: my-interface-develop
description: Core Interface Skill for developing. Executes the authorized, unfinished, eligible Tasks of the current Plan for each selected (or every active and developable) Target phase, claiming each Task, recording evidence in its Task Log, updating its status, and recording one State Log Entry. Use when the Human asks to develop a planned phase or when Implement coordinates Development.
argument-hint: "[phase-id ...]"
---

<!--
Native realization (Claude Code) of the Core Skill Contract `develop`, synchronized by
/my-interface-agent-native. The Human-owned Agent Module remains authoritative; this Skill is
not a second authority. Its operational meaning is owned by the Develop Operation Component,
which this Skill reads from its current location at run time.
-->

# Develop (`my-interface-develop`)

Stable key: `develop`. Required. Invocable directly by the Human (`/my-interface-develop [phase-id ...]`) or by an Agent.

- **Input:** an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers).
- **Output:** the Skill execution result and status.
- **Requirements:** a successful Configure execution must have established the required Config records before this Skill runs; each selected phase must have a current Plan.

## Before acting

1. Apply the synchronized project Rules (`.claude/rules/`), especially *Agent Interface Skill policy* and *Agent Interface bootstrap*.
2. Establish Interface Understanding from `.interface/interface.md` and its linked Foundation section files, then Target Understanding from the Target definitions the Interface locates.
3. Through the Interface, locate and read the Develop Operation Component Definition (currently `.interface/implementation/operations/develop/develop.md`) and Preferences (`develop.yaml`), and the Development authorities the Interface names for the targeted Components. They own this Skill's meaning; when they differ from the summary below, they win.

## Prerequisites

- Considers selected phases, or every active and developable Target phase when none is selected, **in Target order**. A phase is developable only when the required Config records are valid and its current Plan exists.
- If either is absent, stop and record the unmet prerequisite in State. **Never** run Configure or Plan.
- Once prerequisites hold, record the Workflow position `development`.

## What Develop does

- Reads the current Plan for each applicable phase and executes only its authorized, unfinished, eligible Tasks whose authority, scope, inputs, outputs, and completion conditions are understood; readiness comes from explicit dependencies.
- **Claims** each eligible Task before changing its result.
- Considers each Task's Task Skills and may use any other suitable available Skill.
- When a new Task identifies an earlier developed Task through `replaces`, marks the earlier Task `replaced` and records the relationship in its Task Log **before** executing the new Task.
- Preserves valid existing work. Constructs and runs the concrete check that satisfies each Task's verification condition; a Task is complete only when that check passes. Records the check used, relevant locations, and observed outcome (no secret values) in the Task Log, and updates Task status.
- On verified Blocker resolution: record evidence and transition, clear the obsolete Blocker reference, return unfinished work to pending, and recheck dependencies before claiming. Resolution never marks work complete.
- Records one State Log Entry with the overall outcome, unresolved conditions, and Skills used. If no eligible Task exists, records that no development was required.

## Boundaries

- **Never** invokes another Core Operation, designs or changes Tasks, expands Task scope, or changes Target meaning, Plan authority, Development Principles, or another Component's record.
- Write authority: the Development results the Tasks authorize, the Task status/Task Log fields in the Plan Config, and Develop's own Workflow position and Log Entry in State. Every other `.interface/` path is read-only.

## Stop conditions

A dependency or prerequisite is unmet, verification fails, or an unresolved condition prevents completion; also stop and report when another Operation is required. Always report the reason.
