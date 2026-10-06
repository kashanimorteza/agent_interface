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

Every Principle in the Definition is mandatory. Plan Preferences, when present, can never add technical or project meaning.

Apply the project Rules (`.claude/rules/`). Establish Interface Understanding through `.interface/interface.md` and its linked Foundation section files, and Target Understanding from the Target definitions the Interface locates.

## Workflow

1. If the State Config record exists and is structurally valid, create this execution's State Log Entry first, so that every outcome — including a stop — is recorded in it.
2. Verify that the Plan Config and State Config records exist and are structurally valid. If either is missing or invalid, stop — never create, repair, initialize, or replace a Config record. Record the stopped outcome in the Log Entry when State is writable; otherwise report explicitly that the Entry could not be written.
3. Establish current Interface Understanding and Target Understanding. Read State only as an execution record (prior Planning results, Blockers, Open Questions, aggregate phase progress); never treat a previous Plan as current without comparing it with current Understanding.
4. Select phases: the given identifiers, or every active and plannable Target phase when none is given; process them in Target order. Skip a selected inactive or unplannable phase. Stop before a later phase when an earlier applicable phase has an open Blocker.
5. For each phase, produce or reconcile its one Plan against current Understanding, once:
   - the Plan holds the phase identity, order, target, intended outcome, and phase-wide context (target Component and work-specific constraints derivable from no other source);
   - every Task belongs to one Group; a Group explains what its implementation area is, what it accomplishes, and where within the phase's target Component its work belongs, and holds the work area and work-specific constraints its Tasks share; a Group never absorbs the activity, expected result, or acceptance of one Task;
   - each Task is one atomic activity with one independently observable result, carrying only what is its own: activity, reason, inputs, dependencies (every Task whose completed result it needs), Task Skills (every Skill identified as useful — guidance for Develop, not a limit), expected result, acceptance as observable behaviour, progress fields, and any constraint specific to it alone; divide large work into as many precise Tasks as necessary; a Task never combines unrelated changes or hides several outcomes behind one title;
   - read together with its Group and Plan, a Task explains what must be done, why, what result it produces, its phase and Group context, its target Component and work area, the governing authorities and constraints, its inputs, dependencies, constraints, and Task Skills, and what completion must deliver;
   - context is written once, at the highest level where it holds, and inherited: a Task never stores its phase or Group, never repeats the identity or general description of the project, phase, or Group, and may add to or tighten inherited context but never repeat or contradict it; the same statement never appears in more than one Task — move it to the common Group or Plan;
   - a Task states what must be achieved, why, where its responsibility belongs, and what proves completion; it never takes ownership of its implementation or makes a technical decision;
   - dependencies are named explicitly; readiness is derived from them, never from file order or proximity, and unrelated Tasks stay independently executable;
   - planning content never names a file, folder, path, module, layout, class, function, symbol, or command, never asserts an artifact's location, carries no list of sources, and stores no project concepts, resolved technical choices, Component rules, or explanations its sources already hold; target and work area identify a Component and a responsibility, not a directory; a constraint is recorded only when it is specific to the work and derivable from no other source;
   - acceptance never names the command, tool, path, or code that observes it and never doubles as an implementation procedure or a check; Plan checks nothing.
6. Replanning preserves still-valid work and adds newly required work. A Task Develop has not begun may be removed and replaced. A begun or completed Task is never removed or rewritten: create a new Task with `replaces` pointing to it; the new Task keeps the earlier one visible and does not itself change its execution status (Develop marks it `replaced`). Every created or materially changed Task records this execution's State Log Entry id in `source_id`. Record every addition, change, removal, preservation, and replacement with its reason in this execution's Log Entry.
7. Provide Task status, Blocker reference, and Task Log fields, but never update execution progress (Develop owns it). Update only aggregate Planning progress in State; it summarizes the phase and never replaces or duplicates Task status or Task Logs, and a Task never duplicates the active Workflow position or the shared Blocker and Open Question records State keeps.
8. Complete the Log Entry and report.

Stop and report when Config records or prerequisites are unavailable, coverage is contradictory, or ownership is unresolved. Never invent a phase or silently change an existing phase's meaning; never perform another Core Operation's responsibility.

## Execution Log

Every execution creates one Log Entry in State with its `id` and Skill, and updates that same Entry with outcome, report, and any applicable `data`, Open Questions, or Blockers when work completes, stops, or is blocked. Follow the State Component (`.interface/implementation/operations/state/state.md`) and State Schema. When invoked by Implement, use the supplied Implement Log Entry ID as `parent_id`.

## Outputs

The Skill execution result and status.
