---
name: my-interface-plan
description: Core Skill for planning. Turns selected Target phases into Plans of Groups and atomic, verifiable Tasks in the Plan Config record, reconciling existing Plans without destroying begun work. Use when asked to plan a phase or when invoked as /my-interface-plan [phase ...].
argument-hint: "[phase-id ...]"
---
<!-- managed by /my-interface-native-implement: realized from the Executor Module Skill Contract `plan`; regenerated on every run — do not edit by hand -->

# Plan

The Core Skill for planning. Required. Stable key: `plan`. Skill name: `my-interface-plan`.

## Inputs

An invocation request and an optional phase selection: `$ARGUMENTS` (zero or more Target phase identifiers).

## Invocation

May be invoked directly by a Human (`/my-interface-plan`) or by an Agent. Among Core Skills, only Implement may invoke it. Plan never invokes another Core Skill; it may use any Provider Skill or other suitable available Skill.

## Authority — read at runtime

Read completely at the start of every run and follow them; this workflow is the Native realization of that understanding and never overrides them.

- `.interface/implementation/operations/plan/plan.md` — Plan's mandatory Principles.
- `.interface/implementation/operations/plan/plan.yaml` — Plan Preferences.
- The Plan Schema and State Schema the Configure Preferences map to the Plan and State Config records.

Apply the project Rules (`.claude/rules/`). Establish Interface Understanding through `.interface/interface.md` and its linked Foundation section files, and Target Understanding from the Target definitions the Interface locates.

## Workflow

1. Verify that the Plan Config and State Config records exist and are structurally valid. If either is missing or invalid, stop — never create, repair, initialize, or replace a Config record.
2. Create this execution's State Log Entry.
3. Establish current Interface Understanding and Target Understanding.
4. Select phases: the given identifiers, or every active and plannable Target phase when none is given; process them in Target order. Skip a selected inactive or unplannable phase. Stop before a later phase when an earlier applicable phase has an open Blocker.
5. For each phase, produce or reconcile its one Plan against current Understanding, once:
   - the Plan holds the phase identity, order, target, intended outcome, and phase-wide context (target Component and work-specific constraints derivable from no other source);
   - every Task belongs to one Group; a Group holds its work area and the context its Tasks share;
   - each Task is one atomic activity with one independently observable result, carrying only what is its own: activity, reason, inputs, dependencies (every Task whose completed result it needs), Task Skills (every Skill identified as useful), expected result, acceptance as observable behaviour, progress fields, and any constraint specific to it alone;
   - context is written once, at the highest level where it holds, and inherited; the same statement never appears in more than one Task;
   - planning content never names a file, folder, path, module, layout, class, function, symbol, or command, never asserts an artifact's location, carries no list of sources, and stores no project concepts, resolved technical choices, or Component rules;
   - acceptance never names the command, tool, path, or code that observes it; Plan checks nothing.
6. Replanning preserves still-valid work and adds newly required work. A Task Develop has not begun may be removed and replaced. A begun or completed Task is never removed or rewritten: create a new Task with `replaces` pointing to it. Every created or materially changed Task records this execution's State Log Entry id in `source_id`. Record every addition, change, removal, preservation, and replacement with its reason in this execution's Log Entry.
7. Provide Task status, Blocker reference, and Task Log fields, but never update execution progress (Develop owns it). Update only aggregate Planning progress in State.
8. Complete the Log Entry and report.

Stop and report when Config records or prerequisites are unavailable, coverage is contradictory, or ownership is unresolved. Never invent a phase or silently change an existing phase's meaning; never perform another Core Operation's responsibility.

## Execution Log

Every execution creates one Log Entry in State with its `id` and Skill, and updates that same Entry with outcome, report, and any applicable `data`, Open Questions, or Blockers when work completes, stops, or is blocked. Follow the State Component (`.interface/implementation/operations/state/state.md`) and State Schema. When invoked by Implement, use the supplied Implement Log Entry ID as `parent_id`.

## Outputs

The Skill execution result and status.
