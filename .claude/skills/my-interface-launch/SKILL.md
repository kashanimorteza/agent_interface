---
name: my-interface-launch
description: Core Skill for launching. Verifies readiness and activates a completed implementation for one runtime Development Component or the complete scope, idempotently preserving healthy running parts and recording the observable runtime result. Use when asked to launch, start, or bring the implementation online, or when invoked as /my-interface-launch [scope].
argument-hint: "[component | complete | all]"
---
<!-- managed by /my-interface-native-implement: realized from the Executor Module Skill Contract `launch`; regenerated on every run — do not edit by hand -->

# Launch

The Core Skill for launching. Required. Stable key: `launch`. Skill name: `my-interface-launch`.

## Inputs

An invocation request and an optional scope: `$ARGUMENTS` — one Development Component that has a runtime, or `complete` (`all` is an alias). With no scope, use the default scope from Launch Preferences and record that decision in the Log.

## Invocation

May be invoked directly by a Human (`/my-interface-launch`) or by an Agent. Launch never invokes another Core Skill; it may use any Provider Skill or other available Skill.

## Authority — read at runtime

Read completely at the start of every run and follow them; this workflow is the Native realization of that understanding and never overrides them.

- `.interface/implementation/operations/launch/launch.md` — Launch's mandatory Principles.
- `.interface/implementation/operations/launch/launch.yaml` — Launch Preferences (including the default scope).
- Platform Principles and Preferences, located through the Interface.

Every Principle in the Definition is mandatory. Launch Preferences supply only activation defaults where higher authorities are silent.

Apply the project Rules (`.claude/rules/`).

## Workflow

1. Create this execution's State Log Entry.
2. Establish current Interface and Target Understanding; read Target and Platform selections, Platform Principles and Preferences, operational State, developed parts, public interfaces, and observable runtime state.
3. Resolve the Environment and Launch definition from explicit Target decisions before Platform defaults; never invent a missing definition.
4. Verify readiness: Development complete for the scope, required dependencies available, bindings safe.
5. Prepare only declared project-scoped runtime requirements.
6. Activate only the selected parts, in dependency order; preserve every healthy running part and change only runtime elements that do not satisfy the current scope. Deliver bindings through public boundaries; never record or expose secret values.
7. Observe the result and record startup or preservation outcomes, readiness evidence, Access Points, Blockers, Open Questions, and any required Human action in the Log Entry; complete it and report.

Stop on an unresolved Environment or Launch definition, missing system preparation, failed preparation or prerequisite startup, incomplete Development, failed readiness, or an unsafe binding.

## Boundaries

Never repair product Source, change Target meaning, redefine Platform authority, alter product or Platform authority to make activation appear ready, or expose secrets.

## Execution Log

Every execution creates one Log Entry in State with its `id` and Skill, and updates that same Entry with outcome, report, and any applicable `data`, Open Questions, or Blockers when work completes, stops, or is blocked. Follow the State Component (`.interface/implementation/operations/state/state.md`) and State Schema.

## Outputs

The Skill execution result and status.
