---
name: my-interface-develop
description: Core Skill for developing. Executes eligible planned Tasks of selected Target phases and generates the Development Component output they realize, recording Task evidence and progress in Task Logs. Use when asked to develop or implement planned Tasks, or when invoked as /my-interface-develop [phase ...].
argument-hint: "[phase-id ...]"
---
<!-- managed by /my-interface-native-implement: realized from the Executor Module Skill Contract `develop`; regenerated on every run — do not edit by hand -->

# Develop

The Core Skill for developing. Required. Stable key: `develop`. Skill name: `my-interface-develop`.

## Inputs

An invocation request and an optional phase selection: `$ARGUMENTS` (zero or more Target phase identifiers).

## Invocation

May be invoked directly by a Human (`/my-interface-develop`) or by an Agent. Among Core Skills, only Implement may invoke it. Develop never invokes another Core Skill; it considers each Task's Task Skills and may use any Provider Skill or other suitable available Skill.

## Authority — read at runtime

Read completely at the start of every run and follow them; this workflow is the Native realization of that understanding and never overrides them.

- `.interface/implementation/operations/develop/develop.md` — Develop's mandatory Execution and Generation Principles.
- `.interface/implementation/operations/develop/develop.yaml` — Develop Preferences.
- The Definition and Preferences of every Development Component a Task realizes, located through the Interface.

Apply the project Rules (`.claude/rules/`). Establish Interface Understanding and Target Understanding before acting.

## Workflow

1. Verify required Config records are valid and the current Plan exists for each applicable phase; if Config or Plan is unavailable, stop.
2. Create this execution's State Log Entry.
3. Establish current Interface and Target Understanding.
4. Select phases: the given identifiers, or every active and developable Target phase when none is given, in Target order.
5. For each eligible Task whose authority, scope, inputs, outputs, and completion conditions are understood and whose dependencies are complete:
   - if it `replaces` an earlier developed Task, mark that earlier Task `replaced` and record the relationship in its Task Log first;
   - claim the Task before changing its result;
   - generate, change, document, or remove artifacts only inside the Component the Task realizes, under that Component's own authorities;
   - preserve valid existing work; record Task-specific evidence, progress transitions, and any Task-specific Blocker in the append-only Task Log, and update Task status;
   - record every choice made on Develop's own proposal as a decision in the Task Log, and list the Task under `decisions` in this execution's State Log Entry;
   - when a blocking condition is verified resolved, record the evidence and transition, clear the obsolete Blocker reference, return the unfinished Task to pending, and recheck dependencies and remaining conditions before claiming it again; resolution never marks work complete and a missing Blocker record alone is not evidence.
6. If no eligible Task exists, complete without changing implementation work.
7. Update aggregate Development progress in State, complete the Log Entry, and report.

Stop when a dependency or prerequisite is unmet, verification fails, or an unresolved condition other than an unset choice prevents completion; report when another Operation is required.

## Generation obligations

- Deterministic: unchanged Target, Definition, Preferences, and technical selections produce the same ordered output with zero source or documentation difference. Classify authoritative additions, modifications, explicit renames, and removals; update every affected public surface together; remove only the Component's own obsolete output; never infer a rename or removal from name similarity, missing understanding, or generator limitation; own no data migration.
- Atomic and explicit failure: collect independent actionable failures when safe, identify the affected item without exposing sensitive values, publish only complete output, preserve the last valid output.
- Technology standard: write to the selected technology's standard with only necessary, version-stabilized dependencies; no dead, duplicate, incomplete, cached, compiled, machine-specific, Agent-identifying, timestamped, or narratively generated artifact.
- Develop checks nothing beyond completing its own output; conformance is established by Review.

## Boundaries

Never change Target meaning, Plan authority, Development Principles, or another Component's owned record without explicit authority. Never design or change Tasks or expand Task scope. Never change a Component's contract because another Component lacks a capability.

## Execution Log

Every execution creates one Log Entry in State with its `id` and Skill, and updates that same Entry with outcome, report, and any applicable `data` (including `decisions`), Open Questions, or Blockers when work completes, stops, or is blocked. Follow the State Component (`.interface/implementation/operations/state/state.md`) and State Schema. When invoked by Implement, use the supplied Implement Log Entry ID as `parent_id`.

## Outputs

The Skill execution result and status.
