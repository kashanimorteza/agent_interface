---
name: my-interface-develop
description: Core Interface Skill "Develop" (stable key `develop`). Executes the authorized, eligible, unfinished Tasks of the current Plan for each selected (or every active and developable) Target phase - claiming each Task, producing and verifying its result, recording evidence and progress in its Task Log - and records one State Log Entry. Use when planned Tasks need implementing. Optional argument - one or more Target phase identifiers.
argument-hint: "[phase-id ...]"
---

# Develop

The Core Skill for developing. Required. Stable key: `develop`. Skill name: `my-interface-develop`.

This Skill is a synchronized Runtime realization. It never reads, searches, or resolves the Agent Module; a missing or unusable Runtime capability is reported as Runtime drift and the Human is asked to run Agent Native Sync.

## Contract

- **Inputs:** an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers).
- **Invocation:** may be invoked directly by a Human (`/my-interface-develop`) or by an Agent (Skill tool).
- **Requirements:** a successful Configure execution must have established the required Config records before this Skill runs. Each selected phase must have a current Plan.
- **Outputs:** the Skill execution result and status.

## Start of workflow

1. Apply the Runtime Rules `interface-bootstrap` and `interface-skill-policy` (`.claude/rules/`) before anything else.
2. Establish Interface Understanding from `.interface/interface.md` and the Foundation section files it links, then Target Understanding from both Target definitions the Interface locates, under the precedence it declares.
3. Locate through the Interface, then read completely, the current **Develop Operation Component** Definition and Preferences (currently `.interface/implementation/operations/develop/develop.md` and `develop.yaml`), plus the Development authorities that govern the work. They are the authority; this file only summarizes them, and on any difference the current sources win.

## Procedure

1. **Phases.** Use the selected phase identifiers, or every active and developable Target phase when none is selected, in Target order. A phase is developable only when the required Config records are valid and its current Plan exists.
2. **Prerequisites.** If Config or the Plan is unavailable, stop and record the unmet prerequisite in State. Never run Configure or Plan.
3. Record the active Workflow position as `development`.
4. For each eligible, understood Task (authority, scope, inputs, outputs, and completion conditions understood; dependencies satisfied):
   - if a new Task identifies an earlier developed Task through `replaces`, first mark that earlier Task `replaced` and record the relationship in its Task Log;
   - **claim** the Task before changing its result;
   - consider its Task Skills, and use any other suitable available Skill;
   - preserve valid existing work; build the concrete check that satisfies the Task's verification condition and run it;
   - record evidence, progress transitions, verification results (the check used and its outcome, no secret values), and any Task-specific Blocker in the Task Log (append-only), and update the Task status. A Task is complete only when its check has passed.
   - When a Blocker is verified resolved: record the resolution evidence and transition, clear the obsolete Blocker reference, return unfinished work to its initial pending status, and recheck dependencies and remaining conditions before claiming it again. Resolving a Blocker never marks work complete; a missing Blocker record alone is not evidence of resolution.
5. Record one State Log Entry: overall outcome, unresolved conditions, and Skills used. If no eligible Task exists, record that no development was required.

## Stop when

A dependency or prerequisite is unmet, verification fails, or an unresolved condition prevents completion. Always report the reason.

## Never

- invoke another Core Operation (Configure, Plan, Review, Implement) — stop and report when one is required;
- design or change Tasks, expand Task scope, or replace Target meaning, Plan authority, Development Principles, or another Component's owned record.
